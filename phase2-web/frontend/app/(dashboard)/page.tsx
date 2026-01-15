"use client"

import { useEffect, useState } from "react"
import { TaskForm } from "@/components/TaskForm"
import { TaskList } from "@/components/TaskList"
import { TaskStats } from "@/components/TaskStats"
import { TaskSkeletonList } from "@/components/TaskSkeleton"
import { api, Task } from "@/lib/api/client"
import { Search, Filter } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

type FilterType = "all" | "active" | "completed"

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [filter, setFilter] = useState<FilterType>("all")
  const [searchQuery, setSearchQuery] = useState("")

  const filteredTasks = tasks.filter((task) => {
    const matchesFilter =
      filter === "all" ||
      (filter === "active" && !task.completed) ||
      (filter === "completed" && task.completed)

    const matchesSearch =
      searchQuery === "" ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase())

    return matchesFilter && matchesSearch
  })

  async function loadTasks() {
    try {
      setLoading(true)
      const response = await api.getTasks()
      setTasks(response.tasks)
      setError("")
    } catch (err: any) {
      setError("Failed to load tasks")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          My Tasks
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Manage your personal todo list
        </p>
      </div>

      {!loading && !error && <TaskStats tasks={tasks} />}

      <TaskForm onTaskCreated={loadTasks} />

      {!loading && !error && tasks.length > 0 && (
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div className="flex items-center gap-2 flex-1">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>

          <div className="flex items-center gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">
            {(["all", "active", "completed"] as FilterType[]).map((f) => (
              <Button
                key={f}
                variant={filter === f ? "default" : "ghost"}
                size="sm"
                onClick={() => setFilter(f)}
                className={`capitalize ${filter === f ? "shadow-sm" : ""}`}
              >
                {f === "all" && <Filter className="h-4 w-4 mr-1" />}
                {f}
              </Button>
            ))}
          </div>
        </div>
      )}

      {loading ? (
        <TaskSkeletonList count={5} />
      ) : error ? (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md">
          {error}
        </div>
      ) : (
        <TaskList tasks={filteredTasks} onTasksChanged={loadTasks} />
      )}
    </div>
  )
}
