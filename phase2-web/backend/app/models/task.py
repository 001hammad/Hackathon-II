"""Task model for todo items."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task model for todo application.

    Each task belongs to exactly one user (enforced by user_id foreign key).
    User isolation is CRITICAL - all queries MUST filter by user_id.

    Attributes:
        id: Unique task identifier (auto-increment integer)
        user_id: Owner's user ID (string - Better Auth format)
        description: Task description text (max 500 characters)
        completed: Completion status (boolean)
        created_at: Task creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=255)  # Better Auth string ID
    description: str = Field(max_length=500, nullable=False)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        status = "✓" if self.completed else "○"
        desc_preview = self.description[:30] + "..." if len(self.description) > 30 else self.description
        return f"<Task(id={self.id}, description='{desc_preview}', {status})>"

    def to_dict(self) -> dict:
        """
        Convert task to dictionary for API responses.

        Returns:
            dict: Task data suitable for JSON serialization
        """
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
