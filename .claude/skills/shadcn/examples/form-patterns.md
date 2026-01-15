# Form Patterns

Comprehensive form patterns using shadcn/ui components with react-hook-form and zod validation.

## Basic Form Pattern

```tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  title: z.string().min(1, "Title is required").max(100),
  description: z.string().optional(),
})

export function BasicTaskForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { title: "", description: "" },
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
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input placeholder="Buy groceries" {...field} />
              </FormControl>
              <FormDescription>Task title (required)</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea placeholder="Add details..." {...field} />
              </FormControl>
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

## Form with Date Picker

```tsx
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { CalendarIcon } from "lucide-react"
import { format } from "date-fns"
import { cn } from "@/lib/utils"

const formSchema = z.object({
  title: z.string().min(1),
  dueDate: z.date().optional(),
})

<FormField
  control={form.control}
  name="dueDate"
  render={({ field }) => (
    <FormItem className="flex flex-col">
      <FormLabel>Due Date</FormLabel>
      <Popover>
        <PopoverTrigger asChild>
          <FormControl>
            <Button
              variant="outline"
              className={cn(
                "w-full pl-3 text-left font-normal",
                !field.value && "text-muted-foreground"
              )}
            >
              {field.value ? format(field.value, "PPP") : "Pick a date"}
              <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
            </Button>
          </FormControl>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={field.value}
            onSelect={field.onChange}
            disabled={(date) => date < new Date()}
          />
        </PopoverContent>
      </Popover>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Form with Select Dropdown

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const formSchema = z.object({
  priority: z.enum(["low", "medium", "high"]),
})

<FormField
  control={form.control}
  name="priority"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Priority</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select priority" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="low">Low</SelectItem>
          <SelectItem value="medium">Medium</SelectItem>
          <SelectItem value="high">High</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Form with Checkbox

```tsx
import { Checkbox } from "@/components/ui/checkbox"

const formSchema = z.object({
  notifications: z.boolean().default(false),
})

<FormField
  control={form.control}
  name="notifications"
  render={({ field }) => (
    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox
          checked={field.value}
          onCheckedChange={field.onChange}
        />
      </FormControl>
      <div className="space-y-1 leading-none">
        <FormLabel>Email notifications</FormLabel>
        <FormDescription>
          Receive notifications about task updates
        </FormDescription>
      </div>
    </FormItem>
  )}
/>
```

## Form with Loading State

```tsx
"use client"

import { useState } from "react"
import { Loader2 } from "lucide-react"

export function TaskFormWithLoading() {
  const [isSubmitting, setIsSubmitting] = useState(false)

  const form = useForm({
    resolver: zodResolver(formSchema),
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSubmitting(true)
    try {
      await createTask(values)
      toast({ title: "Task created successfully" })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create task",
        variant: "destructive"
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* Form fields */}

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {isSubmitting ? "Creating..." : "Create Task"}
        </Button>
      </form>
    </Form>
  )
}
```

## Multi-Step Form Pattern

```tsx
"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function MultiStepTaskForm() {
  const [step, setStep] = useState("details")
  const form = useForm({
    resolver: zodResolver(formSchema),
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <Tabs value={step} onValueChange={setStep}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="details">Details</TabsTrigger>
            <TabsTrigger value="dates">Dates</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="details" className="space-y-4">
            {/* Title and description fields */}
          </TabsContent>

          <TabsContent value="dates" className="space-y-4">
            {/* Date picker fields */}
          </TabsContent>

          <TabsContent value="settings" className="space-y-4">
            {/* Priority, notifications, etc. */}
          </TabsContent>
        </Tabs>

        <div className="flex justify-between mt-6">
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              const steps = ["details", "dates", "settings"]
              const currentIndex = steps.indexOf(step)
              if (currentIndex > 0) setStep(steps[currentIndex - 1])
            }}
          >
            Previous
          </Button>

          {step === "settings" ? (
            <Button type="submit">Create Task</Button>
          ) : (
            <Button
              type="button"
              onClick={() => {
                const steps = ["details", "dates", "settings"]
                const currentIndex = steps.indexOf(step)
                if (currentIndex < steps.length - 1) setStep(steps[currentIndex + 1])
              }}
            >
              Next
            </Button>
          )}
        </div>
      </form>
    </Form>
  )
}
```

## Form in Dialog

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

export function TaskFormDialog() {
  const [open, setOpen] = useState(false)
  const form = useForm({
    resolver: zodResolver(formSchema),
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    await createTask(values)
    setOpen(false)
    form.reset()
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            {/* Form fields */}
            <Button type="submit" className="w-full">Create</Button>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}
```

## Form with Dynamic Fields

```tsx
"use client"

import { useFieldArray } from "react-hook-form"
import { Plus, X } from "lucide-react"

const formSchema = z.object({
  subtasks: z.array(
    z.object({
      title: z.string().min(1, "Subtask title required"),
    })
  ),
})

export function TaskFormWithSubtasks() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      subtasks: [{ title: "" }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "subtasks",
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <FormLabel>Subtasks</FormLabel>
          {fields.map((field, index) => (
            <FormField
              key={field.id}
              control={form.control}
              name={`subtasks.${index}.title`}
              render={({ field }) => (
                <FormItem>
                  <div className="flex gap-2">
                    <FormControl>
                      <Input placeholder="Subtask title" {...field} />
                    </FormControl>
                    {fields.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => remove(index)}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
          ))}
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => append({ title: "" })}
          >
            <Plus className="mr-2 h-4 w-4" />
            Add Subtask
          </Button>
        </div>

        <Button type="submit">Create Task</Button>
      </form>
    </Form>
  )
}
```

## Key Takeaways

1. **Always use Form component** - Wraps form with react-hook-form context
2. **Zod for validation** - Type-safe schema validation
3. **FormField pattern** - Use render prop for each field
4. **Loading states** - Show feedback during async operations
5. **Error handling** - Display validation errors with FormMessage
6. **Accessibility** - FormLabel, FormDescription for screen readers
7. **Reset on success** - Clear form after successful submission
