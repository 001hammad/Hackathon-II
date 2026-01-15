# List Tasks with Filter - Complete Implementation

This document provides a complete implementation of listing tasks with filtering, sorting, and optional pagination. It covers both backend API endpoints and frontend components with React Query integration.

## Architecture Overview

```
┌──────────────────┐
│  TaskListPage    │
│  (Next.js)       │
└────────┬─────────┘
         │
         │ 1. Mount + Filter Change
         ▼
┌──────────────────┐
│  useTasks(       │
│    status="all"  │ ← React Query Hook
│  )               │
└────────┬─────────┘
         │
         │ 2. api.getTasks(status)
         ▼
┌──────────────────┐
│  GET /api/tasks  │
│  ?status=all     │ ← API Request + JWT
└────────┬─────────┘
         │
         │ 3. Query Database
         ▼
┌──────────────────┐
│  list_tasks()    │ ← FastAPI Route
│  Filter by user  │
└────────┬─────────┘
         │
         │ 4. Return Tasks
         ▼
┌──────────────────┐
│  PostgreSQL      │
└──────────────────┘
```

## Backend Implementation

### 1. FastAPI Route with Filtering

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session, select, col
from typing import Literal

from app.models.task import Task
from app.models.user import User
from app.api.dependencies import get_current_user, get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get(
    "/",
    response_model=list[Task],
    summary="List all tasks",
    description="Get all tasks for the authenticated user with optional filtering and sorting",
    responses={
        200: {
            "description": "List of tasks",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "Complete documentation",
                            "description": "Write API docs",
                            "completed": False,
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            }
        },
        401: {"description": "Unauthorized"}
    }
)
async def list_tasks(
    status: Literal["all", "pending", "completed"] = Query(
        "all",
        description="Filter by completion status",
        example="all"
    ),
    sort: Literal["newest", "oldest", "title"] = Query(
        "newest",
        description="Sort order",
        example="newest"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Task]:
    """
    List all tasks for the authenticated user.

    **Query Parameters:**
    - `status`: Filter by completion status
      - `all`: Show all tasks (default)
      - `pending`: Show only incomplete tasks
      - `completed`: Show only completed tasks
    - `sort`: Sort order
      - `newest`: Most recent first (default)
      - `oldest`: Oldest first
      - `title`: Alphabetical by title

    **Authentication:**
    - Requires valid JWT token in Authorization header

    **Returns:**
    - Array of tasks matching the filter criteria
    - Empty array if no tasks found

    **Example:**
    ```
    GET /api/tasks?status=pending&sort=newest
    ```
    """
    # Build base query - ALWAYS filter by user_id for security
    statement = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    # "all" - no additional filter

    # Apply sorting
    if sort == "newest":
        statement = statement.order_by(col(Task.created_at).desc())
    elif sort == "oldest":
        statement = statement.order_by(col(Task.created_at).asc())
    elif sort == "title":
        statement = statement.order_by(col(Task.title).asc())

    # Execute query
    results = db.exec(statement)
    tasks = results.all()

    return tasks
```

### 2. Advanced Filtering with Pagination

```python
# app/api/routes/tasks.py (additional endpoint)
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: list[Task]
    total: int
    page: int
    size: int
    pages: int

@router.get(
    "/paginated",
    response_model=PaginatedResponse,
    summary="List tasks with pagination",
    description="Get paginated list of tasks with filtering"
)
async def list_tasks_paginated(
    status: Literal["all", "pending", "completed"] = Query("all"),
    sort: Literal["newest", "oldest", "title"] = Query("newest"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, max_length=200, description="Search in title"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse:
    """
    List tasks with pagination and search.

    **Query Parameters:**
    - `status`: Filter by completion status (all, pending, completed)
    - `sort`: Sort order (newest, oldest, title)
    - `page`: Page number (1-indexed, default: 1)
    - `size`: Items per page (1-100, default: 20)
    - `search`: Search query for title (optional)

    **Returns:**
    ```json
    {
        "items": [...tasks...],
        "total": 100,
        "page": 1,
        "size": 20,
        "pages": 5
    }
    ```
    """
    # Build base query
    statement = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)

    # Apply search filter
    if search:
        statement = statement.where(col(Task.title).ilike(f"%{search}%"))

    # Apply sorting
    if sort == "newest":
        statement = statement.order_by(col(Task.created_at).desc())
    elif sort == "oldest":
        statement = statement.order_by(col(Task.created_at).asc())
    elif sort == "title":
        statement = statement.order_by(col(Task.title).asc())

    # Get total count before pagination
    count_results = db.exec(statement)
    total = len(count_results.all())

    # Apply pagination
    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size)

    # Execute query
    results = db.exec(statement)
    tasks = results.all()

    # Calculate total pages
    pages = (total + size - 1) // size  # Ceiling division

    return PaginatedResponse(
        items=tasks,
        total=total,
        page=page,
        size=size,
        pages=pages,
    )
```

## Frontend Implementation

### 1. API Client Methods

```typescript
// lib/api.ts
export const api = {
  /**
   * Get all tasks with optional status filter
   */
  getTasks: (status?: "all" | "pending" | "completed") => {
    const params = new URLSearchParams()
    if (status && status !== "all") {
      params.append("status", status)
    }

    const queryString = params.toString()
    const url = `/api/tasks${queryString ? `?${queryString}` : ""}`

    return authenticatedFetch<Task[]>(url)
  },

  /**
   * Get tasks with advanced filtering
   */
  getTasksAdvanced: (options: {
    status?: "all" | "pending" | "completed"
    sort?: "newest" | "oldest" | "title"
    search?: string
  }) => {
    const params = new URLSearchParams()

    if (options.status && options.status !== "all") {
      params.append("status", options.status)
    }
    if (options.sort) {
      params.append("sort", options.sort)
    }
    if (options.search) {
      params.append("search", options.search)
    }

    const queryString = params.toString()
    const url = `/api/tasks${queryString ? `?${queryString}` : ""}`

    return authenticatedFetch<Task[]>(url)
  },

  /**
   * Get paginated tasks
   */
  getTasksPaginated: (options: {
    status?: "all" | "pending" | "completed"
    sort?: "newest" | "oldest" | "title"
    page?: number
    size?: number
    search?: string
  }) => {
    const params = new URLSearchParams()

    if (options.status && options.status !== "all") {
      params.append("status", options.status)
    }
    if (options.sort) {
      params.append("sort", options.sort)
    }
    if (options.page) {
      params.append("page", String(options.page))
    }
    if (options.size) {
      params.append("size", String(options.size))
    }
    if (options.search) {
      params.append("search", options.search)
    }

    return authenticatedFetch<PaginatedResponse<Task>>("/api/tasks/paginated?" + params.toString())
  },
}

// Type definitions
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}
```

### 2. React Query Hooks

```typescript
// hooks/use-tasks.ts
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

