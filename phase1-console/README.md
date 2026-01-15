# Phase 1: In-Memory Console Todo App

A simple command-line todo application built with Python 3.13+ that supports 5 basic CRUD operations using in-memory storage.

## Features

- ✅ Add tasks with title and optional description
- 📋 List all tasks with ID, title, status, and creation date
- ✔️ Mark tasks as complete or incomplete
- ✏️ Update task title or description
- 🗑️ Delete tasks
- 💾 In-memory storage (data lost on exit)

## Prerequisites

- Python 3.13 or higher
- UV (modern Python package manager)

## Installation

### Install UV

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup Project

1. Navigate to the phase1-console directory:
```bash
cd phase1-console
```

2. Install dependencies (optional - pytest for testing):
```bash
uv add --dev pytest
```

## Usage

### Run the Application

From the `phase1-console/` directory:

```bash
uv run python -m todo_app.main
```

Or using the entry point script:

```bash
uv run todo
```

### Main Menu

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

### Example Workflow

1. **Add a task**: Select option 1, enter title "Buy groceries" and description "Milk, eggs, bread"
2. **List tasks**: Select option 2 to view all tasks
3. **Mark complete**: Select option 5, enter task ID, choose 1 for Complete
4. **Update task**: Select option 3, enter task ID, update title or description
5. **Delete task**: Select option 4, enter task ID, confirm deletion
6. **Exit**: Select option 6 to quit

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

## Project Structure

```
phase1-console/
├── pyproject.toml          # Project configuration
├── .python-version         # Python version (3.13)
├── README.md               # This file
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py       # Task dataclass
│       ├── storage.py      # In-memory storage (CRUD)
│       ├── cli.py          # CLI interface
│       └── main.py         # Entry point
└── tests/
    ├── __init__.py
    ├── test_models.py      # Task tests
    ├── test_storage.py     # Storage tests
    └── test_cli.py         # CLI tests
```

## Development

### Code Quality

- Follows PEP8 style guide
- Type hints on all functions
- Modular design (models/storage/cli/main)
- Comprehensive test coverage

### Testing

Tests follow TDD approach:
- Tests written before implementation
- Storage layer fully tested
- CLI layer tested for user flows

## Notes

- All data is stored in memory only
- Data is lost when the application exits
- This is Phase 1 of a 5-phase evolution project
- Phase 2 will add persistent storage with PostgreSQL

## Troubleshooting

### "uv: command not found"

UV is not installed. Follow installation instructions above.

### "Module not found: todo_app"

Make sure you're in the `phase1-console/` directory and run:
```bash
uv sync
```

### Tests Failing

Install dev dependencies:
```bash
uv add --dev pytest
```

## License

This is a hackathon project for learning purposes.

## Next Steps

After Phase 1 completion:
1. Verify all CRUD operations work
2. Run full test suite (100% pass)
3. Validate PEP8 compliance
4. Proceed to Phase 2: Web Application
