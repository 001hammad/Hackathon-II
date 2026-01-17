import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"
import { Pool } from "pg"

function requireEnv(name: string): string {
  const value = process.env[name]
  if (!value) throw new Error(`Missing env var: ${name}`)
  return value
}

export const auth = betterAuth({
  // Better Auth docs recommend setting baseURL explicitly (do not rely on inference).
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Better Auth uses BETTER_AUTH_SECRET/AUTH_SECRET by default, but we set it explicitly.
  secret: requireEnv("BETTER_AUTH_SECRET"),

  database: new Pool({
    // Neon pooled connection strings do NOT allow startup parameters like `options=-c search_path=...`.
    // So we connect directly using DATABASE_URL as-is.
    connectionString: requireEnv("DATABASE_URL"),
  }),

  emailAndPassword: {
    enabled: true,
  },

  advanced: {
    database: {
      // Properly configure UUID generation for PostgreSQL
      generateId: "uuid",
    },
  },

  // Must be last plugin per Better Auth docs.
  plugins: [nextCookies()],
})