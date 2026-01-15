---
name: nextjs-app-router
description: Expert in Next.js 16+ App Router structure, server/client components, layouts, loading/error states. Use proactively when setting up pages, routes, or frontend structure in Phase 2.
---

# Next.js App Router Expert

Expert guidance for Next.js App Router architecture, server/client component patterns, and modern routing structure.

## Core Principles

### Always Use App Router (app/ folder)

The App Router is the modern Next.js routing system that provides:
- File-system based routing
- Server components by default
- Built-in loading and error states
- Nested layouts
- Parallel routes and intercepting routes

### Server Components by Default

**Server components** are the default in App Router:
- Run on the server only
- Can fetch data directly
- Have zero client-side JavaScript
- Can access backend resources securely
- Cannot use browser APIs or React hooks

```tsx
// This is a server component (default)
export default async function TasksPage() {
  const tasks = await fetchTasks() // Direct data fetching
  return <TaskList tasks={tasks} />
}
```

### Client Components Only When Needed

Add `"use client"` directive only when you need:
- React hooks (useState, useEffect, etc.)
- Browser APIs (localStorage, window, etc.)
- Event handlers (onClick, onChange, etc.)
- React Context

```tsx
"use client"

import { useState } from "react"

export default function TaskForm() {
  const [title, setTitle] = useState("")
  // Now you can use hooks and event handlers
}
```

### Layouts for Shared UI

Use `layout.tsx` to wrap pages with shared UI:
- Headers, navigation bars
- Footers
- Sidebars
- Common wrappers

Layouts **persist** across route changes (don't remount).

```tsx
// app/layout.tsx (root layout)
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  )
}
```

### Loading and Error States

Create `loading.tsx` and `error.tsx` files for better UX:

```tsx
// app/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}

// app/error.tsx
"use client"
export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

### Export Metadata for SEO

```tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "My Tasks",
  description: "Manage your todo list"
}
```

## File Structure

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── loading.tsx             # Global loading state
├── error.tsx               # Global error boundary
├── globals.css             # Global styles
│
├── (auth)/                 # Route group (no URL segment)
│   ├── layout.tsx          # Auth layout
│   ├── login/
│   │   └── page.tsx        # /login
│   └── signup/
│       └── page.tsx        # /signup
│
├── (dashboard)/            # Route group
│   ├── layout.tsx          # Dashboard layout
│   ├── page.tsx            # /dashboard or /
│   ├── loading.tsx         # Dashboard loading
│   ├── error.tsx           # Dashboard error
│   │
│   ├── tasks/
│   │   ├── page.tsx        # /tasks
│   │   ├── [id]/
│   │   │   └── page.tsx    # /tasks/:id
│   │   └── new/
│   │       └── page.tsx    # /tasks/new
│   │
│   └── settings/
│       └── page.tsx        # /settings
│
└── api/                    # API routes (if needed)
    └── tasks/
        └── route.ts        # /api/tasks
```

## Key Patterns

### Pattern 1: Server Component Data Fetching

```tsx
// app/(dashboard)/tasks/page.tsx
import { getTasks } from "@/lib/api"

export default async function TasksPage() {
  const tasks = await getTasks()

  return (
    <div>
      <h1>My Tasks</h1>
      <TaskList tasks={tasks} />
    </div>
  )
}
```

### Pattern 2: Client Component for Interactivity

```tsx
// components/tasks/task-list.tsx
"use client"

import { useState } from "react"

export function TaskList({ tasks }) {
  const [filter, setFilter] = useState("all")

  const filtered = tasks.filter(/* ... */)

  return (
    <div>
      <FilterButtons onChange={setFilter} />
      {filtered.map(task => <TaskCard key={task.id} task={task} />)}
    </div>
  )
}
```

### Pattern 3: Nested Layouts

```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">
        {children}
      </main>
    </div>
  )
}
```

### Pattern 4: Dynamic Routes

```tsx
// app/tasks/[id]/page.tsx
export default async function TaskDetailPage({
  params
}: {
  params: { id: string }
}) {
  const task = await getTask(params.id)

  return <TaskDetail task={task} />
}
```

### Pattern 5: Route Groups

Use `(groupName)` to organize routes without affecting URLs:

```tsx
app/
├── (marketing)/
│   ├── about/page.tsx      # URL: /about
│   └── contact/page.tsx    # URL: /contact
└── (app)/
    └── dashboard/page.tsx  # URL: /dashboard
```

## Common Mistakes to Avoid

❌ **Don't add "use client" unnecessarily**
- Increases bundle size
- Loses server component benefits

❌ **Don't fetch data in client components**
- Use server components for data fetching
- Pass data as props to client components

❌ **Don't forget loading/error states**
- Always provide feedback to users
- Create loading.tsx and error.tsx

❌ **Don't mix async with "use client"**
- Client components cannot be async
- Use useEffect for client-side data fetching

❌ **Don't skip metadata exports**
- Important for SEO
- Easy to add, big impact

## When to Use Server vs Client Components

### Use Server Components When:
- Fetching data from APIs or databases
- Accessing backend resources
- Keeping sensitive data on server (API keys)
- Reducing client-side JavaScript
- Static content rendering

### Use Client Components When:
- Using React hooks (useState, useEffect, etc.)
- Handling user interactions (onClick, onChange)
- Using browser APIs (localStorage, window)
- Using React Context
- Using third-party libraries that need browser

## Best Practices

1. **Start with server components**: Only add "use client" when necessary
2. **Fetch data close to where it's used**: Server components make this easy
3. **Use Suspense boundaries**: Combine with loading.tsx for better UX
4. **Leverage route groups**: Organize without affecting URLs
5. **Export metadata**: Always add title and description
6. **Use TypeScript**: Type your params and searchParams
7. **Handle errors gracefully**: Create error.tsx files

## Additional Resources

- See `templates/` for ready-to-use page and layout templates
- See `examples.md` for more common patterns and use cases
- Next.js Docs: https://nextjs.org/docs/app