/**
 * Hook to fetch tasks with optional filter
 */
export function useTasks(status: "all" | "pending" | "completed" = "all") {
  return useQuery({
    queryKey: ["tasks", status],
    queryFn: () => api.getTasks(status),
    staleTime: 30000, // 30 seconds
    refetchOnWindowFocus: true,
  })
}

/**
 * Hook for advanced filtering
 */
export function useTasksAdvanced(options: {
  status?: "all" | "pending" | "completed"
  sort?: "newest" | "oldest" | "title"
  search?: string
}) {
  return useQuery({
    queryKey: ["tasks", "advanced", options],
    queryFn: () => api.getTasksAdvanced(options),
    staleTime: 30000,
  })
}

/**
 * Hook for paginated tasks
 */
export function useTasksPaginated(options: {
  status?: "all" | "pending" | "completed"
  sort?: "newest" | "oldest" | "title"
  page?: number
  size?: number
  search?: string
}) {
  return useQuery({
    queryKey: ["tasks", "paginated", options],
    queryFn: () => api.getTasksPaginated(options),
    staleTime: 30000,
    keepPreviousData: true, // Keep old data while fetching new page
  })
}
```

### 3. Basic Task List Component

```typescript
// components/task-list.tsx
"use client"

import { useState } from "react"
import { useTasks } from "@/hooks/use-tasks"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"

