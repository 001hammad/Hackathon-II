// Animated Card Template
// Copy to components/animations/AnimatedCard.tsx

"use client"

import { motion } from "framer-motion"
import { useReducedMotion } from "framer-motion"

interface AnimatedCardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  href?: string
  delay?: number
}

export function AnimatedCard({
  children,
  className = "",
  onClick,
  href,
  delay = 0
}: AnimatedCardProps) {
  const shouldReduceMotion = useReducedMotion()

  const motionProps = shouldReduceMotion
    ? {
        initial: { opacity: 0 },
        animate: { opacity: 1 },
        transition: { duration: 0, delay }
      }
    : {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        whileHover: { y: -4, boxShadow: "0 8px 16px rgba(0,0,0,0.1)" },
        whileTap: { scale: 0.98 },
        transition: { duration: 0.3, delay, ease: "easeOut" }
      }

  const content = (
    <motion.div
      {...motionProps}
      onClick={onClick}
      className={`bg-card rounded-lg border p-4 ${className}`}
      style={{ cursor: onClick ? "pointer" : "default" }}
    >
      {children}
    </motion.div>
  )

  // If href is provided, wrap in Link
  if (href) {
    return (
      <motion.a href={href} className="block no-underline">
        {content}
      </motion.a>
    )
  }

  return content
}

// Task-specific card variant
interface TaskCardProps {
  task: {
    id: string
    title: string
    description?: string
    status: string
    due_date?: string
  }
  onClick?: () => void
  onDelete?: () => void
}

export function TaskCard({ task, onClick, onDelete }: TaskCardProps) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <AnimatedCard
      onClick={onClick}
      className="hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold truncate">{task.title}</h3>
          {task.description && (
            <p className="text-sm text-muted-foreground truncate mt-1">
              {task.description}
            </p>
          )}
        </div>

        {onDelete && (
          <motion.button
            whileHover={shouldReduceMotion ? {} : { scale: 1.1 }}
            whileTap={shouldReduceMotion ? {} : { scale: 0.9 }}
            onClick={(e) => {
              e.stopPropagation()
              onDelete()
            }}
            className="text-muted-foreground hover:text-destructive p-1 rounded"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M3 6h18" />
              <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
              <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
            </svg>
          </motion.button>
        )}
      </div>

      <div className="flex items-center gap-2 mt-3">
        <span
          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
            task.status === "completed"
              ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
              : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
          }`}
        >
          {task.status}
        </span>

        {task.due_date && (
          <span className="text-xs text-muted-foreground">
            Due {new Date(task.due_date).toLocaleDateString()}
          </span>
        )}
      </div>
    </AnimatedCard>
  )
}

// Usage
/*
import { AnimatedCard, TaskCard } from "@/components/animations/AnimatedCard"

// Generic animated card
<AnimatedCard delay={0}>
  <h3>Card Title</h3>
  <p>Card content</p>
</AnimatedCard>

// Task-specific card
<TaskCard
  task={task}
  onClick={() => router.push(`/tasks/${task.id}`)}
  onDelete={() => deleteTask(task.id)}
/>
*/
