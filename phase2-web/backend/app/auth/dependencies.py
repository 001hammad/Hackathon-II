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


INTERNAL_TIME_SKEW_MS = 5 * 60 * 1000  # 5 minutes


async def get_current_user(request: Request):
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

    # Debug logging
    print(f"[AUTH DEBUG] Received signature: {signature}")
    print(f"[AUTH DEBUG] Expected signature: {expected}")
    print(f"[AUTH DEBUG] Payload: {payload}")
    print(f"[AUTH DEBUG] User ID: {user_id}")
    print(f"[AUTH DEBUG] Timestamp: {timestamp}")
    print(f"[AUTH DEBUG] Method: {method}")
    print(f"[AUTH DEBUG] Path: {path}")
    print(f"[AUTH DEBUG] Body: {body_text}")

    if not hmac.compare_digest(expected, signature):
        print(f"[AUTH DEBUG] Signature mismatch!")
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Better Auth uses string IDs, not UUIDs
    # Return the user_id as-is (it's a string)
    print(f"[AUTH DEBUG] Authentication successful, returning user_id: {user_id}")
    return user_id
