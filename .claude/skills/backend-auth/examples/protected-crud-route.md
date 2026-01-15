# Protected CRUD Route Implementation

Complete protected CRUD operations with user isolation.

## Task Model

```python
# app/models/task.py
from sqlalchemy import Column, String, Text, Boolean, DateTime
from app.database import Base
import uuid
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)  # CRITICAL
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
```

## Protected Routes

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, list

from app.database import get_db
from app.models.task import Task
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=list[dict])
async def get_tasks(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for authenticated user."""
    query = db.query(Task).filter(Task.user_id == current_user_id)

    if status:
        query = query.filter(Task.status == status)

    offset = (page - 1) * limit
    tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()

    return [task.to_dict() for task in tasks]

@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()

@router.post("/", response_model=dict, status_code=201)
async def create_task(
    task_data: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task."""
    task = Task(
        **task_data,
        user_id=current_user_id  # Assign to authenticated user
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task.to_dict()

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: str,
    task_update: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task.to_dict()

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None

@router.get("/stats/summary")
async def get_task_stats(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get task statistics."""
    total = db.query(Task).filter(Task.user_id == current_user_id).count()
    pending = db.query(Task).filter(
        Task.user_id == current_user_id,
        Task.status == "pending"
    ).count()
    completed = db.query(Task).filter(
        Task.user_id == current_user_id,
        Task.status == "completed"
    ).count()

    return {
        "total": total,
        "pending": pending,
        "completed": completed
    }
```

## Key Points

1. Always use `Depends(get_current_user)` to get authenticated user_id
2. Filter ALL queries by `user_id == current_user_id`
3. Return 404 (not 403) for not found - don't reveal ownership
4. Assign user_id from JWT when creating new resources
