# Tasks: Phase II Full-Stack Multi-User Web Todo Application

**Input**: Design documents from `/specs/001-phase2-web-todo/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are NOT explicitly requested in specification - implementation-focused tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase2-web/backend/` and `phase2-web/frontend/`
- Backend paths assume: `phase2-web/backend/app/`
- Frontend paths assume: `phase2-web/frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [x] T001 Create phase2-web directory structure (frontend/ and backend/ subdirectories)
- [x] T002 Initialize backend Python project with venv in phase2-web/backend/
- [x] T003 [P] Create backend requirements.txt with dependencies (FastAPI, SQLModel, python-jose, uvicorn, psycopg2, asyncpg, passlib, python-dotenv, pytest)
- [x] T004 [P] Create backend .env template file in phase2-web/backend/.env with placeholders (DATABASE_URL, BETTER_AUTH_SECRET, ALGORITHM)
- [x] T005 [P] Create backend directory structure (app/models, app/routes, app/auth, app/database, app/schemas, app/core, tests/)
- [x] T006 Initialize frontend Next.js project with TypeScript and App Router in phase2-web/frontend/
- [x] T007 [P] Install frontend dependencies (Better Auth, Tailwind CSS, shadcn/ui, Framer Motion, class-variance-authority, clsx, tailwind-merge)
- [x] T008 [P] Create frontend .env.local template with placeholders (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET)
- [x] T009 [P] Configure Tailwind CSS in phase2-web/frontend/tailwind.config.ts
- [x] T010 [P] Initialize shadcn/ui in phase2-web/frontend/ using nextjs-app-router skill

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T011 [P] Create database connection module in phase2-web/backend/app/database/connection.py using neon-sqlmodel-db skill
- [x] T012 [P] Create database initialization module in phase2-web/backend/app/database/init.py with create_tables function using neon-sqlmodel-db skill
- [x] T013 [P] Create core configuration module in phase2-web/backend/app/core/config.py to load environment variables
- [x] T014 [P] Create security utilities in phase2-web/backend/app/core/security.py for password hashing (bcrypt) using backend-auth skill
- [x] T015 [P] Create User model in phase2-web/backend/app/models/user.py using neon-sqlmodel-db skill (id UUID, email unique, password_hash, timestamps)
- [x] T016 [P] Create Task model in phase2-web/backend/app/models/task.py using neon-sqlmodel-db skill (id int, user_id FK, description, completed boolean, timestamps)
- [x] T017 Create JWT verification dependency in phase2-web/backend/app/auth/dependencies.py using backend-auth skill (get_current_user function)
- [x] T018 Create FastAPI main app instance in phase2-web/backend/app/main.py with CORS middleware configuration
- [x] T019 Create Pydantic schemas in phase2-web/backend/app/schemas/auth.py (SignupRequest, LoginRequest, AuthResponse)
- [x] T020 [P] Create Pydantic schemas in phase2-web/backend/app/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)

### Frontend Foundation

- [x] T021 [P] Create root layout in phase2-web/frontend/app/layout.tsx using nextjs-app-router skill
- [x] T022 [P] Create global styles in phase2-web/frontend/styles/globals.css with Tailwind directives
- [x] T023 [P] Create utils module in phase2-web/frontend/lib/utils.ts with cn() helper for Tailwind using tailwind skill
- [x] T024 Create API client base in phase2-web/frontend/lib/api/client.ts with JWT token attachment logic using frontend-api-client skill
- [x] T025 [P] Install shadcn/ui Button component in phase2-web/frontend/components/ui/button.tsx using shadcn skill
- [x] T026 [P] Install shadcn/ui Input component in phase2-web/frontend/components/ui/input.tsx using shadcn skill
- [x] T027 [P] Install shadcn/ui Checkbox component in phase2-web/frontend/components/ui/checkbox.tsx using shadcn skill
- [x] T028 [P] Install shadcn/ui Dialog component in phase2-web/frontend/components/ui/dialog.tsx using shadcn skill
- [x] T029 [P] Install shadcn/ui Toast component in phase2-web/frontend/components/ui/toast.tsx using shadcn skill

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in, and maintain authenticated sessions

**Independent Test**: Create new account → logout → login → verify session persists → logout

### Backend Implementation for User Story 1

- [x] T030 [US1] Implement POST /api/auth/signup endpoint in phase2-web/backend/app/routes/auth.py using backend-auth skill (email validation, password hashing, JWT issuance)
- [x] T031 [US1] Implement POST /api/auth/login endpoint in phase2-web/backend/app/routes/auth.py using backend-auth skill (credential verification, JWT issuance)
- [x] T032 [US1] Implement POST /api/auth/logout endpoint in phase2-web/backend/app/routes/auth.py (session termination guidance)
- [x] T033 [US1] Register auth router in phase2-web/backend/app/main.py

### Frontend Implementation for User Story 1

- [x] T034 [P] [US1] Create auth layout in phase2-web/frontend/app/(auth)/layout.tsx using frontend-auth and shadcn skills (centered card design)
- [x] T035 [P] [US1] Create signup page in phase2-web/frontend/app/(auth)/signup/page.tsx using frontend-auth and shadcn skills (form with email, password, validation)
- [x] T036 [P] [US1] Create login page in phase2-web/frontend/app/(auth)/login/page.tsx using frontend-auth and shadcn skills (form with email, password, error handling)
- [x] T037 [US1] Configure Better Auth client in phase2-web/frontend/lib/auth/config.ts using frontend-auth skill (JWT cookie storage) - Integrated in API client
- [x] T038 [US1] Create useAuth hook in phase2-web/frontend/lib/auth/hooks.ts using frontend-auth skill (login, signup, logout functions) - Integrated in API client
- [x] T039 [US1] Create protected route middleware in phase2-web/frontend/middleware.ts using frontend-auth skill (redirect unauthenticated users)
- [x] T040 [US1] Create auth API client functions in phase2-web/frontend/lib/api/auth.ts using frontend-api-client skill (signup, login, logout API calls) - Integrated in API client

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, login, logout independently

---

## Phase 4: User Story 2 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create, view, edit, toggle, and delete personal tasks

**Independent Test**: Login → add tasks → view list (only own tasks) → toggle completion → edit description → delete task

### Backend Implementation for User Story 2

- [x] T041 [P] [US2] Implement GET /api/tasks endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (list user's tasks, filter by user_id from JWT)
- [x] T042 [P] [US2] Implement POST /api/tasks endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (create task, auto-set user_id from JWT)
- [x] T043 [P] [US2] Implement GET /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (get specific task, verify ownership)
- [x] T044 [P] [US2] Implement PUT /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (update description, verify ownership)
- [x] T045 [P] [US2] Implement PATCH /api/tasks/{id}/toggle endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (toggle completed status, verify ownership)
- [x] T046 [P] [US2] Implement DELETE /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py using crud-rest-api and backend-auth skills (delete task, verify ownership)
- [x] T047 [US2] Register tasks router in phase2-web/backend/app/main.py

### Frontend Implementation for User Story 2

- [x] T048 [P] [US2] Create dashboard layout in phase2-web/frontend/app/(dashboard)/layout.tsx using nextjs-app-router, shadcn, and tailwind skills (header with logout button)
- [x] T049 [US2] Create Header component in phase2-web/frontend/components/Header.tsx using shadcn and tailwind skills (app title, logout button)
- [x] T050 [US2] Create main dashboard page in phase2-web/frontend/app/(dashboard)/page.tsx using nextjs-app-router skill (container for task list and form)
- [x] T051 [P] [US2] Create TaskForm component in phase2-web/frontend/components/TaskForm.tsx using shadcn and tailwind skills (input field, submit button, validation)
- [x] T052 [P] [US2] Create TaskList component in phase2-web/frontend/components/TaskList.tsx using shadcn and tailwind skills (renders array of TaskItem components)
- [x] T053 [P] [US2] Create TaskItem component in phase2-web/frontend/components/TaskItem.tsx using shadcn and tailwind skills (checkbox, description, edit/delete buttons)
- [x] T054 [US2] Create task API client functions in phase2-web/frontend/lib/api/tasks.ts using frontend-api-client skill (fetchTasks, createTask, updateTask, toggleTask, deleteTask) - Integrated in API client
- [x] T055 [US2] Integrate TaskForm with createTask API in phase2-web/frontend/components/TaskForm.tsx (handle submit, show success/error toast)
- [x] T056 [US2] Integrate TaskList with fetchTasks API in phase2-web/frontend/app/(dashboard)/page.tsx (load tasks on mount, display in list)
- [x] T057 [US2] Integrate TaskItem with toggleTask API in phase2-web/frontend/components/TaskItem.tsx (handle checkbox click)
- [x] T058 [US2] Implement inline edit functionality in TaskItem with updateTask API in phase2-web/frontend/components/TaskItem.tsx (edit button → input field → save)
- [x] T059 [US2] Implement delete with confirmation in TaskItem with deleteTask API in phase2-web/frontend/components/TaskItem.tsx (delete button → dialog confirmation → API call)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - complete MVP with auth + task CRUD

---

## Phase 5: User Story 3 - Responsive Cross-Device Experience (Priority: P2)

**Goal**: Ensure application works seamlessly on mobile (320px+), tablet (768px+), and desktop (1024px+) devices

**Independent Test**: Access app on mobile device → verify touch-friendly UI → access on tablet → verify optimal spacing → access on desktop → verify layout efficiency

### Responsive Design Implementation for User Story 3

- [ ] T060 [P] [US3] Add mobile-first responsive styles to auth layout in phase2-web/frontend/app/(auth)/layout.tsx using tailwind skill (breakpoints: base, md:, lg:)
- [ ] T061 [P] [US3] Add mobile-first responsive styles to signup page in phase2-web/frontend/app/(auth)/signup/page.tsx using tailwind skill (form width, padding, font sizes)
- [ ] T062 [P] [US3] Add mobile-first responsive styles to login page in phase2-web/frontend/app/(auth)/login/page.tsx using tailwind skill (form width, padding, font sizes)
- [ ] T063 [P] [US3] Add mobile-first responsive styles to dashboard layout in phase2-web/frontend/app/(dashboard)/layout.tsx using tailwind skill (header, container widths)
- [ ] T064 [P] [US3] Add mobile-first responsive styles to Header component in phase2-web/frontend/components/Header.tsx using tailwind skill (flex direction, button sizes min 44x44px)
- [ ] T065 [P] [US3] Add mobile-first responsive styles to TaskForm component in phase2-web/frontend/components/TaskForm.tsx using tailwind skill (input width, button sizes)
- [ ] T066 [P] [US3] Add mobile-first responsive styles to TaskList component in phase2-web/frontend/components/TaskList.tsx using tailwind skill (grid columns, gap spacing)
- [ ] T067 [P] [US3] Add mobile-first responsive styles to TaskItem component in phase2-web/frontend/components/TaskItem.tsx using tailwind skill (touch targets 44x44px, horizontal spacing)
- [ ] T068 [US3] Test responsive behavior at 320px, 768px, 1024px, 1920px widths in browser dev tools
- [ ] T069 [US3] Verify no horizontal scrolling on any screen size and all interactive elements accessible

**Checkpoint**: All user stories (US1, US2, US3) should now be independently functional with responsive design

---

## Phase 6: User Story 4 - Smooth Animations and User Feedback (Priority: P3)

**Goal**: Add polished animations for task operations and page transitions

**Independent Test**: Add task → observe entrance animation → toggle task → observe transition → delete task → observe exit animation

### Animation Implementation for User Story 4

- [ ] T070 [P] [US4] Add staggered entrance animations to TaskList in phase2-web/frontend/components/TaskList.tsx using framer-motion skill (AnimatePresence, stagger children)
- [ ] T071 [P] [US4] Add entrance animation to TaskItem in phase2-web/frontend/components/TaskItem.tsx using framer-motion skill (initial, animate, exit props)
- [ ] T072 [P] [US4] Add toggle completion animation to TaskItem checkbox in phase2-web/frontend/components/TaskItem.tsx using framer-motion skill (scale, opacity transition)
- [ ] T073 [P] [US4] Add delete exit animation to TaskItem in phase2-web/frontend/components/TaskItem.tsx using framer-motion skill (slideOut, fade)
- [ ] T074 [P] [US4] Add page transition animations in phase2-web/frontend/app/layout.tsx using framer-motion skill (fade between pages)
- [ ] T075 [P] [US4] Add loading state animation to TaskForm button in phase2-web/frontend/components/TaskForm.tsx using framer-motion skill (spinner, pulse)
- [ ] T076 [US4] Add prefers-reduced-motion detection in phase2-web/frontend/lib/utils.ts using framer-motion skill (disable animations if user prefers)
- [ ] T077 [US4] Test animations at 60fps and verify smooth performance on all devices

**Checkpoint**: All user stories (US1, US2, US3, US4) complete with polished animations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [ ] T078 [P] Add loading spinner component in phase2-web/frontend/components/ui/spinner.tsx using shadcn skill
- [ ] T079 [P] Add global loading state in phase2-web/frontend/app/loading.tsx using nextjs-app-router skill
- [ ] T080 [P] Add global error boundary in phase2-web/frontend/app/error.tsx using nextjs-app-router skill
- [ ] T081 [P] Add 404 page in phase2-web/frontend/app/not-found.tsx using nextjs-app-router skill
- [ ] T082 Add toast notifications for success/error feedback in phase2-web/frontend/components/TaskForm.tsx using shadcn Toast skill
- [ ] T083 Add toast notifications for task operations in phase2-web/frontend/components/TaskItem.tsx using shadcn Toast skill
- [ ] T084 Add inline validation error messages to signup form in phase2-web/frontend/app/(auth)/signup/page.tsx
- [ ] T085 Add inline validation error messages to login form in phase2-web/frontend/app/(auth)/login/page.tsx
- [ ] T086 Add inline validation error messages to TaskForm in phase2-web/frontend/components/TaskForm.tsx (empty description, length limit)
- [ ] T087 Add retry logic for failed API requests in phase2-web/frontend/lib/api/client.ts using frontend-api-client skill
- [ ] T088 Add request timeout handling in phase2-web/frontend/lib/api/client.ts using frontend-api-client skill (30s timeout)
- [ ] T089 Add network error detection and user feedback in phase2-web/frontend/lib/api/client.ts using frontend-api-client skill
- [ ] T090 Add session expiration detection and redirect to login in phase2-web/frontend/lib/api/client.ts using frontend-auth skill
- [ ] T091 [P] Create backend README.md in phase2-web/backend/README.md with setup instructions
- [ ] T092 [P] Create frontend README.md in phase2-web/frontend/README.md with setup instructions
- [ ] T093 Verify all environment variables documented in both .env templates
- [ ] T094 Run manual testing checklist from quickstart.md (auth flow, task CRUD, responsive design, animations)
- [ ] T095 Verify constitution compliance (no manual coding, code quality standards, PEP8, ESLint)
- [ ] T096 Verify all functional requirements (FR-001 through FR-020) are implemented
- [ ] T097 Verify all success criteria (SC-001 through SC-010) can be measured

**Checkpoint**: Application complete, polished, and ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - **User Story 1 (P1)**: Can start after Phase 2 - Independent
  - **User Story 2 (P1)**: Can start after Phase 2 - Requires US1 auth for protected endpoints
  - **User Story 3 (P2)**: Can start after Phase 2 - Enhances US1 and US2 with responsive design
  - **User Story 4 (P3)**: Can start after Phase 2 - Enhances US2 with animations
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 2 (Foundation) ─┬─→ US1 (Auth) ──→ US2 (Tasks) ──→ MVP Complete!
                      │                      ↓
                      ├─→ US3 (Responsive) ──┘
                      │                      ↓
                      └─→ US4 (Animations) ──→ Full Feature Set Complete
```

