---
name: frontend-auth
description: Expert in frontend authentication using Better Auth with JWT in Next.js App Router. Use PROACTIVELY whenever implementing login, signup, protected routes, or API calls with authentication in Phase 2.
---

# Frontend Auth Expert (Better Auth + JWT)

Expert guidance for implementing frontend authentication with Better Auth and JWT tokens in Next.js App Router.

## Core Responsibilities

### ✅ What This Skill Handles (Frontend Only)

1. **Better Auth Configuration** - Set up Better Auth client with JWT plugin
2. **Auth UI Pages** - Login, signup, logout pages in Next.js
3. **JWT Storage** - Store tokens securely (httpOnly cookies via Better Auth)
4. **API Client** - Automatically attach JWT to all API requests
5. **Route Protection** - Redirect unauthorized users to login
6. **Auth Redirects** - Redirect authenticated users away from auth pages
7. **Session Management** - Check auth state, get user data

### ❌ What This Skill Does NOT Handle (Backend)

- Backend JWT verification (handled by backend-auth expert)
- Database operations for users
- Password hashing
- Token generation
- User model definitions

## Quick Start

### 1. Install Dependencies

```bash
npm install better-auth @better-auth/jwt
npm install -D @types/better-auth
```

### 2. Create Better Auth Client

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react"
import { jwtClient } from "better-auth/plugins"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  plugins: [jwtClient()],
})

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient
```

### 3. Create API Client with JWT

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
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Redirect to login
      window.location.href = "/login"
    }
    throw new Error(`API Error: ${response.statusText}`)
  }

  return response.json()
}

export const api = {
  // Tasks endpoints
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

### 4. Create Auth Provider

```tsx
// app/providers.tsx
"use client"

import { SessionProvider } from "better-auth/react"

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      {children}
    </SessionProvider>
  )
}
```

### 5. Wrap App with Provider

```tsx
// app/layout.tsx
import { Providers } from "./providers"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

## Authentication Flow

### Login Flow

```tsx
"use client"

import { useState } from "react"
import { signIn } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError("")

    try {
      await signIn.email({
        email,
        password,
      })
      router.push("/dashboard")
    } catch (err) {
      setError("Invalid email or password")
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="text-destructive">{error}</p>}
      <button type="submit">Sign In</button>
    </form>
  )
}
```

### Signup Flow

```tsx
"use client"

import { useState } from "react"
import { signUp } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export default function SignupPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError("")

    try {
      await signUp.email({
        email,
        password,
        name,
      })
      router.push("/dashboard")
    } catch (err) {
      setError("Failed to create account")
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
        required
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="text-destructive">{error}</p>}
      <button type="submit">Sign Up</button>
    </form>
  )
}
```

### Logout

```tsx
"use client"

import { signOut } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export function LogoutButton() {
  const router = useRouter()

  async function handleLogout() {
    await signOut()
    router.push("/login")
  }

  return (
    <button onClick={handleLogout}>
      Sign Out
    </button>
  )
}
```

## Protected Routes

### Method 1: Middleware

```typescript
// middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("better-auth.session_token")

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    if (!token) {
      return NextResponse.redirect(new URL("/login", request.url))
    }
  }

  // Redirect authenticated users away from auth pages
  if (request.nextUrl.pathname.startsWith("/login") ||
      request.nextUrl.pathname.startsWith("/signup")) {
    if (token) {
      return NextResponse.redirect(new URL("/dashboard", request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/signup"]
}
```

### Method 2: Server Component Check

```tsx
// app/(dashboard)/tasks/page.tsx
import { redirect } from "next/navigation"
import { authClient } from "@/lib/auth-client"

export default async function TasksPage() {
  const session = await authClient.getSession()

  if (!session) {
    redirect("/login")
  }

  return (
    <div>
      <h1>Tasks</h1>
      <p>Welcome, {session.user.name}</p>
    </div>
  )
}
```

### Method 3: Client Component Hook

