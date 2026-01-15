// Better Auth client configuration
// Copy to lib/auth-client.ts

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
