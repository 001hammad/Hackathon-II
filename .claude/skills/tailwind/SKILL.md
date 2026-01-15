---
name: tailwind-css
description: Expert in Tailwind CSS best practices, responsive design, dark mode, cn() utility, theming, and styling patterns. Use proactively when styling any component in Phase 2 web app.
---

# Tailwind CSS Expert for Todo App

Master utility-first CSS with Tailwind for building modern, responsive UIs.

## Core Principles

### All Styling Must Use Tailwind CSS

❌ **NO inline styles**
```tsx
<div style={{ color: 'red' }}>Bad</div>
```

❌ **NO separate CSS files**
```css
/* styles.css - Don't do this */
.my-class { color: red; }
```

✅ **YES - Tailwind utility classes**
```tsx
<div className="text-red-500">Good</div>
```

### Use cn() Utility for Class Merging

```tsx
import { cn } from "@/lib/utils"

// Merge classes intelligently, handles conflicts
<div className={cn(
  "base-class",
  condition && "conditional-class",
  "override-class"
)}>
  Content
</div>
```

### Mobile-First Responsive Design

Always start with mobile, then add breakpoints:

```tsx
// Mobile first (no prefix) → Tablet (md:) → Desktop (lg:)
<div className="w-full md:w-1/2 lg:w-1/3">
  Responsive width
</div>
```

### Dark Mode with "class" Strategy

```tsx
// Light and dark mode variants
<div className="bg-white dark:bg-slate-900 text-black dark:text-white">
  Adapts to theme
</div>
```

## Quick Start

### Tailwind Config (tailwind.config.ts)

```typescript
import type { Config } from "tailwindcss"
import animate from "tailwindcss-animate"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [animate],
}

export default config
```

### Global CSS (app/globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
```

## Essential Tailwind Patterns

### 1. Layout Patterns

```tsx
// Flexbox
<div className="flex items-center justify-between gap-4">
  <span>Left</span>
  <span>Right</span>
</div>

// Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

// Container
<div className="container mx-auto px-4 md:px-6 lg:px-8">
  Centered container with padding
</div>

// Stack
<div className="space-y-4">
  <div>Stacked item 1</div>
  <div>Stacked item 2</div>
</div>
```

### 2. Typography Patterns

```tsx
// Headings
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight">
  Page Title
</h1>

<h2 className="text-2xl md:text-3xl font-semibold">
  Section Title
</h2>

// Body text
<p className="text-sm md:text-base text-muted-foreground leading-relaxed">
  Body text with good readability
</p>

// Truncate
<p className="truncate">
  Very long text that will be cut off with ellipsis...
</p>

// Line clamp
<p className="line-clamp-3">
  Text that shows only 3 lines then adds ellipsis
</p>
```

### 3. Color Patterns

```tsx
// Semantic colors
<div className="bg-primary text-primary-foreground">Primary</div>
<div className="bg-secondary text-secondary-foreground">Secondary</div>
<div className="bg-destructive text-destructive-foreground">Destructive</div>
<div className="bg-muted text-muted-foreground">Muted</div>

// Borders
<div className="border border-border">With border</div>
<div className="ring-2 ring-ring ring-offset-2">With ring</div>

// Hover states
<button className="bg-primary hover:bg-primary/90 transition-colors">
  Hover me
</button>
```

### 4. Spacing Patterns

```tsx
// Padding
<div className="p-4 md:p-6 lg:p-8">Responsive padding</div>
<div className="px-4 py-2">Horizontal and vertical</div>

// Margin
<div className="mt-4 mb-6">Margin top and bottom</div>
<div className="mx-auto">Center horizontally</div>

// Gap (in flex/grid)
<div className="flex gap-4">Items with gap</div>
<div className="grid gap-x-4 gap-y-6">Grid with different gaps</div>

// Space between
<div className="flex flex-col space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### 5. Responsive Design Patterns

```tsx
// Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px)

// Hide/show at breakpoints
<div className="hidden md:block">Desktop only</div>
<div className="block md:hidden">Mobile only</div>

// Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  Cards
</div>

// Responsive flex direction
<div className="flex flex-col md:flex-row gap-4">
  Stacked on mobile, side-by-side on desktop
</div>

// Responsive text size
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">
  Scales with screen size
</h1>
```

### 6. Dark Mode Patterns

```tsx
// Background and text
<div className="bg-white dark:bg-slate-900 text-black dark:text-white">
  Adapts to theme
</div>

// Borders
<div className="border border-gray-200 dark:border-gray-800">
  Border changes with theme
</div>

// Hover in dark mode
<button className="hover:bg-gray-100 dark:hover:bg-gray-800">
  Hover adapts
</button>

// Use semantic colors (automatically adapt)
<div className="bg-background text-foreground">
  Automatically adapts to theme
</div>
```

