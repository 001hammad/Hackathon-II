# Dark Mode Patterns

Complete dark mode implementation using Tailwind's class strategy.

## Setup

```tsx
// tailwind.config.ts
export default {
  darkMode: ["class"],
  // ...
}
```

## Basic Dark Mode

```tsx
<div className="bg-white dark:bg-slate-900 text-black dark:text-white">
  Adapts to theme
</div>
```

## Semantic Colors (Auto Dark Mode)

```tsx
// Use semantic colors - automatically adapt
<div className="bg-background text-foreground">
  Background color adapts
</div>

<div className="bg-card text-card-foreground">
  Card colors adapt
</div>
```

## Borders and Shadows

```tsx
<div className="border border-gray-200 dark:border-gray-800">
  Border adapts
</div>

<div className="shadow-md dark:shadow-lg dark:shadow-slate-900/50">
  Shadow adapts
</div>
```

## Hover States

```tsx
<button className="hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
  Hover adapts to theme
</button>
```

## Input Fields

```tsx
<input
  className="bg-white dark:bg-slate-900 border-gray-300 dark:border-gray-700 text-black dark:text-white"
  type="text"
/>
```

## Complete Card Example

```tsx
<div className="rounded-lg border border-border bg-card text-card-foreground shadow-sm p-6">
  <h3 className="font-semibold text-lg mb-2">Task Title</h3>
  <p className="text-sm text-muted-foreground">Description</p>
</div>
```

## Theme Toggle Component

```tsx
"use client"

import { useTheme } from "next-themes"
import { Moon, Sun } from "lucide-react"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="p-2 rounded-md hover:bg-accent"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 dark:-rotate-90 dark:scale-0 transition-transform" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 dark:rotate-0 dark:scale-100 transition-transform" />
    </button>
  )
}
```

## Best Practices

1. Use semantic colors from theme (bg-background, text-foreground)
2. Test both light and dark modes
3. Ensure proper contrast in both modes
4. Use dark: prefix for specific overrides
5. Transitions for smooth theme switches
