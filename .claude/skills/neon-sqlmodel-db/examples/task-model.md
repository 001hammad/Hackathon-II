# Task Model Examples

Complete SQLModel definitions for Task and related models.

## Task Model

```python
# app/models/task.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid

class Task(SQLModel, table=True):
    """Task model for todo application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        max_length=36,
        index=True,
        foreign_key="user.id",
        description="User ID from Better Auth"
    )
    title: str = Field(max_length=255, description="Task title")
    description: Optional[str] = Field(
        default=None,
        description="Optional task description"
    )
    completed: bool = Field(
        default=False,
        description="Whether task is completed"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

    class Config:
        arbitrary_types_allowed = True
        table_name = "tasks"

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


# Pydantic model for creation
class TaskCreate(SQLModel):
    title: str = Field(max_length=255, min_length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


# Pydantic model for update
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(max_length=255, default=None)
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# Pydantic model for response
class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[str]
    created_at: str
    updated_at: str

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

## User Model

```python
# app/models/user.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    """User model - managed by Better Auth."""
    id: str = Field(
        primary_key=True,
        max_length=36,
        description="User ID from Better Auth"
    )
    email: str = Field(
        unique=True,
        index=True,
        description="User email"
    )
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User display name"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

    class Config:
        table_name = "users"
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
```

## Key Points

1. Use `Field()` to define columns and constraints
2. Add `index=True` for frequently queried columns
3. Use `ForeignKey` for relationships
4. Define separate Pydantic models for Create/Update/Response
5. Use `from_orm()` or custom methods for response conversion
