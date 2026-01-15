# Update Task Example - Complete Implementation

This document provides complete implementations for updating tasks, including full updates (PUT), partial updates, toggle completion (PATCH), and delete operations with optimistic updates.

## Architecture Overview

```
┌─────────────────┐
│  EditTaskForm   │
│  (Component)    │
└────────┬────────┘
         │
         │ 1. User edits task
         ▼
┌─────────────────┐
│  useUpdateTask()│ ← React Query Mutation
└────────┬────────┘
         │
         │ 2. api.updateTask(id, data)
         ▼
┌─────────────────┐
│  PUT /api/tasks │
│  /{id}          │ ← API Request + JWT
└────────┬────────┘
         │
         │ 3. Verify ownership & update
         ▼
┌─────────────────┐
│  update_task()  │ ← FastAPI Route
└────────┬────────┘
         │
         │ 4. Return updated task
         ▼
┌─────────────────┐
│  PostgreSQL     │
└─────────────────┘
```

## Backend Implementation

### 1. Update Task Route (PUT)

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime

from app.models.task import Task, TaskUpdate
from app.models.user import User
from app.api.dependencies import get_current_user, get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.put(
    "/{task_id}",
    response_model=Task,
    summary="Update a task",
    description="Update a task's title, description, or completion status",
    responses={
        200: {
            "description": "Task updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Updated Title",
                        "description": "Updated description",
                        "completed": True,
                        "user_id": "123e4567-e89b-12d3-a456-426614174000",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T11:00:00Z"
                    }
                }
            }
        },
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"}
    }
)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Update a task.

    Only provided fields will be updated (partial update supported).

    **Path Parameters:**
    - `task_id`: Task UUID

    **Request Body:**
    - `title` (optional): New task title
    - `description` (optional): New task description
    - `completed` (optional): New completion status

    **Authentication:**
    - Requires valid JWT token
    - User must own the task

    **Example:**
    ```json
    {
        "title": "Updated Title",
        "completed": true
    }
    ```
    """
    # Fetch task from database
    task = db.get(Task, task_id)

    # Check if task exists and belongs to current user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        # Strip whitespace from string fields
        if field in ["title", "description"] and isinstance(value, str):
            value = value.strip() if value else None
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Save changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### 2. Toggle Complete Route (PATCH)

```python
@router.patch(
    "/{task_id}/complete",
    response_model=Task,
    summary="Toggle task completion",
    description="Toggle the completion status of a task"
)
async def toggle_task_complete(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Toggle task completion status.

    This is a convenience endpoint for toggling the completed field
    without sending a full update request.

    **Path Parameters:**
    - `task_id`: Task UUID

    **Authentication:**
    - Requires valid JWT token
    - User must own the task

    **Example:**
    ```
    PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000/complete
    ```
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check ownership
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    # Save changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### 3. Delete Task Route

```python
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task"
)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a task permanently.

    **Path Parameters:**
    - `task_id`: Task UUID

    **Authentication:**
    - Requires valid JWT token
    - User must own the task

    **Returns:**
    - 204 No Content on success
    - 404 if task not found or not owned by user
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check ownership
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    db.delete(task)
    db.commit()

    return None
```

## Frontend Implementation

### 1. Update Task Form Component

```typescript
// components/edit-task-form.tsx
"use client"

import { useState, useEffect } from "react"
import { useUpdateTask, useTask } from "@/hooks/use-tasks"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import { toast } from "sonner"

interface EditTaskFormProps {
  taskId: string
  onSuccess?: () => void
  onCancel?: () => void
}

export function EditTaskForm({ taskId, onSuccess, onCancel }: EditTaskFormProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  // Fetch existing task data
  const { data: task, isLoading: isLoadingTask } = useTask(taskId)

  // Update mutation
  const updateTask = useUpdateTask()

  // Populate form when task data loads
  useEffect(() => {
    if (task) {
      setTitle(task.title)
      setDescription(task.description || "")
    }
  }, [task])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!title.trim()) {
      toast.error("Title is required")
      return
    }

    try {
      await updateTask.mutateAsync({
        id: taskId,
        data: {
          title: title.trim(),
          description: description.trim() || undefined,
        },
      })

      onSuccess?.()
    } catch (error) {
      // Error handled by mutation
    }
  }

  if (isLoadingTask) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Edit Task</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Task title"
              required
              disabled={updateTask.isPending}
              maxLength={200}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              rows={4}
              disabled={updateTask.isPending}
              maxLength={1000}
            />
          </div>

          <div className="flex gap-2">
            <Button
              type="submit"
              disabled={updateTask.isPending || !title.trim()}
            >
              {updateTask.isPending && (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              )}
              {updateTask.isPending ? "Saving..." : "Save Changes"}
            </Button>

            {onCancel && (
              <Button
                type="button"
                variant="outline"
                onClick={onCancel}
                disabled={updateTask.isPending}
              >
                Cancel
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
```

### 2. Inline Edit Component

```typescript
// components/task-item-editable.tsx
"use client"

import { useState } from "react"
import { useUpdateTask, useDeleteTask, useToggleTaskComplete } from "@/hooks/use-tasks"
import { Task } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Card, CardContent } from "@/components/ui/card"
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
import { Edit2, Trash2, Check, X } from "lucide-react"

interface TaskItemEditableProps {
  task: Task
}

export function TaskItemEditable({ task }: TaskItemEditableProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedTitle, setEditedTitle] = useState(task.title)

  const updateTask = useUpdateTask()
  const deleteTask = useDeleteTask()
  const toggleComplete = useToggleTaskComplete()

  async function handleSave() {
    if (!editedTitle.trim()) return

    try {
      await updateTask.mutateAsync({
        id: task.id,
        data: { title: editedTitle.trim() },
      })
      setIsEditing(false)
    } catch (error) {
      // Error handled by mutation
    }
  }

  function handleCancel() {
    setEditedTitle(task.title)
    setIsEditing(false)
  }

  function handleDelete() {
    deleteTask.mutate(task.id)
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center gap-3">
          {/* Checkbox */}
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => toggleComplete.mutate(task.id)}
            disabled={toggleComplete.isPending}
          />

          {/* Title (editable) */}
          <div className="flex-1">
            {isEditing ? (
              <div className="flex gap-2">
                <Input
                  value={editedTitle}
                  onChange={(e) => setEditedTitle(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSave()
                    if (e.key === "Escape") handleCancel()
                  }}
                  autoFocus
                  disabled={updateTask.isPending}
                />
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={handleSave}
                  disabled={updateTask.isPending || !editedTitle.trim()}
                >
                  <Check className="h-4 w-4" />
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={handleCancel}
                  disabled={updateTask.isPending}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ) : (
              <span
                className={`${
                  task.completed ? "line-through text-muted-foreground" : ""
                }`}
              >
                {task.title}
              </span>
            )}
          </div>

          {/* Actions */}
          {!isEditing && (
            <div className="flex gap-2">
              <Button
                size="icon"
                variant="ghost"
                onClick={() => setIsEditing(true)}
              >
                <Edit2 className="h-4 w-4" />
              </Button>

              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button size="icon" variant="ghost">
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete Task</AlertDialogTitle>
                    <AlertDialogDescription>
                      Are you sure you want to delete "{task.title}"? This
                      action cannot be undone.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction
                      onClick={handleDelete}
                      className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                    >
                      Delete
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
```

### 3. Toggle Complete Checkbox

```typescript
// components/task-checkbox.tsx
"use client"

import { useToggleTaskComplete } from "@/hooks/use-tasks"
import { Task } from "@/lib/api"
import { Checkbox } from "@/components/ui/checkbox"

interface TaskCheckboxProps {
  task: Task
}

export function TaskCheckbox({ task }: TaskCheckboxProps) {
  const toggleComplete = useToggleTaskComplete()

  return (
    <Checkbox
      checked={task.completed}
      onCheckedChange={() => toggleComplete.mutate(task.id)}
      disabled={toggleComplete.isPending}
      aria-label={`Mark "${task.title}" as ${task.completed ? "incomplete" : "complete"}`}
    />
  )
}
```

### 4. Delete Task Button with Confirmation

```typescript
// components/delete-task-button.tsx
"use client"

import { useDeleteTask } from "@/hooks/use-tasks"
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
import { Trash2 } from "lucide-react"

interface DeleteTaskButtonProps {
  taskId: string
  taskTitle: string
  onSuccess?: () => void
}

export function DeleteTaskButton({
  taskId,
  taskTitle,
  onSuccess,
}: DeleteTaskButtonProps) {
  const deleteTask = useDeleteTask()

  async function handleDelete() {
    try {
      await deleteTask.mutateAsync(taskId)
      onSuccess?.()
    } catch (error) {
      // Error handled by mutation
    }
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button
          variant="destructive"
          size="icon"
          disabled={deleteTask.isPending}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Task</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{taskTitle}"? This action cannot be
            undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={deleteTask.isPending}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            {deleteTask.isPending ? "Deleting..." : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

### 5. Optimistic Update Patterns

```typescript
// hooks/use-tasks.ts (enhanced with optimistic updates)
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api, Task } from "@/lib/api"
import { toast } from "sonner"

/**
 * Update task with optimistic update
 */
export function useUpdateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskInput }) =>
      api.updateTask(id, data),

    // Optimistic update
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["tasks"] })

      // Snapshot previous values
      const previousLists = queryClient.getQueriesData({ queryKey: ["tasks", "list"] })
      const previousTask = queryClient.getQueryData<Task>(["tasks", "detail", id])

      // Optimistically update lists
      queryClient.setQueriesData<Task[]>({ queryKey: ["tasks", "list"] }, (old) => {
        return old?.map((task) =>
          task.id === id ? { ...task, ...data } : task
        )
      })

      // Optimistically update detail
      if (previousTask) {
        queryClient.setQueryData<Task>(["tasks", "detail", id], {
          ...previousTask,
          ...data,
        })
      }

      return { previousLists, previousTask }
    },

    onSuccess: (updatedTask, { id }) => {
      // Update with server response
      queryClient.setQueryData(["tasks", "detail", id], updatedTask)
      toast.success("Task updated!")
    },

    onError: (error, { id }, context) => {
      // Rollback on error
      if (context?.previousLists) {
        context.previousLists.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }
      if (context?.previousTask) {
        queryClient.setQueryData(["tasks", "detail", id], context.previousTask)
      }

      toast.error("Failed to update task")
    },

    onSettled: () => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}
```

## Complete Request/Response Examples

### 1. Update Task (PUT)

**Request:**
```http
PUT /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### 2. Toggle Complete (PATCH)

**Request:**
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000/complete HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete documentation",
  "description": "Write API docs",
  "completed": true,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### 3. Delete Task (DELETE)

**Request:**
```http
DELETE /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (204):**
```http
HTTP/1.1 204 No Content
```

## Testing

### Backend Tests

```python
def test_update_task_success(client: TestClient, auth_headers: dict):
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    # Update task
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "completed": True},
        headers=auth_headers
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated"
    assert data["completed"] == True

def test_update_task_ownership(client: TestClient, auth_headers_user1: dict, auth_headers_user2: dict):
    # User 1 creates task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Test"},
        headers=auth_headers_user1
    )
    task_id = create_response.json()["id"]

    # User 2 tries to update
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=auth_headers_user2
    )

    assert update_response.status_code == 404
```

### Frontend Tests

```typescript
describe("useUpdateTask", () => {
  it("updates task successfully", async () => {
    const { result } = renderHook(() => useUpdateTask(), { wrapper: QueryWrapper })

    await act(async () => {
      await result.current.mutateAsync({
        id: "task-1",
        data: { title: "Updated" }
      })
    })

    expect(mockApi.updateTask).toHaveBeenCalledWith("task-1", { title: "Updated" })
  })

  it("performs optimistic update", async () => {
    const queryClient = new QueryClient()
    queryClient.setQueryData(["tasks", "list", "all"], [
      { id: "task-1", title: "Original", completed: false }
    ])

    const { result } = renderHook(() => useUpdateTask(), {
      wrapper: ({ children }) => (
        <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
      )
    })

    result.current.mutate({
      id: "task-1",
      data: { title: "Updated" }
    })

    // Check optimistic update
    const tasks = queryClient.getQueryData(["tasks", "list", "all"])
    expect(tasks[0].title).toBe("Updated")
  })
})
```

## Key Takeaways

1. **Verify Ownership** - Always check `task.user_id == current_user.id`
2. **Partial Updates** - Use `model_dump(exclude_unset=True)` for PUT
3. **Update Timestamps** - Always update `updated_at` field
4. **Optimistic Updates** - Instant UI feedback, rollback on error
5. **Confirmation Dialogs** - Always confirm destructive actions
6. **Inline Editing** - Better UX than separate edit pages
7. **Loading States** - Disable controls during mutations
