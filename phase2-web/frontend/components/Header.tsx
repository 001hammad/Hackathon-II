"use client"

import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
// import { authClient } from "@/lib/auth-client"
import { authClient } from "../lib/auth-client"
import { LogOut, CheckCircle2 } from "lucide-react"
import { motion } from "framer-motion"

export function Header() {
  const router = useRouter()

  async function handleLogout() {
    await authClient.signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/login")
        },
      },
    })
  }

  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="border-b bg-white dark:bg-gray-800 backdrop-blur-sm bg-opacity-95"
    >
      <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-4xl">
        <div className="flex items-center gap-2">
          <div className="bg-linear-to-br from-blue-600 to-blue-400 p-2 rounded-lg">
            <CheckCircle2 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Todo App
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Phase II - Multi-user
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          onClick={handleLogout}
          className="gap-2 hover:bg-red-50 hover:text-red-600 hover:border-red-300 dark:hover:bg-red-900/20 dark:hover:text-red-400 dark:hover:border-red-700"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </Button>
      </div>
    </motion.header>
  )
}
