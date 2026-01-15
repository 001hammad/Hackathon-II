# Theming Reference

Complete guide to theming shadcn/ui components with CSS variables, dark mode, and custom color schemes.

## CSS Variables System

shadcn/ui uses CSS variables defined in HSL format for easy theming.

### Light Theme (app/globals.css)

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
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
}
```

### Dark Theme

```css
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --popover: 222.2 84% 4.9%;
  --popover-foreground: 210 40% 98%;
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
```

## Dark Mode Setup

### Install next-themes

```bash
npm install next-themes
```

### Create Theme Provider

```tsx
// app/providers.tsx
"use client"

import { ThemeProvider as NextThemesProvider } from "next-themes"
import { type ThemeProviderProps } from "next-themes/dist/types"

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
```

### Wrap App with Provider

```tsx
// app/layout.tsx
import { ThemeProvider } from "./providers"

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### Theme Toggle Component

```tsx
"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function ThemeToggle() {
  const { setTheme } = useTheme()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

## Custom Color Schemes

### Blue Theme Example

```css
:root {
  --primary: 221.2 83.2% 53.3%;  /* Blue */
  --primary-foreground: 210 40% 98%;
}

.dark {
  --primary: 217.2 91.2% 59.8%;  /* Lighter blue for dark mode */
  --primary-foreground: 222.2 47.4% 11.2%;
}
```

### Green Theme Example

```css
:root {
  --primary: 142.1 76.2% 36.3%;  /* Green */
  --primary-foreground: 355.7 100% 97.3%;
}

.dark {
  --primary: 142.1 70.6% 45.3%;  /* Lighter green */
  --primary-foreground: 144.9 80.4% 10%;
}
```

## Theme Customization Tips

1. **Use HSL format** - Easier to adjust lightness/darkness
2. **Maintain contrast** - Ensure WCAG AA compliance
3. **Test both themes** - Check light and dark mode
4. **Use semantic names** - primary, destructive, muted, etc.
5. **Keep consistent** - Similar lightness levels across colors

## Tailwind Integration

shadcn/ui components use Tailwind classes that reference CSS variables:

```tsx
// These classes reference the CSS variables
<div className="bg-background text-foreground">
  <Card className="bg-card text-card-foreground">
    <Button className="bg-primary text-primary-foreground">
      Click me
    </Button>
  </Card>
</div>
```

## Custom Themes

Create multiple themes by adding new classes:

```css
.theme-ocean {
  --primary: 199 89% 48%;
  --secondary: 185 84% 44%;
  --accent: 152 76% 36%;
}

.theme-sunset {
  --primary: 24 95% 53%;
  --secondary: 343 81% 61%;
  --accent: 45 97% 54%;
}
```

Apply with JavaScript:

```tsx
document.documentElement.classList.add('theme-ocean')
```
