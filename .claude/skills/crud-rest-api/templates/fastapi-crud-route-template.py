"""
FastAPI CRUD Route Template

This template provides a complete, production-ready implementation of CRUD
endpoints for the Task resource following RESTful conventions.

Usage:
1. Copy this file to your FastAPI project as `app/api/routes/tasks.py`
2. Ensure models are defined in `app/models/task.py`
3. Ensure dependencies are in `app/api/dependencies.py`
4. Register router in main FastAPI app
5. Customize as needed for your specific requirements

Features:
- Full CRUD operations (Create, Read, Update, Delete)
- JWT authentication on all endpoints
- User isolation (users can only access their own tasks)
- Input validation with Pydantic
- Proper HTTP status codes
- Comprehensive error handling
- Query parameter filtering
- Type hints throughout
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from typing import Optional
from datetime import datetime

# Import models
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User

# Import dependencies
from app.api.dependencies import get_current_user, get_db

# Create router
router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={
        401: {"description": "Unauthorized - Invalid or missing JWT token"},
        404: {"description": "Task not found or access denied"},
    },
)


# ==================== CREATE ====================

@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user",
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Create a new task.

    Args:
        task_data: Task creation data (title, description)
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        Created task object

    Raises:
        400: Validation error (automatic from Pydantic)
        401: Unauthorized (no valid JWT)
    """
    # Create new task instance
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Add to database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==================== READ (LIST) ====================

@router.get(
    "/",
    response_model=list[Task],
    summary="List all tasks",
    description="Get all tasks for the authenticated user with optional filtering",
)
async def list_tasks(
    status_filter: str = Query(
        "all",
        alias="status",
        description="Filter by completion status",
        regex="^(all|pending|completed)$",
    ),
    sort: str = Query(
        "newest",
        description="Sort order",
        regex="^(newest|oldest|title)$",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Task]:
    """
    List all tasks for the authenticated user.

    Args:
        status_filter: Filter by completion status (all, pending, completed)
        sort: Sort order (newest, oldest, title)
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        List of tasks matching criteria

    Raises:
        401: Unauthorized (no valid JWT)
    """
    # Build base query - ALWAYS filter by user_id
    statement = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status_filter == "pending":
        statement = statement.where(Task.completed == False)
    elif status_filter == "completed":
        statement = statement.where(Task.completed == True)
    # "all" - no additional filter

    # Apply sorting
    if sort == "newest":
        statement = statement.order_by(col(Task.created_at).desc())
    elif sort == "oldest":
        statement = statement.order_by(col(Task.created_at).asc())
    elif sort == "title":
        statement = statement.order_by(col(Task.title).asc())

    # Execute query
    results = db.exec(statement)
    tasks = results.all()

    return tasks


# ==================== READ (SINGLE) ====================

@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get a task by ID",
    description="Get a single task by its ID",
)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Get a single task by ID.

    Args:
        task_id: Task UUID
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        Task object

    Raises:
        401: Unauthorized (no valid JWT)
        404: Task not found or not owned by user
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check if task exists and belongs to user
    # IMPORTANT: Use 404 for both cases to not reveal if task exists
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# ==================== UPDATE ====================

@router.put(
    "/{task_id}",
    response_model=Task,
    summary="Update a task",
    description="Update a task's title, description, or completion status",
)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Update a task.

    Only provided fields will be updated (partial update).

    Args:
        task_id: Task UUID
        task_data: Fields to update (title, description, completed)
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        Updated task object

    Raises:
        400: Validation error
        401: Unauthorized (no valid JWT)
        404: Task not found or not owned by user
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check if task exists and belongs to user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Save changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# ==================== TOGGLE COMPLETE ====================

@router.patch(
    "/{task_id}/complete",
    response_model=Task,
    summary="Toggle task completion",
    description="Toggle the completion status of a task",
)
async def toggle_task_complete(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    """
    Toggle task completion status.

    This is a convenience endpoint for toggling completed field
    without sending a full update request.

    Args:
        task_id: Task UUID
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        Updated task object

    Raises:
        401: Unauthorized (no valid JWT)
        404: Task not found or not owned by user
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check if task exists and belongs to user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    # Save changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# ==================== DELETE ====================

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task",
)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a task.

    Args:
        task_id: Task UUID
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        None (204 No Content)

    Raises:
        401: Unauthorized (no valid JWT)
        404: Task not found or not owned by user
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Check if task exists and belongs to user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Delete task
    db.delete(task)
    db.commit()

    # Return None for 204 status
    return None


# ==================== ADDITIONAL PATTERNS ====================

# Example: Bulk operations
@router.post(
    "/bulk/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Bulk delete tasks",
    description="Delete multiple tasks at once",
)
async def bulk_delete_tasks(
    task_ids: list[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete multiple tasks at once.

    Only tasks owned by the authenticated user will be deleted.
    Invalid IDs or tasks owned by others are silently ignored.

    Args:
        task_ids: List of task UUIDs to delete
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        None (204 No Content)
    """
    # Fetch all tasks that exist and belong to user
    statement = select(Task).where(
        Task.id.in_(task_ids),
        Task.user_id == current_user.id,
    )
    results = db.exec(statement)
    tasks = results.all()

    # Delete each task
    for task in tasks:
        db.delete(task)

    db.commit()

    return None


# Example: Pagination
@router.get(
    "/paginated",
    response_model=dict,
    summary="List tasks with pagination",
    description="Get paginated list of tasks",
)
async def list_tasks_paginated(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    status_filter: str = Query("all", alias="status", regex="^(all|pending|completed)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    List tasks with pagination.

    Returns:
        {
            "items": [...],
            "total": 100,
            "page": 1,
            "size": 20,
            "pages": 5
        }
    """
    # Build base query
    statement = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter
    if status_filter == "pending":
        statement = statement.where(Task.completed == False)
    elif status_filter == "completed":
        statement = statement.where(Task.completed == True)

    # Get total count
    count_statement = statement
    total = len(db.exec(count_statement).all())

    # Apply pagination
    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size)

    # Execute query
    results = db.exec(statement)
    tasks = results.all()

    # Calculate total pages
    pages = (total + size - 1) // size  # Ceiling division

    return {
        "items": tasks,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


# ==================== USAGE EXAMPLE ====================

"""
# Register router in main.py:

from fastapi import FastAPI
from app.api.routes import tasks

app = FastAPI()
app.include_router(tasks.router)

# Test with curl:

# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task details"}'

# List tasks
curl -X GET http://localhost:8000/api/tasks?status=all \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get single task
curl -X GET http://localhost:8000/api/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Update task
curl -X PUT http://localhost:8000/api/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "completed": true}'

# Toggle complete
curl -X PATCH http://localhost:8000/api/tasks/TASK_ID/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Delete task
curl -X DELETE http://localhost:8000/api/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
"""
