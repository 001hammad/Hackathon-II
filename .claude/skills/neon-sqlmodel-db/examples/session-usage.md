# Session Usage Examples

Complete guide to async session management with SQLModel and Neon.

## Dependency Injection Pattern

### FastAPI Dependency

```python
# app/database.py
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL_ASYNC")


# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,  # Recycle after 1 hour
    connect_args={
        "ssl": "require",
        "timeout": 10  # Connection timeout in seconds
    }
)


# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Dependency for FastAPI routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async session dependency for FastAPI.

    Usage:
        @router.get("/tasks")
        async def get_tasks(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Context manager for standalone scripts
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for non-FastAPI usage.

    Usage:
        async with get_session_context() as session:
            result = await session.execute(select(Task))
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Dependency with User Context

```python
# app/deps.py
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.database import get_async_session
from app.models.user import User


async def get_current_user(
    token: str,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Extract user from JWT token and return User model.
    """
    from app.core.auth import verify_jwt_token

    try:
        user_id = verify_jwt_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    from sqlalchemy import select
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


async def get_optional_user(
    token: str | None,
    session: AsyncSession = Depends(get_async_session)
) -> User | None:
    """
    Extract user if token is present, otherwise return None.
    """
    if not token:
        return None

    try:
        return await get_current_user(token, session)
    except HTTPException:
        return None


# Usage in routes
# @router.get("/tasks")
# async def list_tasks(
#     current_user: User = Depends(get_current_user),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     tasks = await get_user_tasks(current_user.id, session)
#     return tasks
```

## Transaction Management

### Manual Transaction Control

```python
# app/transactions.py
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task_with_category(
    task_data: dict,
    category_data: dict,
    user_id: str,
    session: AsyncSession
) -> tuple[Task, Category]:
    """
    Create task and category in a single transaction.

    Either both succeed or both fail.
    """
    # Start transaction (implicit with session)

    # Create category first
    category = Category(**category_data)
    session.add(category)
    await session.flush()  # Get category.id without committing

    # Create task with category_id
    task = Task(**task_data, category_id=category.id, user_id=user_id)
    session.add(task)

    # Commit both together
    await session.commit()

    # Refresh to get all IDs
    await session.refresh(category)
    await session.refresh(task)

    return task, category


async def create_task_with_rollback(
    task_data: dict,
    user_id: str,
    session: AsyncSession
) -> Task:
    """
    Create task with explicit rollback on error.
    """
    try:
        task = Task(**task_data, user_id=user_id)
        session.add(task)

        # Some operation that might fail
        await validate_task_data(task_data)

        await session.commit()
        await session.refresh(task)
        return task

    except ValueError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


# Nested transactions with savepoints
async def complex_transaction(
    user_id: str,
    session: AsyncSession
) -> None:
    """
    Use savepoints for partial rollback.
    """
    # Main operation
    task1 = Task(title="Task 1", user_id=user_id)
    session.add(task1)
    await session.flush()

    try:
        # Start savepoint
        async with session.begin_nested():
            # This can fail independently
            task2 = Task(title="Task 2", user_id=user_id)
            session.add(task2)

            if some_condition:
                raise ValueError("Rollback to savepoint")

        # If we get here, savepoint committed
        await session.commit()

    except ValueError:
        # Only task2 is rolled back, task1 is preserved
        await session.rollback(savepoint=False)
```

### Automatic Retry on Transient Errors

```python
# app/retry.py
import asyncio
from functools import wraps
from sqlalchemy.exc import OperationalError, DBAPIError


def retry_on_transient_error(max_retries: int = 3, delay: float = 0.1):
    """
    Decorator to retry operations on transient database errors.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except (OperationalError, DBAPIError) as e:
                    last_exception = e

                    # Check if it's a transient error
                    if is_transient_error(e):
                        await asyncio.sleep(delay * (2 ** attempt))
                        continue
                    else:
                        raise

            raise last_exception

        return wrapper
    return decorator


def is_transient_error(error: Exception) -> bool:
    """
    Determine if a database error is transient.
    """
    error_str = str(error).lower()

    transient_patterns = [
        "connection refused",
        "connection reset",
        "deadlock detected",
        "lock not available",
        "server closed connection",
        "ssl connection",
        "timeout"
    ]

    return any(pattern in error_str for pattern in transient_patterns)


# Usage
# @retry_on_transient_error(max_retries=3)
# async def critical_operation(session: AsyncSession) -> Task:
#     ...
```

## Session Pool Configuration

### Development vs Production

```python
# app/database.py - Development configuration
import os

def get_development_engine():
    """Development: More permissive settings for debugging."""
    return create_async_engine(
        os.getenv("DATABASE_URL_ASYNC"),
        echo=True,  # Log all SQL for debugging
        pool_size=2,  # Smaller pool
        max_overflow=5,
        pool_pre_ping=False,  # Disable for faster queries
        connect_args={
            "ssl": "require",
            "timeout": 30  # Longer timeout
        }
    )


# app/database.py - Production configuration
def get_production_engine():
    """Production: Optimized for performance and reliability."""
    return create_async_engine(
        os.getenv("DATABASE_URL_ASYNC"),
        echo=False,  # No logging in production
        pool_size=int(os.getenv("DATABASE_POOL_SIZE", "5")),
        max_overflow=int(os.getenv("DATABASE_MAX_OVERFLOW", "10")),
        pool_pre_ping=True,  # Verify connections
        pool_recycle=3600,  # Recycle hourly
        pool_reset_on_return="commit",  # Reset after commit
        connect_args={
            "ssl": "require",
            "timeout": int(os.getenv("DATABASE_TIMEOUT", "10"))
        }
    )


# Singleton pattern
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        if os.getenv("ENVIRONMENT") == "production":
            _engine = get_production_engine()
        else:
            _engine = get_development_engine()
    return _engine
```

### Connection Pool Monitoring

```python
# app/monitoring.py
from sqlalchemy.pool import AsyncAdaptedQueuePool
from app.database import async_engine


class DatabaseMetrics:
    """Track database connection metrics."""

    def __init__(self):
        self.pool = async_engine.pool

    def get_pool_status(self) -> dict:
        """Get current pool status."""
        return {
            "size": self.pool.size(),
            "checked_in": self.pool.checkedin(),
            "checked_out": self.pool.checkedout(),
            "overflow": self.pool.overflow(),
            "invalid": self.pool.invalid()
        }

    async def check_connection_health(self) -> bool:
        """
        Verify database is reachable.
        """
        from sqlalchemy import text

        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
                return True
        except Exception:
            return False


# Usage in health check
# @router.get("/health/database")
# async def database_health():
#     metrics = DatabaseMetrics()
#     status = await metrics.check_connection_health()
#     return {
#         "healthy": status,
#         "pool": metrics.get_pool_status() if status else None
#     }
```

## Session in Background Tasks

```python
# app/background.py
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


async def process_tasks_background(
    task_ids: list[int],
    user_id: str
) -> None:
    """
    Background task processing - creates new session.
    """
    # Create a new session for background work
    async with AsyncSessionLocal() as session:
        for task_id in task_ids:
            try:
                result = await session.execute(
                    select(Task).where(
                        Task.id == task_id,
                        Task.user_id == user_id
                    )
                )
                task = result.scalar_one_or_none()

                if task:
                    # Process task...
                    task.processed = True
                    await session.commit()

            except Exception as e:
                # Log error and continue
                print(f"Failed to process task {task_id}: {e}")
                await session.rollback()


# Trigger from FastAPI
# @router.post("/tasks/process")
# async def trigger_processing(
#     task_ids: list[int],
#     current_user: User = Depends(get_current_user)
# ):
#     # Don't await - runs in background
#     asyncio.create_task(
#         process_tasks_background(task_ids, current_user.id)
#     )
#     return {"message": "Processing started"}
```

## Session Best Practices

### Do: Use Context Managers

```python
# Good: Using context manager
async with AsyncSessionLocal() as session:
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    # Session automatically closed
```

### Don't: Leak Sessions

```python
# Bad: Forgetting to close
async def bad_example():
    session = AsyncSessionLocal()  # Never closed!
    result = await session.execute(select(Task))
    return result.scalars().all()


# Bad: Not using async
def sync_example():
    sync_session = SyncSessionLocal()  # Wrong for async
    # ...
```

### Do: Use expire_on_commit=False

```python
# Good: Access attributes after commit without re-fetch
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False  # Access committed objects without DB hit
)


