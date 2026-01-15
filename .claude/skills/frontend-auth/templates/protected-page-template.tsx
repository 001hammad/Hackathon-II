// Protected page template
// Copy to app/(dashboard)/page.tsx

import { redirect } from "next/navigation"
import { authClient } from "@/lib/auth-client"

export default async function DashboardPage() {
  const session = await authClient.getSession()

  if (!session) {
    redirect("/login")
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
    </div>
  )
}
