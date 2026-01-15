# Reduced Motion

Supporting users who prefer reduced motion.

## Check User Preference

```tsx
import { useReducedMotion } from "framer-motion"

export function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      initial={shouldReduceMotion ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{
        duration: shouldReduceMotion ? 0 : 0.3
      }}
    >
      Content
    </motion.div>
  )
}
```

## CSS Media Query

```css
/* styles/globals.css */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Complete Support Pattern

```tsx
"use client"

import { useReducedMotion } from "framer-motion"
import { motion } from "framer-motion"

const pageVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

const reducedVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

export function AnimatedPage({ children }) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      variants={shouldReduceMotion ? reducedVariants : pageVariants}
      initial="hidden"
      animate="visible"
      transition={{
        duration: shouldReduceMotion ? 0 : 0.4,
        ease: shouldReduceMotion ? "linear" : "easeOut"
      }}
    >
      {children}
    </motion.div>
  )
}
```

## Disable Specific Animations

```tsx
"use client"

import { useReducedMotion } from "framer-motion"
import { motion } from "framer-motion"

export function TaskCard({ task }) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      // Disable hover scale for reduced motion users
      whileHover={shouldReduceMotion ? {} : { scale: 1.02 }}
      // Disable tap scale for reduced motion users
      whileTap={shouldReduceMotion ? {} : { scale: 0.98 }}
      // Keep fade animation but make it instant
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
    >
      <TaskContent task={task} />
    </motion.div>
  )
}
```

## Key Points

1. Always check `useReducedMotion()` preference
2. Provide instant transitions for reduced motion
3. Keep essential state changes visible
4. Remove decorative animations only
5. Test with `prefers-reduced-motion: reduce` enabled
