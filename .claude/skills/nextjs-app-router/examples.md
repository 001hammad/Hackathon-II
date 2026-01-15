# Examples

Common patterns and real-world examples for Next.js App Router.

## 1. Server Component Page (Data Fetching)

```tsx
// app/(dashboard)/tasks/page.tsx
import type { Metadata } from "next"
import { getTasks } from "@/lib/api"
import { TaskList } from "@/components/tasks/task-list"

export const metadata: Metadata = {
  title: "My Tasks",
  description: "Manage your todo list"
}

export default async function TasksPage() {
  // Fetch data directly in server component
  const tasks = await getTasks()

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">My Tasks</h1>
      <TaskList tasks={tasks} />
    </div>
  )
}
```

## 2. Client Component (Interactive)

```tsx
// components/tasks/task-form.tsx
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

export function TaskForm() {
  const [title, setTitle] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      })

      if (res.ok) {
        router.push("/tasks")
        router.refresh() // Refresh server component data
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
        required
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create Task"}
      </button>
    </form>
  )
}
```

## 3. Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: {
    default: "Todo App",
    template: "%s | Todo App"
  },
  description: "A modern todo application built with Next.js"
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  )
}
```

## 4. Nested Layout (Dashboard)

```tsx
// app/(dashboard)/layout.tsx
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

## 5. Dynamic Route (Task Detail)

```tsx
// app/tasks/[id]/page.tsx
import { notFound } from "next/navigation"
import { getTask } from "@/lib/api"

export default async function TaskDetailPage({
  params
}: {
  params: { id: string }
}) {
  const task = await getTask(params.id)

  if (!task) {
    notFound() // Shows 404 page
  }

  return (
    <div>
      <h1>{task.title}</h1>
      <p>{task.description}</p>
      <p>Status: {task.status}</p>
    </div>
  )
}

// Generate static params for static generation (optional)
export async function generateStaticParams() {
  const tasks = await getTasks()

  return tasks.map((task) => ({
    id: task.id.toString()
  }))
}
```

## 6. Loading State

```tsx
// app/(dashboard)/tasks/loading.tsx
export default function TasksLoading() {
  return (
    <div className="container mx-auto p-8">
      <div className="h-8 w-48 bg-gray-200 animate-pulse rounded mb-6" />
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-24 bg-gray-200 animate-pulse rounded" />
        ))}
      </div>
    </div>
  )
}
```

## 7. Error Boundary

```tsx
// app/(dashboard)/tasks/error.tsx
"use client"

export default function TasksError({
  error,
  reset
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="container mx-auto p-8">
      <h2 className="text-2xl font-bold text-red-600 mb-4">
        Something went wrong!
      </h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  )
}
```

## 8. Route Groups

```tsx
// Use parentheses to group routes without affecting URLs

app/
├── (auth)/                 # Auth-related pages
│   ├── layout.tsx          # Auth layout (centered, simple)
│   ├── login/
│   │   └── page.tsx        # URL: /login
│   └── signup/
│       └── page.tsx        # URL: /signup
│
└── (dashboard)/            # Dashboard pages
    ├── layout.tsx          # Dashboard layout (header, sidebar)
    ├── page.tsx            # URL: / (home/dashboard)
    └── tasks/
        └── page.tsx        # URL: /tasks
```

```tsx
// app/(auth)/layout.tsx
export default function AuthLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  )
}
```

## 9. Parallel Routes (Advanced)

```tsx
// app/dashboard/@tasks/page.tsx
export default function TasksSlot() {
  return <TasksList />
}

// app/dashboard/@analytics/page.tsx
export default function AnalyticsSlot() {
  return <Analytics />
}

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  tasks,
  analytics
}: {
  children: React.ReactNode
  tasks: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2 gap-4">
        {tasks}
        {analytics}
      </div>
    </div>
  )
}
```

## 10. Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react"

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<TasksSkeleton />}>
        <TasksWrapper />
      </Suspense>

      <Suspense fallback={<StatsSkeleton />}>
        <StatsWrapper />
      </Suspense>
    </div>
  )
}

async function TasksWrapper() {
  const tasks = await getTasks() // Slow data fetch
  return <TaskList tasks={tasks} />
}

async function StatsWrapper() {
  const stats = await getStats() // Another slow fetch
  return <Stats data={stats} />
}
```

## 11. Search Params

```tsx
// app/tasks/page.tsx
export default async function TasksPage({
  searchParams
}: {
  searchParams: { status?: string; page?: string }
}) {
  const status = searchParams.status || "all"
  const page = parseInt(searchParams.page || "1")

  const tasks = await getTasks({ status, page })

  return (
    <div>
      <h1>Tasks - {status}</h1>
      <TaskList tasks={tasks} />
      <Pagination currentPage={page} />
    </div>
  )
}

// URL: /tasks?status=completed&page=2
```

## 12. Not Found Page

```tsx
// app/tasks/[id]/not-found.tsx
export default function TaskNotFound() {
  return (
    <div>
      <h2>Task Not Found</h2>
      <p>The task you're looking for doesn't exist.</p>
      <a href="/tasks">Back to Tasks</a>
    </div>
  )
}

// Trigger it in page.tsx:
import { notFound } from "next/navigation"

export default async function TaskPage({ params }) {
  const task = await getTask(params.id)

  if (!task) {
    notFound() // Shows not-found.tsx
  }

  return <TaskDetail task={task} />
}
```

## 13. API Routes

```tsx
// app/api/tasks/route.ts
import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const tasks = await fetchTasksFromDB()
  return NextResponse.json(tasks)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const newTask = await createTaskInDB(body)
  return NextResponse.json(newTask, { status: 201 })
}
```

## 14. Middleware for Auth

```tsx
// middleware.ts (root level)
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")

  // Redirect to login if not authenticated
  if (!token && !request.nextUrl.pathname.startsWith("/login")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/tasks/:path*"]
}
```

## Key Takeaways

1. **Server components by default** - Only add "use client" when needed
2. **Fetch data in server components** - Pass as props to client components
3. **Use loading.tsx and error.tsx** - Better UX with loading and error states
4. **Route groups for organization** - Group routes without affecting URLs
5. **Export metadata** - Always add title and description for SEO
6. **Dynamic routes** - Use [param] for dynamic segments
7. **Suspense for streaming** - Show content as it loads
8. **Type your params** - Use TypeScript for type safety
