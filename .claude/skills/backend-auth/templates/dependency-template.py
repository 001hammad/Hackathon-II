# Auth Dependencies Template
# Copy to app/auth/dependencies.py

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from typing import Optional
import os

# Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"


async def get_current_user(request: Request) -> str:
    """
    Dependency to get the current authenticated user ID.

    Usage:
        @router.get("/")
        async def endpoint(current_user_id: str = Depends(get_current_user)):
            # current_user_id is validated JWT user_id
            pass
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing or invalid"
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user identifier"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


async def get_optional_user(request: Request) -> Optional[str]:
    """
    Dependency that returns user_id if authenticated, None otherwise.

    Usage:
        @router.get("/")
        async def endpoint(user_id: Optional[str] = Depends(get_optional_user)):
            if user_id:
                # Authenticated
            else:
                # Not authenticated
            pass
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


class CurrentUser:
    """
    Class-based dependency for cleaner access to current user.

    Usage:
        @router.get("/")
        async def endpoint(current: CurrentUser = Depends(CurrentUser)):
            user_id = current.id
            # Access other user properties
            pass
    """

    def __init__(self, user_id: str = Depends(get_current_user)):
        self.id = user_id


# Example usage in a complete route file:

"""
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/tasks")
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # All queries are filtered by current_user_id
    tasks = db.query(Task).filter(Task.user_id == current_user_id).all()
    return tasks
"""
