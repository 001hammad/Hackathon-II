# JWT Middleware Implementation

Complete JWT verification middleware for FastAPI.

## Basic Middleware

```python
# app/auth/middleware.py
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def get_current_user(request: Request) -> str:
    """
    Verify JWT token from Authorization header.
    Returns user_id on success, raises 401 on failure.
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
```

## Advanced Middleware with Caching

```python
# app/auth/middleware.py
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from cachetools import TTLCache
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

# Cache valid tokens for 5 minutes
token_cache = TTLCache(maxsize=1000, ttl=300)

async def get_current_user(
    request: Request,
    cache: dict = token_cache
) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]

    # Check cache first
    if token in cache:
        return cache[token]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        cache[token] = user_id
        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Key Points

1. Extract token from "Authorization: Bearer <token>" header
2. Decode JWT using shared SECRET_KEY
3. Extract user_id from "sub" claim
4. Return 401 for missing/invalid tokens
5. Cache valid tokens to reduce overhead
