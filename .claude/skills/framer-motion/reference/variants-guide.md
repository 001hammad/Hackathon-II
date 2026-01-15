# Variants Guide

Reusable animation definitions with variants.

## Basic Variants

```tsx
const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

const fadeOut = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 }
}

// Usage
<motion.div
  variants={fadeIn}
  initial="hidden"
  animate="visible"
>
  Content
</motion.div>
```

## Combined Fade In/Out

```tsx
const fadeInOut = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 }
}

// Usage with AnimatePresence
<AnimatePresence>
  <motion.div variants={fadeInOut} initial="hidden" animate="visible" exit="hidden">
    Content
  </motion.div>
</AnimatePresence>
```

## Slide Variants

```tsx
const slideInUp = {
  hidden: { opacity: 0, y: 50 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: "easeOut" }
  },
  exit: {
    opacity: 0,
    y: -50,
    transition: { duration: 0.2 }
  }
}

const slideInLeft = {
  hidden: { opacity: 0, x: -50 },
  visible: { opacity: 1, x: 0 }
}

const slideInRight = {
  hidden: { opacity: 0, x: 50 },
  visible: { opacity: 1, x: 0 }
}
```

## Scale Variants

```tsx
const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: { opacity: 1, scale: 1 }
}

const popIn = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { type: "spring", bounce: 0.3 }
  }
}
```

## Stagger Container

```tsx
const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
}

const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}
```

## Variants with Conditional Properties

```tsx
const hoverScale = {
  scale: 1,
  transition: { duration: 0.2 }
}

const hoverCard = {
  scale: 1,
  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  transition: { duration: 0.2 }
}

<motion.div
  whileHover={{ scale: 1.02, boxShadow: "0 4px 12px rgba(0,0,0,0.15)" }}
>
  Content
</motion.div>
```

## Key Points

1. Variants are reusable animation definitions
2. Use descriptive names (fadeIn, slideUp, staggerContainer)
3. Include `hidden`, `visible`, `exit` states
4. Define transition timing in variants
5. Use `staggerChildren` for list animations
