"""Task CRUD endpoints with user isolation."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from ..database.connection import get_session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=dict)
async def list_tasks(
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.

    CRITICAL: Filters by user_id to enforce user isolation.
    Users can only see their own tasks.
    """
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()

    return {"tasks": [task.to_dict() for task in tasks]}


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    The user_id is automatically set from the JWT token,
    not from the request body (security).
    """
    new_task = Task(
        user_id=current_user_id,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    CRITICAL: Verifies task belongs to authenticated user.
    Returns 404 if task doesn't exist or belongs to another user.
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or access denied"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task's description.

    CRITICAL: Verifies task belongs to authenticated user before updating.
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or access denied"
        )

    # Update description
    task.description = task_update.description
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    task_id: int,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle a task's completion status.

    CRITICAL: Verifies task belongs to authenticated user before toggling.
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or access denied"
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    CRITICAL: Verifies task belongs to authenticated user before deleting.
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or access denied"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}
