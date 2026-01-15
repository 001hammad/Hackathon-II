# Animations Reference

Animation patterns, transitions, and motion design for shadcn/ui components.

## Tailwind Animate

shadcn/ui uses `tailwindcss-animate` for animations.

```bash
npm install tailwindcss-animate
```

## Built-in Animations

### Accordion Animations

```css
@keyframes accordion-down {
  from { height: 0 }
  to { height: var(--radix-accordion-content-height) }
}

@keyframes accordion-up {
  from { height: var(--radix-accordion-content-height) }
  to { height: 0 }
}
```

### Spin Animation

```tsx
import { Loader2 } from "lucide-react"

<Loader2 className="h-4 w-4 animate-spin" />
```

### Pulse Animation

```tsx
<div className="animate-pulse">Loading...</div>
```

### Bounce Animation

```tsx
<div className="animate-bounce">Notification</div>
```

## Custom Animations

### Fade In

```tsx
<div className="animate-in fade-in duration-200">
  Content
</div>
```

### Slide In

```tsx
<div className="animate-in slide-in-from-bottom duration-300">
  Modal Content
</div>
```

### Scale In

```tsx
<div className="animate-in zoom-in-95 duration-200">
  Popover
</div>
```

## Framer Motion Integration

```bash
npm install framer-motion
```

```tsx
import { motion } from "framer-motion"

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.2 }}
>
  Content
</motion.div>
```

## Animation Best Practices

1. **Keep it subtle** - Don't distract from content
2. **Use appropriate duration** - 200-300ms for most UI
3. **Respect reduced motion** - Check `prefers-reduced-motion`
4. **Animate transform and opacity** - Better performance
5. **Use easing functions** - `ease-out` for entrances, `ease-in` for exits
