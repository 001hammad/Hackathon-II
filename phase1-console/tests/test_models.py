"""Tests for Task dataclass."""

from datetime import datetime
from todo_app.models import Task


def test_task_creation_with_all_fields():
    """Test creating a task with all fields specified."""
    created_time = datetime(2025, 12, 30, 10, 0, 0)
    task = Task(
        id=1,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=created_time
    )

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False
    assert task.created_at == created_time


def test_task_creation_with_defaults():
    """Test creating a task with default values for optional fields."""
    before_creation = datetime.now()
    task = Task(id=1, title="Test task")
    after_creation = datetime.now()

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description is None
    assert task.completed is False
    assert before_creation <= task.created_at <= after_creation


def test_task_creation_title_only():
    """Test creating a task with only required fields (id and title)."""
    task = Task(id=5, title="Simple task")

    assert task.id == 5
    assert task.title == "Simple task"
    assert task.description is None
    assert task.completed is False
    assert isinstance(task.created_at, datetime)


def test_task_timestamp_auto_generation():
    """Test that created_at is automatically set to current time."""
    before = datetime.now()
    task = Task(id=1, title="Test")
    after = datetime.now()

    assert before <= task.created_at <= after


def test_task_completed_defaults_to_false():
    """Test that completed field defaults to False (pending status)."""
    task = Task(id=1, title="New task")
    assert task.completed is False


def test_task_repr():
    """Test string representation of Task."""
    task = Task(id=1, title="Test task", description="Test description")
    repr_str = repr(task)

    assert "Task" in repr_str
    assert "id=1" in repr_str
    assert "title='Test task'" in repr_str
    assert "Pending" in repr_str
