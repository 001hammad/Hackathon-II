# Feedback Patterns

User feedback patterns using Toast, Alert, Dialog, and loading states.

## Toast Notifications

```tsx
"use client"

import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"

export function ToastExamples() {
  const { toast } = useToast()

  return (
    <div className="space-y-4">
      {/* Success toast */}
      <Button
        onClick={() => {
          toast({
            title: "Task created",
            description: "Your task has been created successfully.",
          })
        }}
      >
        Success Toast
      </Button>

      {/* Error toast */}
      <Button
        variant="destructive"
        onClick={() => {
          toast({
            variant: "destructive",
            title: "Error",
            description: "Failed to create task. Please try again.",
          })
        }}
      >
        Error Toast
      </Button>

      {/* Toast with action */}
      <Button
        onClick={() => {
          toast({
            title: "Task deleted",
            description: "Task was removed from your list.",
            action: (
              <Button variant="outline" size="sm">
                Undo
              </Button>
            ),
          })
        }}
      >
        Toast with Action
      </Button>
    </div>
  )
}
```

## Alert Messages

```tsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle, CheckCircle2, Info, AlertTriangle } from "lucide-react"

export function AlertExamples() {
  return (
    <div className="space-y-4">
      {/* Info alert */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertTitle>Info</AlertTitle>
        <AlertDescription>
          Your tasks are automatically saved.
        </AlertDescription>
      </Alert>

      {/* Success alert */}
      <Alert className="border-green-500 bg-green-50 text-green-900">
        <CheckCircle2 className="h-4 w-4" />
        <AlertTitle>Success</AlertTitle>
        <AlertDescription>
          All tasks have been completed successfully.
        </AlertDescription>
      </Alert>

      {/* Warning alert */}
      <Alert className="border-yellow-500 bg-yellow-50 text-yellow-900">
        <AlertTriangle className="h-4 w-4" />
        <AlertTitle>Warning</AlertTitle>
        <AlertDescription>
          You have 5 tasks due today.
        </AlertDescription>
      </Alert>

      {/* Error alert */}
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          Failed to sync tasks. Please check your connection.
        </AlertDescription>
      </Alert>
    </div>
  )
}
```

## Confirmation Dialog

```tsx
"use client"

import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { AlertTriangle } from "lucide-react"
import { useState } from "react"

export function DeleteConfirmation({ onConfirm }) {
  const [open, setOpen] = useState(false)

  async function handleConfirm() {
    await onConfirm()
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete Task</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <div className="flex items-center gap-2">
            <div className="rounded-full bg-destructive/10 p-2">
              <AlertTriangle className="h-5 w-5 text-destructive" />
            </div>
            <DialogTitle>Are you sure?</DialogTitle>
          </div>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your task.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button variant="destructive" onClick={handleConfirm}>
            Delete
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

## Loading States

```tsx
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"

// Skeleton loader
export function TaskSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-3/4" />
        <Skeleton className="h-4 w-1/2 mt-2" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6 mt-2" />
      </CardContent>
    </Card>
  )
}

// Spinner loader
export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  )
}

// Button with loading state
export function LoadingButton({ isLoading, children, ...props }) {
  return (
    <Button disabled={isLoading} {...props}>
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {isLoading ? "Loading..." : children}
    </Button>
  )
}
```

## Progress Indicator

```tsx
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function TaskProgress({ completed, total }) {
  const percentage = Math.round((completed / total) * 100)

  return (
    <Card>
      <CardHeader>
        <CardTitle>Task Progress</CardTitle>
        <CardDescription>
          {completed} of {total} tasks completed
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Progress value={percentage} className="w-full" />
        <p className="text-sm text-muted-foreground mt-2">{percentage}%</p>
      </CardContent>
    </Card>
  )
}
```

## Badge Status Indicators

```tsx
import { Badge } from "@/components/ui/badge"
import { CheckCircle2, Clock, XCircle, AlertCircle } from "lucide-react"

export function StatusIndicators() {
  return (
    <div className="flex flex-wrap gap-2">
      <Badge variant="default" className="gap-1">
        <CheckCircle2 className="h-3 w-3" />
        Completed
      </Badge>

      <Badge variant="secondary" className="gap-1">
        <Clock className="h-3 w-3" />
        Pending
      </Badge>

      <Badge variant="outline" className="gap-1">
        <AlertCircle className="h-3 w-3" />
        In Progress
      </Badge>

      <Badge variant="destructive" className="gap-1">
        <XCircle className="h-3 w-3" />
        Overdue
      </Badge>
    </div>
  )
}
```

## Empty State with Call-to-Action

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckSquare, Plus } from "lucide-react"

export function EmptyState({ onCreateTask }) {
  return (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-16">
        <div className="rounded-full bg-muted p-6 mb-4">
          <CheckSquare className="h-10 w-10 text-muted-foreground" />
        </div>
        <h3 className="text-xl font-semibold mb-2">No tasks yet</h3>
        <p className="text-sm text-muted-foreground mb-6 text-center max-w-sm">
          Get started by creating your first task. Keep track of your todos and stay organized.
        </p>
        <Button onClick={onCreateTask}>
          <Plus className="mr-2 h-4 w-4" />
          Create Your First Task
        </Button>
      </CardContent>
    </Card>
  )
}
```

## Error State

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertCircle, RefreshCw } from "lucide-react"

export function ErrorState({ onRetry, message }) {
  return (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-16">
        <div className="rounded-full bg-destructive/10 p-6 mb-4">
          <AlertCircle className="h-10 w-10 text-destructive" />
        </div>
        <h3 className="text-xl font-semibold mb-2">Something went wrong</h3>
        <p className="text-sm text-muted-foreground mb-6 text-center max-w-sm">
          {message || "Failed to load tasks. Please try again."}
        </p>
        <Button onClick={onRetry}>
          <RefreshCw className="mr-2 h-4 w-4" />
          Try Again
        </Button>
      </CardContent>
    </Card>
  )
}
```

## Popover Info

```tsx
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { Info } from "lucide-react"

export function InfoPopover() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon">
          <Info className="h-4 w-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="space-y-2">
          <h4 className="font-medium">About Tasks</h4>
          <p className="text-sm text-muted-foreground">
            Tasks help you stay organized. Create, edit, and complete tasks to track your progress.
          </p>
        </div>
      </PopoverContent>
    </Popover>
  )
}
```

## Tooltip Hints

```tsx
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"
import { Trash2, Edit, Copy } from "lucide-react"

export function ActionButtons() {
  return (
    <TooltipProvider>
      <div className="flex gap-2">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon">
              <Edit className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Edit task</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon">
              <Copy className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Duplicate task</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon">
              <Trash2 className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Delete task</p>
          </TooltipContent>
        </Tooltip>
      </div>
    </TooltipProvider>
  )
}
```

## Key Takeaways

1. **Toast for transient feedback** - Success, error, info messages
2. **Alert for persistent messages** - Important information that stays visible
3. **Dialog for confirmations** - Require user action before proceeding
4. **Skeleton for loading** - Show placeholder while content loads
5. **Progress for long operations** - Visual feedback for ongoing processes
6. **Badge for status** - Quick visual indicators
7. **Empty states** - Guide users when no data exists
8. **Tooltip for hints** - Provide contextual help without cluttering UI
