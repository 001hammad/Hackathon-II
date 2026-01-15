/**
 * Frontend CRUD Hook Template
 *
 * This template provides complete React Query hooks for all CRUD operations
 * on the Task resource, following best practices for data fetching, caching,
 * and mutations.
 *
 * Usage:
 * 1. Copy this file to your Next.js project as `hooks/use-tasks.ts`
 * 2. Ensure API client is set up in `lib/api.ts`
 * 3. Ensure React Query is configured in your app
 * 4. Import and use hooks in your components
 *
 * Features:
 * - Type-safe hooks with TypeScript
 * - Automatic caching and refetching
 * - Optimistic updates
 * - Loading and error states
 * - Cache invalidation after mutations
 * - Toast notifications
 */

import { useQuery, useMutation, useQueryClient, UseQueryOptions } from "@tanstack/react-query"
import { api, Task, CreateTaskInput, UpdateTaskInput, APIError } from "@/lib/api"
import { toast } from "sonner"

// ==================== QUERY KEYS ====================

/**
 * Centralized query key factory
 * Makes it easier to invalidate related queries
 */
export const taskKeys = {
  all: ["tasks"] as const,
  lists: () => [...taskKeys.all, "list"] as const,
  list: (status?: string) => [...taskKeys.lists(), { status }] as const,
  details: () => [...taskKeys.all, "detail"] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
}

// ==================== READ OPERATIONS ====================

/**
 * Hook to fetch all tasks with optional status filter
 *
 * @param status - Filter by completion status (all, pending, completed)
 * @param options - Additional React Query options
 *
 * @example
 * ```tsx
 * function TaskList() {
 *   const { data: tasks, isLoading, error } = useTasks("pending")
 *
 *   if (isLoading) return <Skeleton />
 *   if (error) return <Error message={error.message} />
 *
 *   return <div>{tasks.map(task => <TaskCard key={task.id} task={task} />)}</div>
 * }
 * ```
 */
export function useTasks(
  status: "all" | "pending" | "completed" = "all",
  options?: Omit<UseQueryOptions<Task[], Error>, "queryKey" | "queryFn">
) {
  return useQuery<Task[], Error>({
    queryKey: taskKeys.list(status),
    queryFn: () => api.getTasks(status),
    staleTime: 30000, // Consider data fresh for 30 seconds
    ...options,
  })
}

/**
 * Hook to fetch a single task by ID
 *
 * @param id - Task UUID
 * @param options - Additional React Query options
 *
 * @example
 * ```tsx
 * function TaskDetail({ taskId }: { taskId: string }) {
 *   const { data: task, isLoading } = useTask(taskId)
 *
 *   if (isLoading) return <Skeleton />
 *   if (!task) return <NotFound />
 *
 *   return <div>{task.title}</div>
 * }
 * ```
 */
export function useTask(
  id: string,
  options?: Omit<UseQueryOptions<Task, Error>, "queryKey" | "queryFn">
) {
  return useQuery<Task, Error>({
    queryKey: taskKeys.detail(id),
    queryFn: () => api.getTask(id),
    enabled: !!id, // Only fetch if ID is provided
    staleTime: 30000,
    ...options,
  })
}

// ==================== CREATE OPERATION ====================

/**
 * Hook to create a new task
 *
 * Features:
 * - Invalidates task list cache after success
 * - Shows success/error toast notifications
 * - Returns mutation state (isLoading, error, etc.)
 *
 * @example
 * ```tsx
 * function CreateTaskForm() {
 *   const createTask = useCreateTask()
 *
 *   async function handleSubmit(data: CreateTaskInput) {
 *     try {
 *       const newTask = await createTask.mutateAsync(data)
 *       console.log("Created:", newTask)
 *     } catch (error) {
 *       console.error("Failed:", error)
 *     }
 *   }
 *
 *   return (
 *     <form onSubmit={handleSubmit}>
 *       <Button disabled={createTask.isPending}>
 *         {createTask.isPending ? "Creating..." : "Create Task"}
 *       </Button>
 *     </form>
 *   )
 * }
 * ```
 */
