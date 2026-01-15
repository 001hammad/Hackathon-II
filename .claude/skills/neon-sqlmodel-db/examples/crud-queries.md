# CRUD Queries Examples

Complete CRUD operations with SQLModel and async sessions.

## Create Operations

### Create a Single Task

```python
# app/crud/task.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlmodel import select

from app.models.task import Task, TaskCreate
from app.models.user import User


async def create_task(
    task_data: TaskCreate,
    user_id: str,
    session: AsyncSession
) -> Task:
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title, description, due_date)
        user_id: Authenticated user ID from JWT
        session: Async database session

    Returns:
        Created Task instance

    Raises:
        ValueError: If user does not exist
    """
    # Verify user exists (optional - depends on your cascade settings)
    user_result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise ValueError(f"User with id {user_id} not found")

    # Create task with user_id
    task = Task(
        **task_data.model_dump(),
        user_id=user_id
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


# Usage
# task = await create_task(
#     TaskCreate(title="Buy groceries", description="Milk, eggs, bread"),
#     current_user_id,
#     session
# )
```

### Bulk Create Tasks

```python
async def create_tasks_bulk(
    tasks_data: list[TaskCreate],
    user_id: str,
    session: AsyncSession
) -> list[Task]:
    """
    Create multiple tasks in a single transaction.

    Uses batch insert for efficiency with many tasks.
    """
    tasks = [
        Task(**data.model_dump(), user_id=user_id)
        for data in tasks_data
    ]

    for task in tasks:
        session.add(task)

    await session.commit()

    # Refresh all to get IDs
    for task in tasks:
        await session.refresh(task)

    return tasks


# Alternative: Use raw SQL for bulk insert performance
async def create_tasks_bulk_optimized(
    tasks_data: list[dict],
    user_id: str,
    session: AsyncSession
) -> list[Task]:
    """
    Optimized bulk insert using VALUES clause.

    Better performance for 10+ tasks.
    """
    from sqlalchemy.dialects.postgresql import insert

    values = [
        {**data, "user_id": user_id}
        for data in tasks_data
    ]

    stmt = insert(Task).values(values).returning(Task)

    result = await session.execute(stmt)
    tasks = result.scalars().all()

    return list(tasks)
```

## Read Operations

### Get Task by ID

```python
async def get_task(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> Optional[Task]:
    """
    Retrieve a single task by ID with user isolation.

    CRITICAL: Always filter by user_id to ensure data isolation.
    """
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation!
        )
    )
    return result.scalar_one_or_none()


# Usage with error handling
# task = await get_task(task_id, current_user_id, session)
# if not task:
#     raise HTTPException(status_code=404, detail="Task not found")
```

### Get All Tasks with Filters

```python
from enum import Enum
from typing import Optional
from sqlalchemy import func


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ALL = "all"


async def get_tasks(
    user_id: str,
    session: AsyncSession,
    status: TaskStatus = TaskStatus.ALL,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> dict:
    """
    Retrieve tasks with filtering, pagination, and sorting.

    Returns:
        Dict with 'items' (list) and 'total' (count)
    """
    # Base query with user isolation
    base_query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status == TaskStatus.COMPLETED:
        base_query = base_query.where(Task.completed == True)
    elif status == TaskStatus.PENDING:
        base_query = base_query.where(Task.completed == False)

    # Get total count
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar()

    # Apply sorting
    column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        base_query = base_query.order_by(column.desc())
    else:
        base_query = base_query.order_by(column.asc())

    # Apply pagination
    offset = (page - 1) * limit
    base_query = base_query.offset(offset).limit(limit)

    # Execute query
    result = await session.execute(base_query)
    tasks = result.scalars().all()

    return {
        "items": list(tasks),
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


# Usage
# result = await get_tasks(
#     user_id=current_user_id,
#     session=session,
#     status=TaskStatus.PENDING,
#     page=1,
#     limit=10
# )
# tasks = result["items"]
```

### Search Tasks

