# Phase 0: Research - Phase II Full-Stack Multi-User Web Todo Application

**Date**: 2026-01-02
**Feature**: 001-phase2-web-todo

## Research Summary

This document resolves technical unknowns and documents architectural decisions for the Phase II full-stack multi-user web todo application.

## 1. Architecture Pattern

### Decision: Monorepo with Frontend/Backend Separation

**Rationale**:
- Clear separation of concerns between frontend (Next.js) and backend (FastAPI)
- Independent development and deployment of frontend and backend
- Shared project root for constitution, specifications, and reusable skills
- Aligns with Constitution Principle II (Phase Isolation) - all Phase 2 code in phase2-web/

**Structure**:
```
phase2-web/
├── frontend/          # Next.js 16+ App Router
└── backend/           # Python FastAPI
```

**Alternatives Considered**:
- **Single unified project**: Rejected - mixing TypeScript and Python in same directory would complicate build tools and deployment
- **Separate repositories**: Rejected - violates project structure requirements and complicates shared configuration

## 2. Authentication Flow

### Decision: Better Auth (Frontend) + JWT Verification (Backend)

**Rationale**:
- Better Auth handles user registration, login, and token generation on frontend
- JWT tokens are issued after successful authentication
- Frontend automatically attaches JWT to all API requests via Authorization header
- Backend verifies JWT signature and extracts user_id for user isolation
- Shared BETTER_AUTH_SECRET ensures token compatibility

**Flow**:
1. User signs up/logs in via Better Auth (frontend)
2. Better Auth issues JWT token and stores in secure cookie
3. Frontend API client automatically adds `Authorization: Bearer <token>` header
4. Backend middleware verifies JWT signature and extracts user_id
5. All database queries filter by authenticated user_id

**Alternatives Considered**:
- **Session-based authentication**: Rejected - requirement explicitly specifies JWT
- **OAuth2 third-party**: Rejected - out of scope, simple email/password required

## 3. Database Schema Design

### Decision: Two Core Tables (User, Task)

**User Table** (Managed by Better Auth):
```
users
├── id (UUID, primary key)
├── email (unique, not null)
├── password_hash (not null)
├── created_at (timestamp)
└── updated_at (timestamp)
```

**Task Table** (Custom for todo functionality):
```
tasks
├── id (integer, primary key, auto-increment)
├── user_id (UUID, foreign key → users.id, indexed)
├── description (varchar(500), not null)
├── completed (boolean, default false)
├── created_at (timestamp)
└── updated_at (timestamp)
```

**Rationale**:
- Simple schema meets all functional requirements (FR-001 through FR-020)
- user_id foreign key enforces referential integrity
- Index on user_id optimizes filtering queries for user isolation
- 500 character limit on description balances functionality with UI constraints
- Auto-timestamps track record lifecycle

**Alternatives Considered**:
- **Add task categories/tags**: Rejected - out of scope per specification
- **Add due_date field**: Rejected - out of scope per specification
- **Use UUID for task.id**: Rejected - auto-increment integers sufficient and simpler

## 4. API Endpoint Design

### Decision: RESTful API with Standard HTTP Methods

**Endpoints**:

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/signup | User registration | No |
| POST | /api/auth/login | User login | No |
| POST | /api/auth/logout | User logout | Yes |
| GET | /api/tasks | List user's tasks | Yes |
| POST | /api/tasks | Create new task | Yes |
| GET | /api/tasks/{id} | Get specific task | Yes |
| PUT | /api/tasks/{id} | Update task description | Yes |
| PATCH | /api/tasks/{id}/toggle | Toggle task completion | Yes |
| DELETE | /api/tasks/{id} | Delete task | Yes |

**Rationale**:
- Follows REST conventions (GET=read, POST=create, PUT=update, DELETE=delete)
- PATCH for toggle operation follows semantic HTTP method usage
- All task endpoints require JWT authentication
- Backend verifies user_id from JWT matches task owner before operations
- Clear, predictable URL structure

