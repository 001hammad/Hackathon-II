/**
 * Next.js Middleware for route protection
 *
 * Redirects:
 * - Unauthenticated users accessing /dashboard → /login
 * - Authenticated users accessing /login or /signup → /dashboard
 */
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // Check for auth token in localStorage (client-side check will be more robust)
  // For now, we'll redirect unauthenticated users to login
  const authToken = request.cookies.get("better-auth.session_token")

  const isAuthPage = request.nextUrl.pathname.startsWith("/login") ||
                     request.nextUrl.pathname.startsWith("/signup")
  const isProtectedPage =
    request.nextUrl.pathname === "/" ||
    request.nextUrl.pathname.startsWith("/dashboard")

  // Redirect unauthenticated users from protected pages to login
  if (isProtectedPage && !authToken) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  // Redirect authenticated users away from auth pages to dashboard
  if (isAuthPage && authToken) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/", "/dashboard", "/login", "/signup"]
}