export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateTaskInput) => api.createTask(data),
    onSuccess: (newTask) => {
      // Invalidate all task lists to refetch with new task
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })

      // Optionally, optimistically add to cache
      // queryClient.setQueryData<Task[]>(taskKeys.list("all"), (old) => {
      //   return old ? [...old, newTask] : [newTask]
      // })

      toast.success("Task created successfully!")
    },
    onError: (error: Error) => {
      if (error instanceof APIError) {
        if (error.isValidationError()) {
          toast.error("Please check your input and try again")
        } else {
          toast.error(error.message)
        }
      } else {
        toast.error("Failed to create task")
      }
    },
  })
}

// ==================== UPDATE OPERATION ====================

/**
 * Hook to update an existing task
 *
 * Features:
 * - Invalidates affected caches (list + detail)
 * - Shows success/error toast notifications
 * - Supports partial updates
 *
 * @example
 * ```tsx
 * function EditTaskForm({ task }: { task: Task }) {
 *   const updateTask = useUpdateTask()
 *
 *   function handleSave(data: UpdateTaskInput) {
 *     updateTask.mutate({
 *       id: task.id,
 *       data: data,
 *     })
 *   }
 *
 *   return <form>...</form>
 * }
 * ```
 */
export function useUpdateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskInput }) =>
      api.updateTask(id, data),
    onSuccess: (updatedTask, variables) => {
      // Invalidate list cache
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })

      // Update specific task in cache
      queryClient.setQueryData(taskKeys.detail(variables.id), updatedTask)

      toast.success("Task updated successfully!")
    },
    onError: (error: Error) => {
      if (error instanceof APIError) {
        toast.error(error.message)
      } else {
        toast.error("Failed to update task")
      }
    },
  })
}

// ==================== TOGGLE COMPLETE OPERATION ====================

/**
 * Hook to toggle task completion status
 *
 * Features:
 * - Optimistic update (instant UI feedback)
 * - Automatic rollback on error
 * - Invalidates cache after success
 *
 * @example
 * ```tsx
 * function TaskCheckbox({ task }: { task: Task }) {
 *   const toggleComplete = useToggleTaskComplete()
 *
 *   return (
 *     <Checkbox
 *       checked={task.completed}
 *       onCheckedChange={() => toggleComplete.mutate(task.id)}
 *       disabled={toggleComplete.isPending}
 *     />
 *   )
 * }
 * ```
 */
export function useToggleTaskComplete() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => api.toggleTaskComplete(id),
    // Optimistic update
    onMutate: async (id) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() })
      await queryClient.cancelQueries({ queryKey: taskKeys.detail(id) })

      // Snapshot current values
      const previousLists = queryClient.getQueriesData({ queryKey: taskKeys.lists() })
      const previousTask = queryClient.getQueryData<Task>(taskKeys.detail(id))

      // Optimistically update task lists
      queryClient.setQueriesData<Task[]>({ queryKey: taskKeys.lists() }, (old) => {
        return old?.map((task) =>
          task.id === id ? { ...task, completed: !task.completed } : task
        )
      })

      // Optimistically update single task
      if (previousTask) {
        queryClient.setQueryData<Task>(taskKeys.detail(id), {
          ...previousTask,
          completed: !previousTask.completed,
        })
      }

      // Return context for rollback
      return { previousLists, previousTask }
    },
    onSuccess: (updatedTask, id) => {
      // Update with server response
      queryClient.setQueryData(taskKeys.detail(id), updatedTask)
    },
    onError: (error, id, context) => {
      // Rollback optimistic updates
      if (context?.previousLists) {
        context.previousLists.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }
      if (context?.previousTask) {
        queryClient.setQueryData(taskKeys.detail(id), context.previousTask)
      }

      toast.error("Failed to update task")
    },
    onSettled: () => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })
    },
  })
}