export function TaskList() {
  const [statusFilter, setStatusFilter] = useState<"all" | "pending" | "completed">("all")

  const { data: tasks, isLoading, error } = useTasks(statusFilter)

  if (isLoading) {
    return <TaskListSkeleton />
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          {error instanceof Error ? error.message : "Failed to load tasks"}
        </AlertDescription>
      </Alert>
    )
  }

  const pendingCount = tasks?.filter((t) => !t.completed).length || 0
  const completedCount = tasks?.filter((t) => t.completed).length || 0

  return (
    <div className="space-y-4">
      {/* Filter Controls */}
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          <Badge variant="outline">
            Total: {tasks?.length || 0}
          </Badge>
          <Badge variant="outline">
            Pending: {pendingCount}
          </Badge>
          <Badge variant="outline">
            Completed: {completedCount}
          </Badge>
        </div>

        <Select
          value={statusFilter}
          onValueChange={(value) => setStatusFilter(value as any)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter tasks" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Task List */}
      {!tasks || tasks.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">
              {statusFilter === "all"
                ? "No tasks yet. Create your first task!"
                : `No ${statusFilter} tasks.`}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  )
}

function TaskCard({ task }: { task: Task }) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          <div className="flex-1">
            <h3
              className={`font-medium ${
                task.completed ? "line-through text-muted-foreground" : ""
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-muted-foreground mt-1">
                {task.description}
              </p>
            )}
            <div className="flex items-center gap-2 mt-2">
              {task.completed && (
                <Badge variant="success">Completed</Badge>
              )}
              <span className="text-xs text-muted-foreground">
                {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function TaskListSkeleton() {
  return (
    <div className="space-y-2">
      {[1, 2, 3].map((i) => (
        <Card key={i}>
          <CardContent className="pt-6">
            <Skeleton className="h-5 w-3/4 mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-3 w-1/4" />
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

### 4. Advanced Task List with Sorting and Search

```typescript
// components/task-list-advanced.tsx
"use client"

import { useState, useMemo } from "react"
import { useTasksAdvanced } from "@/hooks/use-tasks"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Search } from "lucide-react"
import { useDebounce } from "@/hooks/use-debounce"

export function TaskListAdvanced() {
  const [statusFilter, setStatusFilter] = useState<"all" | "pending" | "completed">("all")
  const [sortOrder, setSortOrder] = useState<"newest" | "oldest" | "title">("newest")
  const [searchQuery, setSearchQuery] = useState("")

  // Debounce search to avoid too many API calls
  const debouncedSearch = useDebounce(searchQuery, 300)

  const { data: tasks, isLoading, error } = useTasksAdvanced({
    status: statusFilter,
    sort: sortOrder,
    search: debouncedSearch || undefined,
  })

  // Calculate stats
  const stats = useMemo(() => {
    if (!tasks) return { total: 0, pending: 0, completed: 0 }
    return {
      total: tasks.length,
      pending: tasks.filter((t) => !t.completed).length,
      completed: tasks.filter((t) => t.completed).length,
    }
  }, [tasks])

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>

        {/* Status Filter */}
        <Select
          value={statusFilter}
          onValueChange={(value) => setStatusFilter(value as any)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks ({stats.total})</SelectItem>
            <SelectItem value="pending">Pending ({stats.pending})</SelectItem>
            <SelectItem value="completed">Completed ({stats.completed})</SelectItem>
          </SelectContent>
        </Select>

        {/* Sort */}
        <Select
          value={sortOrder}
          onValueChange={(value) => setSortOrder(value as any)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest First</SelectItem>
            <SelectItem value="oldest">Oldest First</SelectItem>
            <SelectItem value="title">Alphabetical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Task List */}
      {isLoading ? (
        <TaskListSkeleton />
      ) : error ? (
        <Alert variant="destructive">
          <AlertDescription>Failed to load tasks</AlertDescription>
        </Alert>
      ) : !tasks || tasks.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">
              {searchQuery ? "No tasks match your search." : "No tasks found."}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  )
}

// Custom debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}
```

### 5. Paginated Task List

```typescript
// components/task-list-paginated.tsx
"use client"

import { useState } from "react"
import { useTasksPaginated } from "@/hooks/use-tasks"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"

export function TaskListPaginated() {
  const [page, setPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState<"all" | "pending" | "completed">("all")
  const pageSize = 10

  const { data, isLoading, error, isPreviousData } = useTasksPaginated({
    status: statusFilter,
    page,
    size: pageSize,
  })

  if (isLoading && !isPreviousData) {
    return <TaskListSkeleton />
  }

  if (error) {
    return <Alert variant="destructive">Failed to load tasks</Alert>
  }

  return (
    <div className="space-y-4">
      {/* Task List */}
      <div className="space-y-2">
        {data?.items.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>

      {/* Pagination Controls */}
      {data && data.pages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {(page - 1) * pageSize + 1} to{" "}
            {Math.min(page * pageSize, data.total)} of {data.total} tasks
          </p>

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1 || isPreviousData}
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </Button>

            <div className="flex items-center gap-1">
              {Array.from({ length: data.pages }, (_, i) => i + 1).map((p) => (
                <Button
                  key={p}
                  variant={p === page ? "default" : "outline"}
                  size="sm"
                  onClick={() => setPage(p)}
                  disabled={isPreviousData}
                >
                  {p}
                </Button>
              ))}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.min(data.pages, p + 1))}
              disabled={page === data.pages || isPreviousData}
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
```

## Testing

### Backend Tests

```python
def test_list_tasks_all(client: TestClient, auth_headers: dict):
    """Test listing all tasks"""
    response = client.get("/api/tasks?status=all", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_tasks_pending(client: TestClient, auth_headers: dict):
    """Test filtering pending tasks"""
    response = client.get("/api/tasks?status=pending", headers=auth_headers)
    tasks = response.json()
    assert all(not task["completed"] for task in tasks)

def test_list_tasks_user_isolation(client: TestClient, auth_headers_user1: dict, auth_headers_user2: dict):
    """Test that users only see their own tasks"""
    # User 1 creates task
    client.post("/api/tasks", json={"title": "User 1 Task"}, headers=auth_headers_user1)

    # User 2 creates task
    client.post("/api/tasks", json={"title": "User 2 Task"}, headers=auth_headers_user2)

    # User 1 should only see their task
    response = client.get("/api/tasks", headers=auth_headers_user1)
    tasks = response.json()
    assert len([t for t in tasks if "User 2" in t["title"]]) == 0
```

## Key Takeaways

1. **Always filter by user_id** - Security critical
2. **Use query parameters** - For filters, sorting, pagination
3. **Debounce search inputs** - Reduce API calls
4. **Show loading states** - Better UX
5. **Cache effectively** - Use React Query's staleTime
6. **Keep previous data** - Use keepPreviousData for pagination
7. **Provide empty states** - Guide users when no data
