---
id: 005
title: Better Auth BFF proxy integration
stage: green
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase2-web-todo
branch: 001-phase2-web-todo
user: 001hammad <hammadhafeez435@gmail.com>
command: claude-code
labels: ["better-auth","nextjs","fastapi","bff","hmac","tasks-api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase2-web/frontend/app/api/tasks/route.ts
 - phase2-web/frontend/app/api/tasks/[task_id]/route.ts
 - phase2-web/frontend/app/api/tasks/[task_id]/toggle/route.ts
 - phase2-web/backend/app/auth/dependencies.py
 - phase2-web/backend/app/main.py
tests:
 - npm run build (phase2-web/frontend)
 - pytest -q (repo root; failed collecting phase1-console)
 - pytest -q phase2-web/backend (no tests)
---

## Prompt

continue

## Response snapshot

Implemented Next.js BFF proxy routes for task CRUD that validate Better Auth cookie sessions and forward to FastAPI with signed internal headers. Updated FastAPI to remove the custom /api/auth router and to trust the BFF by verifying an HMAC signature header, keeping strict per-user task isolation.

## Outcome

- ✅ Impact: Phase 2 tasks API is now accessed via Next.js same-origin proxy that uses Better Auth session cookies; FastAPI no longer accepts end-user JWTs and instead verifies signed identity headers.
- 🧪 Tests: Frontend build passes; backend has no pytest tests; repo-level pytest currently fails due to phase1-console import paths.
- 📁 Files: Added 3 Next.js route handlers; modified backend auth dependency and main router registration.
- 🔁 Next prompts: Run the app end-to-end (frontend + backend) and verify task CRUD + user isolation with two accounts; optionally fix phase1-console test packaging if you want repo-wide pytest to pass.
- 🧠 Reflection: When mixing Better Auth (Node) with a Python API, a signed BFF boundary avoids trying to validate cookie sessions inside FastAPI.

## Evaluation notes (flywheel)

- Failure modes observed: Next.js App Router route handler types required `params` to be typed as a Promise; TypeScript build also required `@types/pg`.
- Graders run and results (PASS/FAIL): Frontend build PASS; repo pytest FAIL (phase1-console collection); backend pytest N/A (no tests).
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add a small FastAPI test file that verifies signature rejection/acceptance to lock in the trust boundary behavior.
