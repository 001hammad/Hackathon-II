# Research: Phase I - In-Memory Console Todo App

**Feature**: In-Memory Console Todo App
**Date**: 2025-12-30
**Purpose**: Resolve technical decisions for implementation

## Technology Decisions

### Python Version

**Decision**: Python 3.13+

**Rationale**: Specified in technical constraints. Python 3.13 is the latest stable release, providing modern features, improved performance, and long-term support.

**Alternatives considered**:
- Python 3.11/3.12: Slightly older, but stable; rejected to use latest as specified
- Python 3.14 (beta): Not stable; rejected for production code

---

### Dependency Management

**Decision**: UV for virtual environment and dependency management

**Rationale**: Specified in technical constraints. UV is a modern, fast Python package manager and project tool that provides superior performance compared to pip/venv, with unified project management via pyproject.toml.

**Alternatives considered**:
- pip + venv: Standard approach but slower; rejected as UV is specified
- Poetry: Mature but heavier weight; rejected as UV is specified
- PDM: Good alternative but UV specified in constraints

---

### Dependencies

**Decision**: No external packages for core functionality (Python stdlib only). Optional: `rich` for pretty formatting

**Rationale**: Spec specifies "minimal external packages (only if needed for better formatting)". Core functionality can be achieved with standard library. Rich provides enhanced CLI output with colors, tables, and progress bars, improving user experience significantly while keeping dependency minimal.

**Alternatives considered**:
- `typer`: Powerful CLI framework but overkill for simple menu
- `click`: Feature-rich CLI library but adds complexity
- `argparse` (stdlib): Sufficient but less elegant than rich tables
- `prompt_toolkit`: Advanced input handling but unnecessary complexity

---

### Storage Strategy

**Decision**: In-memory using Python dataclasses and list

**Rationale**: Spec explicitly requires "in-memory storage only (data lost on exit)". Using a Python list with Task dataclass objects provides type safety, clean code structure, and meets requirements without complexity.

**Alternatives considered**:
- Dictionary with ID keys: Fast lookup but doesn't preserve insertion order cleanly
- Class-based objects: More verbose than dataclasses; rejected for conciseness
- Database (SQLite, etc.): Violates "in-memory only" requirement

---

### CLI Design Pattern

**Decision**: Menu-driven interactive CLI with numbered options

**Rationale**: Spec allows "menu-driven or command-based". Menu-driven is more intuitive for a simple todo app, provides clear options display, and guides users through operations without requiring command memorization. Better for first-time users.

**Alternatives considered**:
- Command-based (e.g., `todo add`, `todo list`): More efficient for power users but steeper learning curve
- Mixed approach (menu + commands): Adds unnecessary complexity for this phase

---

### Input/Output Design

**Decision**: Standard I/O (stdin/stdout) with Rich for formatted output

**Rationale**: Using Python's built-in `input()` for user input and `print()` for output is standard for CLI apps. Rich library enhances output with tables, colors, and formatting while maintaining simplicity.

**Alternatives considered**:
- `prompt_toolkit`: Powerful but overkill for simple input
- `readline` (stdlib): Basic but lacks formatting options

---

### Code Organization

**Decision**: Modular structure with clear separation: models, storage, cli, main

**Rationale**: Follows constitution requirements for modular, clean code with PEP8 compliance. Separating concerns improves testability and maintainability.

**Alternatives considered**:
- Single-file script: Easier but violates modularity principle
- Complex package structure: Over-engineering for simple phase

---

### Testing Framework

**Decision**: pytest (no external dependency if not needed; otherwise minimal setup)

**Rationale**: pytest is the de facto standard for Python testing, provides fixtures, parametrization, and clean assertion output. Can be included via UV if needed.

**Alternatives considered**:
- unittest (stdlib): Sufficient but less feature-rich
- nose2: Less popular, maintained sporadically

---

### Project Structure

**Decision**: Single module inside phase1-console/ directory

**Rationale**: Constitution requires phase isolation. All code goes in phase1-console/ folder with standard Python project layout.

Structure:
```
phase1-console/
├── pyproject.toml          # UV project configuration
├── src/
│   ├── todo_app/
│   │   ├── __init__.py
│   │   ├── models.py           # Task dataclass
│   │   ├── storage.py          # In-memory storage layer
│   │   ├── cli.py              # CLI interface and menu
│   │   └── main.py            # Entry point
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_storage.py
    └── test_cli.py
```

**Alternatives considered**:
- Flat structure in phase1-console/: No separation of concerns
- Nested packages: Unnecessary complexity for this phase

---

## Summary of Technical Decisions

| Decision | Choice | Key Rationale |
|-----------|----------|----------------|
| Python Version | 3.13+ | Specified in constraints |
| Package Manager | UV | Specified in constraints |
| Core Dependencies | None (stdlib only) | Keep minimal as specified |
| Optional Dependencies | rich (for formatting) | Better UX, minimal addition |
| Storage | In-memory dataclass + list | Spec requirement |
| CLI Pattern | Menu-driven | Intuitive for simple app |
| I/O | stdin/stdout + Rich | Standard + enhanced output |
| Organization | Modular (models/storage/cli/main) | Clean, testable, PEP8 |
| Testing | pytest | Standard Python testing |
| Structure | Single module in phase1-console/ | Phase isolation required |

## Next Steps

1. Create Phase 1 artifacts: data-model.md, contracts/, quickstart.md
2. Proceed to implementation planning (tasks.md via /sp.tasks)
