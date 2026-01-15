# Quickstart Guide - Phase II Full-Stack Multi-User Web Todo Application

**Date**: 2026-01-02
**Feature**: 001-phase2-web-todo
**Branch**: 001-phase2-web-todo

## Overview

This guide provides step-by-step instructions for setting up and implementing the Phase II full-stack multi-user web todo application.

## Prerequisites

### System Requirements

- **Node.js**: 18+ (LTS recommended)
- **Python**: 3.11+
- **Git**: Latest version
- **Neon Account**: https://neon.tech (free tier sufficient)
- **Code Editor**: VS Code recommended

### Knowledge Requirements

- TypeScript / JavaScript basics
- Python basics
- React fundamentals
- REST API concepts
- Basic SQL understanding

## Project Structure

```
phase2-web/
├── frontend/              # Next.js application
│   ├── app/              # App Router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│   └── tsconfig.json     # TypeScript config
│
└── backend/              # FastAPI application
    ├── app/              # Application code
    │   ├── models/       # SQLModel ORM models
    │   ├── routes/       # API endpoints
    │   ├── auth/         # JWT verification
    │   ├── database/     # DB connection
    │   └── main.py       # FastAPI app instance
    ├── tests/            # Backend tests
    ├── requirements.txt  # Python dependencies
    └── .env              # Environment variables (not in git)
```

## Implementation Sequence

Follow this order for optimal results:

### Phase 2A: Backend Foundation (Days 1-2)

1. **Setup Backend Project**
2. **Configure Database Connection**
3. **Implement Auth Middleware**
4. **Create Task CRUD Endpoints**
5. **Write Backend Tests**

### Phase 2B: Frontend Core (Days 3-4)

6. **Setup Frontend Project**
7. **Implement Auth Pages**
8. **Create Dashboard Layout**
9. **Build Task Components**
10. **Integrate API Client**

### Phase 2C: Polish (Day 5)

11. **Add Responsive Design**
12. **Implement Animations**
13. **Error Handling & Loading States**
14. **End-to-End Testing**

## Step-by-Step Implementation

### Step 1: Setup Backend Project

**Location**: `phase2-web/backend/`

**Actions**:
1. Create directory structure
2. Initialize Python virtual environment
3. Install dependencies
4. Setup environment variables

**Commands**:
```bash
# Create backend directory
mkdir -p phase2-web/backend
cd phase2-web/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt <<EOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
asyncpg==0.29.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
DATABASE_URL_ASYNC=postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
EOF
```

**Skill Reference**: None (basic setup)

---

### Step 2: Configure Database Connection

**Location**: `phase2-web/backend/app/database/`

**Actions**:
1. Create database connection module
2. Implement session management
3. Create table initialization function

**Skill Reference**: `neon-sqlmodel-db`

**Implementation Pattern**:
```python
# app/database/connection.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

**Commands**:
```bash
# Create database directory
mkdir -p app/database

# Use neon-sqlmodel-db skill to generate connection code
# (Claude will use this skill during implementation)
```

---

### Step 3: Implement Auth Middleware

**Location**: `phase2-web/backend/app/auth/`

**Actions**:
1. Create JWT verification dependency
2. Implement get_current_user function
3. Handle 401 errors for invalid tokens

**Skill Reference**: `backend-auth`

**Implementation Pattern**:
```python
# app/auth/dependencies.py
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def get_current_user(request: Request) -> str:
    """Verify JWT and return user_id."""
    # See backend-auth skill for full implementation
    pass
```

**Commands**:
```bash
# Create auth directory
mkdir -p app/auth

