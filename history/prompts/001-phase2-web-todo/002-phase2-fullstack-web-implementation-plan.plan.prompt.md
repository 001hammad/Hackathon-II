---
id: 002
title: Phase II Full-Stack Web Implementation Plan
stage: plan
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase2-web-todo
branch: 001-phase2-web-todo
user: 001hammad
command: /sp.plan
labels: ["plan", "full-stack", "architecture", "backend", "frontend", "api-design", "phase2"]
links:
  spec: specs/001-phase2-web-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-phase2-web-todo/plan.md
 - specs/001-phase2-web-todo/research.md
 - specs/001-phase2-web-todo/data-model.md
 - specs/001-phase2-web-todo/quickstart.md
 - specs/001-phase2-web-todo/contracts/openapi.yaml
tests:
 - Constitution check (all principles passed)
 - Phase gate criteria validation (all passed)
 - Complexity tracking (no violations)
---

## Prompt

Objective:
Create a detailed technical plan for implementing the full-stack multi-user web todo app.

Key Points to Cover:
- High-level architecture (frontend Next.js + backend FastAPI + Neon DB)
- Monorepo structure inside phase2-web/ (frontend/ and backend/ subfolders)
- Authentication flow (Better Auth signup/login → JWT → attach to API calls → backend verify)
- Database schema and models (users and tasks with user_id FK)
- API endpoints design
- Frontend pages and components plan
- Implementation sequence (what to build first: backend models → API routes → DB connection → frontend auth → task UI)
- How to use existing reusable skills (frontend-api-client, backend-auth, shadcn-ui, etc.)

## Response snapshot

Created comprehensive implementation plan with:

### Phase 0: Research (research.md)

Resolved 13 technical unknowns:
1. **Architecture Pattern**: Monorepo with frontend/backend separation in phase2-web/
2. **Authentication Flow**: Better Auth (frontend) + JWT verification (backend)
3. **Database Schema**: 2 tables (User, Task) with foreign key relationship
4. **API Design**: RESTful with 9 endpoints (3 auth, 6 tasks)
5. **Frontend Structure**: Next.js App Router with route groups
6. **State Management**: Server Components (no global state library)
7. **Responsive Strategy**: Tailwind CSS mobile-first breakpoints
8. **Animation Strategy**: Framer Motion for P3 features
9. **Error Handling**: Try-catch with user-friendly messages
10. **Development Setup**: Standard Node.js + Python tooling
11. **Testing Strategy**: pytest (backend) + Jest (frontend)
12. **Skills Utilization**: All 9 existing skills (no new skills needed)
13. **Implementation Sequence**: Backend-first, then frontend, then polish

### Phase 1: Design (data-model.md, contracts/, quickstart.md)

**Data Model**:
- User entity: UUID id, email (unique), password_hash, timestamps
- Task entity: integer id, user_id (FK), description (500 chars), completed (boolean), timestamps
- Relationship: One User → Many Tasks (cascade delete)
- User isolation: ALL queries filter by user_id

**API Contracts** (contracts/openapi.yaml):
- OpenAPI 3.0 specification with 9 endpoints
- Request/response schemas for auth and tasks
- Error responses (401, 404, 400)
- JWT Bearer authentication scheme
- Examples for all operations

**Quickstart Guide** (quickstart.md):
- 14-step implementation sequence
- Prerequisites and system requirements
- Backend setup (Phase 2A: 7 steps)
- Frontend setup (Phase 2B: 7 steps)
- Commands, troubleshooting, testing strategies

### Implementation Plan (plan.md)

**Constitution Check**: ✅ All principles passed
- Shared root architecture: ✅ PASS
- Phase isolation: ✅ PASS (phase2-web/)
- Sequential completion: ✅ PASS (Phase 1 complete before Phase 2)
- No manual coding: ✅ PASS (all via Claude Code)
- Code quality standards: ✅ PASS (PEP8, type hints, ESLint)
- Specification-driven: ✅ PASS (derived from spec.md)

