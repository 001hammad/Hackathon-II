# Better Auth with JWT Plugin

Complete reference for Better Auth JWT plugin in Next.js.

## Installation

```bash
npm install better-auth @better-auth/jwt
```

## Client Configuration

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react"
import { jwtClient } from "better-auth/plugins"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [jwtClient()],
})

export const { signIn, signUp, signOut, useSession } = authClient
```

## Available Methods

### signIn.email()
```typescript
await signIn.email({
  email: "user@example.com",
  password: "password123"
})
```

### signUp.email()
```typescript
await signUp.email({
  email: "user@example.com",
  password: "password123",
  name: "John Doe"
})
```

### signOut()
```typescript
await signOut()
```

### useSession() Hook
```typescript
const { data: session, isPending } = useSession()
```

### getSession()
```typescript
const session = await authClient.getSession()
```

## Session Object

```typescript
{
  user: {
    id: string
    email: string
    name: string
  },
  accessToken: string,
  expiresAt: number
}
```

## Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```
