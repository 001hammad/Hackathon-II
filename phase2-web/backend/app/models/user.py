"""User model for authentication - managed by Better Auth."""
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .task import Task


class User(SQLModel, table=True):
    """
    User model for multi-user todo application.

    This model stores user authentication data. In Phase 2, users are
    created through the Better Auth signup flow, and tasks are associated
    with users via the user_id foreign key.

    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (unique, used for login)
        password_hash: Bcrypt hashed password (never store plaintext)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        tasks: Relationship to user's tasks (one-to-many)
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