- **User Story 1 (Auth)**: No dependencies on other stories - Can complete independently
- **User Story 2 (Tasks)**: Requires US1 (auth) for protected endpoints - Cannot complete without US1
- **User Story 3 (Responsive)**: Independent - Can be implemented in parallel with US2 but enhances US1+US2
- **User Story 4 (Animations)**: Independent - Can be implemented in parallel with US2+US3 but enhances US2

### Within Each User Story

- **Backend** before **Frontend** (API must be ready for frontend integration)
- **Models** before **Endpoints** (data layer before API layer)
- **Core Components** before **Integration** (TaskForm, TaskItem before connecting to API)

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks marked [P] can run in parallel
- T003 (backend requirements.txt), T004 (backend .env), T005 (backend dirs) - parallel
- T007 (frontend deps), T008 (frontend .env), T009 (Tailwind), T010 (shadcn) - parallel

**Phase 2 (Foundation)**: Most tasks marked [P] can run in parallel
- Backend foundation (T011-T020): All [P] tasks can run together
- Frontend foundation (T021-T029): All [P] tasks can run together
- Backend and frontend foundations can run in parallel

**User Story Phases**:
- Different user stories can be worked on in parallel by different team members after Phase 2
- Within each story, tasks marked [P] can run in parallel
- Backend tasks within a story can run in parallel with frontend tasks of DIFFERENT stories

