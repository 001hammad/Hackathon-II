# Implementation Plan: Phase II Full-Stack Multi-User Web Todo Application

**Branch**: `001-phase2-web-todo` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase2-web-todo/spec.md`

## Summary

Transform the Phase I console todo application into a modern, responsive, multi-user web application with persistent storage and secure authentication. The application will use Next.js 16+ (App Router) for the frontend, FastAPI for the backend API, and Neon Serverless PostgreSQL for persistent storage. Authentication is implemented using Better Auth with JWT tokens for secure user isolation.

**Primary Requirement**: Enable multiple users to independently manage their personal todo lists through a responsive web interface accessible from any device.

**Technical Approach**: Monorepo structure with separate frontend and backend directories in `phase2-web/`. Backend-first implementation ensures stable API before frontend integration. All code utilizes existing reusable skills (backend-auth, neon-sqlmodel-db, nextjs-app-router, shadcn, tailwind, framer-motion, etc.) to maintain consistency and quality standards.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x + JavaScript (ES2022)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Better Auth, Tailwind CSS, shadcn/ui, Framer Motion
- Backend: FastAPI 0.109+, SQLModel 0.0.14+, python-jose (JWT), uvicorn, psycopg2, asyncpg

**Storage**: Neon Serverless PostgreSQL 15+ (hosted cloud service)

**Testing**:
- Frontend: Jest + React Testing Library, Playwright (optional E2E)
- Backend: pytest + pytest-asyncio + httpx

**Target Platform**:
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Backend: Linux/Windows server (Python runtime)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Login page load: < 3 seconds
- Task operations: < 2 seconds response time
- Task toggle: < 1 second response time
- Concurrent users: 100+ without degradation

**Constraints**:
- Must use specified tech stack (Next.js, FastAPI, Neon PostgreSQL, Better Auth with JWT)
- Must enforce user data isolation at database level
- Must use existing reusable skills (no manual coding)
- Must follow REST API conventions
- Responsive design: 320px to 1920px+ screen widths
- Password must be hashed (bcrypt), never stored in plaintext

**Scale/Scope**:
- MVP: 2 core entities (User, Task)
- Expected users: 100+ concurrent
- Expected tasks per user: 100-500
- API endpoints: 9 (3 auth, 6 tasks)
- Frontend pages: 4 (login, signup, dashboard, loading/error states)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Core Principles Compliance

**I. Shared Root Architecture**
- ✅ **PASS**: Constitution, specifications, history, agents, and skills remain in project root
- ✅ **PASS**: Single source of truth for governance and reusable intelligence

**II. Phase Isolation**
- ✅ **PASS**: All Phase 2 code isolated in `phase2-web/` directory
- ✅ **PASS**: Clear separation: `phase2-web/frontend/` and `phase2-web/backend/`
- ✅ **PASS**: No mixing of phase code

**III. Sequential Completion**
- ✅ **PASS**: Phase 1 (console app) completed before starting Phase 2
- ✅ **PASS**: Phase 2 must be complete before Phase 3 (chatbot)
- ✅ **PASS**: Definition of done: working app, clean code, tests passing

**IV. No Manual Coding**
- ✅ **PASS**: All code created via Claude Code tools (Read, Write, Edit)
- ✅ **PASS**: All implementation uses existing reusable skills
- ✅ **PASS**: No direct file editing permitted

**V. Code Quality Standards**
- ✅ **PASS**: Python follows PEP8, TypeScript follows ESLint rules
- ✅ **PASS**: Type hints (Python) and TypeScript strict mode (frontend)
- ✅ **PASS**: Modular code with separation of concerns
- ✅ **PASS**: Comprehensive tests for backend and frontend

**VI. Specification-Driven Development**
- ✅ **PASS**: Implementation plan derived from spec.md
- ✅ **PASS**: All functional requirements (FR-001 through FR-020) mapped to implementation
- ✅ **PASS**: Success criteria (SC-001 through SC-010) define acceptance

### ✅ Phase Gate Criteria

1. ✅ **Application works as specified**: All user stories (P1, P2, P3) implemented and testable
2. ✅ **Code follows all quality standards**: PEP8, type hints, ESLint, modular structure
3. ✅ **All tests pass**: pytest (backend), Jest (frontend), E2E (optional)
4. ✅ **Documentation is complete**: spec.md, plan.md, data-model.md, contracts, quickstart.md
5. ✅ **No manual coding detected**: All code via Claude Code with skill references
6. ✅ **Specification requirements met**: FR-001 through FR-020, SC-001 through SC-010

### ✅ Re-check After Phase 1 Design

**Data Model Review**:
- ✅ **PASS**: Simple schema (2 entities) aligns with "smallest viable change" principle
- ✅ **PASS**: No unnecessary complexity (no categories, tags, due dates per spec)
- ✅ **PASS**: Foreign key relationship enforces data integrity

**API Contract Review**:
- ✅ **PASS**: RESTful design follows standard HTTP conventions
- ✅ **PASS**: 9 endpoints sufficient for all functional requirements
- ✅ **PASS**: Authentication required only where specified

**Implementation Sequence Review**:
- ✅ **PASS**: Backend-first approach enables independent testing
- ✅ **PASS**: Phased rollout (Foundation → Core → Polish) reduces risk
- ✅ **PASS**: Skills utilization prevents duplication and ensures consistency

## Project Structure

### Documentation (this feature)

```text
specs/001-phase2-web-todo/
├── spec.md              # Feature specification (✅ Complete)
├── plan.md              # This file - implementation plan (✅ Complete)
├── research.md          # Phase 0 research output (✅ Complete)
├── data-model.md        # Phase 1 data model (✅ Complete)
├── quickstart.md        # Phase 1 quickstart guide (✅ Complete)
├── contracts/           # Phase 1 API contracts (✅ Complete)
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── checklists/          # Quality validation
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 task breakdown (⏳ Created by /sp.tasks)
```

### Source Code (repository root)

```text
phase2-web/                        # Phase 2 isolated directory
│
├── frontend/                      # Next.js 16+ Application
│   ├── app/                       # App Router (Next.js 16+)
│   │   ├── (auth)/                # Auth route group (no layout prefix)
│   │   │   ├── layout.tsx         # Auth layout (centered card)
│   │   │   ├── signup/
│   │   │   │   └── page.tsx       # Signup page with Better Auth
│   │   │   └── login/
│   │   │       └── page.tsx       # Login page with Better Auth
│   │   │
│   │   ├── (dashboard)/           # Dashboard route group (protected)
│   │   │   ├── layout.tsx         # Dashboard layout (header + nav)
│   │   │   └── page.tsx           # Main dashboard (task list + form)
│   │   │
│   │   ├── layout.tsx             # Root layout (HTML shell)
│   │   ├── loading.tsx            # Global loading state
│   │   ├── error.tsx              # Global error boundary
│   │   └── not-found.tsx          # 404 page
│   │
│   ├── components/                # React Components
│   │   ├── ui/                    # shadcn/ui components (auto-generated)
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   │
│   │   ├── TaskList.tsx           # Task list container
│   │   ├── TaskItem.tsx           # Individual task with actions
│   │   ├── TaskForm.tsx           # Add/edit task form
│   │   ├── Header.tsx             # App header with logout
│   │   └── AuthGuard.tsx          # Protected route wrapper
│   │
│   ├── lib/                       # Utilities
│   │   ├── api/                   # API client
│   │   │   ├── client.ts          # Base API client with JWT
│   │   │   ├── auth.ts            # Auth API calls
│   │   │   └── tasks.ts           # Task CRUD calls
│   │   │
│   │   ├── auth/                  # Better Auth configuration
│   │   │   ├── config.ts          # Better Auth setup
│   │   │   └── hooks.ts           # useAuth hook
│   │   │
│   │   └── utils.ts               # Utility functions (cn, etc.)
│   │
│   ├── public/                    # Static assets
│   │   ├── favicon.ico
│   │   └── images/
│   │
│   ├── styles/                    # Global styles
│   │   └── globals.css            # Tailwind directives
│   │
│   ├── tests/                     # Frontend tests
│   │   ├── unit/                  # Component unit tests
│   │   ├── integration/           # Integration tests
│   │   └── e2e/                   # Playwright E2E tests (optional)
│   │
│   ├── .env.local                 # Environment variables (not in git)
│   ├── next.config.js             # Next.js configuration
│   ├── tailwind.config.ts         # Tailwind configuration
│   ├── tsconfig.json              # TypeScript configuration
│   ├── package.json               # Dependencies
│   └── README.md                  # Frontend documentation
│
└── backend/                       # FastAPI Application
    ├── app/                       # Application code
    │   ├── models/                # SQLModel ORM models
    │   │   ├── __init__.py
    │   │   ├── user.py            # User model (managed by Better Auth)
    │   │   └── task.py            # Task model
    │   │
    │   ├── routes/                # API endpoints
    │   │   ├── __init__.py
    │   │   ├── auth.py            # Auth endpoints (signup, login, logout)
    │   │   └── tasks.py           # Task CRUD endpoints
    │   │
    │   ├── auth/                  # Authentication
    │   │   ├── __init__.py
    │   │   └── dependencies.py    # JWT verification, get_current_user
    │   │
    │   ├── database/              # Database management
    │   │   ├── __init__.py
    │   │   ├── connection.py      # SQLModel engine and session
    │   │   └── init.py            # Create tables function
    │   │
    │   ├── schemas/               # Pydantic schemas (request/response)
    │   │   ├── __init__.py
    │   │   ├── auth.py            # AuthRequest, AuthResponse
    │   │   └── task.py            # TaskCreate, TaskUpdate, TaskResponse
    │   │
    │   ├── core/                  # Core configuration
    │   │   ├── __init__.py
    │   │   ├── config.py          # Environment variables
    │   │   └── security.py        # Password hashing utilities
    │   │
    │   └── main.py                # FastAPI app instance + CORS
    │
    ├── tests/                     # Backend tests
    │   ├── __init__.py
    │   ├── conftest.py            # pytest fixtures
    │   ├── test_auth.py           # Auth endpoint tests
    │   ├── test_tasks.py          # Task CRUD tests
    │   └── test_user_isolation.py # User isolation tests
    │
    ├── .env                       # Environment variables (not in git)
    ├── requirements.txt           # Python dependencies
    ├── pytest.ini                 # pytest configuration
    └── README.md                  # Backend documentation
