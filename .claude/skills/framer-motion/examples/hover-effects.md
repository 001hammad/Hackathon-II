# Hover Effects

Interactive hover and tap animations for cards, buttons, and interactive elements.

## Task Card Hover

```tsx
"use client"

import { motion } from "framer-motion"

export function TaskCard({ task }) {
  return (
    <motion.div
      whileHover={{
        y: -4,
        boxShadow: "0 8px 16px rgba(0,0,0,0.1)"
      }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.2 }}
      className="bg-card rounded-lg border p-4 cursor-pointer"
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

## Button Hover Effects

```tsx
"use client"

import { motion } from "framer-motion"

export function AnimatedButton({ children, onClick }) {
  return (
    <motion.button
      whileHover={{
        scale: 1.02,
        boxShadow: "0 4px 12px rgba(0,0,0,0.15)"
      }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.15 }}
      onClick={onClick}
      className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
    >
      {children}
    </motion.button>
  )
}

// Icon button
export function IconButton({ icon, onClick }) {
  return (
    <motion.button
      whileHover={{ scale: 1.1, rotate: 5 }}
      whileTap={{ scale: 0.9 }}
      transition={{ duration: 0.15 }}
      onClick={onClick}
      className="p-2 rounded-full hover:bg-accent"
    >
      {icon}
    </motion.button>
  )
}
```

## Checkbox Animation

```tsx
"use client"

import { motion } from "framer-motion"

export function AnimatedCheckbox({ checked, onChange }) {
  return (
    <motion.button
      onClick={onChange}
      whileTap={{ scale: 0.9 }}
      className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
        checked ? "bg-primary border-primary" : "border-input"
      }`}
    >
      {checked && (
        <motion.svg
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="w-3 h-3 text-primary-foreground"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <motion.path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={3}
            d="M5 13l4 4L19 7"
          />
        </motion.svg>
      )}
    </motion.button>
  )
}
```

## Card Selection Animation

```tsx
"use client"

import { motion } from "framer-motion"

export function SelectableCard({ selected, onSelect, children }) {
  return (
    <motion.div
      onClick={onSelect}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      animate={{
        borderColor: selected ? "hsl(var(--primary))" : "hsl(var(--border))",
        boxShadow: selected
          ? "0 0 0 2px hsl(var(--primary))"
          : "0 1px 3px rgba(0,0,0,0.1)"
      }}
      transition={{ duration: 0.2 }}
      className="bg-card rounded-lg border p-4 cursor-pointer"
    >
      {children}
    </motion.div>
  )
}
```

## Key Points

1. Use `whileHover` for mouse hover effects
2. Use `whileTap` for click/touch feedback
3. Keep duration short (0.15-0.2s) for responsive feel
4. Combine with scale and shadow for depth
5. Add subtle animations, don't overdo it
