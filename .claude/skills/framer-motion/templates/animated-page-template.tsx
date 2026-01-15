// Animated Page Template
// Copy to components/animations/AnimatedPage.tsx

"use client"

import { motion } from "framer-motion"
import { useReducedMotion } from "framer-motion"

const pageVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: "easeOut" }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.2 }
  }
}

const reducedVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 }
}

interface AnimatedPageProps {
  children: React.ReactNode
}

export function AnimatedPage({ children }: AnimatedPageProps) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      variants={shouldReduceMotion ? reducedVariants : pageVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      {children}
    </motion.div>
  )
}

// Usage in app/template.tsx
/*
import { AnimatedPage } from "@/components/animations/AnimatedPage"

export default function Template({ children }) {
  return <AnimatedPage>{children}</AnimatedPage>
}
*/
