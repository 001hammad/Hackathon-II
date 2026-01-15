// Template for creating new pages in Next.js App Router
// Server component by default - can fetch data directly

import type { Metadata } from "next"

// Export metadata for SEO
export const metadata: Metadata = {
  title: "My Tasks",
  description: "Todo app dashboard"
}

// Server component (default) - async is allowed
export default async function TasksPage() {
  // Fetch data directly in server component
  // const tasks = await fetchTasks()

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">My Tasks</h1>

      {/* Your page content goes here */}
      <div className="space-y-4">
        <p className="text-gray-600">Task list will go here</p>
      </div>
    </div>
  )
}

// Optional: Generate static params for static generation
// export async function generateStaticParams() {
//   return [
//     { id: '1' },
//     { id: '2' },
//   ]
// }

// Optional: Revalidate data every X seconds
// export const revalidate = 60 // Revalidate every 60 seconds