```tsx
"use client"

import { useSession } from "@/lib/auth-client"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function DashboardPage() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login")
    }
  }, [session, isPending, router])

  if (isPending) return <div>Loading...</div>
  if (!session) return null

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}</p>
    </div>
  )
}
```

## Getting User Data

### In Server Components

```tsx
import { authClient } from "@/lib/auth-client"

export default async function ProfilePage() {
  const session = await authClient.getSession()

  if (!session) {
    return <div>Not authenticated</div>
  }

  return (
    <div>
      <h1>{session.user.name}</h1>
      <p>{session.user.email}</p>
    </div>
  )
}
```

### In Client Components

```tsx
"use client"

import { useSession } from "@/lib/auth-client"

export function UserProfile() {
  const { data: session, isPending } = useSession()

  if (isPending) return <div>Loading...</div>
  if (!session) return <div>Not signed in</div>

  return (
    <div>
      <h2>{session.user.name}</h2>
      <p>{session.user.email}</p>
    </div>
  )
}
```

## API Calls with JWT

All API calls automatically include JWT token:

```tsx
import { api } from "@/lib/api"

// GET request
const tasks = await api.getTasks()

// POST request
const newTask = await api.createTask({
  title: "New task",
  description: "Description"
})

// PUT request
const updated = await api.updateTask("task-id", {
  status: "completed"
})

// DELETE request
await api.deleteTask("task-id")
```

## Security Best Practices

1. **Never store JWT in localStorage** - Use httpOnly cookies (Better Auth default)
2. **Always use HTTPS** in production
3. **Set short token expiry** - 15 minutes for access tokens
4. **Validate on every request** - Backend validates JWT
5. **Handle 401 errors** - Redirect to login automatically
6. **Secure password requirements** - Minimum 8 characters
7. **Rate limit login attempts** - Prevent brute force
8. **Use CSRF protection** - Better Auth handles this

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Common Patterns

### Loading State

```tsx
"use client"

import { useSession } from "@/lib/auth-client"

export function AuthContent() {
  const { data: session, isPending } = useSession()

  if (isPending) {
    return <div>Loading...</div>
  }

  return session ? <DashboardView /> : <LoginPrompt />
}
```

### Conditional Rendering

```tsx
"use client"

import { useSession } from "@/lib/auth-client"

export function Navbar() {
  const { data: session } = useSession()

  return (
    <nav>
      <Link href="/">Home</Link>
      {session ? (
        <>
          <Link href="/dashboard">Dashboard</Link>
          <LogoutButton />
        </>
      ) : (
        <>
          <Link href="/login">Login</Link>
          <Link href="/signup">Sign Up</Link>
        </>
      )}
    </nav>
  )
}
```

### Protected API Route

```tsx
// app/api/profile/route.ts
import { authClient } from "@/lib/auth-client"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await authClient.getSession()

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  return NextResponse.json({ user: session.user })
}
```

## Error Handling

```tsx
try {
  const tasks = await api.getTasks()
  setTasks(tasks)
} catch (error) {
  if (error.message.includes("401")) {
    // User is not authenticated - redirect happens automatically
    toast.error("Session expired. Please login again.")
  } else {
    toast.error("Failed to fetch tasks")
  }
}
```

## Key Principles

1. **Client-side only** - This skill handles frontend auth
2. **Better Auth client** - Use Better Auth React client
3. **JWT in cookies** - Stored securely by Better Auth
4. **Auto-attach tokens** - API client handles this
5. **Protect routes** - Use middleware or component checks
6. **Redirect patterns** - Unauthenticated → login, authenticated → dashboard
7. **Session hooks** - Use `useSession()` in client components

## Additional Resources

- See `examples/` for complete implementation patterns
- See `reference/` for Better Auth JWT plugin docs
- See `templates/` for ready-to-use files

## Summary

This skill provides **frontend-only** authentication with Better Auth and JWT:

✅ Auth configuration
✅ Login/signup/logout flows
✅ Protected routes
✅ API calls with JWT
✅ Session management
✅ Security best practices

❌ Backend JWT verification (use backend auth-expert)
❌ Database operations
❌ Token generation
