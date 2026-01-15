# CLI Interface Contract: In-Memory Console Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-30
**Type**: Internal CLI Contract (User Interface)

## Overview

This document defines the command-line interface contract for the todo application, including menu options, input prompts, output formats, and error handling.

## Main Menu

### Display Format

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

### Menu Loop

- Display menu after each operation completes
- Wait for user input (1-6)
- Execute corresponding action
- Display success/error message
- Return to menu (unless exit selected)

## Operation Contracts

### 1. Add Task

**Input Prompts**:
```
Enter task title (1-200 characters): _
Enter task description (optional, max 1000 characters): _
```

**Success Output**:
```
✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Pending
  Created: 2025-12-30 10:00
```

**Error Cases**:
- Empty title: `✗ Error: Title cannot be empty`
- Title > 200 chars: `✗ Error: Title must be between 1 and 200 characters`
- Description > 1000 chars: `✗ Error: Description must be at most 1000 characters`

---

### 2. List Tasks

**No Input Required**

**Success Output (with tasks)**:
```
═══════════════════════════════════════════════════════════════
  📋 Task List (3 tasks)
═══════════════════════════════════════════════════════════════

┌────┬────────────────────────┬───────────┬─────────────────────┐
│ ID │ Title                 │ Status    │ Created            │
├────┼────────────────────────┼───────────┼─────────────────────┤
│  1 │ Buy groceries         │ Pending   │ 2025-12-30 10:00   │
│  2 │ Complete project      │ Complete  │ 2025-12-30 11:30   │
│  3 │ Call mom             │ Pending   │ 2025-12-30 12:00   │
└────┴────────────────────────┴───────────┴─────────────────────┘

(Use option 3/4/5 for details/update/delete/mark)
```

**Success Output (no tasks)**:
```
ℹ No tasks found. Add your first task with option 1!
```

---

### 3. Update Task

**Input Prompts**:
```
Enter task ID to update: _
Enter new title (leave blank to keep current): _
Enter new description (leave blank to keep current): _
```

**Success Output**:
```
✓ Task updated successfully!
  ID: 1
  Title: Buy groceries and household items
  Description: Milk, eggs, bread, soap
  Status: Pending
  Created: 2025-12-30 10:00
```

**Error Cases**:
- Non-existent ID: `✗ Error: Task not found (ID: 99)`
- Invalid ID format: `✗ Error: Invalid task ID. Please enter a number`
- New title > 200 chars: `✗ Error: Title must be between 1 and 200 characters`
- New description > 1000 chars: `✗ Error: Description must be at most 1000 characters`
- Both fields blank: `ℹ No changes made`

---

### 4. Delete Task

**Input Prompts**:
```
Enter task ID to delete: _
Are you sure you want to delete this task? (y/n): _
```

**Success Output**:
```
✓ Task deleted successfully! (ID: 2)
```

**Error Cases**:
- Non-existent ID: `✗ Error: Task not found (ID: 99)`
- Invalid ID format: `✗ Error: Invalid task ID. Please enter a number`
- User cancels (n): `ℹ Delete cancelled`

---

### 5. Mark Task Complete/Incomplete

**Input Prompts**:
```
Enter task ID: _
Mark as (1) Complete or (2) Incomplete: _
```

**Success Output (mark complete)**:
```
✓ Task marked as complete!
  ID: 1
  Title: Buy groceries
  Status: Complete
```

**Success Output (mark incomplete)**:
```
✓ Task marked as incomplete!
  ID: 2
  Title: Complete project
  Status: Pending
```

**Error Cases**:
- Non-existent ID: `✗ Error: Task not found (ID: 99)`
- Invalid ID format: `✗ Error: Invalid task ID. Please enter a number`
- Invalid choice (not 1 or 2): `✗ Error: Invalid choice. Enter 1 or 2`

---

### 6. Exit

**Output**:
```
👋 Thank you for using TODO APP! Goodbye.
```

## Error Handling

### Input Validation Errors

All validation errors should:
1. Display clear error message with `✗` prefix
2. Explain what went wrong
3. Indicate valid input range/format
4. Allow user to retry or return to menu

### System Errors

For unexpected errors:
```
✗ An unexpected error occurred: [error message]
  Please try again or report this issue.
```

## Status Indicators

- `✓` - Success
- `✗` - Error
- `ℹ` - Info
- `📝` - Todo App Icon
- `📋` - List Icon
- `👋` - Goodbye Icon

## Date/Time Format

**Standard Format**: `YYYY-MM-DD HH:MM`

Examples:
- `2025-12-30 10:00`
- `2025-12-30 23:45`

## Color Scheme (if Rich used)

- Menu title: Bold cyan
- Success messages: Green
- Error messages: Red
- Info messages: Yellow
- Task status "Pending": Yellow
- Task status "Complete": Green
- Prompts: White
- Table headers: Bold white

## Input Handling

### General Rules
1. Trim leading/trailing whitespace from all inputs
2. Accept case-insensitive menu choices (1-6)
3. Validate input before processing
4. Provide clear error messages for invalid input
5. Allow blank input where optional

### Special Cases
- Ctrl+C: Gracefully exit with goodbye message
- Ctrl+D (EOF): Gracefully exit with goodbye message
- Empty line on optional field: Keep existing value (update) or skip (add)

## Exit Codes

- `0` - Normal exit
- `1` - Error during execution (unexpected errors only)

## Non-Interactive Mode

Not supported in Phase 1. All operations require interactive menu-driven input.
