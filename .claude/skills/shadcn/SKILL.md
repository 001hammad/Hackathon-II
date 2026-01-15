---
name: shadcn-ui
description: Comprehensive shadcn/ui component library with theming, customization, accessibility, and patterns. Use proactively when building any UI in Phase 2 web app. Always use shadcn/ui components from @/components/ui/.
---

# shadcn/ui Expert for Todo App

Beautiful, accessible components built with Radix UI and Tailwind CSS.

## What is shadcn/ui?

shadcn/ui is **not a traditional component library**. Instead, it's a collection of re-usable components that you can copy and paste into your apps. The components:
- Live in your codebase (`components/ui/`)
- Are fully customizable
- Built with Radix UI primitives
- Styled with Tailwind CSS
- Are accessible by default
- Support theming out of the box

## Quick Start Installation

```bash
# Initialize shadcn in the project
npx shadcn@latest init

# During initialization, configure:
# - TypeScript: Yes
# - Style: Default (or New York)
# - Base color: Slate, Zinc, or your preference
# - Global CSS: app/globals.css
# - CSS variables: Yes (recommended)
# - Tailwind config: tailwind.config.ts
# - Components directory: @/components
# - Utils directory: @/lib/utils
```

```bash
# Add components as needed
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add table
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add checkbox
npx shadcn@latest add select
npx shadcn@latest add badge
npx shadcn@latest add toast
npx shadcn@latest add calendar
npx shadcn@latest add popover
npx shadcn@latest add sheet
npx shadcn@latest add textarea
npx shadcn@latest add avatar
npx shadcn@latest add alert
npx shadcn@latest add tabs
npx shadcn@latest add accordion
npx shadcn@latest add separator
npx shadcn@latest add scroll-area

# Add multiple at once
npx shadcn@latest add button card input label form
```

## Essential Components for Todo App

### Forms & Inputs
- **Button** - Actions, submissions, triggers
- **Input** - Text input fields
- **Textarea** - Multi-line text input
- **Label** - Form field labels
- **Form** - Form wrapper with validation
- **Checkbox** - Task completion toggles
- **Select** - Dropdown selections
- **Calendar** - Date picker for due dates
- **Switch** - Toggle settings

### Data Display
- **Card** - Task cards, containers
- **Table** - Task list view
- **Badge** - Status indicators, tags
- **Avatar** - User profile pictures
- **Separator** - Visual dividers
- **Accordion** - Collapsible sections

### Navigation
- **Tabs** - Multiple views (All, Active, Completed)
- **Dropdown Menu** - User menu, actions
- **Sheet** - Mobile sidebar drawer
- **Dialog** - Modals, confirmations
- **Popover** - Contextual information

### Feedback
- **Toast** - Success/error notifications
- **Alert** - Important messages
- **Progress** - Loading indicators
- **Skeleton** - Loading placeholders

## Component Usage Patterns

### 1. Button Variants

```tsx
import { Button } from "@/components/ui/button"

// Primary button (default)
<Button>Save Task</Button>

// Secondary button
<Button variant="secondary">Cancel</Button>

// Destructive button
<Button variant="destructive">Delete</Button>

// Outline button
<Button variant="outline">Edit</Button>

// Ghost button
<Button variant="ghost">More</Button>

// Link button
<Button variant="link">Learn More</Button>

// Icon button
<Button size="icon">
  <Plus className="h-4 w-4" />
</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Saving...
</Button>
```

### 2. Card Component

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Task Title</CardTitle>
    <CardDescription>Task description or metadata</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main task content goes here</p>
  </CardContent>
  <CardFooter>
    <Button>Complete</Button>
  </CardFooter>
</Card>
```

### 3. Form with Validation

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  title: z.string().min(1, "Title is required"),
})

function TaskForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { title: "" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Task Title</FormLabel>
              <FormControl>
                <Input placeholder="Buy groceries" {...field} />
              </FormControl>
              <FormDescription>Enter your task title</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Create Task</Button>
      </form>
    </Form>
  )
}
```

### 4. Dialog (Modal)

```tsx
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Delete Task</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone. This will permanently delete your task.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button variant="destructive">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 5. Dropdown Menu

```tsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { MoreHorizontal } from "lucide-react"

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon">
      <MoreHorizontal className="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuLabel>Actions</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Edit</DropdownMenuItem>
    <DropdownMenuItem>Duplicate</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### 6. Toast Notifications

```tsx
import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"

function TaskActions() {
  const { toast } = useToast()

  return (
    <Button
      onClick={() => {
        toast({
          title: "Task created",
          description: "Your task has been created successfully.",
        })
      }}
    >
      Create Task
    </Button>
  )
}

// Error toast
toast({
  variant: "destructive",
  title: "Error",
  description: "Failed to create task. Please try again.",
})

// Success with action
toast({
  title: "Task deleted",
  description: "Task was removed from your list.",
  action: <Button variant="outline" size="sm">Undo</Button>,
})
```

### 7. Tabs for Views

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

<Tabs defaultValue="all">
  <TabsList>
    <TabsTrigger value="all">All Tasks</TabsTrigger>
    <TabsTrigger value="active">Active</TabsTrigger>
    <TabsTrigger value="completed">Completed</TabsTrigger>
  </TabsList>
  <TabsContent value="all">
    <AllTasksList />
  </TabsContent>
  <TabsContent value="active">
    <ActiveTasksList />
  </TabsContent>
  <TabsContent value="completed">
    <CompletedTasksList />
  </TabsContent>
