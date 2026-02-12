import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

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

  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Disable for development/testing
  },

  socialProviders: {}, // No social providers needed

  // Must be last plugin per Better Auth docs.
  plugins: [nextCookies()],
})