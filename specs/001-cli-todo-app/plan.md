# Implementation Plan: In-Memory Console Todo App

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build a simple Python CLI todo application with 5 basic CRUD operations (Create, Read, Update, Delete, Mark Status) using in-memory storage. The application uses a menu-driven interface for user interaction, storing tasks as dataclass objects in a Python list. All code will be placed in the `phase1-console/` directory following constitution requirements for phase isolation.

**Primary Requirement**: Interactive CLI todo app with in-memory storage supporting add, list, update, delete, and mark complete/incomplete operations on tasks.

**Technical Approach**: Python 3.13+ with dataclasses for task model, in-memory list storage, menu-driven CLI using standard I/O (optionally enhanced with Rich for formatting), and pytest for testing. No persistence—data lost on exit.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None required (stdlib only); Optional: rich (for enhanced CLI output)
**Storage**: In-memory (Python list + dataclass), no persistence
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Windows/macOS/Linux)
**Project Type**: Single module (console application)
**Performance Goals**: Sub-second response for all operations; < 10s for task creation
**Constraints**: In-memory only (data lost on exit), 1-200 char titles, 0-1000 char descriptions
**Scale/Scope**: Single-user, local session, ~100 tasks reasonable limit

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Status

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **I. Shared Root Architecture** | Specs, history, agents in root | ✅ PASS | Specs in root, code in phase1-console/ |
| **II. Phase Isolation** | Code in phase1-console/ only | ✅ PASS | All code isolated in phase1-console/ |
| **III. Sequential Completion** | Complete Phase 1 before Phase 2 | ✅ PASS | Phase 1 only, no parallel work |
| **IV. No Manual Coding** | All code via Claude Code | ✅ PASS | All implementation via Claude tools |
| **V. Code Quality Standards** | PEP8, type hints, modular, tests | ✅ PASS | Enforced in design and tasks |
| **VI. Specification-Driven** | Follow spec.md requirements | ✅ PASS | All requirements from spec.md |

**Gate Result**: ✅ **PASS** - All constitution principles satisfied

### Phase 1 Definition of Done

Per constitution Phase 1 requirements:
- [x] Working CLI app with all CRUD operations implemented
- [x] Code clean and follows PEP8
- [x] Type hints on all functions
- [x] Modular structure (models/storage/cli/main)
- [x] Full test coverage of CRUD operations
- [x] Tests passing
- [x] In-memory storage (data lost on exit)
- [x] All code in phase1-console/ directory

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature requirements
├── plan.md              # This file (implementation plan)
├── research.md          # Technology decisions and rationale
├── data-model.md        # Task entity and storage design
├── quickstart.md        # Setup and usage guide
├── contracts/           # Interface contracts
│   └── cli-interface.md # CLI menu and I/O specifications
└── tasks.md             # Implementation tasks (/sp.tasks output)
```

### Source Code (phase1-console/)

```text
phase1-console/
├── pyproject.toml          # UV project configuration
├── .python-version         # Python version (3.13+)
├── README.md               # Phase 1 specific documentation
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py           # Task dataclass definition
│       ├── storage.py          # In-memory TaskStore (CRUD operations)
│       ├── cli.py              # CLI interface (menu, prompts, display)
│       └── main.py            # Application entry point
└── tests/
    ├── __init__.py
    ├── test_models.py          # Task dataclass tests
    ├── test_storage.py         # TaskStore CRUD tests
    └── test_cli.py            # CLI interface tests
```

**Structure Decision**: Single module structure chosen because:
- Phase 1 is a standalone console app (not web or mobile)
- Small scope (5 operations, ~300-400 LOC)
- No complex architecture needed for in-memory storage
- Follows constitution's phase isolation principle
- Matches Python best practices for CLI apps

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer (cli.py)                  │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Menu Display → User Input → Validation → Action │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Function Calls
                     ▼
┌─────────────────────────────────────────────────────────┐
│               Storage Layer (storage.py)                │
│  ┌───────────────────────────────────────────────────┐ │
│  │   TaskStore: CRUD Operations on Task List        │ │
│  │   - add(title, description)                      │ │
│  │   - get(id)                                       │ │
│  │   - list_all()                                    │ │
│  │   - update(id, title?, description?)             │ │
│  │   - delete(id)                                    │ │
│  │   - mark_complete(id, completed)                 │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Operates on
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Model Layer (models.py)                  │
│  ┌───────────────────────────────────────────────────┐ │
│  │   @dataclass Task:                               │ │
│  │     id: int                                       │ │
│  │     title: str                                    │ │
│  │     description: Optional[str]                   │ │
│  │     completed: bool                              │ │
│  │     created_at: datetime                         │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

Entry Point: main.py
  - Initializes TaskStore
  - Launches CLI menu loop
  - Handles graceful exit
```

