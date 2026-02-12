"""User model for authentication - managed by Better Auth."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    """
    User model for multi-user todo application.

    Note: This model is primarily for reference. Better Auth manages users
    in the 'user' table (singular). Tasks reference Better Auth's user table.

    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (unique, used for login)
        password_hash: Bcrypt hashed password (never store plaintext)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
