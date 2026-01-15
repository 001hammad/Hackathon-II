# Modal & Dialog Animations

Enter/exit animations for modals, dialogs, and overlays.

## Basic Modal Animation

```tsx
"use client"

import { motion, AnimatePresence } from "framer-motion"

export function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50"
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
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

## Slide Modal Animation

```tsx
"use client"

import { motion, AnimatePresence } from "framer-motion"

export function SlideModal({ isOpen, onClose, children, side = "bottom" }) {
  const sideVariants = {
    bottom: {
      initial: { y: "100%" },
      animate: { y: 0 },
      exit: { y: "100%" }
    },
    right: {
      initial: { x: "100%" },
      animate: { x: 0 },
      exit: { x: "100%" }
    },
    left: {
      initial: { x: "-100%" },
      animate: { x: 0 },
      exit: { x: "-100%" }
    }
  }

  const sideStyles = {
    bottom: "bottom-0 left-0 right-0 rounded-t-lg",
    right: "right-0 top-0 bottom-0 rounded-l-lg",
    left: "left-0 top-0 bottom-0 rounded-r-lg"
  }

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
            initial={sideVariants[side].initial}
            animate={sideVariants[side].animate}
            exit={sideVariants[side].exit}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className={`fixed p-6 bg-background shadow-lg ${sideStyles[side]}`}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Confirm Dialog Animation

```tsx
"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"

export function ConfirmDialog({ isOpen, onConfirm, onCancel, title, message }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 m-auto w-full max-w-sm h-fit p-6 bg-background rounded-lg shadow-lg"
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h2 className="text-lg font-semibold mb-2">{title}</h2>
              <p className="text-muted-foreground mb-4">{message}</p>

              <div className="flex gap-3 justify-end">
                <Button variant="outline" onClick={onCancel}>
                  Cancel
                </Button>
                <Button variant="destructive" onClick={onConfirm}>
                  Confirm
                </Button>
              </div>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Toast Notification Animation

```tsx
"use client"

import { motion, AnimatePresence } from "framer-motion"

export function Toast({ toasts, onDismiss }) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      <AnimatePresence mode="popLayout">
        {toasts.map((toast, index) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, x: 100, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.9 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className={`p-4 rounded-lg shadow-lg ${
              toast.type === "success"
                ? "bg-green-500 text-white"
                : toast.type === "error"
                ? "bg-destructive text-white"
                : "bg-background border"
            }`}
          >
            <div className="flex items-center justify-between gap-4">
              <p>{toast.message}</p>
              <button onClick={() => onDismiss(toast.id)}>×</button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
```

## Key Points

1. Always wrap modals in `AnimatePresence`
2. Use `initial`, `animate`, `exit` for full lifecycle
3. Add backdrop with click-to-close
4. Use `scale` and `opacity` for smooth modal entry
5. Keep animation duration under 0.3s for responsiveness
