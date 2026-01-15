// Template for creating layouts in Next.js App Router
// Layouts wrap pages and persist across route changes

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-100">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold">Todo App</h1>
          </div>
        </header>

        {/* Main content */}
        <main>
          {children}
        </main>

        {/* Footer (optional) */}
        <footer className="bg-white border-t mt-auto">
          <div className="container mx-auto p-4 text-center text-gray-600">
            <p>&copy; 2025 Todo App. All rights reserved.</p>
          </div>
        </footer>
      </body>
    </html>
  )
}

// Optional: Add metadata to the root layout
// import type { Metadata } from "next"
//
// export const metadata: Metadata = {
//   title: {
//     default: "Todo App",
//     template: "%s | Todo App"
//   },
//   description: "A modern todo application"
// }
