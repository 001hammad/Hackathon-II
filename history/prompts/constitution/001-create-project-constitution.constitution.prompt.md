---
id: 001
title: Create project constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: <user>
command: /sp.constitution
labels: ["constitution","governance","setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (created/updated)
tests:
  - N/A (constitution setup only)
---

## Prompt

Project Name: Hackathon II - Evolution of Todo App

Project Overview:

Build a todo application that evolves across 5 phases from a simple console app to a full cloud-native, event-driven, AI-powered distributed system.

Core Rules:

1. Folder Structure

- All shared and reusable items (this constitution, all specifications, history, agents, skills) stay in the project root.

- Each phase has its own isolated folder for code and phase-specific files only:

  - phase1-console/

  - phase2-web/

  - phase3-chatbot/

  - phase4-k8s-local/

  - phase5-cloud/

- Create the phase folder automatically when starting a new phase.

2. Phase Progression

Complete one phase fully (working app + clean code + tests) before starting the next.

- Phase 1: In-memory Python CLI todo app (5 basic CRUD operations)

- Phase 2: Full-stack web app (Next.js frontend + FastAPI backend + Neon PostgreSQL + Better Auth with JWT)

- Phase 3: AI chatbot interface using natural language (OpenAI ChatKit + Agents SDK + MCP tools)

- Phase 4: Local Kubernetes deployment (Minikube + Helm + Docker + kubectl-ai/kagent)

- Phase 5: Advanced cloud deployment (AKS/GKE + Kafka/Redpanda + Dapr + CI/CD)

3. Development Rules

- No manual coding allowed — all code must be created and edited only through Claude Code.

- All code must be clean, follow PEP8, use type hints, be modular, and include tests.

- Always read and reference the correct specification before implementing anything.

4. Reusable Intelligence (Bonus Focus)

- Create and use subagents for specialized roles (e.g., planner, coder, tester, reviewer, deployment expert).

- Create reusable skills for common patterns (e.g., CRUD operations, authentication, MCP tools, testing, Urdu support).

- Support Urdu language in the final chatbot (text input/output).

- Bonus ideas: voice commands, Qdrant vector search, recurring tasks, reminders.

5. Final Goal

Public GitHub repo with:

- Clean structure (root shared + phase folders)

- All phases completed progressively

This constitution guides the entire project from start to finish.

## Response snapshot

Created comprehensive project constitution (v1.0.0) with:

**Core Principles** (6):
1. Shared Root Architecture - all governance/intelligence in root
2. Phase Isolation - each phase in separate folder
3. Sequential Completion - complete one phase before next
4. No Manual Coding - all code through Claude Code only
5. Code Quality Standards - PEP8, type hints, tests required
6. Specification-Driven Development - read specs before implementing

**Folder Structure**: Root (shared) + 5 isolated phase folders

**Phase Progression**: 5 defined phases with tech stacks, scope, and Definition of Done

**Development Rules**: Code creation, standards, testing, spec adherence

**Reusable Intelligence**: Subagents, skills, Urdu language support, bonus features

**Code Quality Standards**: PEP8, organization, error handling, documentation

**Governance**: Amendment process, compliance review, phase gates, violation handling

File written to `.specify/memory/constitution.md` with full Sync Impact Report.

## Outcome

- ✅ Impact: Project governance framework established with clear rules for 5-phase evolution
- 🧪 Tests: N/A (constitution setup)
- 📁 Files: 1 created/updated (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify to create first feature specification
- 🧠 Reflection: Constitution provides clear guardrails for complex multi-phase project; key constraints are no manual coding and sequential phase completion

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start Phase 1 with /sp.specify to create console app specification
