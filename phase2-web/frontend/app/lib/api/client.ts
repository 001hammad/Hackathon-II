/**
 * API Client for Phase II Todo Application
 *
 * Provides type-safe API methods with automatic JWT token attachment
 * and error handling.
 */

// Configuration
// With Better Auth cookie sessions, we call our Next.js BFF routes (same-origin)
// and let them validate the session + proxy to the FastAPI backend.
const API_BASE_URL = ""
const ENABLE_LOGGING = process.env.NODE_ENV === "development"


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


  // Build headers with proper typing
  const baseHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  }

  // Merge with existing headers if provided
  const existingHeaders = options?.headers
  if (existingHeaders) {
    if (Array.isArray(existingHeaders)) {
      existingHeaders.forEach(([key, value]) => {
        baseHeaders[key as string] = value
      })
    } else {
      Object.entries(existingHeaders).forEach(([key, value]) => {
        baseHeaders[key] = value as string
      })
    }
  }


  const headers: HeadersInit = baseHeaders

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    })

    // Handle authentication errors
    if (response.status === 401) {
      // Redirect to login if not already there
      if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
        window.location.href = "/login"
      }

      throw new APIError("Authentication required", 401)
    }

    // Handle permission errors
    if (response.status === 403) {
      throw new APIError("You don't have permission to perform this action", 403)
    }

    // Handle validation errors
    if (response.status === 400) {
      const error = await response.json().catch(() => ({ detail: "Invalid request" }))
      throw new APIError(
        error.detail || "Invalid request",
        400,
        error.details
      )
    }

    // Handle not found
    if (response.status === 404) {
      const error = await response.json().catch(() => ({ detail: "Resource not found" }))
      throw new APIError(error.detail || "Resource not found", 404)
    }

    // Handle conflict (e.g., duplicate email)
    if (response.status === 409) {
      const error = await response.json().catch(() => ({ detail: "Conflict" }))
      throw new APIError(error.detail || "Conflict", 409)
    }

    // Handle server errors
    if (response.status >= 500) {
      const error = await response.json().catch(() => ({ detail: "Server error" }))
      throw new APIError(
        error.detail || "Server error - please try again later",
        response.status
      )
    }

    // Handle other non-OK responses
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }))
      throw new APIError(error.detail || "Request failed", response.status)
    }

    // Handle empty responses (e.g., 204 No Content, DELETE responses)
    const contentType = response.headers.get("content-type")
    if (
      response.status === 204 ||
      !contentType?.includes("application/json")
    ) {
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
 * Type-safe API client
 * Provides methods for all API endpoints
 */
export const api = {
  // ==================== Task Endpoints ====================

  /**
   * Get all tasks for the authenticated user
   */
  getTasks: () => authenticatedFetch<{ tasks: Task[] }>("/api/tasks"),

  /**
   * Get a single task by ID
   */
  getTask: (id: number) => authenticatedFetch<Task>(`/api/tasks/${id}`),

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
  updateTask: (id: number, data: UpdateTaskInput) =>
    authenticatedFetch<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  /**
   * Delete a task
   */
  deleteTask: (id: number) =>
    authenticatedFetch<{ message: string }>(`/api/tasks/${id}`, {
      method: "DELETE",
    }),

  /**
   * Toggle task completion status
   */
  toggleTask: (id: number) =>
    authenticatedFetch<Task>(`/api/tasks/${id}/toggle`, {
      method: "PATCH",
    }),

}

// ==================== Type Definitions ====================

/**
 * Task model - matches backend SQLModel
 */
export interface Task {
  id: number
  user_id: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

/**
 * Input for creating a new task
 */
export interface CreateTaskInput {
  description: string
}

/**
 * Input for updating a task
 */
export interface UpdateTaskInput {
  description: string
}

/**
 * User model
 *
 * Note: Authentication is handled by Better Auth via httpOnly cookie sessions.
 * The FastAPI backend only needs a user identifier for task ownership.
 */
export interface User {
  id: string
  email: string
}