```python
async def search_tasks(
    user_id: str,
    session: AsyncSession,
    query: str,
    page: int = 1,
    limit: int = 10
) -> list[Task]:
    """
    Search tasks by title or description.

    Uses case-insensitive containment.
    """
    search_query = select(Task).where(
        Task.user_id == user_id,
        (
            Task.title.ilike(f"%{query}%") |
            Task.description.ilike(f"%{query}%")
        )
    )

    search_query = search_query.offset((page - 1) * limit).limit(limit)

    result = await session.execute(search_query)
    return list(result.scalars().all())


# Usage
# tasks = await search_tasks(current_user_id, session, "groceries")
```

### Get Task Statistics

```python
from datetime import datetime, timedelta
from sqlalchemy import func


async def get_task_stats(
    user_id: str,
    session: AsyncSession
) -> dict:
    """
    Get task statistics for the user.

    Returns counts for total, completed, pending, overdue tasks.
    """
    # Total tasks
    total_query = select(func.count()).select_from(
        select(Task).where(Task.user_id == user_id).subquery()
    )

    # Completed tasks
    completed_query = select(func.count()).select_from(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == True
        ).subquery()
    )

    # Pending tasks
    pending_query = select(func.count()).select_from(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False
        ).subquery()
    )

    # Overdue tasks (due_date in past and not completed)
    overdue_query = select(func.count()).select_from(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date < datetime.utcnow()
        ).subquery()
    )

    # Due today
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    due_today_query = select(func.count()).select_from(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date >= today_start,
            Task.due_date <= today_end
        ).subquery()
    )

    # Execute all queries
    total = (await session.execute(total_query)).scalar()
    completed = (await session.execute(completed_query)).scalar()
    pending = (await session.execute(pending_query)).scalar()
    overdue = (await session.execute(overdue_query)).scalar()
    due_today = (await session.execute(due_today_query)).scalar()

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "due_today": due_today,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
    }


# Usage
# stats = await get_task_stats(current_user_id, session)
# print(f"Completed: {stats['completed']}/{stats['total']}")
```

## Update Operations

### Update Task

```python
from datetime import datetime
from sqlmodel import update


async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str,
    session: AsyncSession
) -> Optional[Task]:
    """
    Update task fields with user isolation.

    Only updates fields that are explicitly set (exclude_unset=True).
    """
    # First, fetch the task to ensure ownership
    task = await get_task(task_id, user_id, session)

    if not task:
        return None

    # Build update dict with only set fields
    update_data = task_update.model_dump(exclude_unset=True)

    if not update_data:
        return task  # Nothing to update

    # Update fields
    for field, value in update_data.items():
        setattr(task, field, value)

    # Always update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task


# Usage
# updated = await update_task(
#     task_id=1,
#     task_update=TaskUpdate(completed=True),
#     user_id=current_user_id,
#     session=session
# )
```

### Toggle Task Completion

```python
async def toggle_task_completion(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> Optional[Task]:
    """
    Toggle the completed status of a task.

    More efficient than full update for simple toggle.
    """
    task = await get_task(task_id, user_id, session)

    if not task:
        return None

    # Toggle the status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task


# Usage
# task = await toggle_task_completion(1, current_user_id, session)
```

### Bulk Update Tasks

```python
async def mark_tasks_completed(
    task_ids: list[int],
    user_id: str,
    session: AsyncSession
) -> int:
    """
    Mark multiple tasks as completed.

    Returns the number of tasks updated.
    """
    from datetime import datetime

    result = await session.execute(
        update(Task)
        .where(
            Task.id.in_(task_ids),
            Task.user_id == user_id
        )
        .values(
            completed=True,
            updated_at=datetime.utcnow()
        )
    )

    await session.commit()
    return result.rowcount


# Usage
# count = await mark_tasks_completed([1, 2, 3], current_user_id, session)
```

## Delete Operations

### Delete Task

```python
async def delete_task(
    task_id: int,
    user_id: str,
    session: AsyncSession
) -> bool:
    """
    Delete a task with user isolation.

    Returns True if deleted, False if not found.
    """
    task = await get_task(task_id, user_id, session)

    if not task:
        return False

    await session.delete(task)
    await session.commit()

    return True


# Usage
# deleted = await delete_task(1, current_user_id, session)
# if not deleted:
#     raise HTTPException(status_code=404, detail="Task not found")
```

### Bulk Delete Tasks