### 7. Card Pattern

```tsx
<div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
  <h3 className="font-semibold text-lg mb-2">Task Title</h3>
  <p className="text-sm text-muted-foreground mb-4">
    Task description
  </p>
  <div className="flex gap-2">
    <span className="text-xs bg-secondary px-2 py-1 rounded">Tag</span>
  </div>
</div>
```

### 8. Button Patterns

```tsx
// Primary button
<button className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50">
  Click me
</button>

// Secondary button
<button className="inline-flex items-center justify-center rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground hover:bg-secondary/80 transition-colors">
  Secondary
</button>

// Outline button
<button className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground transition-colors">
  Outline
</button>

// Ghost button
<button className="inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground transition-colors">
  Ghost
</button>
```

### 9. Form Patterns

```tsx
// Input field
<input
  type="text"
  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
  placeholder="Enter text"
/>

// Textarea
<textarea
  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
  placeholder="Enter description"
/>

// Label
<label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
  Task Title
</label>
```

### 10. State Patterns

```tsx
// Hover
<div className="hover:bg-accent transition-colors cursor-pointer">
  Hover me
</div>

// Focus
<input className="focus:ring-2 focus:ring-ring focus:ring-offset-2" />

// Active
<button className="active:scale-95 transition-transform">
  Press me
</button>

// Disabled
<button className="disabled:opacity-50 disabled:cursor-not-allowed" disabled>
  Disabled
</button>

// Group hover
<div className="group">
  <span className="group-hover:text-primary transition-colors">
    Hover parent to change me
  </span>
</div>
```

## cn() Utility Function

Essential for merging Tailwind classes:

```tsx
// lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Usage Examples

```tsx
import { cn } from "@/lib/utils"

// Conditional classes
<div className={cn(
  "base-class",
  isActive && "active-class",
  isError && "error-class"
)}>

// Merge with props
<div className={cn("default-classes", className)}>

// Handle conflicts (twMerge resolves)
<div className={cn(
  "p-4",      // padding: 1rem
  "p-6"       // padding: 1.5rem (wins)
)}>
```

## Common Tailwind Patterns for Todo App

### Task Card

```tsx
<div className={cn(
  "rounded-lg border bg-card text-card-foreground shadow-sm p-4",
  "hover:shadow-md transition-shadow",
  task.completed && "opacity-60"
)}>
  <div className="flex items-start gap-3">
    <div className="flex-1">
      <h3 className={cn(
        "font-semibold text-base",
        task.completed && "line-through text-muted-foreground"
      )}>
        {task.title}
      </h3>
      {task.description && (
        <p className="text-sm text-muted-foreground mt-1">
          {task.description}
        </p>
      )}
    </div>
  </div>
</div>
```

### Empty State

```tsx
<div className="flex flex-col items-center justify-center py-16 px-4">
  <div className="rounded-full bg-muted p-6 mb-4">
    <CheckSquare className="h-10 w-10 text-muted-foreground" />
  </div>
  <h3 className="text-xl font-semibold mb-2">No tasks yet</h3>
  <p className="text-sm text-muted-foreground text-center max-w-sm mb-6">
    Get started by creating your first task
  </p>
  <button className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">
    Create Task
  </button>
</div>
```

## Best Practices

1. **Always use mobile-first** - Start with base styles, add md:, lg: breakpoints
2. **Use semantic colors** - bg-background, text-foreground, etc. (auto dark mode)
3. **Use cn() for conditional classes** - Handles conflicts and conditions
4. **Add transitions** - transition-colors, transition-transform for smooth UX
5. **Focus states** - Always add focus-visible:ring for accessibility
6. **Consistent spacing** - Use Tailwind's spacing scale (4, 6, 8, etc.)
7. **Responsive gaps** - gap-4 md:gap-6 for flexible layouts

## Common Mistakes to Avoid

❌ **Don't mix custom CSS with Tailwind**
❌ **Don't use arbitrary values excessively** - [#ff0000] (use theme colors)
❌ **Don't forget dark mode variants**
❌ **Don't skip responsive design**
❌ **Don't use !important** (use proper specificity)

## Additional Resources

- See `examples/` for complete pattern implementations
- See `reference/` for detailed guides and cheatsheets
- See `templates/` for ready-to-use configs

## Key Principles Summary

1. **Utility-first** - Use Tailwind classes only
2. **Mobile-first** - Base → md → lg → xl
3. **Semantic colors** - Use theme variables
4. **cn() for merging** - Handle conflicts intelligently
5. **Dark mode ready** - Use dark: prefix or semantic colors
6. **Responsive always** - Test mobile, tablet, desktop
7. **Accessibility** - Focus states, ARIA, contrast
