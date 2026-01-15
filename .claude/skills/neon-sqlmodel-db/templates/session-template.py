# Session Management Template
# Copy to app/crud/task.py or app/repositories/

from typing import Optional, TypeVar, Generic, Type
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.future import select as future_select

from app.models import Task, TaskCreate, TaskUpdate, TaskResponse


# ============== TYPE VARIABLES ==============

ModelType = TypeVar("ModelType", bound=Task)


# ============== CRUD REPOSITORY ==============

class BaseRepository:
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_user(self, id: int, user_id: str) -> Optional[ModelType]:
        """
        Get a single record by ID with user isolation.

        CRITICAL: Always use this for user-owned data.
        """
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.user_id == user_id  # User isolation!
            )
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> list[ModelType]:
        """
        Get multiple records for a user with optional filters.

        Args:
            user_id: Filter by owner
            skip: Pagination offset
            limit: Max records to return
            completed: Filter by completion status (None = all)
        """
        query = select(self.model).where(self.model.user_id == user_id)

        if completed is not None:
            query = query.where(self.model.completed == completed)

        query = query.offset(skip).limit(limit)
        query = query.order_by(self.model.created_at.desc())

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        """Create a new record."""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def create_with_user(
        self,
        data: TaskCreate,
        user_id: str
    ) -> Task:
        """
        Create a new task for a specific user.

        Args:
            data: Task creation data
            user_id: Owner user ID

        Returns:
            Created Task instance
        """
        task = Task(
            **data.model_dump(),
            user_id=user_id
        )
        return await self.create(task)

    async def update(
        self,
        id: int,
        data: TaskUpdate,
        user_id: str
    ) -> Optional[ModelType]:
        """
        Update a record with user isolation.

        Args:
            id: Task ID
            data: Update data (partial update)
            user_id: Owner user ID

        Returns:
            Updated Task or None if not found
        """
        # First get with user isolation
        task = await self.get_with_user(id, user_id)

        if not task:
            return None

        # Apply updates
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Always update timestamp
        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, id: int, user_id: str) -> bool:
        """
        Delete a record with user isolation.

        Args:
            id: Record ID
            user_id: Owner user ID

        Returns:
            True if deleted, False if not found
        """
        task = await self.get_with_user(id, user_id)

        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()

        return True


# ============== TASK REPOSITORY ==============

class TaskRepository(BaseRepository):
    """Task-specific repository with user isolation."""

    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_pending(self, user_id: str, limit: int = 50) -> list[Task]:
        """Get pending tasks for a user."""
        return await self.get_multi(
            user_id=user_id,
            completed=False,
            limit=limit
        )

    async def get_completed(self, user_id: str, limit: int = 50) -> list[Task]:
        """Get completed tasks for a user."""
        return await self.get_multi(
            user_id=user_id,
            completed=True,
            limit=limit
        )

    async def toggle_complete(self, id: int, user_id: str) -> Optional[Task]:
        """
        Toggle task completion status.

        Returns:
            Updated task or None if not found
        """
        task = await self.get_with_user(id, user_id)

        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def count(self, user_id: str) -> int:
        """Count total tasks for a user."""
        result = await self.session.execute(
            select(func.count()).select_from(Task).where(Task.user_id == user_id)
        )
        return result.scalar() or 0

    async def count_by_status(self, user_id: str) -> dict:
        """Count tasks grouped by completion status."""
        # Total
        total = await self.count(user_id)

        # Pending
        result = await self.session.execute(
            select(func.count()).select_from(Task).where(
                Task.user_id == user_id,
                Task.completed == False
            )
        )
        pending = result.scalar() or 0

        # Completed
        completed = total - pending

        return {
            "total": total,
            "pending": pending,
            "completed": completed
        }

    async def search(
        self,
        user_id: str,
        query: str,
        limit: int = 50
    ) -> list[Task]:
        """
        Search tasks by title or description.

        Uses case-insensitive matching.
        """
        result = await self.session.execute(
            select(Task).where(
                Task.user_id == user_id,
                (
                    Task.title.ilike(f"%{query}%") |
                    Task.description.ilike(f"%{query}%")
                )
            ).limit(limit)
        )
        return list(result.scalars().all())


# ============== FASTAPI DEPENDENCIES ==============

from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.database import get_async_session
from app.models.user import User


async def get_current_user(
    token: str,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Extract and validate user from JWT token.

    Returns:
        User instance

    Raises:
        HTTPException if authentication fails
    """
    from app.core.auth import verify_jwt_token

    try:
        user_id = verify_jwt_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def get_task_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> TaskRepository:
    """
    Provide a TaskRepository instance.

    Usage:
        @router.get("/tasks")
        async def list_tasks(
            repo: TaskRepository = Depends(get_task_repository),
            user: User = Depends(get_current_user)
        ):
            tasks = await repo.get_multi(user.id)
    """
    return TaskRepository(session)


# ============== USAGE EXAMPLES ==============

"""
# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Task, TaskCreate, TaskUpdate
from app.crud.task import TaskRepository, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def list_tasks(
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''List all tasks for the current user.'''
    tasks = await repo.get_multi(user.id)
    return tasks


@router.get("/pending")
async def list_pending_tasks(
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''List pending tasks for the current user.'''
    return await repo.get_pending(user.id)


@router.get("/stats")
async def get_task_stats(
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Get task statistics for the current user.'''
    return await repo.count_by_status(user.id)


@router.post("")
async def create_task(
    task_data: TaskCreate,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Create a new task.'''
    return await repo.create_with_user(task_data, user.id)


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Get a specific task.'''
    task = await repo.get_with_user(task_id, user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Update a task.'''
    task = await repo.update(task_id, task_data, user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Delete a task.'''
    deleted = await repo.delete(task_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


@router.post("/{task_id}/toggle")
async def toggle_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Toggle task completion status.'''
    task = await repo.toggle_complete(task_id, user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/search")
async def search_tasks(
    q: str,
    repo: TaskRepository = Depends(get_task_repository),
    user: User = Depends(get_current_user)
):
    '''Search tasks by title or description.'''
    return await repo.search(user.id, q)
"""
