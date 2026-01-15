# SQLModel Best Practices

Comprehensive guidelines for using SQLModel effectively with PostgreSQL.

## Model Design

### Use Descriptive Field Names

```python
# Good: Descriptive names
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="Owner user ID")
    title: str = Field(max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task details")
    is_completed: bool = Field(default=False, description="Completion status")
    due_date: Optional[datetime] = Field(None, description="Due date")


# Avoid: Ambiguous names
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str  # What is uid?
    ttl: str  # What does ttl mean?
    stat: bool  # Status or statistic?
```

### Define Appropriate Field Lengths

```python
class Task(SQLModel, table=True):
    # Always set max_length for string fields
    title: str = Field(max_length=255)  # Standard for titles
    description: Optional[str] = Field(None, max_length=1000)  # Reasonable limit
    email: str = Field(max_length=255)  # Email addresses
    name: str = Field(max_length=100)  # Names
    slug: str = Field(max_length=100, unique=True)  # URL slugs
    code: str = Field(max_length=50)  # Short codes
```

### Use Appropriate Field Types

```python
from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    # Use datetime for timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    # Use date for calendar dates (without time)
    due_date: Optional[date] = Field(None, description="Due date (date only)")

    # Use Optional for nullable fields
    description: Optional[str] = None

    # Use bool for flags
    is_active: bool = Field(default=True)
    is_completed: bool = Field(default=False)
```

### Add Indexes for Query Performance

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        index=True,  # Index for user lookups
        description="Owner user ID"
    )

    # Composite index for common queries
    # For queries filtering by user_id AND completed status
    # Will be created with db_index at DB level

    status: str = Field(default="pending", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # For text search
    title: str = Field(max_length=255, index=True)


# Creating composite indexes
class Task(SQLModel, table=True):
    # Primary key is automatically indexed
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key should be indexed
    user_id: str = Field(
        foreign_key="user.id",
        index=True
    )

    # Add indexes for sort/filter patterns
    completed: bool = Field(default=False, index=True)
    due_date: Optional[datetime] = Field(None, index=True)


# Note: For composite indexes, create them at DB level:
# CREATE INDEX idx_task_user_status
# ON task (user_id, completed) WHERE completed = false;
```

## Relationship Design

### Define Clear Relationships

```python
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=36)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None

    # Define relationship
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        description="Reference to owner User"
    )

    # Define relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

### Use Forward References for Complex Relationships

```python
from __future__ import annotations
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="category.id")
    )

    # Self-referential relationship
    parent: Optional[Category] = Relationship(
        remote_side=[Category.id],
        back_populates="children"
    )
    children: List[Category] = Relationship(back_populates="parent")
```

### Avoid Circular Imports with Lazy Loading

```python
# models/__init__.py
from app.models.user import User  # Import class, not instance
from app.models.task import Task


# models/task.py
from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="tasks")
```

## Pydantic Models for API

### Separate Models for Different Operations

```python
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# Database model (has table=True)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Create model (for POST requests)
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None


# Update model (for PATCH/PUT requests)
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# Response model (for API responses)
class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: str  # Computed from completed
    due_date: Optional[str]  # Serialized datetime
    created_at: str  # Serialized datetime
    updated_at: str  # Serialized datetime

    @classmethod
    def from_orm(cls, task: Task) -> "TaskResponse":
        return cls(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status="completed" if task.completed else "pending",
            due_date=task.due_date.isoformat() if task.due_date else None,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )
```

### Use Config Classes for Model Behavior

```python
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    completed: bool = Field(default=False)

    class Config:
        # Allow arbitrary types
        arbitrary_types_allowed = True

        # Table name (auto-generated from class name otherwise)
        table_name = "tasks"

        # Column naming style
        alias_generator = lambda s: s.replace("_", "_")  # camelCase

        # JSON serialization options
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskPublic(SQLModel):
    """Public-facing model with different rules."""
    id: int
    title: str
    completed: bool

    class Config:
        # Exclude internal fields
        exclude = {"created_at", "updated_at"}
```

## Data Validation

### Use Field Constraints

```python
from pydantic import validator, field_validator
from sqlmodel import SQLModel, Field


class TaskCreate(SQLModel):
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional description"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional due date"
    )

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v < datetime.utcnow():
            raise ValueError("Due date cannot be in the past")
        return v

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else v
```

### Use Enums for Constrained Values

```python
from enum import Enum
from sqlmodel import SQLModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Task status"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Task priority"
    )
```

## Performance Patterns

### Use selectinload for Relationships

```python
from sqlalchemy.orm import selectinload


async def get_user_with_tasks(user_id: str, session: AsyncSession):
    """Load user and tasks in single query."""
    result = await session.execute(
        select(User)
        .options(selectinload(User.tasks))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()


# Avoid N+1 queries:
# Good: Eager loading
user = await get_user_with_tasks(user_id, session)
for task in user.tasks:  # No additional query
    print(task.title)


# Bad: Lazy loading (N+1 problem)
user = await get_user(user_id, session)
for task in user.tasks:  # Additional query for each access!
    print(task.title)
```

### Use exists() for Boolean Checks