**Alternatives Considered**:
- **GraphQL**: Rejected - REST is simpler and specification doesn't require GraphQL
- **Single /tasks endpoint with query params**: Rejected - less RESTful, harder to secure

## 5. Frontend Page Structure

### Decision: App Router with Nested Layouts

**Pages**:
```
app/
├── (auth)/
│   ├── layout.tsx        # Auth layout (centered card)
│   ├── signup/
│   │   └── page.tsx      # Signup page
│   └── login/
│       └── page.tsx      # Login page
├── (dashboard)/
│   ├── layout.tsx        # Dashboard layout (nav + sidebar)
│   └── page.tsx          # Main dashboard (task list + form)
└── layout.tsx            # Root layout
```

**Rationale**:
- Route groups `(auth)` and `(dashboard)` organize related pages
- Separate layouts for auth pages (minimal) vs dashboard (full UI)
- Server components by default for optimal performance
- Client components only where needed (form inputs, interactive elements)
- Protected routes enforced by middleware checking JWT cookie

**Alternatives Considered**:
- **Flat page structure**: Rejected - harder to manage shared layouts
- **Pages router (pages/ directory)**: Rejected - App Router is modern standard for Next.js 16+

## 6. State Management

### Decision: Server Components + URL State (No Global State)

**Rationale**:
- Server components fetch data directly from API
- URL search params for filters/pagination (when added later)
- React Context for theme/UI preferences only
- No need for Redux/Zustand - data fetched fresh on navigation
- Simplifies architecture and reduces client-side complexity

**Alternatives Considered**:
- **Redux/Zustand**: Rejected - unnecessary complexity for simple CRUD app
- **React Query**: Rejected - Server Components handle data fetching natively

## 7. Responsive Design Strategy

### Decision: Tailwind CSS Breakpoints + Mobile-First

**Breakpoints**:
- Mobile: < 768px (base styles)
- Tablet: 768px - 1024px (md:)
- Desktop: > 1024px (lg:, xl:)

**Rationale**:
- Mobile-first ensures optimal experience on smallest screens
- Tailwind's utility classes enable rapid responsive development
- Breakpoints align with industry standards (Bootstrap, Material Design)
- shadcn/ui components are responsive by default

**Alternatives Considered**:
- **CSS Grid only**: Rejected - Tailwind utilities provide faster development
- **Desktop-first**: Rejected - mobile usage is primary for todo apps

## 8. Animation Strategy

### Decision: Framer Motion for Priority P3 Features

**Animations**:
- Task list item entrance (staggered fade-in)
- Task completion toggle (scale + opacity)
- Task deletion (slide-out)
- Page transitions (fade)

**Rationale**:
- Framer Motion provides declarative animation API
- Performance-optimized with GPU acceleration
- Respects `prefers-reduced-motion` for accessibility
- Priority P3 means implemented after core functionality

**Alternatives Considered**:
- **CSS transitions only**: Rejected - less flexible for complex animations
- **GSAP**: Rejected - Framer Motion better integrated with React

## 9. Error Handling Strategy

### Decision: Try-Catch with User-Friendly Messages

**Frontend**:
- Display toast notifications for errors (using shadcn/ui Toast)
- Form validation with inline error messages
- Loading states during API calls
- Graceful degradation on network failure

**Backend**:
- FastAPI HTTPException for known errors (401, 404, 400)
- Generic 500 errors log details but return safe message to client
- Validation errors return specific field-level feedback

**Rationale**:
- Clear user feedback improves UX (FR-017, FR-019)
- Security: don't expose sensitive error details to client
- Logging captures full error context for debugging

**Alternatives Considered**:
- **Silent failures**: Rejected - poor UX
- **Detailed stack traces to client**: Rejected - security risk

## 10. Development Environment Setup

### Decision: Standard Node.js + Python Setup

**Frontend**:
- Node.js 18+ (LTS)
- npm or yarn for package management
- TypeScript strict mode
- ESLint + Prettier for code formatting

