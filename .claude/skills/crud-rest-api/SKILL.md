---
name: crud-rest-api
description: Expert in reusable CRUD REST API patterns for FastAPI backend and frontend calls. Use PROACTIVELY when implementing task operations in Phase 2.
---

# CRUD REST API Expert for Todo App

## Overview

This skill provides comprehensive, production-ready patterns for implementing CRUD (Create, Read, Update, Delete) operations across the full stack. It ensures consistency between FastAPI backend endpoints and Next.js frontend API calls, with proper authentication, validation, and error handling.

## Core Responsibilities

- Implement consistent REST API patterns for task operations
- Ensure all operations are user-scoped via JWT authentication
- Provide type-safe interfaces between frontend and backend
- Handle validation, errors, and edge cases properly
- Follow RESTful conventions and HTTP semantics

## Architecture Overview

```
┌─────────────────┐
│  Next.js Client │
│  (Frontend)     │
└────────┬────────┘
         │ HTTP + JWT
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (Backend)      │
└────────┬────────┘
         │ SQLModel ORM
         ▼
┌─────────────────┐
│  PostgreSQL     │
│  (Neon DB)      │
└─────────────────┘
```

## API Endpoint Conventions

### Standard CRUD Endpoints

All task operations follow RESTful conventions under `/api/tasks`:

| Method | Endpoint                    | Purpose                      | Request Body          | Response       |
|--------|----------------------------|------------------------------|-----------------------|----------------|
| GET    | `/api/tasks`               | List all user's tasks        | Query params (filter) | Task[]         |
| GET    | `/api/tasks/{id}`          | Get single task              | None                  | Task           |
| POST   | `/api/tasks`               | Create new task              | CreateTaskInput       | Task           |
| PUT    | `/api/tasks/{id}`          | Update entire task           | UpdateTaskInput       | Task           |
| PATCH  | `/api/tasks/{id}/complete` | Toggle completion status     | None                  | Task           |
| DELETE | `/api/tasks/{id}`          | Delete task                  | None                  | 204 No Content |

### Query Parameters

- `?status=all|pending|completed` - Filter tasks by completion status
- `?sort=newest|oldest|title` - Sort tasks
- `?limit=N&offset=M` - Pagination (future enhancement)

### HTTP Status Codes

- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing/invalid JWT
- `403 Forbidden` - Valid JWT but not task owner
- `404 Not Found` - Task doesn't exist
- `500 Internal Server Error` - Server error

## Backend (FastAPI) Patterns

### Core Principles

1. **User Isolation**: All queries MUST filter by `user_id` from JWT
2. **JWT Authentication**: Every endpoint requires valid JWT token
3. **Input Validation**: Use Pydantic models for request validation
4. **Error Handling**: Return proper HTTP codes with clear messages
5. **Type Safety**: Use SQLModel for database operations

### Route Structure

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.task import Task, TaskCreate, TaskUpdate
from app.api.dependencies import get_current_user, get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Task:
    """Create a new task for the authenticated user."""
    # Implementation...

