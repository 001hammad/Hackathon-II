"""In-memory storage for tasks with CRUD operations."""

from typing import List, Optional
from todo_app.models import Task


class TaskStore:
    """In-memory storage manager for Task objects.

    Manages task creation, retrieval, updates, and deletion with
    auto-incrementing IDs and validation.

    Attributes:
        tasks: List of all tasks in insertion order
        next_id: Next available task ID (auto-incrementing)
    """

    def __init__(self) -> None:
        """Initialize empty task store."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def validate_title(self, title: str) -> None:
        """Validate task title meets requirements.

        Args:
            title: Task title to validate

        Raises:
            ValueError: If title is invalid (empty, whitespace-only, or >200 chars)
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if len(title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")

    def validate_description(self, description: Optional[str]) -> None:
        """Validate task description meets requirements.

        Args:
            description: Task description to validate (can be None)

        Raises:
            ValueError: If description exceeds 1000 characters
        """
        if description is not None and len(description) > 1000:
            raise ValueError("Description must be at most 1000 characters")

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task to the store.

        Args:
            title: Task title (1-200 characters, required)
            description: Optional task description (0-1000 characters)

        Returns:
            The newly created Task with assigned ID

        Raises:
            ValueError: If title or description validation fails
        """
        self.validate_title(title)
        self.validate_description(description)

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip() if description else None
        )

        self.tasks.append(task)
        self.next_id += 1

        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_all(self) -> List[Task]:
        """Get all tasks in insertion order.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional, keeps current if None)
            description: New description (optional, keeps current if None)

        Returns:
            True if task was found and updated, False otherwise

        Raises:
            ValueError: If new title or description validation fails
        """
        task = self.get(task_id)
        if task is None:
            return False

        if title is not None:
            self.validate_title(title)
            task.title = title.strip()

        if description is not None:
            self.validate_description(description)
            task.description = description.strip() if description else None

        return True

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        task = self.get(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def mark_complete(self, task_id: int, completed: bool) -> bool:
        """Mark task as complete or incomplete.

        Args:
            task_id: ID of task to update
            completed: True for complete, False for incomplete

        Returns:
            True if task was found and updated, False otherwise
        """
        task = self.get(task_id)
        if task is None:
            return False

        task.completed = completed
        return True
