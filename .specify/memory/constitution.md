<!--
SYNC IMPACT REPORT
==================
Version Change: Initial → 1.0.0
Modified Principles: None (initial creation)
Added Sections:
  - Core Principles (6 principles)
  - Folder Structure
  - Phase Progression
  - Development Rules
  - Reusable Intelligence
  - Code Quality Standards
  - Governance
Removed Sections: None (initial creation)
Templates Status:
  - plan-template.md: ✅ No changes needed
  - spec-template.md: ✅ No changes needed
  - tasks-template.md: ✅ No changes needed
  - phr-template.prompt.md: ✅ No changes needed
  - No command files found to update
Follow-up TODOs: None
-->

# Hackathon II - Evolution of Todo App Constitution

## Core Principles

### I. Shared Root Architecture

All shared and reusable items MUST stay in the project root: constitution, all
specifications, history (prompts, ADRs), agents, and skills. This ensures
single source of truth for project governance and reusable intelligence across
all phases.

**Rationale**: Centralized governance and intelligence prevents duplication and
enables consistent application of project standards across evolving
architecture phases.

### II. Phase Isolation

Each phase MUST have its own isolated folder for code and phase-specific files
only. Phase folders are: phase1-console/, phase2-web/, phase3-chatbot/,
phase4-k8s-local/, and phase5-cloud/. Phase folders MUST be created
automatically when starting a new phase.

**Rationale**: Isolation enables clear boundaries between evolution stages,
prevents cross-phase coupling, and allows each phase to be developed and
demonstrated independently.

### III. Sequential Completion

Complete one phase fully (working app + clean code + tests) before starting
the next. Each phase builds upon the previous one, but phases cannot be worked
on in parallel. A phase is complete only when the application is working, code
is clean, and tests pass.

**Rationale**: Sequential progression ensures each phase is stable before
increasing complexity, maintains project momentum, and provides regular
demonstrable milestones.

### IV. No Manual Coding

All code MUST be created and edited only through Claude Code. Manual coding is
strictly prohibited. This includes all file creation, editing, and modification
operations.

**Rationale**: Ensures consistent application of coding standards, maintains
traceability of all changes, and leverages AI-driven development for
reproducibility and learning.

### V. Code Quality Standards

All code MUST be clean, follow PEP8, use type hints, be modular, and include
tests. Code readability and maintainability are non-negotiable. Each phase
MUST have comprehensive tests that verify functionality.

**Rationale**: High code quality standards ensure the project remains
maintainable through rapid architectural evolution and provides a solid
foundation for each subsequent phase.

### VI. Specification-Driven Development

Always read and reference the correct specification before implementing
anything. Specifications (spec.md, plan.md, tasks.md) MUST guide all
implementation. Implementations MUST align with documented requirements and
design decisions.

**Rationale**: Specification-driven development prevents drift from intended
architecture, ensures requirements are fully met, and provides traceability
from user needs to implementation.

## Folder Structure

### Root (Shared)

```
.specify/
├── memory/
│   └── constitution.md              # This file
├── templates/                       # Shared templates
│   ├── plan-template.md
│   ├── spec-template.md
│   ├── tasks-template.md
│   ├── phr-template.prompt.md
│   └── adr-template.md
└── scripts/                         # Shared scripts

specs/                                # Feature specifications (phase-agnostic)
└── [feature-name]/
    ├── spec.md
    ├── plan.md
    └── tasks.md

history/
├── prompts/                         # Prompt History Records
│   ├── constitution/
│   ├── [feature-name]/
│   └── general/
└── adr/                             # Architecture Decision Records
    └── [decision-title].md

agents/                              # Reusable subagents (planner, coder, etc.)
skills/                              # Reusable skills (CRUD patterns, etc.)
CLAUDE.md                            # Project instructions for Claude
```

### Phase-Specific Isolated Folders

```
phase1-console/                      # Phase 1: Python CLI app only
phase2-web/                          # Phase 2: Next.js + FastAPI + Neon DB only
phase3-chatbot/                      # Phase 3: ChatKit + Agents SDK + MCP only
phase4-k8s-local/                    # Phase 4: Minikube + Helm + Docker only
phase5-cloud/                        # Phase 5: AKS/GKE + Kafka + Dapr + CI/CD only
```

**Rule**: Each phase folder contains ONLY code and configuration specific to
that phase. No shared items.

## Phase Progression

### Phase 1: Console Application (In-Memory)
- **Tech Stack**: Python CLI
- **Scope**: 5 basic CRUD operations (Create, Read, Update, Delete, List)
- **Storage**: In-memory data structures
- **Tests**: Full test coverage of CRUD operations
- **Definition of Done**: Working CLI app with all CRUD operations implemented,
  code clean, tests passing

### Phase 2: Web Application
- **Tech Stack**: Next.js frontend + FastAPI backend + Neon PostgreSQL
- **Auth**: Better Auth with JWT
- **Scope**: Full-stack web interface with persistent storage
- **Tests**: Frontend unit/integration tests + backend API tests
- **Definition of Done**: Deployed web app with authentication, CRUD via web
  UI, PostgreSQL persistence, all tests passing

