---
name: framer-motion
description: Expert in Framer Motion for smooth animations, page transitions, list animations, hover effects in Next.js. Use proactively when adding animations or improving UX in Phase 2 web app.
---

# Framer Motion Expert for Todo App

Add subtle, performant animations to enhance user experience without overwhelming users.

## Core Principles

### What This Skill Handles

1. **Page Transitions** - Smooth navigation between pages
2. **List Animations** - Staggered animations for task lists
3. **Hover Effects** - Interactive card and button animations
4. **Modal/Dialog Animations** - Enter/exit animations
5. **Layout Animations** - Smooth reordering and layout changes
6. **Reduced Motion** - Respect user preferences
7. **Performance Optimization** - Hardware-accelerated animations

### Core Guidelines

✅ **Use Framer Motion for all animations** - The standard animation library for React
✅ **Keep animations subtle** - Enhance UX, don't distract
✅ **Respect reduced motion** - Disable animations for users who prefer reduced motion
✅ **Use AnimatePresence** - For mount/unmount animations
✅ **Use layoutId** - For shared element transitions
✅ **Use variants** - For reusable animation definitions

❌ **Don't over-animate** - Avoid excessive animations that slow down the app
❌ **Don't animate everything** - Focus on meaningful interactions
❌ **Don't ignore performance** - Use transform and opacity, not layout properties

## Quick Start

### Installation

```bash
npm install framer-motion
```

### Basic Import

```tsx
import { motion, AnimatePresence } from "framer-motion"
```

### Simple Animation

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeInOut" }}
>
  Animated content
</motion.div>
```

## Essential Patterns

### 1. Page Transitions

```tsx
"use client"

import { motion } from "framer-motion"

export default function PageTransition({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
    >
      {children}
    </motion.div>
  )
}
```

### 2. List Animations with Stagger

```tsx
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

<motion.div
  variants={container}
  initial="hidden"
  animate="show"
>
  {tasks.map(task => (
    <motion.div key={task.id} variants={item}>
      <TaskCard task={task} />
    </motion.div>
  ))}
</motion.div>
```

### 3. Hover Effects

```tsx
<motion.div
  whileHover={{ scale: 1.02, boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.2 }}
>
  <TaskCard task={task} />
</motion.div>
```

### 4. Modal Animations

```tsx
import { AnimatePresence, motion } from "framer-motion"

export function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-0 m-auto w-full max-w-md h-fit p-6 bg-background rounded-lg shadow-lg"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### 5. Layout Animations

```tsx
<motion.div layout>
  {/* This will animate smoothly when siblings change */}
  <TaskCard task={task} />
</motion.div>
```

## Variants for Reusable Animations

```tsx
const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: "easeOut" }
  },
  exit: { opacity: 0, y: -20 }
}

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

// Usage
<motion.div variants={fadeInUp} initial="hidden" animate="visible" exit="exit">
  Content
</motion.div>

<motion.div variants={staggerContainer} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.div variants={fadeInUp} key={item.id}>
      {item.name}
    </motion.div>
  ))}
</motion.div>
```

## Animation Properties

### Initial/Animate/Exit

```tsx
<motion.div
  initial={{ opacity: 0, x: -100 }}  // Starting state
  animate={{ opacity: 1, x: 0 }}      // End state
  exit={{ opacity: 0, x: 100 }}       // Unmount state (needs AnimatePresence)
>
  Content
</motion.div>
```

### Transition Options

```tsx
<motion.div
  transition={{
    duration: 0.3,           // Animation duration in seconds
    ease: "easeInOut",        // Easing function
    delay: 0.1,              // Delay before animation starts
    repeat: 0,               // Number of repetitions (0 = none)
    repeatType: "loop",      // Type of repeat (loop, reverse)
    type: "spring",          // Spring animation type
  }}
>
  Content
</motion.div>
```

### Easing Functions

```tsx
// Common easing options
ease: "easeIn"        // Starts slow, ends fast
ease: "easeOut"       // Starts fast, ends slow
ease: "easeInOut"     // Slow start, fast middle, slow end
ease: "linear"        // Constant speed

// Custom cubic bezier
ease: [0.25, 0.1, 0.25, 1]  // Custom timing curve

// Spring (natural bounce)
type: "spring",
stiffness: 100,      // How "stiff" the spring is
damping: 10,         // How much it bounces
mass: 1              // Heavier items move slower
```

### Interactive Props

```tsx
<motion.div
  whileHover={{ scale: 1.05 }}      // Mouse hover
  whileTap={{ scale: 0.95 }}        // Mouse click/tap
  whileFocus={{ scale: 1.02 }}      // Keyboard focus
  whileInView={{ opacity: 1 }}      // Scroll into view
  viewport={{ once: true }}         // Only animate once
>
  Interactive content
</motion.div>
```

