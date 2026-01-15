"""CLI interface for todo application."""

from typing import List
from todo_app.models import Task
from todo_app.storage import TaskStore


def display_menu() -> None:
    """Display the main menu with available options."""
    print("\n" + "=" * 43)
    print("  TODO APP - Main Menu")
    print("=" * 43)
    print()
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print()
    print("=" * 43)


def add_task_flow(store: TaskStore) -> None:
    """Handle the add task user interaction flow.

    Args:
        store: TaskStore instance to add task to
    """
    try:
        print("\n--- Add New Task ---")
        title = input("Enter task title (1-200 characters): ").strip()

        if not title:
            print("X Error: Title cannot be empty")
            return

        description_input = input("Enter task description (optional, max 1000 characters): ").strip()
        description = description_input if description_input else None

        task = store.add(title, description)

        print(f"\nOK Task added successfully!")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")
        if task.description:
            print(f"  Description: {task.description}")
        print(f"  Status: Pending")
        print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")

    except ValueError as e:
        print(f"\nError: {e}")


def format_task_list(tasks: List[Task]) -> str:
    """Format list of tasks for display.

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted string representation of task list
    """
    if not tasks:
        return "Info: No tasks found. Add your first task with option 1!"

    output = []
    output.append("\n" + "=" * 80)
    output.append(f"   Task List ({len(tasks)} tasks)")
    output.append("=" * 80)
    output.append("")

    # Header
    output.append(f"{'ID':<4} | {'Title':<30} | {'Status':<10} | {'Created':<19}")
    output.append("-" * 80)

    # Tasks
    for task in tasks:
        status = "Complete" if task.completed else "Pending"
        title_display = task.title[:27] + "..." if len(task.title) > 30 else task.title
        created_str = task.created_at.strftime('%Y-%m-%d %H:%M')

        output.append(f"{task.id:<4} | {title_display:<30} | {status:<10} | {created_str}")

    output.append("")
    return "\n".join(output)


def list_tasks_flow(store: TaskStore) -> None:
    """Handle the list tasks user interaction flow.

    Args:
        store: TaskStore instance to list tasks from
    """
    tasks = store.list_all()
    print(format_task_list(tasks))


def update_task_flow(store: TaskStore) -> None:
    """Handle the update task user interaction flow.

    Args:
        store: TaskStore instance to update task in
    """
    try:
        print("\n--- Update Task ---")
        task_id_input = input("Enter task ID to update: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("X Error: Invalid task ID. Please enter a number")
            return

        task = store.get(task_id)
        if not task:
            print(f"X Error: Task not found (ID: {task_id})")
            return

        print(f"\nCurrent task:")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description or '(none)'}")

        new_title = input("\nEnter new title (leave blank to keep current): ").strip()
        new_description = input("Enter new description (leave blank to keep current): ").strip()

        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        if not title_to_update and not description_to_update:
            print("\nInfo: No changes made")
            return

        success = store.update(
            task_id,
            title=title_to_update,
            description=description_to_update
        )

        if success:
            print(f"\nOK Task updated successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description or '(none)'}")
        else:
            print(f"X Error: Failed to update task")

    except ValueError as e:
        print(f"\nError: {e}")


def delete_task_flow(store: TaskStore) -> None:
    """Handle the delete task user interaction flow.

    Args:
        store: TaskStore instance to delete task from
    """
    try:
        print("\n--- Delete Task ---")
        task_id_input = input("Enter task ID to delete: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("X Error: Invalid task ID. Please enter a number")
            return

        task = store.get(task_id)
        if not task:
            print(f"X Error: Task not found (ID: {task_id})")
            return

        print(f"\nTask to delete:")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")

        confirm = input("\nAre you sure you want to delete this task? (y/n): ").strip().lower()

        if confirm == 'y':
            success = store.delete(task_id)
            if success:
                print(f"\nOK Task deleted successfully! (ID: {task_id})")
            else:
                print(f"X Error: Failed to delete task")
        else:
            print("\nInfo: Delete cancelled")

    except Exception as e:
        print(f"\nX Error: {e}")


def mark_complete_flow(store: TaskStore) -> None:
    """Handle the mark task complete/incomplete user interaction flow.

    Args:
        store: TaskStore instance to update task in
    """
    try:
        print("\n--- Mark Task Complete/Incomplete ---")
        task_id_input = input("Enter task ID: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("X Error: Invalid task ID. Please enter a number")
            return

        task = store.get(task_id)
        if not task:
            print(f"X Error: Task not found (ID: {task_id})")
            return

        print(f"\nTask: {task.title}")
        print(f"Current status: {'Complete' if task.completed else 'Pending'}")

        choice = input("\nMark as (1) Complete or (2) Incomplete: ").strip()

        if choice == '1':
            success = store.mark_complete(task_id, True)
            status_text = "complete"
        elif choice == '2':
            success = store.mark_complete(task_id, False)
            status_text = "incomplete"
        else:
            print("X Error: Invalid choice. Enter 1 or 2")
            return

        if success:
            print(f"\nOK Task marked as {status_text}!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Status: {'Complete' if task.completed else 'Pending'}")
        else:
            print(f"X Error: Failed to update task")

    except Exception as e:
        print(f"\nX Error: {e}")
