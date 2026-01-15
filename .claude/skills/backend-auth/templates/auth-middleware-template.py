# JWT Authentication Middleware Template
# Copy to app/auth/dependencies.py

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from typing import Optional
import os

# Configuration - Use environment variables!
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")
ALGORITHM = "HS256"


async def get_current_user(request: Request) -> str:
    """
    Verify JWT token from Authorization header and return user_id.

    Returns:
        str: The authenticated user's ID

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required"
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
                detail="Token does not contain user identifier"
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )


async def get_optional_user(request: Request) -> Optional[str]:
    """
    Return user_id if valid token is present, None otherwise.

    Useful for endpoints that work with or without authentication.
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
