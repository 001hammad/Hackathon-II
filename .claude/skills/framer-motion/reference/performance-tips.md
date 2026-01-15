# Performance Tips

Optimizing Framer Motion for smooth, performant animations.

## GPU Acceleration

### Use transform and opacity

```tsx
// ✅ Good - GPU accelerated
<motion.div
  initial={{ opacity: 0, x: 0, y: 0 }}
  animate={{ opacity: 1, x: 100, y: 50 }}
>
  Content
</motion.div>

// ❌ Bad - Triggers layout recalculation
<motion.div
  initial={{ width: 0, height: 0 }}
  animate={{ width: 100, height: 100 }}
>
  Content
</motion.div>
```

### Properties that trigger layout (avoid)

- `width`, `height`
- `top`, `left`, `right`, `bottom`
- `margin`, `padding`
- `border`

### Safe properties to animate

- `opacity`
- `transform` (`x`, `y`, `scale`, `rotate`)
- `filter` (blur, grayscale)

## Reduce Paint Operations

```tsx
// ✅ Use will-change hint
<motion.div
  will-change="transform, opacity"
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
>
  Content
</motion.div>

// ❌ Don't overuse will-change
// Only add when animation is actively running
```

## Limit Animated Elements

```tsx
// ❌ Don't animate too many elements
{tasks.map(task => (
  <motion.div
    key={task.id}
    whileHover={{ scale: 1.05 }}  // Expensive on hover!
    // This can cause performance issues with many items
  >
    {task.title}
  </motion.div>
))}

// ✅ Use variants with stagger instead
<motion.div
  variants={containerVariants}
  initial="hidden"
  animate="show"
>
  {tasks.map(task => (
    <motion.div key={task.id} variants={itemVariants}>
      {/* No hover on individual items */}
    </motion.div>
  ))}
</motion.div>
```

## Optimize Layout Animations

```tsx
// ✅ Use layout sparingly
<motion.div layout>
  {/* Only use when position actually changes */}
</motion.div>

// ❌ Don't wrap everything in layout
<motion.div layout>
  <StaticContent />
</motion.div>
```

## Use useMemo for Variants

```tsx
import { useMemo } from "react"
import { motion } from "framer-motion"

const variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

// ✅ Good - Memoize variants
const MemoizedList = ({ items }) => {
  const itemVariants = useMemo(() => ({
    hidden: { opacity: 0 },
    visible: { opacity: 1 }
  }), [])

  return (
    <motion.div variants={itemVariants}>
      {items.map(item => (
        <motion.div key={item.id}>{item.name}</motion.div>
      ))}
    </motion.div>
  )
}
```

## Debounce Expensive Animations

```tsx
import { useMotionValue, useTransform, useSpring } from "framer-motion"

// Use spring for smooth physics-based animations
const x = useMotionValue(0)
const springConfig = { damping: 20, stiffness: 100 }
const xSpring = useSpring(x, springConfig)
```

## Reduce Animation Frequency

```tsx
// ❌ Animate on every frame
<motion.div
  animate={{ x: mousePosition.x }}
  transition={{ type: "tween" }}
>
  Content
</motion.div>

// ✅ Use spring for smoother follow
<motion.div
  style={{ x: useSpring(mousePosition.x) }}
>
  Content
</motion.div>
```

## Animation Checklist

- [ ] Use `transform` (x, y, scale, rotate) not layout properties
- [ ] Use `opacity` for fade effects
- [ ] Limit number of animated elements
- [ ] Use `will-change` sparingly
- [ ] Use variants for reuse
- [ ] Avoid `layout` prop unless needed
- [ ] Consider using CSS animations for simple cases
- [ ] Test on low-end devices
- [ ] Use `AnimatePresence` carefully (can cause performance issues)