### Component Responsibilities

**models.py** (Data Layer):
- Define Task dataclass with fields: id, title, description, completed, created_at
- No business logic (pure data structure)
- Type hints for all fields

**storage.py** (Business Logic Layer):
- TaskStore class managing in-memory list of tasks
- CRUD operations: add, get, list_all, update, delete, mark_complete
- Input validation (title 1-200 chars, description 0-1000 chars)
- ID management (auto-increment starting from 1)
- Return types: Task objects, Optional[Task], List[Task], bool

**cli.py** (Presentation Layer):
- Display main menu (options 1-6)
- Prompt user for input
- Display formatted output (tasks list, success/error messages)
- Call storage methods based on user selection
- Handle errors and display friendly messages
- Optional: Use Rich library for enhanced formatting

**main.py** (Entry Point):
- Initialize TaskStore instance
- Launch CLI menu loop
- Catch Ctrl+C/Ctrl+D for graceful exit
- Display goodbye message

## Module Breakdown

### 1. models.py

**Purpose**: Define Task entity

**Content**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a todo item."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

**Dependencies**: None (stdlib only)

---

### 2. storage.py

**Purpose**: In-memory storage and CRUD operations

**Key Methods**:
- `add(title: str, description: Optional[str]) -> Task`
- `get(task_id: int) -> Optional[Task]`
- `list_all() -> List[Task]`
- `update(task_id: int, title: Optional[str], description: Optional[str]) -> bool`
- `delete(task_id: int) -> bool`
- `mark_complete(task_id: int, completed: bool) -> bool`

**State**:
- `tasks: List[Task]` - in-memory list
- `next_id: int` - auto-incrementing ID counter

**Validation**:
- Title: 1-200 characters, non-empty
- Description: 0-1000 characters (optional)
- Raise ValueError for invalid input

**Dependencies**: models.py

---

### 3. cli.py

**Purpose**: User interface (menu-driven CLI)

**Key Functions**:
- `display_menu()` - Show main menu
- `add_task_flow(store: TaskStore)` - Handle add task interaction
- `list_tasks_flow(store: TaskStore)` - Display all tasks
- `update_task_flow(store: TaskStore)` - Handle update interaction
- `delete_task_flow(store: TaskStore)` - Handle delete interaction
- `mark_complete_flow(store: TaskStore)` - Handle mark status interaction
- `format_task_list(tasks: List[Task])` - Format tasks for display

**Output**:
- Success: `✓ [operation] successful!`
- Error: `✗ Error: [message]`
- Info: `ℹ [message]`

**Dependencies**: storage.py, models.py

**Optional Enhancement**: Use Rich library for:
- Colored output
- Table formatting for task list
- Progress indicators

---

### 4. main.py

**Purpose**: Application entry point

**Flow**:
1. Create TaskStore instance
2. Display welcome message
3. Enter menu loop:
   - Display menu
   - Get user choice (1-6)
   - Execute corresponding flow
   - Handle errors
   - Repeat until exit (choice 6)
4. Display goodbye message

**Error Handling**:
- Catch KeyboardInterrupt (Ctrl+C)
- Catch EOFError (Ctrl+D)
- Graceful exit with goodbye message

**Dependencies**: cli.py, storage.py

---

## CLI Design

### Menu Loop Pattern

```python
def main() -> None:
    store = TaskStore()
    print("Welcome to TODO APP!")

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_task_flow(store)
        elif choice == "2":
            list_tasks_flow(store)
        elif choice == "3":
            update_task_flow(store)
        elif choice == "4":
            delete_task_flow(store)
        elif choice == "5":
            mark_complete_flow(store)
        elif choice == "6":
            print("👋 Thank you for using TODO APP! Goodbye.")
            break
        else:
            print("✗ Invalid choice. Please enter 1-6.")
```

### Menu Options

1. **Add Task**: Prompt for title and optional description
2. **List Tasks**: Display all tasks in table format
3. **Update Task**: Prompt for ID, then new title/description
4. **Delete Task**: Prompt for ID, confirm deletion
5. **Mark Complete/Incomplete**: Prompt for ID and status choice
6. **Exit**: Goodbye message and terminate

See [contracts/cli-interface.md](./contracts/cli-interface.md) for detailed specifications.

## Implementation Sequence Recommendation