**Project Structure**: Web application (Option 2)
- phase2-web/frontend/ - Next.js 16+ with App Router
- phase2-web/backend/ - FastAPI with SQLModel ORM
- Complete directory tree with 50+ files mapped

**Implementation Phases**:

**Phase 2A: Backend Foundation** (2 days, MVP critical)
1. Setup Backend Project
2. Configure Database Connection (skill: neon-sqlmodel-db)
3. Implement Data Models (skill: neon-sqlmodel-db)
4. Implement Auth Middleware (skill: backend-auth)
5. Create Auth Endpoints (skill: backend-auth)
6. Create Task CRUD Endpoints (skill: crud-rest-api, backend-auth)
7. Write Backend Tests (pytest)

**Phase 2B: Frontend Core** (2 days, MVP critical)
1. Setup Frontend Project (skill: nextjs-app-router, tailwind, shadcn)
2. Configure Better Auth (skill: frontend-auth)
3. Implement Auth Pages (skill: frontend-auth, shadcn)
4. Create Dashboard Layout (skill: nextjs-app-router, shadcn, tailwind)
5. Build Task Components (skill: shadcn, tailwind)
6. Integrate API Client (skill: frontend-api-client)
7. Write Frontend Tests (Jest + React Testing Library)

**Phase 2C: Polish** (1 day, post-MVP)
1. Add Responsive Design (skill: tailwind)
2. Implement Animations (skill: framer-motion)
3. Error Handling & Loading States (skill: shadcn)
4. End-to-End Testing (Playwright - optional)

**Functional Requirements Mapping**: All 20 requirements (FR-001 to FR-020) mapped to components
**Success Criteria Verification**: All 10 criteria (SC-001 to SC-010) with verification methods
**Risk Analysis**: 6 risks identified with mitigation strategies
**Testing Strategy**: Unit, integration, E2E for both backend and frontend

### Artifacts Generated

1. **research.md** (3,500+ words): Technical decisions with rationale and alternatives
2. **data-model.md** (4,000+ words): Database schema, SQLModel definitions, queries, validation
3. **contracts/openapi.yaml** (800+ lines): Complete OpenAPI 3.0 specification
4. **quickstart.md** (3,000+ words): Step-by-step implementation guide with commands
5. **plan.md** (7,500+ words): Comprehensive implementation plan with phases, mapping, risks

### Key Decisions

**Architecture**: Monorepo with clear frontend/backend separation in phase2-web/
**Authentication**: Better Auth (frontend) + JWT verification (backend) with shared secret
**Database**: Neon PostgreSQL with 2 tables, foreign key relationship
**API**: RESTful with 9 endpoints following HTTP conventions
**Frontend**: Next.js App Router with route groups for auth and dashboard
**Testing**: pytest (backend >80% coverage), Jest (frontend >70% coverage)
**Implementation**: Backend-first (API stable before frontend integration)
**Skills**: All 9 existing skills utilized (no new skills needed)

## Outcome

- ✅ Impact: Complete technical plan for Phase II full-stack multi-user web application with backend-first implementation strategy
- 🧪 Tests: Constitution check passed (all 6 principles), Phase gate criteria validated (all 6 passed), Complexity tracking (zero violations)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml
- 🔁 Next prompts: /sp.tasks (generate task breakdown), /sp.implement (execute implementation), /sp.adr (document architectural decisions)
- 🧠 Reflection: Plan successfully breaks down complex full-stack application into manageable phases with clear backend-first sequence; all existing skills leveraged for consistency; constitution compliance maintained throughout; ready for task breakdown and implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - planning workflow executed successfully with all artifacts generated
- Graders run and results (PASS/FAIL): PASS - Constitution check (6/6 principles), Phase gate criteria (6/6), Complexity tracking (0 violations), Functional requirements mapping (20/20), Success criteria verification (10/10)
- Prompt variant (if applicable): Standard /sp.plan workflow with comprehensive research and design phases
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate detailed task breakdown with testable acceptance criteria