</Tabs>
```

### 8. Badge for Status

```tsx
import { Badge } from "@/components/ui/badge"

// Default
<Badge>Pending</Badge>

// Secondary
<Badge variant="secondary">In Progress</Badge>

// Destructive
<Badge variant="destructive">Overdue</Badge>

// Outline
<Badge variant="outline">Draft</Badge>

// With icon
<Badge>
  <Clock className="mr-1 h-3 w-3" />
  Due Soon
</Badge>
```

## Theming & Customization

### CSS Variables Approach

shadcn/ui uses CSS variables for theming, defined in `app/globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode colors */
  }
}
```

### Dark Mode Toggle

```tsx
"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

### Install next-themes

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
"use client"

import { ThemeProvider } from "next-themes"

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}

// app/layout.tsx
import { Providers } from "./providers"

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

## Accessibility Checklist

✅ **Keyboard navigation** - All interactive elements accessible via keyboard
✅ **Visible focus states** - Clear focus indicators on all focusable elements
✅ **WCAG AA contrast** - Sufficient color contrast ratios
✅ **ARIA labels** - Proper labels for screen readers
✅ **Screen reader support** - Semantic HTML and ARIA attributes
✅ **Reduced motion respect** - Respects `prefers-reduced-motion`

### Accessibility Best Practices

1. **Always use semantic HTML**
```tsx
// Good
<button onClick={handleClick}>Click me</button>

// Bad
<div onClick={handleClick}>Click me</div>
```

2. **Add ARIA labels for icon-only buttons**
```tsx
<Button size="icon" aria-label="Delete task">
  <Trash className="h-4 w-4" />
</Button>
```

3. **Use proper heading hierarchy**
```tsx
<h1>Dashboard</h1>
  <h2>My Tasks</h2>
    <h3>Task Title</h3>
```

4. **Provide form labels**
```tsx
<FormLabel htmlFor="title">Task Title</FormLabel>
<Input id="title" {...field} />
```

5. **Use live regions for dynamic updates**
```tsx
<div role="status" aria-live="polite">
  {successMessage}
</div>
```

## Component Customization

### Using cn() for Conditional Classes

```tsx
import { cn } from "@/lib/utils"

<Card
  className={cn(
    "p-4",
    task.completed && "opacity-50",
    task.overdue && "border-red-500"
  )}
>
  {/* Card content */}
</Card>
```

### Creating Custom Variants

```tsx
// components/ui/button.tsx
const buttonVariants = cva(
  "base-classes",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        destructive: "bg-destructive text-destructive-foreground",
        // Add custom variant
        success: "bg-green-600 text-white hover:bg-green-700",
      },
    },
  }
)

// Usage
<Button variant="success">Complete Task</Button>
```

## Icons with Lucide React

shadcn/ui uses Lucide React for icons:

```bash
npm install lucide-react
```

```tsx
import { Check, X, Clock, Calendar, Trash2, Edit, Plus, Search, Filter } from "lucide-react"

<Button>
  <Plus className="mr-2 h-4 w-4" />
  New Task
</Button>

<Badge>
  <Clock className="mr-1 h-3 w-3" />
  Due Soon
</Badge>
```

## Common Patterns for Todo App

### Task Card Pattern
```tsx
<Card>
  <CardHeader className="flex flex-row items-start justify-between space-y-0">
    <div className="flex items-center space-x-2">
      <Checkbox checked={task.completed} />
      <CardTitle className={task.completed ? "line-through" : ""}>
        {task.title}
      </CardTitle>
    </div>
    <DropdownMenu>
      {/* Actions menu */}
    </DropdownMenu>
  </CardHeader>
  <CardContent>
    <p className="text-sm text-muted-foreground">{task.description}</p>
  </CardContent>
  <CardFooter className="flex gap-2">
    <Badge>{task.status}</Badge>
    {task.dueDate && (
      <Badge variant="outline">
        <Calendar className="mr-1 h-3 w-3" />
        {formatDate(task.dueDate)}
      </Badge>
    )}
  </CardFooter>
</Card>
```

### Form Pattern
```tsx
<Card>
  <CardHeader>
    <CardTitle>Create New Task</CardTitle>
  </CardHeader>
  <CardContent>
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* Form fields */}
      </form>
    </Form>
  </CardContent>
</Card>
```

### Empty State Pattern
```tsx
<div className="flex flex-col items-center justify-center py-12">
  <div className="rounded-full bg-muted p-3 mb-4">
    <CheckSquare className="h-6 w-6 text-muted-foreground" />
  </div>
  <h3 className="font-semibold text-lg mb-2">No tasks yet</h3>
  <p className="text-sm text-muted-foreground mb-4">
    Get started by creating your first task
  </p>
  <Button>
    <Plus className="mr-2 h-4 w-4" />
    New Task
  </Button>
</div>
```

## Additional Resources

- **Examples**: See `examples/` for complete patterns
- **Reference**: See `reference/` for detailed guides
- **Templates**: See `templates/` for starter files
- **Official Docs**: https://ui.shadcn.com
- **Radix UI Docs**: https://www.radix-ui.com
- **Tailwind CSS Docs**: https://tailwindcss.com

## Key Principles

1. **Always use shadcn/ui components** from `@/components/ui/`
2. **Customize freely** - components live in your codebase
3. **Maintain accessibility** - test keyboard navigation and screen readers
4. **Use consistent patterns** - follow examples from this skill
5. **Leverage theming** - use CSS variables for consistent design
6. **Add proper types** - TypeScript for all component props
7. **Test responsiveness** - mobile, tablet, desktop
