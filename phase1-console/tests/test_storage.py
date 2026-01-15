"""Tests for TaskStore storage operations."""

import pytest
from todo_app.storage import TaskStore
from todo_app.models import Task


# Foundational validation tests (T012)

def test_validate_title_valid():
    """Test that valid titles pass validation."""
    store = TaskStore()
    store.validate_title("Valid title")  # Should not raise
    store.validate_title("A")  # Minimum length
    store.validate_title("X" * 200)  # Maximum length


def test_validate_title_empty():
    """Test that empty titles raise ValueError."""
    store = TaskStore()
    with pytest.raises(ValueError, match="Title cannot be empty"):
        store.validate_title("")


def test_validate_title_whitespace_only():
    """Test that whitespace-only titles raise ValueError."""
    store = TaskStore()
    with pytest.raises(ValueError, match="Title cannot be empty"):
        store.validate_title("   ")


def test_validate_title_too_long():
    """Test that titles over 200 characters raise ValueError."""
    store = TaskStore()
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        store.validate_title("X" * 201)


def test_validate_description_valid():
    """Test that valid descriptions pass validation."""
    store = TaskStore()
    store.validate_description(None)  # Optional, can be None
    store.validate_description("")  # Can be empty
    store.validate_description("Valid description")
    store.validate_description("X" * 1000)  # Maximum length


def test_validate_description_too_long():
    """Test that descriptions over 1000 characters raise ValueError."""
    store = TaskStore()
    with pytest.raises(ValueError, match="Description must be at most 1000 characters"):
        store.validate_description("X" * 1001)


# User Story 1 tests (T013-T015) - TDD: Write these FIRST, ensure they FAIL

def test_add_task_with_title_only():
    """Test adding a task with only title (no description)."""
    store = TaskStore()
    task = store.add("Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description is None
    assert task.completed is False
    assert len(store.list_all()) == 1


def test_add_task_with_title_and_description():
    """Test adding a task with both title and description."""
    store = TaskStore()
    task = store.add("Important task", "Complete by Friday")

    assert task.id == 1
    assert task.title == "Important task"
    assert task.description == "Complete by Friday"
    assert task.completed is False


def test_add_task_validation_errors():
    """Test that adding task with invalid data raises ValueError."""
    store = TaskStore()

    # Empty title
    with pytest.raises(ValueError, match="Title cannot be empty"):
        store.add("")

    # Title too long
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        store.add("X" * 201)

    # Description too long
    with pytest.raises(ValueError, match="Description must be at most 1000 characters"):
        store.add("Valid title", "X" * 1001)


def test_add_task_auto_increment_ids():
    """Test that task IDs auto-increment correctly."""
    store = TaskStore()

    task1 = store.add("First task")
    task2 = store.add("Second task")
    task3 = store.add("Third task")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


def test_add_task_trims_whitespace():
    """Test that titles and descriptions have whitespace trimmed."""
    store = TaskStore()
    task = store.add("  Title with spaces  ", "  Description with spaces  ")

    assert task.title == "Title with spaces"
    assert task.description == "Description with spaces"


# User Story 2 tests (T021-T022)

def test_list_all_tasks():
    """Test listing all tasks returns all tasks in order."""
    store = TaskStore()
    store.add("Task 1")
    store.add("Task 2")
    store.add("Task 3")

    tasks = store.list_all()

    assert len(tasks) == 3
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_list_all_when_no_tasks():
    """Test listing when no tasks exist returns empty list."""
    store = TaskStore()
    tasks = store.list_all()

    assert tasks == []
    assert len(tasks) == 0


# User Story 3 tests (T028-T030)

def test_mark_task_complete():
    """Test marking a task as complete."""
    store = TaskStore()
    task = store.add("Task to complete")

    assert task.completed is False
    result = store.mark_complete(task.id, True)

    assert result is True
    assert task.completed is True


def test_mark_task_incomplete():
    """Test marking a completed task as incomplete."""
    store = TaskStore()
    task = store.add("Task")
    store.mark_complete(task.id, True)

    assert task.completed is True
    result = store.mark_complete(task.id, False)

    assert result is True
    assert task.completed is False


def test_mark_complete_nonexistent_task():
    """Test marking non-existent task returns False."""
    store = TaskStore()
    result = store.mark_complete(999, True)

    assert result is False


# User Story 4 tests (T036-T039)

def test_update_task_title():
    """Test updating only the task title."""
    store = TaskStore()
    task = store.add("Old title")

    result = store.update(task.id, title="New title")

    assert result is True
    assert task.title == "New title"


def test_update_task_description():
    """Test updating only the task description."""
    store = TaskStore()
    task = store.add("Task", "Old description")

    result = store.update(task.id, description="New description")

    assert result is True
    assert task.description == "New description"


def test_update_both_title_and_description():
    """Test updating both title and description simultaneously."""
    store = TaskStore()
    task = store.add("Old title", "Old desc")

    result = store.update(task.id, title="New title", description="New desc")

    assert result is True
    assert task.title == "New title"
    assert task.description == "New desc"


def test_update_nonexistent_task():
    """Test updating non-existent task returns False."""
    store = TaskStore()
    result = store.update(999, title="New title")

    assert result is False


# User Story 5 tests (T044-T045)

def test_delete_existing_task():
    """Test deleting an existing task."""
    store = TaskStore()
    task = store.add("Task to delete")

    result = store.delete(task.id)

    assert result is True
    assert len(store.list_all()) == 0
    assert store.get(task.id) is None


def test_delete_nonexistent_task():
    """Test deleting non-existent task returns False."""
    store = TaskStore()
    result = store.delete(999)

    assert result is False


def test_get_existing_task():
    """Test retrieving an existing task by ID."""
    store = TaskStore()
    task1 = store.add("First")
    task2 = store.add("Second")

    retrieved = store.get(task2.id)

    assert retrieved is not None
    assert retrieved.id == task2.id
    assert retrieved.title == "Second"


def test_get_nonexistent_task():
    """Test retrieving non-existent task returns None."""
    store = TaskStore()
    task = store.get(999)

    assert task is None
