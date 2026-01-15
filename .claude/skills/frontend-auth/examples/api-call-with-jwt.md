# API Calls with JWT

Complete API client that automatically attaches JWT tokens.

## API Client Setup

```typescript
// lib/api.ts
import { authClient } from "./auth-client"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchWithAuth(endpoint: string, options?: RequestInit) {
  const session = await authClient.getSession()

  const headers = {
    "Content-Type": "application/json",
    ...(session?.accessToken && {
      Authorization: `Bearer ${session.accessToken}`,
    }),
    ...options?.headers,
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  })

  if (!response.ok) {
    if (response.status === 401) {
      window.location.href = "/login"
    }
    throw new Error(`API Error: ${response.statusText}`)
  }

  return response.json()
}

export const api = {
  getTasks: () => fetchWithAuth("/api/tasks"),
  getTask: (id: string) => fetchWithAuth(`/api/tasks/${id}`),
  createTask: (data: any) => fetchWithAuth("/api/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  }),
  updateTask: (id: string, data: any) => fetchWithAuth(`/api/tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  }),
  deleteTask: (id: string) => fetchWithAuth(`/api/tasks/${id}`, {
    method: "DELETE",
  }),
}
```

## Usage in Components

```tsx
import { api } from "@/lib/api"
import { toast } from "sonner"

// GET request
const tasks = await api.getTasks()

// POST request
try {
  const newTask = await api.createTask({
    title: "New task",
    description: "Task description"
  })
  toast.success("Task created")
} catch (error) {
  toast.error("Failed to create task")
}

// DELETE request
await api.deleteTask(taskId)
```