**Backend**:
- Python 3.11+
- pip with requirements.txt
- Virtual environment (venv)
- Black for code formatting
- mypy for type checking

**Rationale**:
- Standard tooling reduces setup complexity
- Type checking catches bugs early
- Consistent formatting via automated tools

**Alternatives Considered**:
- **Docker for local development**: Deferred to Phase 4 (Kubernetes)
- **Poetry for Python**: Rejected - pip is simpler and sufficient

## 11. Testing Strategy

### Decision: Unit + Integration Tests

**Frontend**:
- Jest + React Testing Library for component tests
- Playwright for E2E tests (optional for MVP)
- Test authentication flows and task CRUD

**Backend**:
- pytest for API endpoint tests
- pytest-asyncio for async tests
- Test JWT verification and user isolation
- Test database operations with test database

**Rationale**:
- Aligns with Constitution principle V (Code Quality Standards)
- Tests verify functional requirements (FR-001 through FR-020)
- Integration tests ensure frontend-backend compatibility

**Alternatives Considered**:
- **No tests**: Rejected - violates constitution
- **Only E2E tests**: Rejected - slower feedback loop

## 12. Existing Skills Utilization

### Available Skills (in .claude/skills/)

**Frontend Skills**:
1. **nextjs-app-router**: App Router structure, server/client components, layouts
2. **frontend-auth**: Better Auth integration, JWT cookie management, protected routes
3. **shadcn**: UI component library (buttons, forms, dialogs, toasts)
4. **tailwind**: Responsive design, utility classes, dark mode
5. **framer-motion**: Animations, transitions, accessibility
6. **frontend-api-client**: API request helpers, error handling, token attachment

**Backend Skills**:
1. **backend-auth**: JWT verification, user ID extraction, auth middleware
2. **neon-sqlmodel-db**: Neon PostgreSQL setup, SQLModel models, database connections
3. **crud-rest-api**: RESTful endpoint patterns, request validation, response formatting

**Rationale**:
- All required functionality covered by existing skills
- No need to create new skills for this phase
- Skills provide battle-tested patterns and examples
- Ensures consistency with Phase 1 patterns

## 13. Implementation Sequence

### Decision: Backend-First, Then Frontend

**Phase 2A: Backend Foundation** (MVP Critical)
1. Database setup (Neon + SQLModel models)
2. JWT verification middleware
3. User registration/login endpoints
4. Task CRUD endpoints with user isolation
5. Backend tests

**Phase 2B: Frontend Core** (MVP Critical)
1. Next.js project setup with App Router
2. Auth pages (signup, login) with Better Auth
3. Protected dashboard layout
4. Task list component
5. Task form component
6. API client integration
7. Frontend tests

**Phase 2C: Polish** (Post-MVP)
1. Responsive design refinements
2. Framer Motion animations
3. Error handling improvements
4. Loading states
5. E2E tests

**Rationale**:
- Backend must be stable before frontend integration
- Can test backend API independently with curl/Postman
- Frontend can mock backend during parallel development if needed
- Aligns with sequential completion principle

**Alternatives Considered**:
- **Frontend-first**: Rejected - requires mocking backend extensively
- **Parallel development**: Rejected - increases integration complexity

## Summary

All technical unknowns resolved. No [NEEDS CLARIFICATION] markers remain. Ready to proceed to Phase 1 (Data Model & Contracts).

**Key Decisions**:
1. Monorepo structure: phase2-web/frontend + phase2-web/backend
2. Authentication: Better Auth + JWT with shared secret
3. Database: Two tables (User, Task) with foreign key relationship
4. API: RESTful with 9 endpoints
5. Frontend: Next.js App Router with route groups
6. State: Server Components (no global state library)
7. Responsive: Tailwind CSS with mobile-first breakpoints
8. Animations: Framer Motion for P3 features
9. Testing: pytest (backend) + Jest (frontend)
10. Skills: Reuse all existing skills (no new skills needed)
11. Implementation: Backend-first, then frontend
