# Quickstart: In-Memory Console Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-30

## Prerequisites

- Python 3.13 or higher
- UV (modern Python package manager)

## Setup

### 1. Install UV (if not already installed)

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation**:
```bash
uv --version
```

### 2. Initialize Project

Navigate to the phase1-console directory:

```bash
cd phase1-console
```

Initialize the Python project with UV:

```bash
uv init
```

This creates:
- `pyproject.toml` - Project configuration
- `.python-version` - Python version specification
- Virtual environment (automatically managed by UV)

### 3. Install Dependencies (Optional)

If using the Rich library for enhanced CLI output:

```bash
uv add rich
```

For development/testing dependencies:

```bash
uv add --dev pytest
```

## Running the Application

### Start the Todo App

From the `phase1-console/` directory:

```bash
uv run python -m todo_app.main
```

Or if you've set up the entry point in pyproject.toml:

```bash
uv run todo
```

### First Run Experience

On first run, you'll see the main menu:

```
═══════════════════════════════════════
  📝 TODO APP - Main Menu
═══════════════════════════════════════

1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

═══════════════════════════════════════
Select an option (1-6):
```

## Basic Usage

### Add Your First Task

1. Select option `1` (Add Task)
2. Enter a title: `Buy groceries`
3. Optionally enter a description: `Milk, eggs, bread`
4. Task is created with auto-generated ID

### List All Tasks

1. Select option `2` (List Tasks)
2. View all your tasks in a formatted table

### Mark Task as Complete

1. Select option `5` (Mark Task Complete/Incomplete)
2. Enter the task ID
3. Choose `1` for Complete or `2` for Incomplete

### Update a Task

1. Select option `3` (Update Task)
2. Enter the task ID
3. Enter new title (or leave blank to keep current)
4. Enter new description (or leave blank to keep current)

### Delete a Task

1. Select option `4` (Delete Task)
2. Enter the task ID
3. Confirm deletion by entering `y`

### Exit

Select option `6` to exit the application.

## Running Tests

Run all tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=todo_app --cov-report=html
```

Run specific test file:

```bash
uv run pytest tests/test_storage.py
```

Run with verbose output:

```bash
uv run pytest -v
```

## Project Structure

```
phase1-console/
├── pyproject.toml          # UV project configuration
├── .python-version         # Python version (3.13+)
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py           # Task dataclass
│       ├── storage.py          # In-memory storage layer
│       ├── cli.py              # CLI interface and menu
│       └── main.py            # Entry point
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_storage.py
    └── test_cli.py
```

## Development Workflow

### 1. Make Changes

Edit files using Claude Code tools:
- models.py - Task data structure
- storage.py - CRUD operations
- cli.py - User interface
- main.py - Application entry point

### 2. Run Tests

```bash
uv run pytest
```

### 3. Run the App

```bash
uv run python -m todo_app.main
```

### 4. Verify Changes

Test the application interactively to ensure changes work as expected.

## Troubleshooting

### "uv: command not found"

UV is not installed or not in your PATH. Follow installation instructions above.

### "Module not found: todo_app"

Make sure you're running from the `phase1-console/` directory and the package is properly installed:

```bash
cd phase1-console
uv sync
```

### "Python 3.13 not found"

Install Python 3.13 or higher:

**Windows**: Download from [python.org](https://www.python.org/downloads/)

**macOS** (with Homebrew):
```bash
brew install python@3.13
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.13
```

### Tests Failing

Ensure all dependencies are installed:

```bash
uv sync --all-extras
```

Run tests with verbose output to see detailed error messages:

```bash
uv run pytest -v
```

## Configuration

### pyproject.toml Example

```toml
[project]
name = "todo-app"
version = "1.0.0"
description = "Phase 1: In-Memory Console Todo App"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.4.0"]
formatting = ["rich>=13.7.0"]

[project.scripts]
todo = "todo_app.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Notes

- All data is stored in memory only
- Data is lost when the application exits
- This is expected behavior for Phase 1
- Restart creates a fresh empty task list
- Phase 2 will add persistent storage

## Next Steps

After completing Phase 1:
1. Verify all CRUD operations work correctly
2. Run full test suite and ensure 100% pass
3. Validate PEP8 compliance
4. Proceed to Phase 2: Web Application with persistent storage

## Support

For issues or questions:
- Review specs/001-cli-todo-app/spec.md for requirements
- Review specs/001-cli-todo-app/plan.md for architecture
- Check tests/ for usage examples
