"""Tests for CLI interface functions."""

import pytest
from todo_app.cli import format_task_list
from todo_app.storage import TaskStore


def test_format_task_list_empty():
    """Test formatting empty task list."""
    output = format_task_list([])

    assert "No tasks found" in output
    assert "Add your first task" in output


def test_format_task_list_with_tasks():
    """Test formatting task list with multiple tasks."""
    store = TaskStore()
    task1 = store.add("First task")
    task2 = store.add("Second task", "With description")
    task3 = store.add("Third task")

    tasks = store.list_all()
    output = format_task_list(tasks)

    assert "Task List (3 tasks)" in output
    assert "First task" in output
    assert "Second task" in output
    assert "Third task" in output
    assert "ID" in output
    assert "Title" in output
    assert "Status" in output
    assert "Created" in output


def test_format_task_list_with_completed_task():
    """Test formatting includes task status (complete/pending)."""
    store = TaskStore()
    task1 = store.add("Pending task")
    task2 = store.add("Completed task")
    store.mark_complete(task2.id, True)

    tasks = store.list_all()
    output = format_task_list(tasks)

    assert "Pending" in output
    assert "Complete" in output


def test_format_task_list_truncates_long_titles():
    """Test that very long titles are truncated with ellipsis."""
    store = TaskStore()
    long_title = "A" * 50  # 50 characters, should be truncated
    task = store.add(long_title)

    tasks = store.list_all()
    output = format_task_list(tasks)

    assert "..." in output  # Ellipsis for truncated title


def test_add_task_integration():
    """Integration test: Add tasks and list them."""
    store = TaskStore()

    # Add multiple tasks
    task1 = store.add("Task 1")
    task2 = store.add("Task 2", "Description 2")
    task3 = store.add("Task 3")

    # Verify they're all there
    tasks = store.list_all()
    assert len(tasks) == 3
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_complete_workflow():
    """Integration test: Full workflow (add, list, update, mark, delete)."""
    store = TaskStore()

    # Add task
    task = store.add("Buy groceries", "Milk and eggs")
    assert task.id == 1
    assert task.completed is False

    # List tasks
    tasks = store.list_all()
    assert len(tasks) == 1

    # Update task
    success = store.update(task.id, title="Buy groceries and bread")
    assert success is True
    assert task.title == "Buy groceries and bread"

    # Mark complete
    success = store.mark_complete(task.id, True)
    assert success is True
    assert task.completed is True

    # Mark incomplete
    success = store.mark_complete(task.id, False)
    assert success is True
    assert task.completed is False

    # Delete task
    success = store.delete(task.id)
    assert success is True
    assert len(store.list_all()) == 0