```python
async def delete_tasks(
    task_ids: list[int],
    user_id: str,
    session: AsyncSession
) -> int:
    """
    Delete multiple tasks.

    Returns the number of tasks deleted.
    """
    from sqlmodel import delete

    # First, get tasks to verify ownership and cascade if needed
    result = await session.execute(
        select(Task).where(
            Task.id.in_(task_ids),
            Task.user_id == user_id
        )
    )
    tasks = result.scalars().all()

    for task in tasks:
        await session.delete(task)

    await session.commit()
    return len(tasks)


# Alternative: Direct delete (faster but no cascade)
async def delete_tasks_fast(
    task_ids: list[int],
    user_id: str,
    session: AsyncSession
) -> int:
    """
    Fast bulk delete without cascade operations.
    """
    result = await session.execute(
        delete(Task).where(
            Task.id.in_(task_ids),
            Task.user_id == user_id
        )
    )

    await session.commit()
    return result.rowcount


# Usage
# count = await delete_tasks([1, 2, 3], current_user_id, session)
```

## Complex Query Patterns

### Eager Load Relationships

```python
async def get_tasks_with_user(
    user_id: str,
    session: AsyncSession
) -> list[Task]:
    """
    Get tasks with user relationship loaded.
    """
    from sqlalchemy.orm import selectinload

    result = await session.execute(
        select(Task)
        .options(selectinload(Task.user))
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )

    return list(result.scalars().all())


# Usage
# tasks = await get_tasks_with_user(current_user_id, session)
# for task in tasks:
#     print(f"Task: {task.title}, User: {task.user.email}")
```

### Tasks Due This Week

```python
async def get_tasks_due_this_week(
    user_id: str,
    session: AsyncSession
) -> list[Task]:
    """
    Get all pending tasks due within the next 7 days.
    """
    from datetime import timedelta

    now = datetime.utcnow()
    week_from_now = now + timedelta(days=7)

    result = await session.execute(
        select(Task)
        .where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date.isnot(None),
            Task.due_date >= now,
            Task.due_date <= week_from_now
        )
        .order_by(Task.due_date.asc())
    )

    return list(result.scalars().all())
```

### Tasks Overdue

```python
async def get_overdue_tasks(
    user_id: str,
    session: AsyncSession
) -> list[Task]:
    """
    Get all overdue pending tasks.
    """
    result = await session.execute(
        select(Task)
        .where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date < datetime.utcnow()
        )
        .order_by(Task.due_date.asc())
    )

    return list(result.scalars().all())


# Usage
# overdue = await get_overdue_tasks(current_user_id, session)
# print(f"You have {len(overdue)} overdue tasks!")
```

### Aggregate with Group By

```python
async def get_tasks_by_status_summary(
    user_id: str,
    session: AsyncSession
) -> list[dict]:
    """
    Get task count grouped by completion status.
    """
    from sqlalchemy import case

    result = await session.execute(
        select(
            case(
                (Task.completed == True, "completed"),
                else_="pending"
            ).label("status"),
            func.count().label("count")
        )
        .where(Task.user_id == user_id)
        .group_by(case(
            (Task.completed == True, "completed"),
            else_="pending"
        ))
    )

    return [{"status": row.status, "count": row.count} for row in result]


# Usage
# summary = await get_tasks_by_status_summary(current_user_id, session)
# for row in summary:
#     print(f"{row['status']}: {row['count']}")
```

## Error Handling Patterns

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


async def safe_create_task(
    task_data: TaskCreate,
    user_id: str,
    session: AsyncSession
) -> Task:
    """
    Create task with comprehensive error handling.
    """
    try:
        return await create_task(task_data, user_id, session)

    except IntegrityError as e:
        await session.rollback()
        # Handle constraint violations
        if "duplicate" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail="Task with this title already exists"
            )
        raise HTTPException(
            status_code=400,
            detail="Database constraint violation"
        )

    except ValueError as e:
        await session.rollback()
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


async def safe_get_tasks(
    user_id: str,
    session: AsyncSession,
    **filters
) -> list[Task]:
    """
    Get tasks with error handling.
    """
    try:
        return await get_tasks(user_id, session, **filters)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )
```
