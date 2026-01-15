# Task List Fetch Example

This example demonstrates how to fetch and display a list of tasks using the authenticated API client.

## Basic Client Component Implementation

```typescript
"use client"

import { api, Task, APIError } from "@/lib/api"
import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Checkbox } from "@/components/ui/checkbox"

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTasks() {
      try {
        const data = await api.getTasks()
        setTasks(data)
        setError(null)
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

  async function handleToggleComplete(taskId: string) {
    try {
      const updatedTask = await api.toggleTaskComplete(taskId)
      setTasks((prev) =>
        prev.map((task) => (task.id === taskId ? updatedTask : task))
      )
    } catch (err) {
      console.error("Failed to toggle task:", err)
    }
  }

  if (loading) {
    return <TaskListSkeleton />
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  if (tasks.length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <p className="text-center text-muted-foreground">
            No tasks yet. Create your first task to get started!
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <Card key={task.id}>
          <CardContent className="flex items-start gap-4 pt-6">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => handleToggleComplete(task.id)}
            />
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
              <p className="text-xs text-muted-foreground mt-2">
                Created {new Date(task.created_at).toLocaleDateString()}
              </p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

function TaskListSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <Card key={i}>
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <Skeleton className="h-5 w-5 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-5 w-3/4" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-3 w-1/4" />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

## With React Query (Recommended)

React Query provides automatic caching, refetching, and loading state management:

```typescript
"use client"

import { useQuery } from "@tanstack/react-query"
import { api, Task } from "@/lib/api"
import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function TaskList() {
  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ["tasks"],
    queryFn: api.getTasks,
    staleTime: 30000, // Consider data fresh for 30 seconds
    refetchOnWindowFocus: true, // Refetch when window regains focus
  })

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

  if (!tasks || tasks.length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <p className="text-center text-muted-foreground">
            No tasks yet. Create your first task to get started!
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}

function TaskCard({ task }: { task: Task }) {
  return (
    <Card>
      <CardContent className="pt-6">
        <h3 className={task.completed ? "line-through" : ""}>{task.title}</h3>
        {task.description && (
          <p className="text-sm text-muted-foreground mt-1">
            {task.description}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

function TaskListSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <Card key={i}>
          <CardContent className="pt-6">
            <Skeleton className="h-5 w-3/4 mb-2" />
            <Skeleton className="h-4 w-full" />
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

## Server Component with Initial Data

For better performance, fetch data on the server and pass to client component:

```typescript
// app/tasks/page.tsx (Server Component)
import { auth } from "@/lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"
import { TaskList } from "@/components/task-list"

export default async function TasksPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    redirect("/login")
  }

  // Fetch initial data on server
  const response = await fetch(`${process.env.API_URL}/api/tasks`, {
    headers: {
      Authorization: `Bearer ${session.token}`,
      "Content-Type": "application/json",
    },
    cache: "no-store", // Don't cache for fresh data
  })

  if (!response.ok) {
    throw new Error("Failed to fetch tasks")
  }

  const initialTasks = await response.json()

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">My Tasks</h1>
      <TaskList initialTasks={initialTasks} />
    </div>
  )
}
```

```typescript
// components/task-list.tsx (Client Component)
"use client"

import { useQuery } from "@tanstack/react-query"
import { api, Task } from "@/lib/api"

interface TaskListProps {
  initialTasks: Task[]
}

export function TaskList({ initialTasks }: TaskListProps) {
  const { data: tasks } = useQuery({
    queryKey: ["tasks"],
    queryFn: api.getTasks,
    initialData: initialTasks, // Use server data initially
    staleTime: 30000,
  })

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

## With Filtering and Sorting

```typescript
"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { api, Task } from "@/lib/api"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function FilterableTaskList() {
  const [filter, setFilter] = useState<"all" | "completed" | "pending">("all")
  const [sort, setSort] = useState<"newest" | "oldest" | "title">("newest")

  const { data: tasks, isLoading } = useQuery({
    queryKey: ["tasks"],
    queryFn: api.getTasks,
  })

  const filteredAndSortedTasks = tasks
    ?.filter((task) => {
      if (filter === "all") return true
      if (filter === "completed") return task.completed
      if (filter === "pending") return !task.completed
      return true
    })
    .sort((a, b) => {
      if (sort === "newest") {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      }
      if (sort === "oldest") {
        return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      }
      if (sort === "title") {
        return a.title.localeCompare(b.title)
      }
      return 0
    })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex gap-4 mb-6">
        <Select value={filter} onValueChange={(v) => setFilter(v as any)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter tasks" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
          </SelectContent>
        </Select>

        <Select value={sort} onValueChange={(v) => setSort(v as any)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest First</SelectItem>
            <SelectItem value="oldest">Oldest First</SelectItem>
            <SelectItem value="title">Alphabetical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-4">
        {filteredAndSortedTasks?.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  )
}
```

## Key Points

1. **Always use `api.getTasks()`** - Never make direct fetch calls
2. **Handle loading and error states** - Provide good UX feedback
3. **Use React Query when possible** - Automatic caching and refetching
4. **Type safety** - TypeScript ensures correct data structure
5. **Server-side data fetching** - Better performance with initial data
6. **Automatic JWT attachment** - Better Auth handles authentication

## Common Patterns

### Polling for Updates
```typescript
const { data: tasks } = useQuery({
  queryKey: ["tasks"],
  queryFn: api.getTasks,
  refetchInterval: 5000, // Poll every 5 seconds
})
```

### Optimistic Updates
```typescript
const queryClient = useQueryClient()

async function handleToggleComplete(taskId: string) {
  // Optimistically update UI
  queryClient.setQueryData(["tasks"], (old: Task[] | undefined) =>
    old?.map((task) =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    )
  )

  try {
    await api.toggleTaskComplete(taskId)
  } catch (error) {
    // Revert on error
    queryClient.invalidateQueries({ queryKey: ["tasks"] })
  }
}
```

### Infinite Scroll
```typescript
import { useInfiniteQuery } from "@tanstack/react-query"

const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ["tasks"],
  queryFn: ({ pageParam = 0 }) => api.getTasks({ page: pageParam }),
  getNextPageParam: (lastPage, pages) => lastPage.nextPage,
})
```
