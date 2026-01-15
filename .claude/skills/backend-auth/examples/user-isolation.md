# User Isolation Patterns

Ensuring data security through proper user isolation.

## The Golden Rule

> Always filter queries by user_id from JWT, NEVER trust user_id from URL or request body.

## Bad Examples (No Isolation)

```python
# BAD: Using user_id from URL - user can change it
@router.delete("/{user_id}/{task_id}")
async def delete_task(user_id: str, task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    return {"deleted": True}

# BAD: Missing filter entirely
@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()  # Returns ALL users' tasks!
    return tasks
```

## Good Examples (Proper Isolation)

```python
# GOOD: Extract user_id from JWT, filter by it
@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),  # From JWT
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # Always filter!
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    return {"deleted": True}

# GOOD: List only user's tasks
@router.get("/tasks")
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(
        Task.user_id == current_user_id
    ).all()
    return tasks
```

## User Isolation in Different Operations

### SELECT - Filter Results

```python
@router.get("/tasks")
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.user_id == current_user_id).all()
    return tasks
```

### INSERT - Assign User

```python
@router.post("/tasks")
async def create_task(
    task_data: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = Task(
        **task_data,
        user_id=current_user_id  # Assign to authenticated user
    )
    db.add(task)
    db.commit()
    return task
```

### UPDATE - Filter Before Update

```python
@router.put("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_update: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # Filter!
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.items():
        setattr(task, field, value)

    db.commit()
    return task
```

## Why User Isolation Matters

- Prevents data leaks
- Ensures data privacy
- Maintains trust
- Meets compliance requirements
