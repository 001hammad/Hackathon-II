# Navigation Patterns

Navigation patterns using Dropdown Menu, Sheet, Tabs, and other navigation components.

## Dropdown Menu Pattern

```tsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger, DropdownMenuShortcut } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { User, Settings, LogOut, HelpCircle } from "lucide-react"

export function UserMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <User className="h-5 w-5" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem>
          <User className="mr-2 h-4 w-4" />
          Profile
          <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <Settings className="mr-2 h-4 w-4" />
          Settings
          <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <HelpCircle className="mr-2 h-4 w-4" />
          Help
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem className="text-destructive">
          <LogOut className="mr-2 h-4 w-4" />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

## Sheet (Mobile Drawer) Pattern

```tsx
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

export function MobileMenu() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>Menu</SheetTitle>
          <SheetDescription>Navigate to different sections</SheetDescription>
        </SheetHeader>
        <nav className="flex flex-col gap-4 mt-4">
          <Button variant="ghost" className="justify-start">
            Dashboard
          </Button>
          <Button variant="ghost" className="justify-start">
            Tasks
          </Button>
          <Button variant="ghost" className="justify-start">
            Settings
          </Button>
        </nav>
      </SheetContent>
    </Sheet>
  )
}
```

## Tabs Pattern

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function TaskTabs() {
  return (
    <Tabs defaultValue="all" className="w-full">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="all">All</TabsTrigger>
        <TabsTrigger value="active">Active</TabsTrigger>
        <TabsTrigger value="completed">Completed</TabsTrigger>
      </TabsList>
      <TabsContent value="all">
        <Card>
          <CardHeader>
            <CardTitle>All Tasks</CardTitle>
            <CardDescription>View all your tasks</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Task list */}
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="active">
        <Card>
          <CardHeader>
            <CardTitle>Active Tasks</CardTitle>
            <CardDescription>Tasks that are in progress</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Active tasks */}
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="completed">
        <Card>
          <CardHeader>
            <CardTitle>Completed Tasks</CardTitle>
            <CardDescription>Tasks you have finished</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Completed tasks */}
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  )
}
```

## Command Menu (Quick Search)

```tsx
"use client"

import { Command, CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { useState, useEffect } from "react"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"

export function TaskSearch() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  return (
    <>
      <Button
        variant="outline"
        className="w-full justify-start text-muted-foreground"
        onClick={() => setOpen(true)}
      >
        <Search className="mr-2 h-4 w-4" />
        Search tasks...
        <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
          <span className="text-xs">⌘</span>K
        </kbd>
      </Button>
      <CommandDialog open={open} onOpenChange={setOpen}>
        <CommandInput placeholder="Type a command or search..." />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          <CommandGroup heading="Tasks">
            <CommandItem>Buy groceries</CommandItem>
            <CommandItem>Finish project</CommandItem>
            <CommandItem>Call dentist</CommandItem>
          </CommandGroup>
          <CommandGroup heading="Actions">
            <CommandItem>Create new task</CommandItem>
            <CommandItem>View settings</CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  )
}
```

## Sidebar Navigation

```tsx
"use client"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Home, ListTodo, Settings, User } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

export function Sidebar() {
  const pathname = usePathname()

  const links = [
    { href: "/", label: "Dashboard", icon: Home },
    { href: "/tasks", label: "Tasks", icon: ListTodo },
    { href: "/profile", label: "Profile", icon: User },
    { href: "/settings", label: "Settings", icon: Settings },
  ]

  return (
    <div className="w-64 border-r bg-muted/40 p-4">
      <nav className="space-y-2">
        {links.map((link) => {
          const Icon = link.icon
          const isActive = pathname === link.href

          return (
            <Button
              key={link.href}
              asChild
              variant={isActive ? "secondary" : "ghost"}
              className={cn(
                "w-full justify-start",
                isActive && "bg-secondary"
              )}
            >
              <Link href={link.href}>
                <Icon className="mr-2 h-4 w-4" />
                {link.label}
              </Link>
            </Button>
          )
        })}
      </nav>
    </div>
  )
}
```

## Breadcrumb Navigation

```tsx
import { ChevronRight, Home } from "lucide-react"
import Link from "next/link"

export function TaskBreadcrumb({ task }) {
  return (
    <nav className="flex items-center space-x-2 text-sm text-muted-foreground">
      <Link href="/" className="hover:text-foreground">
        <Home className="h-4 w-4" />
      </Link>
      <ChevronRight className="h-4 w-4" />
      <Link href="/tasks" className="hover:text-foreground">
        Tasks
      </Link>
      <ChevronRight className="h-4 w-4" />
      <span className="text-foreground">{task.title}</span>
    </nav>
  )
}
```

## Pagination Pattern

```tsx
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"

export function Pagination({ currentPage, totalPages, onPageChange }) {
  return (
    <div className="flex items-center justify-between">
      <p className="text-sm text-muted-foreground">
        Page {currentPage} of {totalPages}
      </p>
      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          <ChevronLeft className="h-4 w-4 mr-1" />
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
          <ChevronRight className="h-4 w-4 ml-1" />
        </Button>
      </div>
    </div>
  )
}
```

## Key Takeaways

1. **Dropdown Menu for actions** - Compact way to show multiple options
2. **Sheet for mobile** - Drawer pattern for small screens
3. **Tabs for views** - Switch between different data views
4. **Command for search** - Quick access with keyboard shortcuts
5. **Sidebar for main navigation** - Persistent navigation for desktop
6. **Breadcrumb for context** - Show user location in hierarchy
7. **Pagination for large lists** - Navigate through pages of data
