# Page Transitions

Complete page transition patterns for Next.js App Router.

## Basic Page Transition

```tsx
// app/template.tsx (Next.js special file for transitions)
"use client"

import { motion } from "framer-motion"

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: "easeOut"
    }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.2 }
  }
}

export default function Template({ children }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="enter"
      exit="exit"
    >
      {children}
    </motion.div>
  )
}
```

## Slide Page Transition

```tsx
// components/animations/SlidePage.tsx
"use client"

import { motion } from "framer-motion"

export function SlidePage({ children, direction = 1 }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: direction * 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: direction * -50 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
    >
      {children}
    </motion.div>
  )
}

// Usage in pages
import { SlidePage } from "@/components/animations/SlidePage"

export default function TasksPage() {
  return (
    <SlidePage direction={1}>
      <TasksList />
    </SlidePage>
  )
}
```

## Fade Page Transition

```tsx
// components/animations/FadePage.tsx
"use client"

import { motion } from "framer-motion"

export function FadePage({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

## Scale Page Transition

```tsx
// components/animations/ScalePage.tsx
"use client"

import { motion } from "framer-motion"

export function ScalePage({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.05 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  )
}
```

## Key Points

1. Use `app/template.tsx` for Next.js page transitions
2. Combine initial, animate, exit for full transition cycle
3. Use consistent duration (0.3-0.5s) for smooth UX
4. Match exit direction with enter direction for natural feel
