---
name: neon-sqlmodel-db
description: Expert in Neon Serverless PostgreSQL setup, SQLModel ORM models, schema, queries, and connection management for Phase 2 backend. Use proactively when working with database in backend.
---

# Neon PostgreSQL + SQLModel Expert

Expert guidance for setting up and working with Neon Serverless PostgreSQL using SQLModel ORM.

## Overview

### Database: Neon Serverless PostgreSQL

Neon provides:
- Serverless PostgreSQL with auto-scaling
- Connection pooling
- Branching for development
- Auto-suspend on inactivity

### ORM: SQLModel

SQLModel combines:
- Pydantic for data validation
- SQLAlchemy for ORM
- Type hints for type safety

## Quick Start

### 1. Install Dependencies

```bash
pip install sqlmodel psycopg2-binary asyncpg
pip install -U sqlalchemy[asyncio]
```

### 2. Environment Variables

```bash
# .env
DATABASE_URL="postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL_ASYNC="postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

### 3. Database URL Format

Neon connection string:
```
postgresql://<username>:<password>@<host>.aws.neon.tech/<database>?sslmode=require
```

For async:
```
postgresql+asyncpg://<username>:<password>@<host>.aws.neon.tech/<database>?sslmode=require
```

## Schema Design

### Task Model

```python
# app/models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import uuid

class Task(SQLModel, table=True):
    """Task model for todo application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id")  # From Better Auth
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": "completed" if self.completed else "pending",
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
```

### User Model (Managed by Better Auth)

```python
# app/models/user.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    """User model - managed by Better Auth."""
    id: str = Field(primary_key=True, max_length=36)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
```

## Connection Management

### Database Setup

```python
# app/database.py
import os
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")

# Sync engine (for migrations, if needed)
sync_engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"sslmode": "require"}
)

# Async engine (for API requests)
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=False,
    connect_args={"sslmode": "require"}
)

# Session factories
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables on startup
def create_tables():
    SQLModel.metadata.create_all(bind=sync_engine)
```

## Session Usage Patterns

### Sync Session Pattern

```python
from app.database import SyncSessionLocal
from app.models.task import Task

def get_tasks(user_id: str) -> list[Task]:
    with SyncSessionLocal() as session:
        tasks = session.query(Task).filter(
            Task.user_id == user_id
        ).all()
        return tasks

def create_task(task_data: dict, user_id: str) -> Task:
    with SyncSessionLocal() as session:
        task = Task(**task_data, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

### Async Session Pattern (Recommended)

```python
from app.database import AsyncSessionLocal
from app.models.task import Task

async def get_tasks(user_id: str) -> list[Task]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Task).where(Task.user_id == user_id)
        )
        tasks = result.scalars().all()
        return list(tasks)

async def create_task(task_data: dict, user_id: str) -> Task:
    async with AsyncSessionLocal() as session:
        task = Task(**task_data, user_id=user_id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
```

## CRUD Operations

### Create

```python
async def create_task(
    task_data: TaskCreate,
    user_id: str,
    session: AsyncSession
) -> Task:
    task = Task(
        **task_data.model_dump(),
        user_id=user_id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Read

```python
async def get_task(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> Optional[Task]:
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation!
        )
    )
    return result.scalar_one_or_none()

async def get_tasks(
    user_id: str,
    session: AsyncSession,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> list[Task]:
    query = select(Task).where(Task.user_id == user_id)

    if status == "completed":
        query = query.where(Task.completed == True)
    elif status == "pending":
        query = query.where(Task.completed == False)

    query = query.offset((page - 1) * limit).limit(limit)
    query = query.order_by(Task.created_at.desc())

    result = await session.execute(query)
    return list(result.scalars().all())
```

### Update

```python
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str,
    session: AsyncSession
) -> Optional[Task]:
    # First, get the task with user isolation
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation!
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task
```

### Delete

```python
async def delete_task(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> bool:
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation!
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
```

## Best Practices

### 1. User Isolation (CRITICAL)

> ALWAYS filter queries by authenticated user_id from JWT

```python
# ✅ GOOD - User isolation
tasks = session.query(Task).filter(Task.user_id == current_user_id)

# ❌ BAD - No user isolation
tasks = session.query(Task).all()
```

### 2. Use Indexes

```python
class Task(SQLModel, table=True):
    user_id: str = Field(index=True)  # Index for user queries
    completed: bool = Field(index=True)  # Index for status queries
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Index for sorting
```

### 3. Connection Pooling

Neon handles connection pooling, but configure in code:

```python
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    pool_size=5,  # Adjust based on traffic
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600  # Recycle connections hourly
)
```

### 4. Use Async Sessions

```python
# ✅ Use async for API requests
async with AsyncSessionLocal() as session:
    # async operations

# ❌ Avoid sync in async FastAPI routes
with SyncSessionLocal() as session:
    # sync operations
```

### 5. Handle Transactions

```python
async def create_task_safe(
    task_data: dict,
    user_id: str,
    session: AsyncSession
) -> Task:
    try:
        task = Task(**task_data, user_id=user_id)
        session.add(task)

        # Additional operations
        await session.execute(
            text("NOTIFY task_created, :task_id"),
            {"task_id": task.id}
        )

        await session.commit()
        return task

    except Exception as e:
        await session.rollback()
        raise e
```

## Error Handling

```python
from sqlalchemy.exc import IntegrityError, NoResultFound

async def get_task_safe(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> Task:
    try:
        result = await session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    except NoResultFound:
        return None

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
```

## Migrations

### Using Alembic

```bash
pip install alembic
alembic init migrations
```

### alembic.ini

```ini
sqlalchemy.url = postgresql://user:password@host.neon.tech/database?sslmode=require
```

### env.py

```python
from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task

target_metadata = SQLModel.metadata
```

## Environment Variables

```bash
# .env
DATABASE_URL="postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL_ASYNC="postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Connection pool settings (optional)
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

## Testing

### Test Database

```python
# conftest.py
import pytest
from sqlmodel import create_engine, Session
from app.models.task import Task
from app.models.user import User

# Use a test database URL
TEST_DATABASE_URL = "postgresql://..."

@pytest.fixture
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session
        # Clean up after test
        session.execute(text("DELETE FROM task"))
        session.execute(text("DELETE FROM user"))
        session.commit()
```

## Key Principles Summary

1. **User Isolation** - ALWAYS filter by user_id from JWT
2. **Use Async** - AsyncSession for FastAPI routes
3. **Connection Pooling** - Neon handles this, configure if needed
4. **Indexes** - Add indexes on user_id, completed, created_at
5. **Error Handling** - Proper exception handling and rollback
6. **Type Safety** - Use SQLModel type hints
7. **Transactions** - Use try/except/finally for transactions

## Additional Resources

- See `examples/` for complete CRUD implementation patterns
- See `reference/` for Neon connection and SQLModel best practices
- See `templates/` for ready-to-use model and session templates
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Neon Docs: https://neon.tech/docs
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

## Summary

This skill provides **backend database** handling with Neon PostgreSQL and SQLModel:

✅ Neon PostgreSQL connection setup
✅ SQLModel ORM models and schema
✅ Async session management
✅ CRUD operations with user isolation
✅ Connection pooling configuration
✅ Migration support with Alembic
✅ Error handling and transactions
✅ Testing patterns

❌ Frontend database operations
❌ User authentication (handled by auth skills)
❌ Backend JWT verification (handled by backend-auth skill)