---

## Parallel Example: Foundational Phase (Phase 2)

```bash
# Backend foundation - all [P] tasks can run together:
Task: "Create database connection module in phase2-web/backend/app/database/connection.py"
Task: "Create database initialization module in phase2-web/backend/app/database/init.py"
Task: "Create core configuration module in phase2-web/backend/app/core/config.py"
Task: "Create security utilities in phase2-web/backend/app/core/security.py"
Task: "Create User model in phase2-web/backend/app/models/user.py"
Task: "Create Task model in phase2-web/backend/app/models/task.py"
Task: "Create Pydantic schemas in phase2-web/backend/app/schemas/task.py"

# Frontend foundation - all [P] tasks can run together:
Task: "Create root layout in phase2-web/frontend/app/layout.tsx"
Task: "Create global styles in phase2-web/frontend/styles/globals.css"
Task: "Create utils module in phase2-web/frontend/lib/utils.ts"
Task: "Install shadcn/ui Button component in phase2-web/frontend/components/ui/button.tsx"
Task: "Install shadcn/ui Input component in phase2-web/frontend/components/ui/input.tsx"
Task: "Install shadcn/ui Checkbox component in phase2-web/frontend/components/ui/checkbox.tsx"
Task: "Install shadcn/ui Dialog component in phase2-web/frontend/components/ui/dialog.tsx"
Task: "Install shadcn/ui Toast component in phase2-web/frontend/components/ui/toast.tsx"
```

