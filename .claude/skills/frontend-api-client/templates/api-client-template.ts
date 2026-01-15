/**
 * API Client Template
 *
 * This template provides a complete, production-ready API client for Next.js
 * that automatically attaches JWT tokens using Better Auth.
 *
 * Usage:
 * 1. Copy this file to your project as `lib/api.ts`
 * 2. Update the type definitions to match your backend models
 * 3. Add/remove API methods as needed for your endpoints
 * 4. Configure environment variables
 */

import { authClient } from "better-auth/client"
import { redirect } from "next/navigation"

// Initialize Better Auth client
const client = authClient()

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
const ENABLE_LOGGING = process.env.NODE_ENV === "development"

/**
 * Generic authenticated fetch wrapper
 * Automatically attaches JWT token and handles common error cases
 */
async function authenticatedFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  if (ENABLE_LOGGING) {
    console.log(`[API] ${options?.method || "GET"} ${url}`)
  }

  try {
    const response = await client.fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    })

    // Handle authentication errors
    if (response.status === 401) {
      console.error("[API] Unauthorized - redirecting to login")
      redirect("/login")
    }

    // Handle permission errors
    if (response.status === 403) {
      throw new APIError("You don't have permission to perform this action", 403)
    }

    // Handle validation errors
    if (response.status === 400) {
      const error = await response.json()
      throw new APIError(error.message || "Invalid request", 400, error.details)
    }

    // Handle not found
    if (response.status === 404) {
      throw new APIError("Resource not found", 404)
    }

    // Handle server errors
    if (response.status >= 500) {
      throw new APIError("Server error - please try again later", response.status)
    }

    // Handle other non-OK responses
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: "Request failed" }))
      throw new APIError(error.message || "Request failed", response.status)
    }

    // Handle empty responses (e.g., 204 No Content)
    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return undefined as T
    }

    const data = await response.json()

    if (ENABLE_LOGGING) {
      console.log(`[API] Response:`, data)
    }

    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw error
    }

    console.error("[API] Request failed:", error)
    throw new APIError(
      error instanceof Error ? error.message : "Network error",
      0
    )
  }
}

/**
 * Custom error class for API errors
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: Record<string, string[]>
  ) {
    super(message)
    this.name = "APIError"
  }

  /**
   * Check if error is a validation error with field details
   */
  isValidationError(): boolean {
    return this.status === 400 && !!this.details
  }

  /**
   * Get validation errors for a specific field
   */
  getFieldErrors(field: string): string[] {
    return this.details?.[field] || []
  }
}

/**
 * Type-safe API client
 * Add your endpoint methods here
 */
export const api = {
  // ==================== Task Endpoints ====================

  /**
   * Get all tasks for the authenticated user
   */
  getTasks: () => authenticatedFetch<Task[]>("/api/tasks"),

  /**
   * Get a single task by ID
   */
  getTask: (id: string) => authenticatedFetch<Task>(`/api/tasks/${id}`),

  /**
   * Create a new task
   */
  createTask: (data: CreateTaskInput) =>
    authenticatedFetch<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  /**
   * Update an existing task
   */
  updateTask: (id: string, data: UpdateTaskInput) =>
    authenticatedFetch<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  /**
   * Delete a task
   */
  deleteTask: (id: string) =>
    authenticatedFetch<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    }),

  /**
   * Toggle task completion status
   */
  toggleTaskComplete: (id: string) =>
    authenticatedFetch<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    }),

  // ==================== User Endpoints ====================

  /**
   * Get current user profile
   */
  getCurrentUser: () => authenticatedFetch<User>("/api/users/me"),

  /**
   * Update user profile
   */
  updateUserProfile: (data: UpdateUserInput) =>
    authenticatedFetch<User>("/api/users/me", {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // ==================== Add More Endpoints Here ====================
}

// ==================== Type Definitions ====================

/**
 * Task model - matches backend SQLModel
 */
export interface Task {
  id: string
  title: string
  description?: string | null
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

/**
 * Input for creating a new task
 */
export interface CreateTaskInput {
  title: string
  description?: string
}

/**
 * Input for updating a task
 */
export interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
}

/**
 * User model
 */
export interface User {
  id: string
  email: string
  name?: string | null
  created_at: string
}

/**
 * Input for updating user profile
 */
export interface UpdateUserInput {
  name?: string
  email?: string
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

/**
 * Generic API error response
 */
export interface ErrorResponse {
  message: string
  details?: Record<string, string[]>
}

// ==================== React Query Hooks (Optional) ====================

/**
 * Example React Query hooks for tasks
 * Uncomment and use with @tanstack/react-query
 */

/*
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"

export function useTasks() {
  return useQuery({
    queryKey: ["tasks"],
    queryFn: api.getTasks,
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
*/

// ==================== Usage Example ====================

/*
// In a client component:
"use client"

import { api } from "@/lib/api"
import { useState, useEffect } from "react"

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTasks() {
      try {
        const data = await api.getTasks()
        setTasks(data)
      } catch (err) {
        if (err instanceof APIError) {
          setError(err.message)
        } else {
          setError("Failed to load tasks")
        }
      } finally {
        setLoading(false)
      }
    }

    loadTasks()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <ul>
      {tasks.map((task) => (
        <li key={task.id}>{task.title}</li>
      ))}
    </ul>
  )
}
*/
