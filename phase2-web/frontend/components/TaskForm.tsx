"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { api } from "@/lib/api/client"
import { toast } from "sonner"
import { Plus } from "lucide-react"

interface TaskFormProps {
  onTaskCreated: () => void
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [description, setDescription] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault()

    if (!description.trim()) {
      toast.error("Please enter a task description")
      return
    }

    if (description.length > 500) {
      toast.error("Description must be 500 characters or less")
      return
    }

    setIsSubmitting(true)

    try {
      await api.createTask({ description: description.trim() })
      toast.success("Task created successfully!")
      setDescription("")
      onTaskCreated()
    } catch (err: any) {
      toast.error(err.message || "Failed to create task")
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Plus className="h-5 w-5 text-blue-600 dark:text-blue-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Add New Task
        </h3>
      </div>
      <div className="flex gap-2">
        <Input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="What do you need to do? (Press Enter to add)"
          disabled={isSubmitting}
          className="flex-1"
          maxLength={500}
          autoFocus
        />
        <Button
          type="button"
          onClick={() => handleSubmit()}
          disabled={isSubmitting || !description.trim()}
        >
          {isSubmitting ? (
            "Adding..."
          ) : (
            <>
              <Plus className="h-4 w-4 mr-1" />
              Add
            </>
          )}
        </Button>
      </div>
      <p className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
        <span>{description.length}/500 characters</span>
        <span className="text-gray-400 dark:text-gray-500">Press Enter to add</span>
      </p>
    </div>
  )
}
