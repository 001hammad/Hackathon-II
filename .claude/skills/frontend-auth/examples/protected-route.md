# Protected Route

Three methods for protecting routes in Next.js App Router.

## Method 1: Middleware (Recommended)

```typescript
// middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("better-auth.session_token")

  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    if (!token) {
      return NextResponse.redirect(new URL("/login", request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/tasks/:path*"]
}
```

## Method 2: Server Component

```tsx
// app/(dashboard)/tasks/page.tsx
import { redirect } from "next/navigation"
import { authClient } from "@/lib/auth-client"

export default async function TasksPage() {
  const session = await authClient.getSession()

  if (!session) {
    redirect("/login")
  }

  return <div>Protected content</div>
}
```

## Method 3: Client Component

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

  return <div>Dashboard content</div>
}
```
