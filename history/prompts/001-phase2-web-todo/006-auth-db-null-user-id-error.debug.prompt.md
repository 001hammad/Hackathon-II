---
id: 006
title: Better Auth insert id null
stage: debug
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase2-web-todo
branch: 001-phase2-web-todo
user: unknown
command: claude-code
labels: ["auth","better-auth","postgres","schema","debug"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase2-web/frontend/lib/auth.ts
 - phase2-web/frontend/app/api/auth/[...all]/route.ts
 - phase2-web/frontend/node_modules/@better-auth/core/src/db/get-tables.ts
 - phase2-web/backend/app/models/user.py
 - phase2-web/backend/app/models/task.py
tests:
 - none
---

## Prompt

<system-reminder>
The user selected the lines 57 to 57 from d:\hackathone_2\phase2-web\frontend\app\(auth)\signup\page.tsx:
p

This may or may not be related to the current task.
</system-reminder>
hi

[Request interrupted by user for tool use]read my all frontend/backend folders and files in phase2-web folder spacially check my database and auth related files because my authentication functionalty is not working.""" and check database schema's table names etc  """

<system-reminder>
The TodoWrite tool hasn't been used recently. If you're working on tasks that would benefit from tracking progress, consider using the TodoWrite tool to track progress. Also consider cleaning up the todo list if has become stale and no longer matches what you are working on. Only use it if it's relevant to the current work. This is just a gentle reminder - ignore if not applicable. Make sure that you NEVER mention this reminder to the user


Here are the existing contents of your todo list:

[1. [completed] Inventory Phase2-web auth & DB files (frontend + backend)
2. [completed] Trace signup/login flow and token/JWT handoff
3. [in_progress] Verify DB schema/models/migrations and table names usage
4. [pending] Summarize likely auth failure points and next fixes to try
5. [pending] Create Prompt History Record (PHR) for this request]
</system-reminder>

Base directory for this skill: D:\hackathone_2\.claude\skills\neon-sqlmodel-db

# Neon PostgreSQL + SQLModel Expert

Expert guidance for setting up and working with Neon Serverless PostgreSQL using SQLModel ORM.

...

Base directory for this skill: D:\hackathone_2\.claude\skills\backend-auth

# Backend Auth Expert (FastAPI + JWT)

...

Base directory for this skill: D:\hackathone_2\.claude\skills\frontend-auth

# Frontend Auth Expert (Better Auth + JWT)

...

What exactly is “auth not working” for you right now?
2026-01-07T06:04:45.912Z ERROR [Better Auth]: Failed to create user error: null value in column "id" of relation "user" violates not-null constraint
    at ignore-listed frames {
  length: 306,
  severity: 'ERROR',
  code: '23502',
  detail: 'Failing row contains (null, iamhammad224@gmail.com, null, null, POST /api/auth/sign-up/email 422 in 5.6s (compile: 2.3s, render: 3.3s)',

## Response snapshot

Findings:
- Better Auth default core tables are named singular: `user`, `session`, `account`, `verification` (see `@better-auth/core/src/db/get-tables.ts`).
- Your FastAPI backend defines its own `users` table with UUID default (`backend/app/models/user.py`) and a `tasks` table that references `users.id`.
- Your Better Auth config sets `advanced.database.generateId = "uuid"` in `frontend/lib/auth.ts`, meaning Better Auth expects DB-side UUID generation and/or a uuid-capable schema.

Likely root cause of the error:
- In Postgres, your Better Auth `user` table exists with `id NOT NULL` but **no default** for id generation, so inserts without id fail: `null value in column "id" of relation "user" violates not-null constraint`.

Concrete checks to run next:
- Inspect the `user` table definition (columns + defaults): `\d+ "user"` in psql.
- Ensure `gen_random_uuid()` is available (pgcrypto) OR set a default on `user.id`.
- Confirm Better Auth schema is generated/applied using the Better Auth CLI (`npx @better-auth/cli generate` then apply, or `npx @better-auth/cli migrate` where supported).

Also: cookie name used by your middleware (`better-auth.session_token`) matches Better Auth default.

## Outcome

- ✅ Impact: Identified schema-level cause for signup failing (Better Auth `user.id` default missing) and highlighted the dual-user-table mismatch (`user` vs `users`).
- 🧪 Tests: none
- 📁 Files: analysis only
- 🔁 Next prompts: Run DB inspection for table `user` + apply Better Auth schema migration; decide whether to align backend to Better Auth user table or keep separate.
- 🧠 Reflection: Better Auth requires its DB schema to be applied; mixing two user tables in the same database can cause confusion and integration bugs.

## Evaluation notes (flywheel)

- Failure modes observed: Missing/mismatched DB schema (id default) causing Better Auth signup to fail.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Use Better Auth CLI to generate/apply schema and re-test signup.