async def example():
    async with AsyncSessionLocal() as session:
        task = await get_task(1, user_id, session)
        task.title = "Updated"

        await session.commit()

        # Can still access task.title without DB hit
        print(task.title)  # Uses committed state
```

### Don't: Share Sessions Across Requests

```python
# Bad: Shared session singleton
class SessionManager:
    _session: AsyncSession | None = None

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = AsyncSessionLocal()
        return cls._session


# Good: Per-request session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

## Complete CRUD Repository Pattern

```python
# app/repositories/base.py
from typing import TypeVar, Generic, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> list[ModelType]:
        query = select(self.model)

        for field, value in filters.items():
            query = query.where(getattr(self.model, field) == value)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(
        self,
        id: int,
        **update_data
    ) -> Optional[ModelType]:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.session.commit()
        return await self.get(id)

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0


# app/repositories/task_repository.py
from app.models.task import Task


class TaskRepository(BaseRepository[Task]):
    """Task-specific repository with user isolation."""

    async def get_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Task]:
        return await self.get_multi(
            skip=skip,
            limit=limit,
            user_id=user_id
        )

    async def get_pending_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Task]:
        return await self.get_multi(
            skip=skip,
            limit=limit,
            user_id=user_id,
            completed=False
        )


# Usage
# router = APIRouter()
#
# @router.get("/tasks")
# async def list_tasks(
#     session: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user)
# ):
#     repo = TaskRepository(Task, session)
#     return await repo.get_by_user(current_user.id)
```