```python
from sqlalchemy import exists, select
from sqlalchemy import func


async def user_has_tasks(user_id: str, session: AsyncSession) -> bool:
    """Check if user has any tasks efficiently."""
    result = await session.execute(
        select(exists().where(Task.user_id == user_id))
    )
    return result.scalar()


async def count_user_tasks(user_id: str, session: AsyncSession) -> int:
    """Count user's tasks."""
    result = await session.execute(
        select(func.count()).select_from(Task).where(Task.user_id == user_id)
    )
    return result.scalar() or 0
```

### Batch Operations for Bulk Data

```python
from sqlalchemy.dialects.postgresql import insert


async def bulk_create_tasks(
    tasks_data: list[dict],
    session: AsyncSession
) -> list[Task]:
    """Bulk insert for better performance."""
    stmt = insert(Task).values(tasks_data).returning(Task)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def bulk_update_tasks(
    updates: list[dict],
    session: AsyncSession
) -> int:
    """Bulk update with ON CONFLICT."""
    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(Task).values(updates).on_conflict_do_update(
        index_elements=["id"],
        set_={
            "title": insert(Task).excluded.title,
            "updated_at": datetime.utcnow()
        }
    )

    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount
```

## Error Handling

### Handle Constraint Violations

```python
from sqlalchemy.exc import IntegrityError, UniqueViolation
from sqlalchemy.orm import exc as orm_exc


async def create_task_safe(
    task_data: TaskCreate,
    user_id: str,
    session: AsyncSession
) -> Task:
    """Create task with proper error handling."""
    try:
        task = Task(**task_data.model_dump(), user_id=user_id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    except IntegrityError as e:
        await session.rollback()

        # Handle specific constraint violations
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="Task with this title already exists"
            )

        # Foreign key violation
        if "foreign key" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail="Invalid user reference"
            )

        raise HTTPException(
            status_code=400,
            detail="Database constraint violation"
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
```

### Handle Query Errors

```python
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from fastapi import HTTPException


async def get_task_by_id(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> Task:
    """Get single task with proper error handling."""
    try:
        result = await session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task

    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    except MultipleResultsFound:
        # This shouldn't happen with proper schema, but handle anyway
        raise HTTPException(
            status_code=500,
            detail="Multiple tasks found - data inconsistency"
        )
```

## Migration Patterns

### Version Control Your Schema

```python
# app/migrations/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlmodel import SQLModel


def upgrade():
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # Create tasks table with foreign key
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, default=False),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE"
        ),
    )

    # Create indexes
    op.create_index("ix_tasks_user_id", "tasks", ["user_id"])
    op.create_index("ix_tasks_completed", "tasks", ["completed"])
    op.create_index("ix_tasks_created_at", "tasks", ["created_at"])


def downgrade():
    op.drop_index("ix_tasks_created_at")
    op.drop_index("ix_tasks_completed")
    op.drop_index("ix_tasks_user_id")
    op.drop_table("tasks")
    op.drop_table("users")
```

### Safe Schema Changes

```python
# app/migrations/versions/002_add_priority.py
"""Add priority to tasks

Revision ID: 002
Revises: 001
Create Date: 2024-01-15
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add column with default (safe)
    op.add_column(
        "tasks",
        sa.Column(
            "priority",
            sa.String(length=20),
            nullable=False,
            server_default="medium"
        )
    )


def downgrade():
    # Remove column (safe)
    op.drop_column("tasks", "priority")
```

## Testing Patterns

### Use Fixtures for Database

```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.task import Task
from app.models.user import User


@pytest.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost/testdb",
        echo=False
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create test session with automatic cleanup."""
    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        # Rollback any uncommitted changes
        await session.rollback()


@pytest.fixture
async def test_user(test_session):
    """Create test user."""
    user = User(
        id="test-user-id",
        email="test@example.com",
        name="Test User"
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def test_task(test_session, test_user):
    """Create test task."""
    task = Task(
        title="Test Task",
        user_id=test_user.id
    )
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    return task
```

### Test Repository Patterns

```python
# tests/test_task_repository.py
import pytest
from app.models.task import Task
from app.repositories.task_repository import TaskRepository


@pytest.mark.asyncio
async def test_create_task(test_session, test_user):
    """Test task creation."""
    repo = TaskRepository(Task, test_session)

    task = await repo.create(
        Task(
            title="New Task",
            user_id=test_user.id
        )
    )

    assert task.id is not None
    assert task.title == "New Task"
    assert task.user_id == test_user.id


@pytest.mark.asyncio
async def test_get_by_user(test_session, test_user, test_task):
    """Test fetching tasks by user."""
    repo = TaskRepository(Task, test_session)

    tasks = await repo.get_by_user(test_user.id)

    assert len(tasks) >= 1
    assert any(t.id == test_task.id for t in tasks)


@pytest.mark.asyncio
async def test_user_isolation(test_session, test_user):
    """Test that users can only see their own tasks."""
    repo = TaskRepository(Task, test_session)

    # Create task for another user
    other_user_id = "other-user-id"
    other_task = Task(title="Other Task", user_id=other_user_id)
    test_session.add(other_task)
    await test_session.commit()

    # User should not see other user's task
    tasks = await repo.get_by_user(test_user.id)
    task_ids = [t.id for t in tasks]

    assert other_task.id not in task_ids
```
