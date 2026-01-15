# SQLModel Models Template
# Copy to app/models/task.py and app/models/user.py

# ============== USER MODEL ==============
# app/models/user.py

from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    User model - managed by Better Auth.

    This model stores user account information. User accounts
    are created and managed by Better Auth, this table provides
    additional profile data and relationships.
    """
    id: str = Field(
        primary_key=True,
        max_length=36,
        description="User ID from Better Auth (UUID format)"
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address"
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
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last profile update timestamp"
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )

    class Config:
        table_name = "users"
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


# ============== TASK MODEL ==============
# app/models/task.py

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    """
    Task model for todo application.

    Represents a single task owned by a user. Tasks can be
    marked as completed and have optional due dates.
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing task ID"
    )
    user_id: str = Field(
        max_length=36,
        index=True,
        foreign_key="user.id",
        description="Owner user ID from Better Auth"
    )
    title: str = Field(
        max_length=255,
        min_length=1,
        description="Task title (required)"
    )
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
    user: Optional["User"] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    class Config:
        table_name = "tasks"
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
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


# ============== PYDANTIC MODELS ==============
# app/models/schemas.py

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class TaskCreate(SQLModel):
    """
    Pydantic model for creating a new task.

    Used in POST /tasks endpoint.
    """
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (1-255 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date and time"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not whitespace only."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()


class TaskUpdate(SQLModel):
    """
    Pydantic model for updating an existing task.

    Used in PATCH /tasks/{id} endpoint.
    All fields are optional - only provided fields are updated.
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Completion status"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Due date"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not whitespace only."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else v


class TaskResponse(SQLModel):
    """
    Pydantic model for task API responses.

    Used in GET /tasks and GET /tasks/{id} endpoints.
    Serializes datetime objects as ISO strings.
    """
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: str  # "pending" or "completed"
    due_date: Optional[str]  # ISO format
    created_at: str  # ISO format
    updated_at: str  # ISO format

    @classmethod
    def from_orm(cls, task: Task) -> "TaskResponse":
        """Create response from SQLModel instance."""
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


class UserResponse(SQLModel):
    """
    Pydantic model for user API responses.
    """
    id: str
    email: str
    name: Optional[str]
    created_at: str

    @classmethod
    def from_orm(cls, user: User) -> "UserResponse":
        """Create response from SQLModel instance."""
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat()
        )


# ============== MODELS INDEX ==============
# app/models/__init__.py

from app.models.user import User
from app.models.task import Task
from app.models.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    UserResponse
)

__all__ = [
    "User",
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "UserResponse",
]


# ============== USAGE ==============
"""
# Creating a new task
from app.models import Task, TaskCreate
from datetime import datetime

task = Task(
    user_id="user-uuid-here",
    title="Buy groceries",
    description="Milk, eggs, bread",
    due_date=datetime.utcnow()
)

# Creating from request body
task_create = TaskCreate(
    title="Buy groceries",
    description="Milk, eggs, bread",
    due_date=datetime.utcnow()
)
task = Task(**task_create.model_dump(), user_id="user-uuid")

# Converting to response
response = TaskResponse.from_orm(task)
"""
