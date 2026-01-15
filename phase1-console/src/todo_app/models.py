"""Data models for the todo application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a todo item in the in-memory store.

    Attributes:
        id: Unique auto-incrementing task identifier
        title: Task title (1-200 characters, required)
        description: Optional task description (0-1000 characters)
        completed: Task completion status (False=pending, True=complete)
        created_at: Timestamp when task was created
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        """Return string representation of Task."""
        status = "Complete" if self.completed else "Pending"
        desc_preview = f", desc='{self.description[:20]}...'" if self.description else ""
        return f"Task(id={self.id}, title='{self.title}'{desc_preview}, status={status})"