// ==================== DELETE OPERATION ====================

/**
 * Hook to delete a task
 *
 * Features:
 * - Optimistic update (instant removal from UI)
 * - Automatic rollback on error
 * - Shows success/error toast notifications
 *
 * @example
 * ```tsx
 * function DeleteTaskButton({ taskId }: { taskId: string }) {
 *   const deleteTask = useDeleteTask()
 *
 *   return (
 *     <AlertDialog>
 *       <AlertDialogTrigger asChild>
 *         <Button variant="destructive">Delete</Button>
 *       </AlertDialogTrigger>
 *       <AlertDialogContent>
 *         <AlertDialogTitle>Delete Task?</AlertDialogTitle>
 *         <AlertDialogDescription>This action cannot be undone.</AlertDialogDescription>
 *         <AlertDialogFooter>
 *           <AlertDialogCancel>Cancel</AlertDialogCancel>
 *           <AlertDialogAction onClick={() => deleteTask.mutate(taskId)}>
 *             Delete
 *           </AlertDialogAction>
 *         </AlertDialogFooter>
 *       </AlertDialogContent>
 *     </AlertDialog>
 *   )
 * }
 * ```
 */
export function useDeleteTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => api.deleteTask(id),
    // Optimistic update
    onMutate: async (id) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() })

      // Snapshot current values
      const previousLists = queryClient.getQueriesData({ queryKey: taskKeys.lists() })

      // Optimistically remove from lists
      queryClient.setQueriesData<Task[]>({ queryKey: taskKeys.lists() }, (old) => {
        return old?.filter((task) => task.id !== id)
      })

      // Remove from detail cache
      queryClient.removeQueries({ queryKey: taskKeys.detail(id) })

      return { previousLists }
    },
    onSuccess: () => {
      toast.success("Task deleted")
    },
    onError: (error, id, context) => {
      // Rollback optimistic updates
      if (context?.previousLists) {
        context.previousLists.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }

      toast.error("Failed to delete task")
    },
    onSettled: () => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })
    },
  })
}

// ==================== BULK OPERATIONS ====================

/**
 * Hook to delete multiple tasks at once
 *
 * @example
 * ```tsx
 * function BulkActions({ selectedIds }: { selectedIds: string[] }) {
 *   const bulkDelete = useBulkDeleteTasks()
 *
 *   return (
 *     <Button
 *       onClick={() => bulkDelete.mutate(selectedIds)}
 *       disabled={bulkDelete.isPending || selectedIds.length === 0}
 *     >
 *       Delete {selectedIds.length} Tasks
 *     </Button>
 *   )
 * }
 * ```
 */
export function useBulkDeleteTasks() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (ids: string[]) => {
      // Execute all deletes in parallel
      await Promise.all(ids.map((id) => api.deleteTask(id)))
    },
    onSuccess: (_, ids) => {
      // Invalidate all lists
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })

      // Remove from detail caches
      ids.forEach((id) => {
        queryClient.removeQueries({ queryKey: taskKeys.detail(id) })
      })

      toast.success(`Deleted ${ids.length} tasks`)
    },
    onError: () => {
      toast.error("Failed to delete tasks")
    },
  })
}

// ==================== PREFETCH UTILITIES ====================

/**
 * Prefetch tasks for better UX
 *
 * Use this to prefetch data before user navigates to a page
 *
 * @example
 * ```tsx
 * function TaskLink({ taskId }: { taskId: string }) {
 *   const prefetchTask = usePrefetchTask()
 *
 *   return (
 *     <Link
 *       href={`/tasks/${taskId}`}
 *       onMouseEnter={() => prefetchTask(taskId)}
 *     >
 *       View Task
 *     </Link>
 *   )
 * }
 * ```
 */
