"""Authentication dependency for Phase 2 (Next.js BFF trusted headers).

We no longer accept end-user JWTs on the FastAPI service.
Instead, the Next.js BFF validates the Better Auth cookie session and
proxies requests to FastAPI with a signed internal identity header.
"""

from fastapi import HTTPException, Request
from uuid import UUID
import hmac
import hashlib
import time

from ..core.config import settings
from ..models.user import User
from ..database.connection import engine
from sqlmodel import Session, select
from datetime import datetime


INTERNAL_TIME_SKEW_MS = 5 * 60 * 1000  # 5 minutes


async def get_current_user(request: Request) -> UUID:
    """Return authenticated user_id from trusted internal headers.

    Expected headers (set by Next.js BFF routes under /api/tasks*):
      - x-user-id
      - x-internal-timestamp (milliseconds since epoch)
      - x-internal-signature (hex hmac sha256)

    Signature payload format (must match frontend proxy):
      "{userId}:{timestamp}:{method}:{path}:{body}"

    Raises 401 for missing/invalid headers or invalid signatures.
    """

    user_id = request.headers.get("x-user-id")
    timestamp = request.headers.get("x-internal-timestamp")
    signature = request.headers.get("x-internal-signature")

    if not user_id or not timestamp or not signature:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        ts_ms = int(timestamp)
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    now_ms = int(time.time() * 1000)
    if abs(now_ms - ts_ms) > INTERNAL_TIME_SKEW_MS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    raw_body = await request.body()
    body_text = raw_body.decode("utf-8") if raw_body else ""

    # request.url.path is the canonical path (e.g. /api/tasks/123)
    method = request.method.upper()
    path = request.url.path

    payload = f"{user_id}:{timestamp}:{method}:{path}:{body_text}"

    expected = hmac.new(
        settings.BETTER_AUTH_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Ensure user exists in our custom User model
    # Create a session and check if user exists, create if not
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(User).where(User.id == user_uuid)).first()

            # If user doesn't exist in our custom model, create a minimal entry
            if not existing_user:
                # Create a new user with the same UUID from Better Auth
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                new_user = User(
                    id=user_uuid,
                    email=f"user_{user_uuid}@better-auth.com",  # Default email
                    password_hash="",  # Empty since Better Auth handles auth
                    created_at=now,
                    updated_at=now
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)  # Refresh to ensure the user is properly saved
    except Exception as e:
        # Log the specific error to help with debugging
        print(f"Error in get_current_user: {str(e)}")
        print(f"User ID: {user_uuid}")
        import traceback
        traceback.print_exc()
        # Don't fail the authentication, but log the error
        pass

    return user_uuid
