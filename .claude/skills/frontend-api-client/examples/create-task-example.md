# Create Task Example

This example demonstrates how to create, update, and delete tasks using the authenticated API client with proper form handling and validation.

## Basic Create Task Form

```typescript
"use client"

import { useState } from "react"
import { api, APIError, CreateTaskInput } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { toast } from "sonner"

export function CreateTaskForm() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      const taskData: CreateTaskInput = {
        title: title.trim(),
        description: description.trim() || undefined,
      }

      const newTask = await api.createTask(taskData)

      // Success!
      toast.success("Task created successfully!")

      // Reset form
      setTitle("")
      setDescription("")

      // Optional: Trigger refetch or navigate
      // router.push(`/tasks/${newTask.id}`)

    } catch (err) {
      if (err instanceof APIError) {
        if (err.isValidationError()) {
          // Handle field-specific validation errors
          const titleErrors = err.getFieldErrors("title")
          if (titleErrors.length > 0) {
            setError(titleErrors[0])
          } else {
            setError(err.message)
          }
        } else {
          setError(err.message)
        }
      } else {
        setError("Failed to create task")
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create New Task</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title"
              required
              disabled={isSubmitting}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter task description (optional)"
              rows={4}
              disabled={isSubmitting}
            />
          </div>

          <Button type="submit" disabled={isSubmitting || !title.trim()}>
            {isSubmitting ? "Creating..." : "Create Task"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```

## With React Query Mutation

```typescript
"use client"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api, CreateTaskInput } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import { useState } from "react"

export function CreateTaskForm() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const queryClient = useQueryClient()

  const createTaskMutation = useMutation({
    mutationFn: api.createTask,
    onSuccess: (newTask) => {
      // Invalidate and refetch tasks list
      queryClient.invalidateQueries({ queryKey: ["tasks"] })

      // Or optimistically add to cache
      // queryClient.setQueryData(["tasks"], (old: Task[]) => [...old, newTask])

      toast.success("Task created successfully!")

      // Reset form
      setTitle("")
      setDescription("")
    },
    onError: (error) => {
      toast.error(error instanceof Error ? error.message : "Failed to create task")
    },
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    const taskData: CreateTaskInput = {
      title: title.trim(),
      description: description.trim() || undefined,
    }

    createTaskMutation.mutate(taskData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
          disabled={createTaskMutation.isPending}
        />
      </div>

      <div className="space-y-2">
        <Textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
          disabled={createTaskMutation.isPending}
        />
      </div>

      <Button
        type="submit"
        disabled={createTaskMutation.isPending || !title.trim()}
      >
        {createTaskMutation.isPending ? "Creating..." : "Create Task"}
      </Button>
    </form>
  )
}
```

## With React Hook Form

```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api, CreateTaskInput } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"

// Validation schema
const createTaskSchema = z.object({
  title: z.string().min(1, "Title is required").max(200, "Title too long"),
  description: z.string().max(1000, "Description too long").optional(),
})

type CreateTaskFormValues = z.infer<typeof createTaskSchema>

export function CreateTaskForm() {
  const queryClient = useQueryClient()

  const form = useForm<CreateTaskFormValues>({
    resolver: zodResolver(createTaskSchema),
    defaultValues: {
      title: "",
      description: "",
    },
  })

  const createTaskMutation = useMutation({
    mutationFn: api.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      toast.success("Task created!")
      form.reset()
    },
    onError: (error) => {
      toast.error(error instanceof Error ? error.message : "Failed to create task")
    },
  })

  function onSubmit(data: CreateTaskFormValues) {
    const taskData: CreateTaskInput = {
      title: data.title.trim(),
      description: data.description?.trim() || undefined,
    }

    createTaskMutation.mutate(taskData)
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
                  disabled={createTaskMutation.isPending}
                />
              </FormControl>
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
                  placeholder="Enter task description"
                  rows={4}
                  {...field}
                  disabled={createTaskMutation.isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={createTaskMutation.isPending}>
          {createTaskMutation.isPending ? "Creating..." : "Create Task"}
        </Button>
      </form>
    </Form>
  )
}
```

## Update Task Example

```typescript
"use client"

import { useState, useEffect } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api, UpdateTaskInput, Task } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"

interface UpdateTaskFormProps {
  taskId: string
  onSuccess?: () => void
}

export function UpdateTaskForm({ taskId, onSuccess }: UpdateTaskFormProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const queryClient = useQueryClient()

  // Fetch existing task data
  const { data: task, isLoading } = useQuery({
    queryKey: ["tasks", taskId],
    queryFn: () => api.getTask(taskId),
  })

  // Populate form when task data loads
  useEffect(() => {
    if (task) {
      setTitle(task.title)
      setDescription(task.description || "")
    }
  }, [task])

  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskInput }) =>
      api.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      queryClient.invalidateQueries({ queryKey: ["tasks", taskId] })
      toast.success("Task updated!")
      onSuccess?.()
    },
    onError: (error) => {
      toast.error(error instanceof Error ? error.message : "Failed to update task")
    },
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    const updateData: UpdateTaskInput = {
      title: title.trim(),
      description: description.trim() || undefined,
    }

    updateTaskMutation.mutate({ id: taskId, data: updateData })
  }

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
          disabled={updateTaskMutation.isPending}
        />
      </div>

      <div className="space-y-2">
        <Textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
          disabled={updateTaskMutation.isPending}
        />
      </div>

      <div className="flex gap-2">
        <Button
          type="submit"
          disabled={updateTaskMutation.isPending || !title.trim()}
        >
          {updateTaskMutation.isPending ? "Saving..." : "Save Changes"}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onSuccess}
          disabled={updateTaskMutation.isPending}
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
```

