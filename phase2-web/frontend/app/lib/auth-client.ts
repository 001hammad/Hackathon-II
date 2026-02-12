import { createAuthClient } from "better-auth/react"

// Better Auth will automatically use the current origin in the browser
// This is the recommended approach for Next.js apps
export const authClient = createAuthClient()