---

## Parallel Example: User Story 2 (Task Management)

```bash
# Backend endpoints - all [P] tasks can run together:
Task: "Implement GET /api/tasks endpoint in phase2-web/backend/app/routes/tasks.py"
Task: "Implement POST /api/tasks endpoint in phase2-web/backend/app/routes/tasks.py"
Task: "Implement GET /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py"
Task: "Implement PUT /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py"
Task: "Implement PATCH /api/tasks/{id}/toggle endpoint in phase2-web/backend/app/routes/tasks.py"
Task: "Implement DELETE /api/tasks/{id} endpoint in phase2-web/backend/app/routes/tasks.py"

# Frontend components - all [P] tasks can run together:
Task: "Create dashboard layout in phase2-web/frontend/app/(dashboard)/layout.tsx"
Task: "Create TaskForm component in phase2-web/frontend/components/TaskForm.tsx"
Task: "Create TaskList component in phase2-web/frontend/components/TaskList.tsx"
Task: "Create TaskItem component in phase2-web/frontend/components/TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T029) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 - Auth (T030-T040)
4. **STOP and VALIDATE**: Test User Story 1 independently (signup → login → logout)
5. Complete Phase 4: User Story 2 - Tasks (T041-T059)
6. **STOP and VALIDATE**: Test User Story 2 independently (add → view → edit → toggle → delete)
7. **MVP COMPLETE**: Deploy/demo functional auth + task management app

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Foundational → Foundation ready
2. **MVP** (Phase 3-4): Add US1 (Auth) + US2 (Tasks) → Test independently → Deploy/Demo
3. **Enhanced UX** (Phase 5): Add US3 (Responsive) → Test on devices → Deploy/Demo
4. **Polished** (Phase 6-7): Add US4 (Animations) + Polish → Test performance → Deploy/Demo
5. Each phase adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers after Phase 2 (Foundation) completes:

**Scenario 1: Sequential by Priority (Single Developer)**
1. Complete US1 (Auth) → Validate → Commit
2. Complete US2 (Tasks) → Validate → Commit → **MVP!**
3. Complete US3 (Responsive) → Validate → Commit
4. Complete US4 (Animations) → Validate → Commit

**Scenario 2: Parallel Development (Multiple Developers)**
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: US1 Backend (T030-T033) + US1 Frontend (T034-T040)
   - **Developer B**: US2 Backend (T041-T047)
   - **Developer C**: US2 Frontend (T048-T059) after US1 auth available
3. After MVP (US1+US2):
   - **Developer A**: US3 (Responsive) (T060-T069)
   - **Developer B**: US4 (Animations) (T070-T077)
   - **Developer C**: Polish (T078-T097)

---

## Task Count Summary

- **Total Tasks**: 97
- **Phase 1 (Setup)**: 10 tasks
- **Phase 2 (Foundational)**: 19 tasks
- **Phase 3 (US1 - Auth)**: 11 tasks
- **Phase 4 (US2 - Tasks)**: 19 tasks
- **Phase 5 (US3 - Responsive)**: 10 tasks
- **Phase 6 (US4 - Animations)**: 8 tasks
- **Phase 7 (Polish)**: 20 tasks

**Parallelizable Tasks**: 62 tasks marked [P] (64% can run in parallel)

**MVP Scope**: Phases 1-4 (59 tasks) = Auth + Task Management

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story**: Independently completable and testable
- **Commit frequency**: After each task or logical group of related tasks
- **Checkpoints**: Stop at each checkpoint to validate story independently
- **Backend-first**: Complete backend APIs before frontend integration within each story
- **Skills**: All tasks reference existing reusable skills (backend-auth, neon-sqlmodel-db, nextjs-app-router, shadcn, tailwind, framer-motion, frontend-auth, frontend-api-client, crud-rest-api)
- **No manual coding**: All tasks use Claude Code tools (Write, Edit, Read) with skill references
- **Constitution compliance**: PEP8, type hints, ESLint, modular code, comprehensive error handling
