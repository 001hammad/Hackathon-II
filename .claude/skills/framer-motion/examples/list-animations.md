# List Animations

Staggered animations for task lists and data grids.

## Staggered List Animation

```tsx
"use client"

import { motion } from "framer-motion"

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0 }
}

export function TaskList({ tasks }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-3"
    >
      {tasks.map(task => (
        <motion.div key={task.id} variants={item}>
          <TaskCard task={task} />
        </motion.div>
      ))}
    </motion.div>
  )
}
```

## List with AnimatePresence (Delete Animation)

```tsx
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

export function TaskListWithDelete({ initialTasks }) {
  const [tasks, setTasks] = useState(initialTasks)

  const deleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id))
  }

  return (
    <motion.div layout className="space-y-3">
      <AnimatePresence mode="popLayout">
        {tasks.map(task => (
          <motion.div
            key={task.id}
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, x: -100 }}
            transition={{ duration: 0.2 }}
          >
            <TaskCard task={task} onDelete={() => deleteTask(task.id)} />
          </motion.div>
        ))}
      </AnimatePresence>
    </motion.div>
  )
}
```

## Grid Stagger Animation

```tsx
"use client"

import { motion } from "framer-motion"

const gridVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1
    }
  }
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

export function TaskGrid({ tasks }) {
  return (
    <motion.div
      variants={gridVariants}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      {tasks.map(task => (
        <motion.div key={task.id} variants={cardVariants}>
          <TaskCard task={task} />
        </motion.div>
      ))}
    </motion.div>
  )
}
```

## Filtered List Animation

```tsx
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

export function FilteredTaskList({ allTasks }) {
  const [filter, setFilter] = useState("all")

  const filteredTasks = allTasks.filter(task => {
    if (filter === "all") return true
    return task.status === filter
  })

  return (
    <>
      <FilterButtons currentFilter={filter} onFilterChange={setFilter} />

      <motion.div layout className="space-y-3">
        <AnimatePresence mode="popLayout">
          {filteredTasks.map(task => (
            <motion.div
              key={task.id}
              layout
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
            >
              <TaskCard task={task} />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
    </>
  )
}
```

## Key Points

1. Use `staggerChildren` for smooth list animations
2. Use `AnimatePresence` with `mode="popLayout"` for delete animations
3. Use `layout` prop for smooth reordering during filtering
4. Set `staggerChildren` to 0.05-0.1 for smooth timing
