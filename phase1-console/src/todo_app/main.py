"""Main entry point for todo application."""

import sys
import io
from todo_app.storage import TaskStore
from todo_app.cli import (
    display_menu,
    add_task_flow,
    list_tasks_flow,
    update_task_flow,
    delete_task_flow,
    mark_complete_flow
)


def main() -> None:
    """Main application loop with interactive menu."""
    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    store = TaskStore()

    print("\nWelcome to TODO APP!")
    print("Manage your tasks efficiently from the command line.")

    try:
        while True:
            display_menu()
            choice = input("Select an option (1-6): ").strip()

            if choice == '1':
                add_task_flow(store)
            elif choice == '2':
                list_tasks_flow(store)
            elif choice == '3':
                update_task_flow(store)
            elif choice == '4':
                delete_task_flow(store)
            elif choice == '5':
                mark_complete_flow(store)
            elif choice == '6':
                print("\nThank you for using TODO APP! Goodbye.\n")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1-6.")

    except (KeyboardInterrupt, EOFError):
        print("\n\nThank you for using TODO APP! Goodbye.\n")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("  Please try again or report this issue.\n")


if __name__ == "__main__":
    main()