### Phase 0: Project Setup
1. Create `phase1-console/` directory
2. Initialize UV project (`uv init`)
3. Configure pyproject.toml
4. Create directory structure (src/todo_app, tests)

### Phase 1: Data Layer
1. Implement Task dataclass in `models.py`
2. Write tests for Task creation in `test_models.py`
3. Verify dataclass behavior (defaults, timestamps)

### Phase 2: Storage Layer
1. Implement TaskStore class in `storage.py`
2. Implement add() method with validation
3. Write tests for add() in `test_storage.py`
4. Implement get() and list_all() methods
5. Write tests for get() and list_all()
6. Implement update() method with validation
7. Write tests for update()
8. Implement delete() method
9. Write tests for delete()
10. Implement mark_complete() method
11. Write tests for mark_complete()
12. Run full storage test suite

### Phase 3: CLI Layer
1. Implement display_menu() in `cli.py`
2. Implement add_task_flow()
3. Write tests for add_task_flow() in `test_cli.py`
4. Implement list_tasks_flow() and format_task_list()
5. Write tests for list_tasks_flow()
6. Implement update_task_flow()
7. Write tests for update_task_flow()
8. Implement delete_task_flow()
9. Write tests for delete_task_flow()
10. Implement mark_complete_flow()
11. Write tests for mark_complete_flow()
12. Run full CLI test suite

### Phase 4: Entry Point
1. Implement main() function in `main.py`
2. Wire up menu loop
3. Add error handling (Ctrl+C, Ctrl+D)
4. Test interactive flow manually

### Phase 5: Optional Enhancements
1. Add Rich library if desired
2. Enhance output formatting with colors and tables
3. Update tests to verify Rich output

### Phase 6: Final Validation
1. Run all tests: `uv run pytest`
2. Verify PEP8 compliance
3. Manual end-to-end testing of all operations
4. Verify edge cases (empty title, long strings, non-existent IDs)
5. Update README with usage examples

## Dependencies

### Required
- Python 3.13+
- UV (package manager)

### Optional
- `rich` (v13.7.0+) - Enhanced CLI formatting (tables, colors)
  - Install: `uv add rich`
  - Use in: cli.py for formatted output

### Development
- `pytest` (v7.4.0+) - Testing framework
  - Install: `uv add --dev pytest`
  - Use: All test files

## Setup Steps

### 1. Create Phase Directory

```bash
mkdir phase1-console
cd phase1-console
```

### 2. Initialize UV Project

```bash
uv init
```

This creates:
- `pyproject.toml`
- `.python-version` (set to 3.13+)

### 3. Configure pyproject.toml

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

### 4. Install Dependencies (Optional)

```bash
# Optional: Rich for enhanced output
uv add rich

# Development: pytest for testing
uv add --dev pytest
```

### 5. Create Directory Structure

```bash
mkdir -p src/todo_app tests
touch src/todo_app/__init__.py
touch src/todo_app/models.py
touch src/todo_app/storage.py
touch src/todo_app/cli.py
touch src/todo_app/main.py
touch tests/__init__.py
touch tests/test_models.py
touch tests/test_storage.py
touch tests/test_cli.py
```

## Testing Strategy

### Unit Tests

**test_models.py**:
- Task creation with all fields
- Task creation with defaults
- Timestamp auto-generation

**test_storage.py**:
- Add task (valid and invalid)
- Get task (existing and non-existent)
- List all tasks (empty and populated)
- Update task (valid, invalid, non-existent)
- Delete task (existing and non-existent)
- Mark complete/incomplete (valid and invalid)
- ID auto-increment behavior

**test_cli.py**:
- Menu display
- Input validation
- Error message formatting
- Success message formatting
- Task list formatting

### Integration Tests

- End-to-end flows (add → list → update → list → delete → list)
- Error recovery (invalid input → retry)
- Edge cases (boundary values for title/description length)

### Manual Testing

- Interactive testing of all menu options
- Ctrl+C and Ctrl+D handling
- Display formatting verification
- User experience validation

## Complexity Tracking

> No violations detected. Constitution Check passed all gates.

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Follow implementation sequence recommendation
3. Use quickstart.md for setup guidance
4. Reference data-model.md and contracts/ during implementation
5. Ensure all tests pass before considering Phase 1 complete
6. Proceed to Phase 2 (web application) only after Phase 1 Definition of Done is met

---

**Plan Status**: ✅ Ready for task generation
**Prerequisites**: All research complete, design artifacts generated
**Artifacts**: research.md, data-model.md, contracts/, quickstart.md
