/**
 * Dashboard Layout - Header with logout button
 */
import { Header } from "@/components/Header"
// import { auth } from "@/lib/auth"
import { auth } from "../../lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    redirect("/login")
  }

  return (
    <div className="min-h-screen flex flex-col bg-linear-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8 max-w-4xl">
        {children}
      </main>
    </div>
  )
}