# Use backend-auth skill to generate middleware code
# (Claude will use this skill during implementation)
```

---

### Step 4: Create Task CRUD Endpoints

**Location**: `phase2-web/backend/app/routes/`

**Actions**:
1. Create tasks router
2. Implement GET /api/tasks (list)
3. Implement POST /api/tasks (create)
4. Implement PUT /api/tasks/{id} (update)
5. Implement PATCH /api/tasks/{id}/toggle (toggle completion)
6. Implement DELETE /api/tasks/{id} (delete)
7. Ensure all endpoints filter by user_id

**Skill Reference**: `crud-rest-api`, `backend-auth`

**Implementation Pattern**:
```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.auth.dependencies import get_current_user
from app.database.connection import get_session
from app.models.task import Task

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
async def list_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all tasks for authenticated user."""
    # See crud-rest-api skill for full implementation
    pass
```

**Commands**:
```bash
# Create routes directory
mkdir -p app/routes

# Use crud-rest-api skill to generate CRUD endpoints
# (Claude will use this skill during implementation)
```

---

### Step 5: Write Backend Tests

**Location**: `phase2-web/backend/tests/`

**Actions**:
1. Create test fixtures (test database, test client)
2. Test JWT verification middleware
3. Test task CRUD operations
4. Test user isolation (User A cannot access User B's tasks)
5. Test error cases (401, 404, 400)

**Skill Reference**: None (use pytest patterns)

**Commands**:
```bash
# Create tests directory
mkdir -p tests

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

---

### Step 6: Setup Frontend Project

**Location**: `phase2-web/frontend/`

**Actions**:
1. Initialize Next.js project with App Router
2. Install dependencies (Tailwind, shadcn, Better Auth, Framer Motion)
3. Configure TypeScript
4. Setup environment variables

**Commands**:
```bash
# Create frontend directory
cd ../..
npx create-next-app@latest phase2-web/frontend \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"

cd phase2-web/frontend

# Install additional dependencies
npm install @better-auth/core @better-auth/client
npm install framer-motion
npm install @radix-ui/react-dialog @radix-ui/react-toast
npm install class-variance-authority clsx tailwind-merge

# Install shadcn/ui
npx shadcn-ui@latest init

# Create .env.local
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-here
EOF
```

**Skill Reference**: `nextjs-app-router`, `tailwind`, `shadcn`

---

### Step 7: Implement Auth Pages

**Location**: `phase2-web/frontend/app/(auth)/`

**Actions**:
1. Create auth layout (centered card design)
2. Create signup page with Better Auth
3. Create login page with Better Auth
4. Configure JWT cookie storage
5. Implement protected route middleware

**Skill Reference**: `frontend-auth`, `shadcn`

**Implementation Pattern**:
```tsx
// app/(auth)/login/page.tsx
"use client"
import { useState } from "react"
import { useAuth } from "@/lib/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function LoginPage() {
  const { login } = useAuth()
  // See frontend-auth skill for full implementation
}
```

**Commands**:
```bash
# Create auth route group
mkdir -p app/(auth)/login app/(auth)/signup

# Use frontend-auth skill to generate auth pages
# (Claude will use this skill during implementation)
```

---

### Step 8: Create Dashboard Layout

**Location**: `phase2-web/frontend/app/(dashboard)/`

**Actions**:
1. Create dashboard layout with header and navigation
2. Implement logout button
3. Add protected route wrapper
4. Create loading and error states

**Skill Reference**: `nextjs-app-router`, `shadcn`, `tailwind`

**Implementation Pattern**:
```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <nav className="container mx-auto px-4 py-4">
          {/* Header content */}
        </nav>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
```

---

### Step 9: Build Task Components

**Location**: `phase2-web/frontend/components/`

**Actions**:
1. Create TaskList component (displays tasks)
2. Create TaskItem component (individual task with actions)
3. Create TaskForm component (add new task)
4. Implement task toggle (completion status)
5. Implement task edit (inline or modal)
6. Implement task delete with confirmation

**Skill Reference**: `shadcn`, `framer-motion`, `tailwind`

**Implementation Pattern**:
```tsx
// components/TaskItem.tsx
"use client"
import { motion } from "framer-motion"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"

export function TaskItem({ task, onToggle, onDelete, onEdit }) {
  // See framer-motion and shadcn skills for full implementation
}
```

---

### Step 10: Integrate API Client

**Location**: `phase2-web/frontend/lib/`

**Actions**:
1. Create API client with JWT token attachment
2. Implement task CRUD functions (fetch, create, update, delete)
3. Handle errors and loading states
4. Configure automatic token refresh

**Skill Reference**: `frontend-api-client`

**Implementation Pattern**:
```tsx
// lib/api/tasks.ts
export async function fetchTasks() {
  const response = await fetch(`${API_URL}/api/tasks`, {
    headers: {
      "Authorization": `Bearer ${getToken()}`
    }
  })
  // See frontend-api-client skill for full implementation
}
```

---

### Step 11: Add Responsive Design

**Location**: All frontend components

**Actions**:
1. Review all pages for mobile responsiveness
2. Test on 320px, 768px, 1024px, 1920px widths
3. Add mobile-specific navigation (hamburger menu if needed)
4. Ensure touch-friendly button sizes (min 44x44px)
5. Test keyboard navigation

**Skill Reference**: `tailwind`

**Implementation Pattern**:
```tsx
<div className="
  grid
  grid-cols-1          /* Mobile: 1 column */
  md:grid-cols-2       /* Tablet: 2 columns */
  lg:grid-cols-3       /* Desktop: 3 columns */
  gap-4
">
  {/* Content */}
</div>
```

---

### Step 12: Implement Animations

**Location**: All frontend components

**Actions**:
1. Add list item entrance animations (staggered)
2. Add task completion toggle animation
3. Add task deletion exit animation
4. Add page transition animations
5. Respect prefers-reduced-motion

**Skill Reference**: `framer-motion`

**Implementation Pattern**:
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, x: -100 }}
  transition={{ duration: 0.2 }}
>
  {/* Task item */}
</motion.div>
```

---

### Step 13: Error Handling & Loading States

**Location**: All frontend pages and components

**Actions**:
1. Add loading spinners during API calls
2. Display toast notifications for success/error
3. Add error boundaries for unexpected errors
4. Show inline validation errors on forms
5. Implement retry logic for failed requests

**Skill Reference**: `shadcn` (Toast component)

**Implementation Pattern**:
```tsx
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()

try {
  await createTask(description)
  toast({ title: "Success", description: "Task created!" })
} catch (error) {
  toast({ title: "Error", description: "Failed to create task", variant: "destructive" })
}
```

---

### Step 14: End-to-End Testing

**Location**: `phase2-web/frontend/e2e/` (optional)

**Actions**:
1. Write E2E tests for user flows
2. Test signup → login → create task → toggle → delete → logout
3. Test error scenarios (network failure, invalid credentials)
4. Test responsive behavior (mobile, tablet, desktop)

**Commands**:
```bash
# Install Playwright (optional for MVP)
npm install -D @playwright/test

# Run E2E tests
npx playwright test
```

---

## Running the Application

### Development Mode

**Terminal 1 - Backend**:
```bash
cd phase2-web/backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd phase2-web/frontend
npm run dev
```

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Testing

**Backend Tests**:
```bash
cd phase2-web/backend
pytest tests/ -v
```

**Frontend Tests**:
```bash
cd phase2-web/frontend
npm test
```

---

## Environment Variables Checklist

### Backend (.env)
- [ ] DATABASE_URL (Neon PostgreSQL connection string)
- [ ] DATABASE_URL_ASYNC (Async version for SQLModel)
- [ ] BETTER_AUTH_SECRET (32+ character secret key)
- [ ] ALGORITHM (HS256)
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES (1440 = 24 hours)

### Frontend (.env.local)
- [ ] NEXT_PUBLIC_API_URL (Backend URL, e.g., http://localhost:8000)
- [ ] NEXT_PUBLIC_BETTER_AUTH_URL (Frontend URL, e.g., http://localhost:3000)
- [ ] BETTER_AUTH_SECRET (Same as backend secret)

**CRITICAL**: BETTER_AUTH_SECRET must be identical in both frontend and backend!

---

## Troubleshooting

### Common Issues

**Issue**: "Module not found" errors in backend
- **Solution**: Activate virtual environment and reinstall dependencies
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Issue**: JWT verification fails (401 errors)
- **Solution**: Verify BETTER_AUTH_SECRET is identical in frontend and backend .env files

**Issue**: Database connection errors
- **Solution**: Check DATABASE_URL is correct and Neon database is active

**Issue**: CORS errors in frontend
- **Solution**: Add CORS middleware to FastAPI backend
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

**Issue**: Responsive design not working
- **Solution**: Verify Tailwind CSS is configured correctly and purging is not removing needed classes

---

## Next Steps After Implementation

1. ✅ Verify all user stories (P1, P2, P3) are implemented
2. ✅ Run all tests (backend + frontend)
3. ✅ Test on multiple devices (mobile, tablet, desktop)
4. ✅ Review against specification requirements (FR-001 through FR-020)
5. ✅ Measure against success criteria (SC-001 through SC-010)
6. → Proceed to Phase 3 (AI Chatbot Interface)

---

## Skills Reference Summary

Use these reusable skills during implementation:

**Backend Skills**:
- `backend-auth`: JWT verification, user isolation
- `neon-sqlmodel-db`: Database connection, models
- `crud-rest-api`: RESTful endpoints

**Frontend Skills**:
- `nextjs-app-router`: App Router structure
- `frontend-auth`: Better Auth integration
- `shadcn`: UI components
- `tailwind`: Responsive design
- `framer-motion`: Animations
- `frontend-api-client`: API integration

---

## Estimated Timeline

- **Phase 2A (Backend)**: 2 days
- **Phase 2B (Frontend)**: 2 days
- **Phase 2C (Polish)**: 1 day
- **Total**: 5 days

**Note**: Timeline assumes working 6-8 hours per day with existing skills.

---

## Success Indicators

✅ Users can sign up and log in
✅ Users can create, read, update, delete, and toggle tasks
✅ Each user can only see their own tasks
✅ Application is responsive on mobile, tablet, and desktop
✅ Animations are smooth and enhance UX
✅ All tests pass
✅ No manual coding violations detected

**Definition of Done**: Working web application with all P1 and P2 user stories implemented, tests passing, and code quality standards met per constitution.
