# Create Task Flow - Complete End-to-End Example

This document provides a complete, production-ready implementation of the create task flow from frontend to backend, including all necessary components, validation, error handling, and testing.

## Architecture Overview

```
┌─────────────────────┐
│  CreateTaskForm     │ ← User Input
│  (Next.js Client)   │
└──────────┬──────────┘
           │
           │ 1. Form Submit
           ▼
┌─────────────────────┐
│  useCreateTask()    │ ← React Query Hook
│  (React Query)      │
└──────────┬──────────┘
           │
           │ 2. api.createTask()
           ▼
┌─────────────────────┐
│  authenticatedFetch │ ← JWT Attached
│  (API Client)       │
└──────────┬──────────┘
           │
           │ 3. POST /api/tasks + JWT
           ▼
┌─────────────────────┐
│  create_task()      │ ← FastAPI Route
│  (Backend)          │
└──────────┬──────────┘
           │
           │ 4. Validate & Save
           ▼
┌─────────────────────┐
│  PostgreSQL         │
│  (Neon DB)          │
└─────────────────────┘
```

## Backend Implementation

### 1. Database Model

```python
# app/models/task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    """Base task fields shared across models"""
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 chars)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 chars)"
    )

class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class Task(TaskBase, table=True):
    """Task database model"""
    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="UUID primary key"
    )
    completed: bool = Field(
        default=False,
        description="Task completion status"
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID (from JWT)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
```

### 2. FastAPI Route

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime

from app.models.task import Task, TaskCreate
from app.models.user import User
from app.api.dependencies import get_current_user, get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user",
    responses={
        201: {
            "description": "Task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Complete project documentation",
                        "description": "Write comprehensive docs",
                        "completed": False,
                        "user_id": "123e4567-e89b-12d3-a456-426614174000",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized - invalid or missing JWT"},
    }
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Create a new task.

    The task will be associated with the authenticated user from the JWT token.

    **Request Body:**
    - `title` (required): Task title (1-200 characters)
    - `description` (optional): Task description (max 1000 characters)

    **Authentication:**
    - Requires valid JWT token in Authorization header

    **Example:**
    ```json
    {
        "title": "Complete project documentation",
        "description": "Write comprehensive docs for the API"
    }
    ```
    """
    try:
        # Create new task instance
        new_task = Task(
            title=task_data.title.strip(),  # Remove leading/trailing whitespace
            description=task_data.description.strip() if task_data.description else None,
            user_id=current_user.id,  # From JWT token
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Add to database
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )
```

### 3. Dependencies

```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.models.user import User

security = HTTPBearer()

async def get_db() -> Session:
    """Database session dependency"""
    session = get_session()
    try:
        yield session
    finally:
        session.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate user from JWT token.

    Raises:
        401: Invalid or missing token
        401: User not found
    """
    try:
        token = credentials.credentials

        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user ID from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )

        # Fetch user from database
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: could not decode"
        )
```

## Frontend Implementation

### 1. API Client

```typescript
// lib/api.ts
import { authClient } from "better-auth/client"

const client = authClient()
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Type definitions
export interface Task {
  id: string
  title: string
  description?: string | null
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
}

// Authenticated fetch wrapper
async function authenticatedFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await client.fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Request failed" }))
    throw new Error(error.message || `HTTP ${response.status}`)
  }

  return response.json()
}

// API methods
export const api = {
  createTask: (data: CreateTaskInput) =>
    authenticatedFetch<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),
}
```

### 2. React Query Hook

```typescript
// hooks/use-tasks.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api, CreateTaskInput } from "@/lib/api"
import { toast } from "sonner"

export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateTaskInput) => api.createTask(data),
    onSuccess: (newTask) => {
      // Invalidate task list to refetch with new task
      queryClient.invalidateQueries({ queryKey: ["tasks"] })

      // Show success message
      toast.success("Task created successfully!")
    },
    onError: (error: Error) => {
      // Show error message
      toast.error(error.message || "Failed to create task")
    },
  })
}
```

### 3. Create Task Form Component

```typescript
// components/create-task-form.tsx
"use client"

import { useState } from "react"
import { useCreateTask } from "@/hooks/use-tasks"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2 } from "lucide-react"

