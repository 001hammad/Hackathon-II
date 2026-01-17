"use client"

import { TaskItem } from "@/components/TaskItem"
import { Task } from "@/lib/api/client"
import { motion, AnimatePresence } from "framer-motion"
import { ClipboardList } from "lucide-react"

interface TaskListProps {
  tasks: Task[]
  onTasksChanged: () => void
}

export function TaskList({ tasks, onTasksChanged }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12 text-center border border-gray-100 dark:border-gray-700"
      >
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 bg-linear-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-full flex items-center justify-center">
            <ClipboardList className="h-8 w-8 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <p className="text-lg font-medium text-gray-900 dark:text-white mb-1">
              No tasks yet
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Add your first task above to get started!
            </p>
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="space-y-2"
    >
      <AnimatePresence mode="popLayout">
        {tasks.map((task, index) => (
          <TaskItem
            key={task.id}
            task={task}
            onTaskChanged={onTasksChanged}
            index={index}
          />
        ))}
      </AnimatePresence>
    </motion.div>
  )
}
