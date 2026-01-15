# Data Model: In-Memory Console Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-30

## Entity: Task

### Description
Represents a todo item that users can create, view, update, delete, and mark as complete/incomplete.

### Fields

| Field | Type | Required | Constraints | Description |
|--------|-------|-----------|-------------|
| `id` | `int` | Yes | Auto-incrementing, unique, starts from 1 |
| `title` | `str` | Yes | 1-200 characters, cannot be empty |
| `description` | `str | None` | No | 0-1000 characters, optional |
| `completed` | `bool` | Yes | `False` (pending) or `True` (complete), defaults to `False` |
| `created_at` | `datetime` | Yes | Timestamp of task creation |

### Python Dataclass Definition

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a todo item in the in-memory store."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

### Validation Rules

#### Title Validation
- Minimum length: 1 character
- Maximum length: 200 characters
- Cannot be empty string or whitespace-only
- Must be string type
- Error message: "Title must be between 1 and 200 characters"

#### Description Validation
- Minimum length: 0 characters (optional, can be None)
- Maximum length: 1000 characters
- Can be None (not provided)
- If provided as string, must be <= 1000 chars
- Error message: "Description must be at most 1000 characters"

#### ID Validation
- Must be positive integer (> 0)
- Must exist in storage for update/delete/mark operations
- Error message: "Task not found"

### State Transitions

```
┌─────────────┐
│   Created   │ (completed=False, created_at set)
└──────┬──────┘
       │
       │ Mark Complete
       ▼
┌─────────────┐
│  Completed  │ (completed=True)
└──────┬──────┘
       │
       │ Mark Incomplete
       ▼
┌─────────────┐
│   Created   │ (completed=False)
└─────────────┘
```

**Allowed Transitions**:
- Create → Pending (initial state, completed=False)
- Pending → Completed (user marks task complete)
- Completed → Pending (user marks task incomplete)

**Transitions Prohibited**:
- Direct Create → Completed (must go through Pending)
- No other state changes

### Invariants

1. ID Uniqueness: Each task has a unique ID that never changes
2. ID Monotonic: New tasks always get the next highest ID
3. Immutability of ID: Task ID cannot be changed after creation
4. Title Required: Every task must have a non-empty title
5. Timestamp Accuracy: created_at never changes after task creation

### Relationships

None. Tasks are standalone entities with no relationships to other entities.

### Collection Structure

```
TaskStore (in-memory collection)
│
├── tasks: List[Task]       # All tasks in insertion order
├── next_id: int              # Next available ID (starts at 1)
│
└── Methods:
    ├── add(title, description) → Task
    ├── get(id) → Task | None
    ├── list_all() → List[Task]
    ├── update(id, title?, description?) → bool
    ├── delete(id) → bool
    └── mark_complete(id, completed) → bool
```

### Storage Layer API

```python
class TaskStore:
    """In-memory storage for tasks."""

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task and return it with assigned ID."""
        pass

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID, or None if not found."""
        pass

    def list_all(self) -> List[Task]:
        """Get all tasks in insertion order."""
        pass

    def update(self, task_id: int, title: Optional[str] = None,
             description: Optional[str] = None) -> bool:
        """Update task title and/or description. Returns True if found."""
        pass

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if found."""
        pass

    def mark_complete(self, task_id: int, completed: bool) -> bool:
        """Mark task as complete or incomplete. Returns True if found."""
        pass
```

### Example Data

```python
# Example tasks in storage
[
    Task(
        id=1,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=datetime(2025, 12, 30, 10, 0, 0)
    ),
    Task(
        id=2,
        title="Complete project report",
        description=None,
        completed=True,
        created_at=datetime(2025, 12, 30, 11, 30, 0)
    ),
    Task(
        id=3,
        title="Call mom",
        description="Wish her happy birthday",
        completed=False,
        created_at=datetime(2025, 12, 30, 12, 0, 0)
    )
]
```

### Display Format

When listing tasks, display as table:

```
┌────┬──────────────────────┬───────────┬─────────────────────┐
│ ID │ Title               │ Status    │ Created            │
├────┼──────────────────────┼───────────┼─────────────────────┤
│  1 │ Buy groceries       │ Pending    │ 2025-12-30 10:00 │
│  2 │ Complete project    │ Complete   │ 2025-12-30 11:30 │
│  3 │ Call mom            │ Pending    │ 2025-12-30 12:00 │
└────┴──────────────────────┴───────────┴─────────────────────┘
```

Or simple text format (if Rich not used):

```
ID: 1 | Title: Buy groceries | Status: Pending | Created: 2025-12-30 10:00
ID: 2 | Title: Complete project | Status: Complete | Created: 2025-12-30 11:30
ID: 3 | Title: Call mom | Status: Pending | Created: 2025-12-30 12:00
```