## Delete Task Example

```typescript
"use client"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { toast } from "sonner"
import { Trash2 } from "lucide-react"

interface DeleteTaskButtonProps {
  taskId: string
  taskTitle: string
}

export function DeleteTaskButton({ taskId, taskTitle }: DeleteTaskButtonProps) {
  const queryClient = useQueryClient()

  const deleteTaskMutation = useMutation({
    mutationFn: api.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      toast.success("Task deleted")
    },
    onError: (error) => {
      toast.error(error instanceof Error ? error.message : "Failed to delete task")
    },
  })

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="destructive" size="icon" disabled={deleteTaskMutation.isPending}>
          <Trash2 className="h-4 w-4" />
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Task</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{taskTitle}"? This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={() => deleteTaskMutation.mutate(taskId)}
            disabled={deleteTaskMutation.isPending}
          >
            {deleteTaskMutation.isPending ? "Deleting..." : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

## Toggle Complete Example

```typescript
"use client"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api, Task } from "@/lib/api"
import { Checkbox } from "@/components/ui/checkbox"
import { toast } from "sonner"

interface TaskCheckboxProps {
  task: Task
}

export function TaskCheckbox({ task }: TaskCheckboxProps) {
  const queryClient = useQueryClient()

  const toggleMutation = useMutation({
    mutationFn: api.toggleTaskComplete,
    onMutate: async (taskId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["tasks"] })

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(["tasks"])

      // Optimistically update
      queryClient.setQueryData<Task[]>(["tasks"], (old) =>
        old?.map((t) =>
          t.id === taskId ? { ...t, completed: !t.completed } : t
        )
      )

      return { previousTasks }
    },
    onError: (error, variables, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks)
      }
      toast.error("Failed to update task")
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })

  return (
    <Checkbox
      checked={task.completed}
      onCheckedChange={() => toggleMutation.mutate(task.id)}
      disabled={toggleMutation.isPending}
    />
  )
}
```

## Batch Operations Example

```typescript
"use client"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"

export function BatchOperations({ taskIds }: { taskIds: string[] }) {
  const queryClient = useQueryClient()

  const deleteAllMutation = useMutation({
    mutationFn: async (ids: string[]) => {
      // Execute all deletes in parallel
      await Promise.all(ids.map((id) => api.deleteTask(id)))
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      toast.success(`Deleted ${taskIds.length} tasks`)
    },
    onError: () => {
      toast.error("Failed to delete tasks")
    },
  })

  return (
    <Button
      variant="destructive"
      onClick={() => deleteAllMutation.mutate(taskIds)}
      disabled={deleteAllMutation.isPending || taskIds.length === 0}
    >
      {deleteAllMutation.isPending
        ? "Deleting..."
        : `Delete ${taskIds.length} Tasks`}
    </Button>
  )
}
```

## Key Points

1. **Always use `api.createTask()`, `api.updateTask()`, etc.** - Never make direct fetch calls
2. **Handle validation errors** - Use `APIError.isValidationError()` and `getFieldErrors()`
3. **Provide loading states** - Disable buttons and show feedback during mutations
4. **Show success/error messages** - Use toast notifications for user feedback
5. **Invalidate queries** - Update cache after mutations with React Query
6. **Optimistic updates** - Update UI immediately, rollback on error
7. **Form validation** - Use Zod and React Hook Form for client-side validation
8. **Confirmation dialogs** - Use AlertDialog for destructive actions

## Common Patterns

### Auto-save on Change
```typescript
const debouncedUpdate = useDebouncedCallback(
  (id: string, data: UpdateTaskInput) => {
    updateTaskMutation.mutate({ id, data })
  },
  1000
)

<Input
  value={title}
  onChange={(e) => {
    setTitle(e.target.value)
    debouncedUpdate(taskId, { title: e.target.value })
  }}
/>
```

### Inline Edit Mode
```typescript
const [isEditing, setIsEditing] = useState(false)

{isEditing ? (
  <UpdateTaskForm taskId={task.id} onSuccess={() => setIsEditing(false)} />
) : (
  <div onClick={() => setIsEditing(true)}>{task.title}</div>
)}
```
