"use client"

import { useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { api, Task } from "@/lib/api/client"
import { toast } from "sonner"
import { Pencil, Trash2, Clock } from "lucide-react"
import { motion } from "framer-motion"
import { formatDistanceToNow } from "date-fns"
import { cn } from "../lib/utils"

interface TaskItemProps {
  task: Task
  onTaskChanged: () => void
  index?: number
}

export function TaskItem({ task, onTaskChanged, index = 0 }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedDescription, setEditedDescription] = useState(task.description)
  const [isDeleting, setIsDeleting] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [isUpdating, setIsUpdating] = useState(false)

  const timeAgo = formatDistanceToNow(new Date(task.created_at), { addSuffix: true })

  async function handleToggle() {
    try {
      await api.toggleTask(task.id)
      onTaskChanged()
    } catch (err: any) {
      toast.error("Failed to update task")
    }
  }

  async function handleSaveEdit() {
    if (!editedDescription.trim()) {
      toast.error("Description cannot be empty")
      return
    }

    if (editedDescription.length > 500) {
      toast.error("Description must be 500 characters or less")
      return
    }

    setIsUpdating(true)

    try {
      await api.updateTask(task.id, { description: editedDescription.trim() })
      toast.success("Task updated!")
      setIsEditing(false)
      onTaskChanged()
    } catch (err: any) {
      toast.error("Failed to update task")
    } finally {
      setIsUpdating(false)
    }
  }

  function handleCancelEdit() {
    setEditedDescription(task.description)
    setIsEditing(false)
  }

  async function handleDelete() {
    setIsDeleting(true)

    try {
      await api.deleteTask(task.id)
      toast.success("Task deleted!")
      setShowDeleteDialog(false)
      onTaskChanged()
    } catch (err: any) {
      toast.error("Failed to delete task")
    } finally {
      setIsDeleting(false)
    }
  }

  return (
    <>
      <motion.div
        layout
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, x: 100 }}
        transition={{
          layout: { type: "spring", bounce: 0.2 },
          opacity: { duration: 0.2 },
          y: { type: "spring", stiffness: 300, damping: 30 },
        }}
        className={cn(
          "bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md",
          "border border-gray-100 dark:border-gray-700",
          "transition-all duration-200 group",
          task.completed && "bg-linear-to-r from-gray-50 to-white dark:from-gray-800/50 dark:to-gray-800"
        )}
      >
        <div className="p-4 flex items-start gap-3">
          <div className="shrink-0 pt-1">
            <Checkbox
              checked={task.completed}
              onCheckedChange={handleToggle}
              className="data-[state=checked]:bg-green-600 data-[state=checked]:border-green-600"
            />
          </div>

          <div className="flex-1 min-w-0">
            {isEditing ? (
              <div className="flex gap-2 items-start">
                <Input
                  type="text"
                  value={editedDescription}
                  onChange={(e) => setEditedDescription(e.target.value)}
                  disabled={isUpdating}
                  className="flex-1"
                  maxLength={500}
                  autoFocus
                />
                <Button
                  size="sm"
                  onClick={handleSaveEdit}
                  disabled={isUpdating || !editedDescription.trim()}
                >
                  {isUpdating ? "Saving..." : "Save"}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleCancelEdit}
                  disabled={isUpdating}
                >
                  Cancel
                </Button>
              </div>
            ) : (
              <>
                <div className="flex items-start gap-2 justify-between group">
                  <div className="flex-1">
                    <p
                      className={cn(
                        "text-sm leading-relaxed",
                        task.completed
                          ? "line-through text-gray-500 dark:text-gray-400"
                          : "text-gray-900 dark:text-white"
                      )}
                    >
                      {task.description}
                    </p>
                    <div className="flex items-center gap-1 mt-2 text-xs text-gray-400 dark:text-gray-500">
                      <Clock className="h-3 w-3" />
                      <span>Created {timeAgo}</span>
                    </div>
                  </div>

                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() => setIsEditing(true)}
                      title="Edit task"
                      className="h-8 w-8"
                    >
                      <Pencil className="h-3 w-3" />
                    </Button>

                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() => setShowDeleteDialog(true)}
                      title="Delete task"
                      className="h-8 w-8 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/20"
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </motion.div>

      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Task</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{task.description}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowDeleteDialog(false)}
              disabled={isDeleting}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={isDeleting}
            >
              {isDeleting ? "Deleting..." : "Delete"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