@router.get("/", response_model=list[Task])
async def list_tasks(
    status: str = "all",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[Task]:
    """List all tasks for the authenticated user."""
    # Implementation...

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Task:
    """Get a single task by ID."""
    # Implementation...

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Task:
    """Update a task."""
    # Implementation...

@router.patch("/{task_id}/complete", response_model=Task)
async def toggle_task_complete(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Task:
    """Toggle task completion status."""
    # Implementation...

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """Delete a task."""
    # Implementation...
```

### Key Backend Patterns

#### 1. User Isolation Pattern
```python
# ALWAYS filter by user_id
statement = select(Task).where(
    Task.user_id == current_user.id
)

# For single task, verify ownership
task = db.get(Task, task_id)
if not task or task.user_id != current_user.id:
    raise HTTPException(status_code=404, detail="Task not found")
```

#### 2. JWT Dependency Pattern
```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Extract and validate user from JWT token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### 3. Validation Pattern
```python
# app/models/task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### 4. Error Response Pattern
```python
# Consistent error responses
{
    "detail": "Task not found"
}

# Validation errors (automatic from Pydantic)
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

## Frontend API Call Patterns

### Core Principles

1. **Use API Client**: Always use `api` object from `frontend-api-client` skill
2. **Type Safety**: Define TypeScript interfaces matching backend models
3. **Loading States**: Show feedback during async operations
4. **Error Handling**: Display user-friendly error messages
5. **Cache Management**: Invalidate queries after mutations (React Query)

### API Client Usage

```typescript
// lib/api.ts
export const api = {
  // List tasks with optional filter
  getTasks: (status?: "all" | "pending" | "completed") =>
    authenticatedFetch<Task[]>(
      `/api/tasks${status && status !== "all" ? `?status=${status}` : ""}`
    ),

  // Get single task
  getTask: (id: string) =>
    authenticatedFetch<Task>(`/api/tasks/${id}`),

  // Create task
  createTask: (data: CreateTaskInput) =>
    authenticatedFetch<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // Update task
  updateTask: (id: string, data: UpdateTaskInput) =>
    authenticatedFetch<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // Toggle complete
  toggleTaskComplete: (id: string) =>
    authenticatedFetch<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    }),

  // Delete task
  deleteTask: (id: string) =>
    authenticatedFetch<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    }),
}
```

### React Query Hooks Pattern

```typescript
// hooks/use-tasks.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useTasks(status?: "all" | "pending" | "completed") {
  return useQuery({
    queryKey: ["tasks", status],
    queryFn: () => api.getTasks(status),
  })
}

export function useTask(id: string) {
  return useQuery({
    queryKey: ["tasks", id],
    queryFn: () => api.getTask(id),
    enabled: !!id,
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}

export function useUpdateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskInput }) =>
      api.updateTask(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      queryClient.invalidateQueries({ queryKey: ["tasks", variables.id] })
    },
  })
}

export function useDeleteTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}

export function useToggleTaskComplete() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.toggleTaskComplete,
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      queryClient.invalidateQueries({ queryKey: ["tasks", id] })
    },
  })
}
```

## Common CRUD Flows

### 1. Create Task Flow

**Backend:**
1. Validate request body (Pydantic)
2. Extract user_id from JWT
3. Create task with user_id
4. Save to database
5. Return created task (201)

**Frontend:**
1. User fills form
2. Client validates input
3. Call `api.createTask()`
4. Show loading state
5. On success: invalidate cache, show toast, clear form
6. On error: show error message

### 2. List Tasks Flow

**Backend:**
1. Extract user_id from JWT
2. Parse query parameters (status filter)
3. Query tasks filtered by user_id and status
4. Return task list (200)

**Frontend:**
1. Component mounts
2. Call `useTasks(status)`
3. Show loading skeleton
4. Render tasks or empty state
5. Handle errors

### 3. Update Task Flow

**Backend:**
1. Extract user_id from JWT
2. Find task by ID
3. Verify task.user_id == current_user.id
4. Apply updates (only provided fields)
5. Update updated_at timestamp
6. Save and return updated task (200)

**Frontend:**
1. User edits task
2. Call `useUpdateTask()`
3. Optimistically update UI (optional)
4. On success: invalidate cache
5. On error: rollback and show message

### 4. Delete Task Flow

**Backend:**
1. Extract user_id from JWT
2. Find task by ID
3. Verify ownership
4. Delete from database
5. Return 204 No Content

**Frontend:**
1. User confirms deletion
2. Call `useDeleteTask()`
3. Optimistically remove from UI (optional)
4. On success: invalidate cache, show toast
5. On error: rollback and show message

### 5. Toggle Complete Flow

**Backend:**
1. Extract user_id from JWT
2. Find task by ID
3. Verify ownership
4. Toggle completed field
5. Update updated_at
6. Return updated task (200)

**Frontend:**
1. User clicks checkbox
2. Call `useToggleTaskComplete()`
3. Optimistically update UI
4. On success: update cache
5. On error: rollback

## Best Practices

### Backend Best Practices

1. **Always verify ownership**
   ```python
   if task.user_id != current_user.id:
       raise HTTPException(status_code=404, detail="Task not found")
   ```

2. **Use proper HTTP codes**
   - 201 for POST (create)
   - 200 for GET/PUT/PATCH
   - 204 for DELETE
   - 404 for not found (don't reveal if resource exists)

3. **Validate input strictly**
   ```python
   class TaskCreate(SQLModel):
       title: str = Field(min_length=1, max_length=200)
   ```

4. **Update timestamps**
   ```python
   task.updated_at = datetime.utcnow()
   ```

5. **Use transactions for complex operations**
   ```python
   with db.begin():
       # Multiple operations
   ```

6. **Return full object after mutations**
   - Helps frontend update cache with server state

### Frontend Best Practices

1. **Always use React Query**
   - Automatic caching and refetching
   - Loading and error states
   - Optimistic updates

2. **Invalidate cache after mutations**
   ```typescript
   queryClient.invalidateQueries({ queryKey: ["tasks"] })
   ```

3. **Use optimistic updates for instant feedback**
   ```typescript
   onMutate: async (newTask) => {
     await queryClient.cancelQueries({ queryKey: ["tasks"] })
     const previousTasks = queryClient.getQueryData(["tasks"])
     queryClient.setQueryData(["tasks"], old => [...old, newTask])
     return { previousTasks }
   }
   ```

4. **Handle errors gracefully**
   ```typescript
   onError: (error, variables, context) => {
     queryClient.setQueryData(["tasks"], context.previousTasks)
     toast.error(error.message)
   }
   ```

5. **Show loading states**
   ```typescript
   if (isLoading) return <Skeleton />
   ```

## Security Considerations

1. **Never trust client input** - Validate on backend
2. **Always filter by user_id** - Prevent unauthorized access
3. **Use 404 for unauthorized** - Don't reveal resource existence
4. **Validate JWT on every request** - No exceptions
5. **Rate limit endpoints** - Prevent abuse
6. **Sanitize error messages** - Don't leak implementation details

## Testing

### Backend Tests
```python
def test_create_task_requires_auth(client):
    response = client.post("/api/tasks", json={"title": "Test"})
    assert response.status_code == 401

def test_create_task_success(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_user_cannot_access_others_tasks(client, auth_headers_user2):
    # User 1 creates task
    response = client.post("/api/tasks", json={"title": "Test"}, headers=auth_headers_user1)
    task_id = response.json()["id"]

    # User 2 tries to access
    response = client.get(f"/api/tasks/{task_id}", headers=auth_headers_user2)
    assert response.status_code == 404
```

### Frontend Tests
```typescript
describe("useTasks", () => {
  it("fetches tasks on mount", async () => {
    const { result } = renderHook(() => useTasks(), { wrapper: QueryWrapper })
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toHaveLength(3)
  })
})

describe("useCreateTask", () => {
  it("creates task and invalidates cache", async () => {
    const { result } = renderHook(() => useCreateTask(), { wrapper: QueryWrapper })

    await act(async () => {
      await result.current.mutateAsync({ title: "New Task" })
    })

    expect(mockApi.createTask).toHaveBeenCalledWith({ title: "New Task" })
    expect(queryClient.invalidateQueries).toHaveBeenCalledWith({ queryKey: ["tasks"] })
  })
})
```

## Integration Points

### With backend-auth Skill
- Uses JWT extraction and validation from `get_current_user` dependency
- Ensures all routes are protected and user-scoped

### With frontend-api-client Skill
- All API calls go through authenticated fetch wrapper
- Automatic JWT attachment to requests

### With neon-sqlmodel-db Skill
- Uses SQLModel for database operations
- Follows schema and query patterns

## Resources

- See `templates/fastapi-crud-route-template.py` for complete backend route implementation
- See `templates/frontend-crud-hook-template.tsx` for React Query hooks
- See `examples/create-task-flow.md` for full create flow
- See `examples/list-tasks-with-filter.md` for list with filtering
- See `examples/update-task-example.md` for update patterns

## Proactive Usage

This skill should be invoked automatically when:
- Implementing any CRUD operation for tasks
- Creating new API endpoints
- Building forms that create or update data
- Implementing list views with filtering
- Adding data fetching hooks
- Reviewing API integration code
- Debugging data flow issues between frontend and backend
