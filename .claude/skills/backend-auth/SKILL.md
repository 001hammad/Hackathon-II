---
name: backend-auth
description: Expert in backend JWT verification in FastAPI for Phase 2. Use PROACTIVELY whenever implementing API routes or database operations that require authentication.
---

# Backend Auth Expert (FastAPI + JWT)

Expert guidance for implementing backend JWT verification, user isolation, and authentication middleware in FastAPI.

## Core Responsibilities

### ✅ What This Skill Handles (Backend Only)

1. **JWT Verification** - Verify tokens from Authorization header
2. **User ID Extraction** - Extract user_id from JWT payload
3. **User Isolation** - Filter all queries by authenticated user_id
4. **Authentication Middleware** - Create reusable auth dependencies
5. **401 Error Handling** - Return proper errors for invalid/missing tokens
6. **Token Validation** - Check expiration, signature, issuer
7. **Secure Configuration** - Use shared BETTER_AUTH_SECRET

### ❌ What This Skill Does NOT Handle (Frontend)

- Frontend auth UI (use frontend-auth skill)
- Better Auth server configuration
- User registration/login endpoints
- Token generation
- Frontend cookie management

## Quick Start

### 1. Install Dependencies

```bash
pip install python-jose passlib[bcrypt] python-multipart
```

### 2. Environment Variable

```bash
# .env
BETTER_AUTH_SECRET=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. JWT Verification Dependency

```python
# app/auth/dependencies.py
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from typing import Optional
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def get_current_user(request: Request) -> str:
    """
    Verify JWT token and return user_id.
    Raises HTTPException 401 if token is missing or invalid.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format. Use: Bearer <token>"
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user identifier"
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
```

### 4. Using Dependency in Routes

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user.
    Tasks are filtered by user_id to ensure isolation.
    """
    tasks = db.query(Task).filter(
        Task.user_id == current_user_id
    ).all()
    return tasks

@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.
    Task is automatically assigned to the authenticated user.
    """
    task = Task(
        **task_data.model_dump(),
        user_id=current_user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task. Only allows updating tasks belonging to the authenticated user.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # CRITICAL: User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task. Only allows deleting tasks belonging to the authenticated user.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # CRITICAL: User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
```

## User Isolation Pattern

### ❌ NEVER Do This (Trust URL Parameters)

```python
# BAD: User can delete ANY task by changing the ID in URL
@router.delete("/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    return {"deleted": True}
```

### ✅ ALWAYS Do This (Filter by user_id from JWT)

```python
# GOOD: Task must belong to the authenticated user
@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),  # From JWT
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user_id  # CRITICAL: User isolation
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
```

## JWT Token Structure

Tokens are created by Better Auth on frontend and contain:

```json
{
  "sub": "user-uuid-here",
  "exp": 1704067200,
  "iat": 1704063600
}
```

- **sub**: User ID (UUID or string)
- **exp**: Expiration timestamp
- **iat**: Issued at timestamp

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Authorization header missing"
}
```

### 404 Not Found (User Isolation)

```json
{
  "detail": "Task not found"
}
```

### 403 Forbidden (Optional)

```json
{
  "detail": "You don't have permission to access this resource"
}
```

## Security Best Practices

1. **Always verify tokens** - Never skip JWT verification
2. **Use https only** - Transmit tokens over secure connections
3. **Short expiration** - Set reasonable token expiry (15-30 minutes)
4. **Secure secret** - Use strong, random SECRET_KEY
5. **Validate all claims** - Check exp, iat, sub
6. **User isolation** - ALWAYS filter by user_id from JWT
7. **No user trust** - Never trust user_id from URL/body

## Common Patterns

### Protected CRUD for Any Resource

```python
@router.get("/{resource_id}")
async def get_resource(
    resource_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user_id  # Always filter!
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource
```

### Optional Authentication

```python
async def get_optional_user(request: Request) -> Optional[str]:
    """Return user_id if valid token, None otherwise."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

### Rate Limiting (Optional)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.get("/")
@limiter.limit("10/minute")
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Your code here
    pass
```

## Testing Protected Routes

### Unit Test Example

```python
from fastapi.testclient import TestClient
from app.main import app
from jose import jwt

def test_get_tasks_unauthorized():
    client = TestClient(app)
    response = client.get("/api/tasks/")
    assert response.status_code == 401

def test_get_tasks_authorized():
    client = TestClient(app)
    token = jwt.encode(
        {"sub": "test-user-id"},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/tasks/", headers=headers)
    assert response.status_code == 200
```

## Environment Variables

```bash
# .env
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Key Principles Summary

1. **Backend-only** - JWT verification and user isolation
2. **Extract from JWT** - user_id comes from token, not URL
3. **Always filter** - WHERE user_id = current_user_id
4. **Return 401** - Invalid/missing token
5. **Return 404** - Resource not found or not owned
6. **Use dependencies** - Reusable auth dependency
7. **Test protected routes** - Verify auth works correctly

## Additional Resources

- See `examples/` for complete CRUD implementation patterns
- See `reference/` for JWT security and attack prevention
- See `templates/` for ready-to-use middleware and route templates
- See frontend-auth skill for frontend authentication

## Summary

This skill provides **backend-only** authentication with JWT verification:

✅ JWT token verification from Authorization header
✅ User ID extraction from token payload
✅ User isolation in all database queries
✅ Protected CRUD routes
✅ Reusable auth dependencies
✅ Security best practices
✅ Testing patterns

❌ Frontend auth UI (use frontend-auth skill)
❌ Token generation (handled by Better Auth)
❌ User registration/login endpoints
