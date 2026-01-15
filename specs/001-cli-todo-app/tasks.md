# Tasks: In-Memory Console Todo App

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: User requested TDD style where possible. Tests are included for core logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All paths relative to `phase1-console/` directory
- **Core modules**: `phase1-console/src/todo_app/`
- **Tests**: `phase1-console/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create phase1-console/ directory in project root
- [ ] T002 Initialize UV project in phase1-console/ with Python 3.13+
- [ ] T003 [P] Create pyproject.toml with project metadata, dependencies, and scripts
- [ ] T004 [P] Create .python-version file specifying Python 3.13
- [ ] T005 Create src/todo_app/ directory structure with __init__.py
- [ ] T006 [P] Create tests/ directory structure with __init__.py
- [ ] T007 [P] Create phase1-console/README.md with setup and usage instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 [P] Implement Task dataclass in phase1-console/src/todo_app/models.py
- [ ] T009 [P] Write unit tests for Task dataclass in phase1-console/tests/test_models.py
- [ ] T010 Implement TaskStore class skeleton with __init__ in phase1-console/src/todo_app/storage.py
- [ ] T011 Add validation helper methods (validate_title, validate_description) to phase1-console/src/todo_app/storage.py
- [ ] T012 Write tests for validation helpers in phase1-console/tests/test_storage.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with title and optional description

**Independent Test**: Create multiple tasks with various title lengths and optional descriptions; verify tasks are created with auto-incremented IDs and pending status

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Write test for adding task with title only in phase1-console/tests/test_storage.py
- [ ] T014 [P] [US1] Write test for adding task with title and description in phase1-console/tests/test_storage.py
- [ ] T015 [P] [US1] Write test for validation errors (empty title, too long) in phase1-console/tests/test_storage.py

### Implementation for User Story 1

- [ ] T016 [US1] Implement TaskStore.add() method in phase1-console/src/todo_app/storage.py
- [ ] T017 [US1] Implement add_task_flow() function in phase1-console/src/todo_app/cli.py
- [ ] T018 [US1] Add error handling and success messages for add operation in phase1-console/src/todo_app/cli.py
- [ ] T019 [US1] Write CLI tests for add_task_flow() in phase1-console/tests/test_cli.py
- [ ] T020 [US1] Run tests and verify User Story 1 is fully functional

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List Tasks (Priority: P1)

**Goal**: Users can view all tasks with ID, title, status, and creation date

**Independent Test**: Add multiple tasks, list them to verify all attributes display correctly; test empty list scenario

### Tests for User Story 2 ⚠️

- [ ] T021 [P] [US2] Write test for listing all tasks in phase1-console/tests/test_storage.py
- [ ] T022 [P] [US2] Write test for listing when no tasks exist in phase1-console/tests/test_storage.py

### Implementation for User Story 2

- [ ] T023 [US2] Implement TaskStore.list_all() method in phase1-console/src/todo_app/storage.py
- [ ] T024 [US2] Implement format_task_list() formatting function in phase1-console/src/todo_app/cli.py
- [ ] T025 [US2] Implement list_tasks_flow() function in phase1-console/src/todo_app/cli.py
- [ ] T026 [US2] Write CLI tests for list_tasks_flow() in phase1-console/tests/test_cli.py
- [ ] T027 [US2] Run tests and verify User Story 2 is fully functional

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Status (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete using task ID

**Independent Test**: Add tasks, mark them complete/incomplete, list to verify status changes

### Tests for User Story 3 ⚠️

- [ ] T028 [P] [US3] Write test for marking task as complete in phase1-console/tests/test_storage.py
- [ ] T029 [P] [US3] Write test for marking task as incomplete in phase1-console/tests/test_storage.py
- [ ] T030 [P] [US3] Write test for marking non-existent task in phase1-console/tests/test_storage.py

### Implementation for User Story 3

- [ ] T031 [US3] Implement TaskStore.get() method for retrieving single task in phase1-console/src/todo_app/storage.py
- [ ] T032 [US3] Implement TaskStore.mark_complete() method in phase1-console/src/todo_app/storage.py
- [ ] T033 [US3] Implement mark_complete_flow() function in phase1-console/src/todo_app/cli.py
- [ ] T034 [US3] Write CLI tests for mark_complete_flow() in phase1-console/tests/test_cli.py
- [ ] T035 [US3] Run tests and verify User Story 3 is fully functional

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can update task title or description using task ID

**Independent Test**: Add tasks, update title/description, list to verify changes

### Tests for User Story 4 ⚠️

- [ ] T036 [P] [US4] Write test for updating task title in phase1-console/tests/test_storage.py
- [ ] T037 [P] [US4] Write test for updating task description in phase1-console/tests/test_storage.py
- [ ] T038 [P] [US4] Write test for updating both title and description in phase1-console/tests/test_storage.py
- [ ] T039 [P] [US4] Write test for updating non-existent task in phase1-console/tests/test_storage.py

### Implementation for User Story 4

- [ ] T040 [US4] Implement TaskStore.update() method in phase1-console/src/todo_app/storage.py
- [ ] T041 [US4] Implement update_task_flow() function in phase1-console/src/todo_app/cli.py
- [ ] T042 [US4] Write CLI tests for update_task_flow() in phase1-console/tests/test_cli.py
- [ ] T043 [US4] Run tests and verify User Story 4 is fully functional

**Checkpoint**: User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks using task ID

**Independent Test**: Add tasks, delete specific tasks by ID, list to verify removal

### Tests for User Story 5 ⚠️

- [ ] T044 [P] [US5] Write test for deleting existing task in phase1-console/tests/test_storage.py
- [ ] T045 [P] [US5] Write test for deleting non-existent task in phase1-console/tests/test_storage.py

### Implementation for User Story 5

- [ ] T046 [US5] Implement TaskStore.delete() method in phase1-console/src/todo_app/storage.py
- [ ] T047 [US5] Implement delete_task_flow() function in phase1-console/src/todo_app/cli.py
- [ ] T048 [US5] Write CLI tests for delete_task_flow() in phase1-console/tests/test_cli.py
- [ ] T049 [US5] Run tests and verify User Story 5 is fully functional

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Main Application & Integration

**Purpose**: Wire all user stories together into interactive menu application

- [ ] T050 Implement display_menu() function in phase1-console/src/todo_app/cli.py
- [ ] T051 Implement main() function with menu loop in phase1-console/src/todo_app/main.py
- [ ] T052 Add error handling for Ctrl+C and Ctrl+D in phase1-console/src/todo_app/main.py
- [ ] T053 Add welcome and goodbye messages in phase1-console/src/todo_app/main.py
- [ ] T054 Test full interactive workflow manually (add → list → update → mark → delete → list)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Run pytest and verify all tests pass in phase1-console/
- [ ] T056 [P] Verify PEP8 compliance across all Python files
- [ ] T057 [P] Add docstrings to all public functions in phase1-console/src/todo_app/
- [ ] T058 [P] Update phase1-console/README.md with final usage examples and screenshots
- [ ] T059 Test all edge cases: boundary values, invalid input, large task lists (100+ tasks)
- [ ] T060 Optional: Add Rich library for enhanced output formatting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Main Application (Phase 8)**: Depends on all desired user stories being complete
- **Polish (Phase 9)**: Depends on Main Application being functional

### User Story Dependencies

- **User Story 1 (P1) - Add Tasks**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1) - List Tasks**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2) - Mark Status**: Depends on US1 (need tasks to mark) and US2 (to verify changes)
- **User Story 4 (P2) - Update Task**: Depends on US1 (need tasks to update) and US2 (to verify changes)
- **User Story 5 (P3) - Delete Task**: Depends on US1 (need tasks to delete) and US2 (to verify deletion)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Storage layer before CLI layer
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- User Stories 1 and 2 can be developed in parallel (both P1, no dependencies)
- User Stories 3, 4, 5 should wait for US1 and US2 to complete
- All tests within a user story marked [P] can run in parallel
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for adding task with title only in phase1-console/tests/test_storage.py"
Task: "Write test for adding task with title and description in phase1-console/tests/test_storage.py"
Task: "Write test for validation errors in phase1-console/tests/test_storage.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Tasks)
4. Complete Phase 4: User Story 2 (List Tasks)
5. Complete Phase 8: Main Application (minimal menu with add/list/exit)
6. **STOP and VALIDATE**: Test US1 and US2 independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + User Story 2 → Test independently → MVP Ready!
3. Add User Story 3 (Mark Status) → Test independently → Deploy/Demo
4. Add User Story 4 (Update Task) → Test independently → Deploy/Demo
5. Add User Story 5 (Delete Task) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Tasks)
   - Developer B: User Story 2 (List Tasks)
3. After US1 and US2 complete:
   - Developer A: User Story 3 (Mark Status)
   - Developer B: User Story 4 (Update Task)
   - Developer C: User Story 5 (Delete Task)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All paths are relative to phase1-console/ directory
- Follow TDD: Write tests first, see them fail, then implement
