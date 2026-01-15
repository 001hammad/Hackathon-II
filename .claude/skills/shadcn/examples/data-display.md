# Data Display Patterns

Patterns for displaying data using Cards, Tables, Lists, Badges, and other shadcn/ui components.

## Task Card Pattern

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Calendar, Clock } from "lucide-react"

export function TaskCard({ task }) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
        <div className="flex items-center space-x-2">
          <Checkbox checked={task.completed} />
          <CardTitle className={task.completed ? "line-through text-muted-foreground" : ""}>
            {task.title}
          </CardTitle>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>Edit</DropdownMenuItem>
            <DropdownMenuItem>Duplicate</DropdownMenuItem>
            <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{task.description}</p>
      </CardContent>
      <CardFooter className="flex gap-2">
        <Badge variant={task.status === "completed" ? "default" : "secondary"}>
          {task.status}
        </Badge>
        {task.dueDate && (
          <Badge variant="outline">
            <Calendar className="mr-1 h-3 w-3" />
            {formatDate(task.dueDate)}
          </Badge>
        )}
      </CardFooter>
    </Card>
  )
}
```

## Task Table Pattern

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export function TaskTable({ tasks }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[50px]">
            <Checkbox />
          </TableHead>
          <TableHead>Title</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Due Date</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {tasks.map((task) => (
          <TableRow key={task.id}>
            <TableCell>
              <Checkbox checked={task.completed} />
            </TableCell>
            <TableCell className="font-medium">{task.title}</TableCell>
            <TableCell>
              <Badge variant={task.status === "completed" ? "default" : "secondary"}>
                {task.status}
              </Badge>
            </TableCell>
            <TableCell>{task.dueDate || "-"}</TableCell>
            <TableCell className="text-right">
              <Button variant="ghost" size="sm">Edit</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

## List with Separator Pattern

```tsx
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"

export function TaskList({ tasks }) {
  return (
    <div className="space-y-4">
      {tasks.map((task, index) => (
        <div key={task.id}>
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center space-x-3">
              <Checkbox checked={task.completed} />
              <div>
                <p className={`font-medium ${task.completed ? "line-through text-muted-foreground" : ""}`}>
                  {task.title}
                </p>
                <p className="text-sm text-muted-foreground">{task.description}</p>
              </div>
            </div>
            <Badge>{task.status}</Badge>
          </div>
          {index < tasks.length - 1 && <Separator />}
        </div>
      ))}
    </div>
  )
}
```

## Badge Variants Pattern

```tsx
import { Badge } from "@/components/ui/badge"
import { Clock, CheckCircle2, AlertCircle, XCircle } from "lucide-react"

export function StatusBadge({ status }) {
  const variants = {
    pending: { variant: "secondary", icon: Clock, label: "Pending" },
    "in-progress": { variant: "outline", icon: AlertCircle, label: "In Progress" },
    completed: { variant: "default", icon: CheckCircle2, label: "Completed" },
    cancelled: { variant: "destructive", icon: XCircle, label: "Cancelled" },
  }

  const config = variants[status]
  const Icon = config.icon

  return (
    <Badge variant={config.variant}>
      <Icon className="mr-1 h-3 w-3" />
      {config.label}
    </Badge>
  )
}
```

## Accordion for Grouped Data

```tsx
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"

export function GroupedTasks({ taskGroups }) {
  return (
    <Accordion type="single" collapsible className="w-full">
      {taskGroups.map((group) => (
        <AccordionItem key={group.id} value={group.id}>
          <AccordionTrigger>
            <div className="flex items-center gap-2">
              {group.name}
              <Badge variant="outline">{group.tasks.length}</Badge>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <div className="space-y-2">
              {group.tasks.map((task) => (
                <TaskCard key={task.id} task={task} />
              ))}
            </div>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  )
}
```

## Avatar with Tooltip

```tsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

export function UserAvatar({ user }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
          <Avatar>
            <AvatarImage src={user.avatar} alt={user.name} />
            <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
          </Avatar>
        </TooltipTrigger>
        <TooltipContent>
          <p>{user.name}</p>
          <p className="text-xs text-muted-foreground">{user.email}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
```

## Empty State Pattern

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckSquare, Plus } from "lucide-react"

export function EmptyTaskState() {
  return (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <CheckSquare className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold mb-2">No tasks yet</h3>
        <p className="text-sm text-muted-foreground mb-4 text-center max-w-sm">
          Get started by creating your first task. Keep track of your todos and stay organized.
        </p>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Create Task
        </Button>
      </CardContent>
    </Card>
  )
}
```

## Scroll Area for Long Lists

```tsx
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"

export function TaskScrollArea({ tasks }) {
  return (
    <ScrollArea className="h-[400px] w-full rounded-md border p-4">
      {tasks.map((task, index) => (
        <div key={task.id}>
          <div className="py-2">
            <p className="font-medium">{task.title}</p>
            <p className="text-sm text-muted-foreground">{task.description}</p>
          </div>
          {index < tasks.length - 1 && <Separator />}
        </div>
      ))}
    </ScrollArea>
  )
}
```

## Stats Cards Pattern

```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { CheckCircle2, Clock, ListTodo } from "lucide-react"

export function StatsCards({ stats }) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
          <ListTodo className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.total}</div>
          <p className="text-xs text-muted-foreground">All your tasks</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Completed</CardTitle>
          <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.completed}</div>
          <p className="text-xs text-muted-foreground">
            {Math.round((stats.completed / stats.total) * 100)}% completion rate
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Pending</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.pending}</div>
          <p className="text-xs text-muted-foreground">Tasks remaining</p>
        </CardContent>
      </Card>
    </div>
  )
}
```

## Key Takeaways

1. **Use Card for containers** - Flexible component for grouping content
2. **Table for data-heavy views** - Better for large datasets
3. **Badge for status indicators** - Consistent visual language
4. **Separator for visual breaks** - Improve readability in lists
5. **Empty states** - Guide users when no data exists
6. **ScrollArea for long content** - Prevent infinite scrolling
7. **Accordion for grouped data** - Collapsible sections save space