```

**Structure Decision**: Selected **Option 2: Web application** structure due to clear frontend/backend separation. This structure:
- Enables independent development and deployment of frontend and backend
- Follows industry-standard monorepo pattern for full-stack applications
- Aligns with Phase Isolation principle (all Phase 2 code in phase2-web/)
- Simplifies shared configuration (environment variables, API contracts)
- Supports parallel development after backend API is stable

## Complexity Tracking

> **No violations detected - this section is empty**

All implementation decisions comply with constitution principles:
- Simple schema (2 entities) meets all functional requirements
- Standard REST API patterns (no custom protocols)
- Proven tech stack (Next.js, FastAPI, PostgreSQL)
- Reusable skills prevent code duplication
- Sequential implementation reduces integration complexity

## Implementation Phases

### Phase 2A: Backend Foundation (MVP Critical)

**Duration**: 2 days

**Goal**: Stable backend API with authentication and task CRUD operations

**Steps**:
1. **Setup Backend Project**
   - Create `phase2-web/backend/` directory structure
   - Initialize Python virtual environment
   - Install dependencies (FastAPI, SQLModel, python-jose, uvicorn, etc.)
   - Configure environment variables (.env)
   - **Skill**: None (basic setup)

2. **Configure Database Connection**
   - Create database connection module using SQLModel
   - Implement session management with dependency injection
   - Create table initialization function
   - Test connection to Neon PostgreSQL
   - **Skill**: `neon-sqlmodel-db`

3. **Implement Data Models**
   - Create User model (managed by Better Auth)
   - Create Task model with foreign key to User
   - Define relationships (User has many Tasks)
   - Add validation rules (description length, etc.)
   - **Skill**: `neon-sqlmodel-db`

4. **Implement Auth Middleware**
   - Create JWT verification dependency
   - Implement `get_current_user` function
   - Handle 401 errors for invalid/missing tokens
   - Extract user_id from JWT payload
   - **Skill**: `backend-auth`

5. **Create Auth Endpoints**
   - POST /api/auth/signup (user registration)
   - POST /api/auth/login (user authentication)
   - POST /api/auth/logout (session termination)
   - Password hashing with bcrypt
   - **Skill**: `backend-auth`

6. **Create Task CRUD Endpoints**
   - GET /api/tasks (list user's tasks)
   - POST /api/tasks (create new task)
   - GET /api/tasks/{id} (get specific task)
   - PUT /api/tasks/{id} (update task description)
   - PATCH /api/tasks/{id}/toggle (toggle completion)
   - DELETE /api/tasks/{id} (delete task)
   - All endpoints filter by authenticated user_id
   - **Skill**: `crud-rest-api`, `backend-auth`

7. **Write Backend Tests**
   - Test JWT verification middleware
   - Test auth endpoints (signup, login, logout)
   - Test task CRUD operations
   - Test user isolation (User A cannot access User B's tasks)
   - Test error cases (401, 404, 400)
   - **Skill**: None (pytest patterns)

**Acceptance Criteria**:
- ✅ Backend starts without errors on http://localhost:8000
- ✅ API documentation accessible at http://localhost:8000/docs
- ✅ All backend tests pass (pytest)
- ✅ User can signup, login, and receive JWT token
- ✅ Protected endpoints return 401 without valid token
- ✅ User isolation enforced at database level

---

### Phase 2B: Frontend Core (MVP Critical)

**Duration**: 2 days

**Goal**: Functional web UI with authentication and task management

**Steps**:
1. **Setup Frontend Project**
   - Initialize Next.js project with App Router
   - Install dependencies (Tailwind, shadcn, Better Auth, Framer Motion)
   - Configure TypeScript strict mode
   - Setup environment variables (.env.local)
   - **Skill**: `nextjs-app-router`, `tailwind`, `shadcn`

2. **Configure Better Auth**
   - Setup Better Auth client
   - Configure JWT cookie storage
   - Create useAuth hook
   - Implement protected route middleware
   - **Skill**: `frontend-auth`

3. **Implement Auth Pages**
   - Create auth layout (centered card design)
   - Create signup page with form validation
   - Create login page with error handling
   - Implement automatic redirect after auth
   - Style with shadcn/ui components
   - **Skill**: `frontend-auth`, `shadcn`

4. **Create Dashboard Layout**
   - Create dashboard layout with header and navigation
   - Implement logout button
   - Add protected route wrapper
   - Create loading and error states
   - **Skill**: `nextjs-app-router`, `shadcn`, `tailwind`

5. **Build Task Components**
   - Create TaskList component (displays tasks)
   - Create TaskItem component (individual task with actions)
   - Create TaskForm component (add new task)
   - Implement task toggle (completion status)
   - Implement task edit (inline or modal)
   - Implement task delete with confirmation
   - **Skill**: `shadcn`, `tailwind`

6. **Integrate API Client**
   - Create API client with JWT token attachment
   - Implement task CRUD functions (fetch, create, update, delete)
   - Handle errors and loading states
   - Configure automatic token refresh
   - **Skill**: `frontend-api-client`

7. **Write Frontend Tests**
   - Test auth flow (signup, login, logout)
   - Test task CRUD operations
   - Test protected route behavior
   - Test error handling and loading states
   - **Skill**: None (Jest + React Testing Library)

**Acceptance Criteria**:
- ✅ Frontend starts without errors on http://localhost:3000
- ✅ Users can signup and see account creation confirmation
- ✅ Users can login and see their dashboard
- ✅ Users can add, view, toggle, edit, and delete tasks
- ✅ Each user only sees their own tasks
- ✅ All frontend tests pass (npm test)
- ✅ Protected routes redirect to login when not authenticated

---

### Phase 2C: Polish (Post-MVP)

**Duration**: 1 day

**Goal**: Enhanced UX with responsive design and animations

**Steps**:
1. **Add Responsive Design**
   - Review all pages for mobile responsiveness
   - Test on 320px, 768px, 1024px, 1920px widths
   - Add mobile-specific navigation (if needed)
   - Ensure touch-friendly button sizes (min 44x44px)
   - Test keyboard navigation
   - **Skill**: `tailwind`

2. **Implement Animations**
   - Add list item entrance animations (staggered)
   - Add task completion toggle animation
   - Add task deletion exit animation
   - Add page transition animations
   - Respect prefers-reduced-motion
   - **Skill**: `framer-motion`

3. **Error Handling & Loading States**
   - Add loading spinners during API calls
   - Display toast notifications for success/error
   - Add error boundaries for unexpected errors
   - Show inline validation errors on forms
   - Implement retry logic for failed requests
   - **Skill**: `shadcn` (Toast component)

4. **End-to-End Testing (Optional)**
   - Write E2E tests for user flows
   - Test signup → login → create task → toggle → delete → logout
   - Test error scenarios (network failure, invalid credentials)
   - Test responsive behavior (mobile, tablet, desktop)
   - **Skill**: None (Playwright)

**Acceptance Criteria**:
- ✅ Application is fully responsive (320px to 1920px+)
- ✅ Animations are smooth and enhance UX
- ✅ All user interactions provide clear feedback
- ✅ Error messages are user-friendly and actionable
- ✅ Loading states prevent user confusion
- ✅ E2E tests pass (if implemented)

---

## Functional Requirements Mapping

| Requirement | Implementation | Component | Priority |
|-------------|----------------|-----------|----------|
| FR-001: User registration | POST /api/auth/signup | backend/routes/auth.py | P1 |
| FR-002: Email validation | Pydantic schema validation | backend/schemas/auth.py | P1 |
| FR-003: Password requirements | Validation + bcrypt hashing | backend/core/security.py | P1 |
| FR-004: User authentication | POST /api/auth/login | backend/routes/auth.py | P1 |
| FR-005: JWT token issuance | python-jose JWT encoding | backend/routes/auth.py | P1 |
| FR-006: JWT auto-attachment | API client interceptor | frontend/lib/api/client.ts | P1 |
| FR-007: JWT verification | Auth middleware dependency | backend/auth/dependencies.py | P1 |
| FR-008: User data isolation | Filter all queries by user_id | backend/routes/tasks.py | P1 |
| FR-009: Create tasks | POST /api/tasks | backend/routes/tasks.py | P1 |
| FR-010: List tasks | GET /api/tasks | backend/routes/tasks.py | P1 |
| FR-011: Toggle completion | PATCH /api/tasks/{id}/toggle | backend/routes/tasks.py | P1 |
| FR-012: Edit tasks | PUT /api/tasks/{id} | backend/routes/tasks.py | P1 |
| FR-013: Delete tasks | DELETE /api/tasks/{id} | backend/routes/tasks.py | P1 |
| FR-014: Persist tasks | Neon PostgreSQL database | backend/database/connection.py | P1 |
| FR-015: Persist users | User model with hashed password | backend/models/user.py | P1 |
| FR-016: Logout mechanism | POST /api/auth/logout | frontend/lib/auth/hooks.ts | P1 |
| FR-017: Error messages | Try-catch with user-friendly messages | All components | P2 |
| FR-018: Responsive layout | Tailwind CSS breakpoints | frontend/app/, components/ | P2 |
| FR-019: Visual feedback | Loading states, toast notifications | frontend/components/ | P2 |
| FR-020: Protected routes | Middleware redirect | frontend/middleware.ts | P1 |

---

## Success Criteria Verification

| Criteria | Target | Verification Method | Status |
|----------|--------|---------------------|--------|
| SC-001: Registration time | < 90 seconds | Manual timing during testing | ⏳ Verify after Phase 2B |
| SC-002: Task creation time | < 2 seconds | API response time measurement | ⏳ Verify after Phase 2A |
| SC-003: Task toggle time | < 1 second | API response time measurement | ⏳ Verify after Phase 2A |
| SC-004: Responsive design | 320px-1920px | Manual testing on multiple devices | ⏳ Verify after Phase 2C |
| SC-005: Operation success rate | 99% | Monitor error logs during testing | ⏳ Verify after Phase 2C |
| SC-006: Multi-device consistency | Consistent data | Login from multiple browsers | ⏳ Verify after Phase 2B |
| SC-007: Initial page load | < 3 seconds | Lighthouse performance audit | ⏳ Verify after Phase 2B |
| SC-008: User isolation | No unauthorized access | Security testing (User A → User B tasks) | ⏳ Verify after Phase 2A |
| SC-009: Signup success rate | 95% | User testing feedback | ⏳ Verify after Phase 2B |
| SC-010: Concurrent users | 100+ | Load testing with locust/k6 | ⏳ Verify after Phase 2C |

---

## Risk Analysis & Mitigation

### Technical Risks

**Risk 1: Better Auth + FastAPI JWT mismatch**
- **Probability**: Medium
- **Impact**: High (breaks authentication)
- **Mitigation**: Use identical BETTER_AUTH_SECRET in both frontend and backend; verify JWT format in early testing
- **Contingency**: Switch to manual JWT implementation if Better Auth incompatible

**Risk 2: Neon database connection issues**
- **Probability**: Low
- **Impact**: High (app unusable)
- **Mitigation**: Test connection early in Phase 2A; verify SSL mode requirement; check Neon service status
- **Contingency**: Use local PostgreSQL for development if Neon unavailable

**Risk 3: CORS errors between frontend and backend**
- **Probability**: Medium
- **Impact**: Medium (blocks API calls)
- **Mitigation**: Configure CORS middleware in FastAPI early; test with frontend before full integration
- **Contingency**: Use Next.js API routes as proxy if CORS issues persist

**Risk 4: User isolation bypass vulnerability**
- **Probability**: Low
- **Impact**: Critical (security breach)
- **Mitigation**: Comprehensive security testing; code review of all endpoints; ensure all queries filter by user_id
- **Contingency**: Add database-level row security if application-level isolation insufficient

### Schedule Risks

**Risk 5: Backend delays impact frontend**
- **Probability**: Medium
- **Impact**: Medium (delays overall completion)
- **Mitigation**: Backend-first approach ensures API stability before frontend integration
- **Contingency**: Frontend can mock API responses to develop in parallel if needed

**Risk 6: Responsive design testing time**
- **Probability**: Low
- **Impact**: Low (polish only)
- **Mitigation**: Test responsiveness incrementally during Phase 2B; use browser dev tools for quick testing
- **Contingency**: Focus on mobile (320px) and desktop (1024px+) if time constrained

---

## Skills Utilization Summary

All implementation will use existing reusable skills:

### Backend Skills
1. **backend-auth**: JWT verification, user ID extraction, auth middleware (Phase 2A, Steps 4-5)
2. **neon-sqlmodel-db**: Neon PostgreSQL setup, SQLModel models, database connections (Phase 2A, Steps 2-3)
3. **crud-rest-api**: RESTful endpoint patterns, request validation, response formatting (Phase 2A, Step 6)

### Frontend Skills
1. **nextjs-app-router**: App Router structure, server/client components, layouts (Phase 2B, Steps 1, 4)
2. **frontend-auth**: Better Auth integration, JWT cookie management, protected routes (Phase 2B, Steps 2-3)
3. **shadcn**: UI component library (buttons, forms, dialogs, toasts) (Phase 2B, Steps 3, 5; Phase 2C, Step 3)
4. **tailwind**: Responsive design, utility classes, breakpoints (Phase 2B, Steps 1, 4-5; Phase 2C, Step 1)
5. **framer-motion**: Animations, transitions, accessibility (Phase 2C, Step 2)
6. **frontend-api-client**: API request helpers, error handling, token attachment (Phase 2B, Step 6)

**No new skills required** - all functionality covered by existing skills.

---

## Testing Strategy

### Backend Testing (pytest)

**Unit Tests** (tests/test_tasks.py, tests/test_auth.py):
- Test model validation (User, Task)
- Test password hashing (bcrypt)
- Test JWT token generation and verification
- Test database queries (CRUD operations)

**Integration Tests** (tests/test_user_isolation.py):
- Test user isolation (User A cannot access User B's tasks)
- Test cascade delete (deleting user deletes their tasks)
- Test endpoint security (401 for missing/invalid tokens)
- Test error handling (400, 404, 500 responses)

**Test Coverage Target**: > 80% for backend code

### Frontend Testing (Jest + React Testing Library)

**Unit Tests** (tests/unit/):
- Test component rendering (TaskItem, TaskList, TaskForm)
- Test form validation (signup, login, task creation)
- Test state management (task toggle, task edit)
- Test utility functions (API client, auth hooks)

**Integration Tests** (tests/integration/):
- Test auth flow (signup → login → logout)
- Test task CRUD flow (create → read → update → delete)
- Test protected routes (redirect to login when unauthenticated)
- Test API error handling (network failure, 401, 404)

**E2E Tests - Optional** (tests/e2e/):
- Test complete user journey (signup → create task → toggle → delete → logout)
- Test responsive behavior on different screen sizes
- Test browser compatibility (Chrome, Firefox, Safari)

**Test Coverage Target**: > 70% for frontend code

### Manual Testing Checklist

**Authentication**:
- [ ] User can signup with valid email and password
- [ ] Signup rejects invalid email format
- [ ] Signup rejects weak password
- [ ] Signup rejects duplicate email
- [ ] User can login with correct credentials
- [ ] Login rejects incorrect credentials
- [ ] User can logout and session is terminated

**Task Management**:
- [ ] User can create new task
- [ ] User can view list of their tasks
- [ ] User can toggle task completion status
- [ ] User can edit task description
- [ ] User can delete task with confirmation
- [ ] User only sees their own tasks (not other users')

**Responsive Design**:
- [ ] Layout works on mobile (320px width)
- [ ] Layout works on tablet (768px width)
- [ ] Layout works on desktop (1024px+ width)
- [ ] Touch targets are 44x44px minimum on mobile
- [ ] No horizontal scrolling on any screen size

**User Experience**:
- [ ] Loading spinners appear during API calls
- [ ] Success toast appears after operations
- [ ] Error toast appears on failures
- [ ] Animations are smooth (60fps)
- [ ] Keyboard navigation works correctly

---

## Deployment Notes (Future Phase)

**Phase 2 Scope**: Local development only (localhost)

**Future Deployment** (deferred to Phase 5):
- Frontend: Vercel/Netlify (Next.js hosting)
- Backend: Railway/Render/AWS Lambda (FastAPI hosting)
- Database: Neon PostgreSQL (already cloud-hosted)
- CI/CD: GitHub Actions (automated testing and deployment)
- Monitoring: Sentry (error tracking), PostHog (analytics)

---

## Next Steps

After completing Phase 2:

1. ✅ Verify all functional requirements (FR-001 through FR-020)
2. ✅ Verify all success criteria (SC-001 through SC-010)
3. ✅ Run all tests (backend + frontend)
4. ✅ Conduct manual testing on multiple devices
5. ✅ Review code quality (PEP8, ESLint, type hints)
6. ✅ Update constitution compliance tracking
7. → Create Phase 2 completion report
8. → Proceed to Phase 3 (AI Chatbot Interface)

---

## Appendix

### Environment Variables Reference

**Backend (.env)**:
```bash
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
DATABASE_URL_ASYNC=postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-here
```

### Key Commands

**Backend**:
```bash
# Start development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

**Frontend**:
```bash
# Start development server
npm run dev

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Build for production
npm run build
```

---

**Plan Status**: ✅ Complete and ready for implementation via /sp.tasks command
