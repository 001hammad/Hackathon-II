---
name: frontend-api-client
description: Expert in attaching JWT to all API requests from frontend using Better Auth client. Use PROACTIVELY whenever making API calls from Next.js to FastAPI backend in Phase 2.
---

# API JWT Client Expert

## Overview

This skill ensures all API calls from the Next.js frontend to the FastAPI backend include proper JWT authentication in the `Authorization: Bearer <token>` header. It provides patterns and utilities for creating a type-safe, authenticated API client using Better Auth.

## Core Responsibilities

- Automatic JWT token attachment to all API requests
- Type-safe API client interface
- Error handling and authentication flow
- Centralized API configuration
- Redirect to login on 401 Unauthorized responses

## Architecture

### Authentication Flow
1. User authenticates via Better Auth (handled by frontend-auth skill)
2. Better Auth stores JWT token in secure storage
3. API client automatically attaches token to all requests
4. Backend validates JWT and extracts user context
5. On 401 errors, redirect user to login page

### Core Pattern

All API calls must go through a centralized `api` object that uses Better Auth's client to automatically attach JWT tokens:

```typescript
import { authClient } from "better-auth/client"

const client = authClient()

export const api = {
  getTasks: () => client.fetch("/api/tasks"),
  createTask: (data) => client.fetch("/api/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  }),
  // ... more methods
}
```

## Implementation Guide

### 1. Create API Client (lib/api.ts)

Create a centralized API client module that wraps Better Auth's authenticated fetch:

```typescript
import { authClient } from "better-auth/client"
import { redirect } from "next/navigation"

const client = authClient()

// Base configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Generic fetch wrapper with error handling
async function authenticatedFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await client.fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    })

    if (response.status === 401) {
      // Redirect to login on authentication failure
      redirect("/login")
    }

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || "API request failed")
    }

    return response.json()
  } catch (error) {
    console.error("API Error:", error)
    throw error
  }
}

// Type-safe API methods
export const api = {
  // Task endpoints
  getTasks: () => authenticatedFetch<Task[]>("/api/tasks"),

  getTask: (id: string) => authenticatedFetch<Task>(`/api/tasks/${id}`),

  createTask: (data: CreateTaskInput) =>
    authenticatedFetch<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateTask: (id: string, data: UpdateTaskInput) =>
    authenticatedFetch<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  deleteTask: (id: string) =>
    authenticatedFetch<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    }),

  toggleTaskComplete: (id: string) =>
    authenticatedFetch<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    }),
}

// Type definitions
interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

interface CreateTaskInput {
  title: string
  description?: string
}

interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
}
```

### 2. Usage in Components

```typescript
"use client"

import { api } from "@/lib/api"
import { useEffect, useState } from "react"

export function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadTasks() {
      try {
        const data = await api.getTasks()
        setTasks(data)
      } catch (error) {
        console.error("Failed to load tasks:", error)
      } finally {
        setLoading(false)
      }
    }

    loadTasks()
  }, [])

  // ... rest of component
}
```

### 3. Usage in Server Components

For server components, use Better Auth's server-side session:

```typescript
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export default async function TasksPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  })

  if (!session) {
    redirect("/login")
  }

  // Make authenticated request to backend
  const response = await fetch(`${process.env.API_URL}/api/tasks`, {
    headers: {
      "Authorization": `Bearer ${session.token}`,
      "Content-Type": "application/json"
    }
  })

  const tasks = await response.json()

  return <TaskList initialTasks={tasks} />
}
```

## Best Practices

### 1. Never Manually Handle Tokens
❌ **DON'T:**
```typescript
const token = localStorage.getItem("token")
fetch("/api/tasks", {
  headers: { Authorization: `Bearer ${token}` }
})
```

✅ **DO:**
```typescript
api.getTasks() // Token automatically attached
```

### 2. Use Type-Safe API Methods
❌ **DON'T:**
```typescript
client.fetch("/api/tasks") // No type safety
```

✅ **DO:**
```typescript
api.getTasks() // Returns Task[] with full type safety
```

### 3. Handle Errors Gracefully
```typescript
try {
  const tasks = await api.getTasks()
  setTasks(tasks)
} catch (error) {
  if (error instanceof Error) {
    toast.error(error.message)
  }
}
```

### 4. Use React Query for Data Fetching
```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useTasks() {
  return useQuery({
    queryKey: ["tasks"],
    queryFn: api.getTasks,
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
```

### 5. Centralize All API Calls
All API endpoints should be defined in `lib/api.ts`. Never make direct fetch calls to the backend from components.

## Error Handling

### 401 Unauthorized
Automatically redirects to `/login` page. User must re-authenticate.

### 403 Forbidden
User is authenticated but lacks permission. Show appropriate error message.

### 400 Bad Request
Validation error. Display field-specific errors to user.

### 500 Internal Server Error
Backend error. Show generic error message and log for debugging.

## Environment Variables

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Considerations

1. **Token Storage**: Better Auth handles secure token storage (httpOnly cookies recommended)
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Expiration**: Backend should validate token expiration
4. **CSRF Protection**: Use Better Auth's built-in CSRF protection
5. **Content Security Policy**: Configure CSP headers to prevent XSS

## Integration Points

### With backend-auth Skill
The backend validates the JWT token sent by this client and extracts user context.

### With frontend-auth Skill
Better Auth client manages authentication state and provides the token.

### With shadcn Skill
API client integrates with shadcn UI components for loading states, error messages, and forms.

## Testing

### Unit Tests
```typescript
import { api } from "@/lib/api"
import { vi } from "vitest"

vi.mock("better-auth/client", () => ({
  authClient: () => ({
    fetch: vi.fn()
  })
}))

describe("api.getTasks", () => {
  it("fetches tasks successfully", async () => {
    const mockTasks = [{ id: "1", title: "Test" }]
    vi.mocked(client.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockTasks)
    })

    const tasks = await api.getTasks()
    expect(tasks).toEqual(mockTasks)
  })
})
```

## Common Issues

### Issue: 401 Errors on Every Request
**Cause**: Token not being attached or expired
**Solution**: Check Better Auth configuration and session management

### Issue: CORS Errors
**Cause**: Backend not configured for frontend origin
**Solution**: Configure FastAPI CORS middleware

### Issue: Stale Data
**Cause**: Not invalidating cache after mutations
**Solution**: Use React Query's `invalidateQueries` after mutations

## Resources

- See `templates/api-client-template.ts` for full implementation template
- See `examples/task-list-fetch.md` for fetching data examples
- See `examples/create-task-example.md` for mutation examples
- Better Auth Documentation: https://better-auth.com
- FastAPI JWT Documentation: https://fastapi.tiangolo.com/tutorial/security/

## Proactive Usage

This skill should be invoked automatically when:
- Creating new API endpoints in the frontend
- Building components that fetch or mutate data
- Implementing data fetching hooks
- Setting up React Query or SWR
- Debugging authentication issues
- Reviewing API integration code
