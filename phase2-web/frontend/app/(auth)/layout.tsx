/**
 * Auth Layout - Centered card design for login and signup pages
 */
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 via-blue-100/50 to-gray-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  )
}