### Layout Animations

```tsx
// Smooth reordering
<motion.div layout>
  {/* Automatically animates position changes */}
</motion.div>

// Shared element transitions (magic move)
<motion.div layoutId="task-card">
  {/* Items with same layoutId will smoothly transition */}
</motion.div>
```

## Common Use Cases

### Task Card Animation

```tsx
import { motion } from "framer-motion"

export function TaskCard({ task }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -2, boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }}
      transition={{ duration: 0.2 }}
      className="bg-card rounded-lg border p-4"
    >
      <h3 className="font-semibold">{task.title}</h3>
      {task.description && (
        <p className="text-sm text-muted-foreground mt-1">
          {task.description}
        </p>
      )}
    </motion.div>
  )
}
```

### Task List with Stagger

```tsx
import { motion } from "framer-motion"

const taskListVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05
    }
  }
}

const taskVariants = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0 }
}

export function TaskList({ tasks }) {
  return (
    <motion.div
      variants={taskListVariants}
      initial="hidden"
      animate="show"
      className="space-y-3"
    >
      {tasks.map(task => (
        <motion.div key={task.id} variants={taskVariants}>
          <TaskCard task={task} />
        </motion.div>
      ))}
    </motion.div>
  )
}
```

### Page Load Animation

```tsx
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

export default function AnimatedPage({ children }) {
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

### Delete with Animation

```tsx
import { AnimatePresence, motion } from "framer-motion"

export function TaskList({ tasks, onDelete }) {
  return (
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
          <TaskCard task={task} onDelete={() => onDelete(task.id)} />
        </motion.div>
      ))}
    </AnimatePresence>
  )
}
```

## Performance Best Practices

### Use transform and opacity

```tsx
// ✅ Good - Hardware accelerated
<motion.div
  initial={{ opacity: 0, x: 0, y: 0 }}
  animate={{ opacity: 1, x: 100, y: 100 }}
>
  Content
</motion.div>

// ❌ Bad - Triggers layout recalculation
<motion.div
  initial={{ width: 0 }}
  animate={{ width: 100 }}
>
  Content
</motion.div>
```

### Use layout prop sparingly

```tsx
// Use layout only when needed
<motion.div layout>
  {/* Automatically animates position changes */}
</motion.div>
```

### Limit animated elements

```tsx
// Don't animate too many elements at once
// Stagger animations to spread out CPU load
<motion.div
  transition={{ staggerChildren: 0.1 }}  // Spread animations
>
  {items.map(item => (
    <motion.div variants={itemVariant}>
      {item.name}
    </motion.div>
  ))}
</motion.div>
```

## Reduced Motion Support

```tsx
import { useReducedMotion } from "framer-motion"

export function TaskCard({ task }) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      initial={shouldReduceMotion ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      Content
    </motion.div>
  )
}
```

### CSS for Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Animation Duration Guidelines

| Animation Type | Duration | Example |
|----------------|----------|---------|
| Micro-interactions | 0.1-0.2s | Button hover, checkbox |
| Page transitions | 0.3-0.5s | Page loads, modal enter |
| List animations | 0.3-0.4s | Task list stagger |
| Complex animations | 0.5-0.8s | Page transitions |

## Easing Guidelines

| Use Case | Easing | Effect |
|----------|--------|--------|
| Natural feel | easeOut | Smooth deceleration |
| Continuous flow | easeInOut | Natural acceleration/deceleration |
| Instant feedback | linear | No easing, constant speed |
| Button clicks | spring | Natural bounce feel |
| List items | easeOut | Items settle smoothly |

## Common Mistakes to Avoid

❌ **Don't animate everything** - Focus on meaningful interactions
❌ **Don't use long durations** - Keep animations under 0.5s
❌ **Don't ignore reduced motion** - Always respect user preferences
❌ **Don't use layout animations excessively** - Can cause performance issues
❌ **Don't forget exit animations** - Use AnimatePresence for unmounts
❌ **Don't use complex easings unnecessarily** - easeOut is usually fine

## Additional Resources

- See `examples/` for complete animation patterns
- See `reference/` for detailed performance tips and variant guides
- See `templates/` for ready-to-use animation components
- Framer Motion Docs: https://www.framer.com/motion/
- Framer Motion API: https://www.framer.com/motion/api/

## Key Principles Summary

1. **Subtle animations** - Enhance UX, don't distract
2. **Performance-first** - Use transform/opacity, avoid layout changes
3. **Respect preferences** - Always support reduced motion
4. **Use variants** - Reusable, consistent animations
5. **AnimatePresence** - For mount/unmount animations
6. **Layout animations** - Use sparingly for reordering
7. **Consistent timing** - Use consistent durations and easings