### Phase 3: AI Chatbot Interface
- **Tech Stack**: OpenAI ChatKit + Agents SDK + MCP tools
- **Scope**: Natural language todo management via chat interface
- **Language**: Support Urdu language (text input/output)
- **Bonus**: Voice commands, Qdrant vector search, recurring tasks, reminders
- **Tests**: Integration tests for chatbot workflows, language tests
- **Definition of Done**: Working chatbot that understands natural language
  commands for todo management, Urdu support verified, all tests passing

### Phase 4: Local Kubernetes Deployment
- **Tech Stack**: Minikube + Helm + Docker + kubectl-ai/kagent
- **Scope**: Containerization and orchestration of full stack
- **Tests**: K8s deployment tests, health checks, integration tests
- **Definition of Done**: Application running in local K8s cluster via Minikube,
  all services communicating correctly, all deployment tests passing

### Phase 5: Advanced Cloud Deployment
- **Tech Stack**: AKS/GKE + Kafka/Redpanda + Dapr + CI/CD
- **Scope**: Production-ready cloud deployment with event-driven architecture
- **Tests**: Cloud deployment validation, end-to-end tests, chaos tests
- **Definition of Done**: Application deployed to cloud with full CI/CD pipeline,
  event-driven message handling, all integration and chaos tests passing

## Development Rules

### Code Creation
- All code MUST be created and edited ONLY through Claude Code
- NO manual coding permitted
- Every file operation must use Claude Code tools

### Code Standards
- Python code MUST follow PEP8 (style guide for Python code)
- All functions MUST have type hints
- Code MUST be modular (separation of concerns, single responsibility)
- All code MUST be clean (readable, maintainable, self-documenting)
- Comments only where logic is not self-evident

### Testing Requirements
- Tests MUST be included for every phase
- Unit tests for individual components
- Integration tests for component interactions
- All tests MUST pass before phase completion
- Test coverage should be comprehensive for critical paths

### Specification Adherence
- Read and reference the correct specification before implementing
- Implementations MUST match documented requirements
- Deviations from specification MUST be documented and justified
- When in doubt, clarify specification before implementing

## Reusable Intelligence

### Subagents
Create and use specialized subagents for common patterns:

- **Planner Agent**: Architecture and implementation planning
- **Coder Agent**: Code implementation and refactoring
- **Tester Agent**: Test creation and execution
- **Reviewer Agent**: Code review and quality checks
- **Deployment Agent**: Deployment automation and validation

### Reusable Skills
Create and maintain skills for common operations:

- **CRUD Operations**: Create, Read, Update, Delete patterns
- **Authentication**: Auth setup, JWT handling, session management, must use better-auth
- **MCP Tools**: Model Context Protocol tool creation and integration
- **Testing Patterns**: Unit, integration, and contract test templates
- **Urdu Support**: Text processing, translation, bidi handling
- **Database Operations**: Schema management, migrations, queries

### Language Support
- **Urdu Language**: Phase 3 chatbot MUST support Urdu text input/output
- **Unicode Handling**: Proper support for RTL (right-to-left) text
- **Transliteration**: Optional bilingual support

### Bonus Features
- Voice command integration (speech-to-text, text-to-speech)
- Qdrant vector search for semantic todo retrieval
- Recurring tasks with configurable intervals
- Reminders with notification delivery

## Code Quality Standards

### Python Code (Phases 1-3 Backend)
- Follow PEP8 style guide strictly
- Use type hints for all function signatures
- Maximum line length: 88 characters (black default)
- Use docstrings for public functions and classes (Google or NumPy style)
- Avoid code duplication (DRY principle)
- Use descriptive variable and function names
- Keep functions focused (single responsibility)

### Code Organization
- Separate concerns: models, services, API/controllers, utilities
- Use dependency injection for testability
- Keep modules focused (single responsibility per file)
- Structure follows project templates (spec/plan/tasks alignment)

### Error Handling
- Use exceptions appropriately for error conditions
- Provide meaningful error messages
- Log errors with appropriate context
- Validate inputs at boundaries

### Documentation
- Inline comments only for non-obvious logic
- Docstrings for public APIs
- README for each phase with setup and usage instructions
- Update documentation as code evolves

## Governance

### Amendment Process
- Constitution changes require explicit documentation
- Version follows semantic versioning (MAJOR.MINOR.PATCH):
  - MAJOR: Backward incompatible governance/principle removals or redefinitions
  - MINOR: New principle/section added or materially expanded guidance
  - PATCH: Clarifications, wording, typo fixes, non-semantic refinements
- Amendments MUST update dependent templates as needed
- All changes MUST have Sync Impact Report at top of file

### Compliance Review
- All PRs and code reviews MUST verify constitution compliance
- Complexity MUST be justified against principles
- Phase transitions require compliance verification
- Code reviews check for manual coding violations
- Test coverage verified at each phase completion

### Phase Gate Criteria
Each phase MUST meet ALL criteria before proceeding:
1. Application works as specified
2. Code follows all quality standards
3. All tests pass
4. Documentation is complete
5. No manual coding detected
6. Specification requirements met

### Violation Handling
- Violations MUST be documented with justification
- Complexity tracking table for required deviations
- Alternative simpler approaches MUST be considered
- Unjustified violations block phase completion

### Runtime Guidance
Use `CLAUDE.md` for runtime development guidance and project-specific
instructions. Constitution provides governance; CLAUDE.md provides execution
context.

---
**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