export function CreateTaskForm() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  const createTask = useCreateTask()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    // Client-side validation
    if (!title.trim()) {
      return
    }

    try {
      await createTask.mutateAsync({
        title: title.trim(),
        description: description.trim() || undefined,
      })

      // Clear form on success
      setTitle("")
      setDescription("")
    } catch (error) {
      // Error handled by mutation
      console.error("Failed to create task:", error)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create New Task</CardTitle>
        <CardDescription>
          Add a new task to your list. Fill in the details below.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">
              Title <span className="text-destructive">*</span>
            </Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Complete project documentation"
              required
              disabled={createTask.isPending}
              maxLength={200}
            />
            <p className="text-xs text-muted-foreground">
              {title.length}/200 characters
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description (Optional)</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add more details about the task..."
              rows={4}
              disabled={createTask.isPending}
              maxLength={1000}
            />
            <p className="text-xs text-muted-foreground">
              {description.length}/1000 characters
            </p>
          </div>

          <Button
            type="submit"
            disabled={createTask.isPending || !title.trim()}
            className="w-full"
          >
            {createTask.isPending && (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            )}
            {createTask.isPending ? "Creating..." : "Create Task"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```

### 4. Enhanced Form with Validation

```typescript
// components/create-task-form-advanced.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useCreateTask } from "@/hooks/use-tasks"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

// Validation schema
const createTaskSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be 200 characters or less")
    .trim(),
  description: z
    .string()
    .max(1000, "Description must be 1000 characters or less")
    .optional()
    .transform((val) => val?.trim() || undefined),
})

type CreateTaskFormValues = z.infer<typeof createTaskSchema>

export function CreateTaskFormAdvanced() {
  const createTask = useCreateTask()

  const form = useForm<CreateTaskFormValues>({
    resolver: zodResolver(createTaskSchema),
    defaultValues: {
      title: "",
      description: "",
    },
  })

  async function onSubmit(data: CreateTaskFormValues) {
    try {
      await createTask.mutateAsync(data)
      form.reset()
    } catch (error) {
      // Error handled by mutation
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input
                  placeholder="Enter task title"
                  {...field}
                  disabled={createTask.isPending}
                />
              </FormControl>
              <FormDescription>
                A brief title for your task (required)
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description (Optional)</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Add more details..."
                  rows={4}
                  {...field}
                  disabled={createTask.isPending}
                />
              </FormControl>
              <FormDescription>
                Additional details about your task
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={createTask.isPending}
          className="w-full"
        >
          {createTask.isPending ? "Creating..." : "Create Task"}
        </Button>
      </form>
    </Form>
  )
}
```

## Complete Request/Response Flow

### 1. Request Example

```http
POST /api/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the API"
}
```

### 2. Success Response (201)

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the API",
  "completed": false,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 3. Validation Error Response (400)

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 4. Authentication Error Response (401)

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Invalid token"
}
```

## Testing

### Backend Tests

```python
# tests/test_tasks.py
import pytest
from fastapi.testclient import TestClient

def test_create_task_success(client: TestClient, auth_headers: dict):
    """Test successful task creation"""
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    assert "id" in data
    assert "user_id" in data

def test_create_task_requires_auth(client: TestClient):
    """Test that authentication is required"""
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task"}
    )

    assert response.status_code == 401

def test_create_task_validation_error(client: TestClient, auth_headers: dict):
    """Test validation errors"""
    # Missing title
    response = client.post(
        "/api/tasks",
        json={"description": "Description without title"},
        headers=auth_headers
    )

    assert response.status_code == 422

    # Title too long
    response = client.post(
        "/api/tasks",
        json={"title": "x" * 201},
        headers=auth_headers
    )

    assert response.status_code == 422
```

### Frontend Tests

```typescript
// __tests__/create-task-form.test.tsx
import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { CreateTaskForm } from "@/components/create-task-form"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

const queryClient = new QueryClient()

function Wrapper({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

describe("CreateTaskForm", () => {
  it("creates task successfully", async () => {
    const user = userEvent.setup()

    render(<CreateTaskForm />, { wrapper: Wrapper })

    // Fill form
    await user.type(screen.getByLabelText(/title/i), "Test Task")
    await user.type(screen.getByLabelText(/description/i), "Test Description")

    // Submit
    await user.click(screen.getByRole("button", { name: /create task/i }))

    // Wait for success
    await waitFor(() => {
      expect(screen.getByText(/task created successfully/i)).toBeInTheDocument()
    })
  })

  it("shows validation error for empty title", async () => {
    const user = userEvent.setup()

    render(<CreateTaskForm />, { wrapper: Wrapper })

    // Try to submit without title
    await user.click(screen.getByRole("button", { name: /create task/i }))

    // Button should be disabled
    expect(screen.getByRole("button", { name: /create task/i })).toBeDisabled()
  })
})
```

## Key Takeaways

1. **User Isolation**: Always filter by `user_id` from JWT
2. **Validation**: Validate on both frontend and backend
3. **Error Handling**: Provide clear error messages
4. **Loading States**: Show feedback during async operations
5. **Cache Management**: Invalidate queries after mutations
6. **Type Safety**: Use TypeScript throughout
7. **Testing**: Test both happy path and error cases
