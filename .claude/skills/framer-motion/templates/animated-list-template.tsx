// Animated List Template
// Copy to components/animations/AnimatedList.tsx

"use client"

import { motion, AnimatePresence } from "framer-motion"
import { useReducedMotion } from "framer-motion"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 }
}

const reducedContainerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

const reducedItemVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

interface AnimatedListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
  keyExtractor: (item: T) => string
  className?: string
  enableDelete?: boolean
  onDelete?: (id: string) => void
}

export function AnimatedList<T>({
  items,
  renderItem,
  keyExtractor,
  className = "space-y-3",
  enableDelete = false,
  onDelete
}: AnimatedListProps<T>) {
  const shouldReduceMotion = useReducedMotion()

  const container = shouldReduceMotion ? reducedContainerVariants : containerVariants
  const item = shouldReduceMotion ? reducedItemVariants : itemVariants

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
      className={className}
    >
      <AnimatePresence mode="popLayout">
        {items.map((item, index) => (
          <motion.div
            key={keyExtractor(item)}
            variants={item}
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{
              opacity: 0,
              scale: 0.95,
              x: -100,
              transition: { duration: 0.2 }
            }}
            transition={{ duration: 0.2 }}
          >
            {renderItem(item)}
          </motion.div>
        ))}
      </AnimatePresence>
    </motion.div>
  )
}

// Usage
/*
import { AnimatedList } from "@/components/animations/AnimatedList"

<AnimatedList
  tasks={tasks}
  keyExtractor={(task) => task.id}
  renderItem={(task) => <TaskCard task={task} />}
  enableDelete
  onDelete={(id) => deleteTask(id)}
/>
*/