export function usePrefetchTask() {
  const queryClient = useQueryClient()

  return (id: string) => {
    queryClient.prefetchQuery({
      queryKey: taskKeys.detail(id),
      queryFn: () => api.getTask(id),
      staleTime: 30000,
    })
  }
}

/**
 * Prefetch task list
 */
export function usePrefetchTasks() {
  const queryClient = useQueryClient()

  return (status: "all" | "pending" | "completed" = "all") => {
    queryClient.prefetchQuery({
      queryKey: taskKeys.list(status),
      queryFn: () => api.getTasks(status),
      staleTime: 30000,
    })
  }
}

// ==================== UTILITY HOOKS ====================

/**
 * Hook to get task count by status
 *
 * @example
 * ```tsx
 * function TaskStats() {
 *   const { total, pending, completed } = useTaskCounts()
 *
 *   return (
 *     <div>
 *       <Badge>Total: {total}</Badge>
 *       <Badge>Pending: {pending}</Badge>
 *       <Badge>Completed: {completed}</Badge>
 *     </div>
 *   )
 * }
 * ```
 */
export function useTaskCounts() {
  const { data: tasks = [] } = useTasks("all")

  return {
    total: tasks.length,
    pending: tasks.filter((t) => !t.completed).length,
    completed: tasks.filter((t) => t.completed).length,
  }
}

/**
 * Hook to check if any tasks are loading
 *
 * Useful for showing a global loading indicator
 */
export function useIsAnyTaskLoading() {
  const queryClient = useQueryClient()

  const queries = queryClient.getQueriesData({ queryKey: taskKeys.all })
  return queries.some(([, data]) => data === undefined)
}

// ==================== USAGE EXAMPLES ====================

/**
 * Example: Task List Component
 *
 * ```tsx
 * "use client"
 *
 * import { useTasks, useToggleTaskComplete } from "@/hooks/use-tasks"
 * import { Checkbox } from "@/components/ui/checkbox"
 *
 * export function TaskList() {
 *   const { data: tasks, isLoading, error } = useTasks("all")
 *   const toggleComplete = useToggleTaskComplete()
 *
 *   if (isLoading) return <div>Loading...</div>
 *   if (error) return <div>Error: {error.message}</div>
 *
 *   return (
 *     <div className="space-y-2">
 *       {tasks?.map((task) => (
 *         <div key={task.id} className="flex items-center gap-2">
 *           <Checkbox
 *             checked={task.completed}
 *             onCheckedChange={() => toggleComplete.mutate(task.id)}
 *           />
 *           <span className={task.completed ? "line-through" : ""}>
 *             {task.title}
 *           </span>
 *         </div>
 *       ))}
 *     </div>
 *   )
 * }
 * ```
 */

/**
 * Example: Create Task Form
 *
 * ```tsx
 * "use client"
 *
 * import { useState } from "react"
 * import { useCreateTask } from "@/hooks/use-tasks"
 * import { Button } from "@/components/ui/button"
 * import { Input } from "@/components/ui/input"
 *
 * export function CreateTaskForm() {
 *   const [title, setTitle] = useState("")
 *   const createTask = useCreateTask()
 *
 *   async function handleSubmit(e: React.FormEvent) {
 *     e.preventDefault()
 *     if (!title.trim()) return
 *
 *     await createTask.mutateAsync({ title })
 *     setTitle("")
 *   }
 *
 *   return (
 *     <form onSubmit={handleSubmit} className="flex gap-2">
 *       <Input
 *         value={title}
 *         onChange={(e) => setTitle(e.target.value)}
 *         placeholder="New task..."
 *         disabled={createTask.isPending}
 *       />
 *       <Button type="submit" disabled={createTask.isPending || !title.trim()}>
 *         {createTask.isPending ? "Adding..." : "Add"}
 *       </Button>
 *     </form>
 *   )
 * }
 * ```
 */
