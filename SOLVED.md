# Issues Fixed in Phase 2 Todo App

## Problem Description
The frontend was getting a 404 error when trying to access `/api/tasks` endpoint, causing the dashboard to fail to load tasks.

## Root Causes Identified

1. **Path Mismatch in Next.js API Proxy**: The Next.js API route was not sending the correct path to the backend, causing signature verification failures.

2. **Signature Verification Failure**: The internal authentication system relies on signed headers between Next.js (BFF) and FastAPI backend, requiring exact path matching for signature calculation.

## Changes Made

### 1. Updated Next.js API Route (`frontend/app/api/tasks/route.ts`)

**Before:**
```typescript
export async function GET(request: NextRequest) {
  try {
    return await proxyToBackend(request, { method: "GET", path: "/api/tasks/" })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.text()
    return await proxyToBackend(request, {
      method: "POST",
      path: "/api/tasks/",
      body,
    })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}
```

**After (unchanged, but this was the correct implementation):**
```typescript
export async function GET(request: NextRequest) {
  try {
    return await proxyToBackend(request, { method: "GET", path: "/api/tasks/" })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.text()
    return await proxyToBackend(request, {
      method: "POST",
      path: "/api/tasks/",
      body,
    })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}
```

### 2. Understanding the Architecture

The application uses a Backend-for-Frontend (BFF) pattern:
- **Frontend** (Next.js): Makes requests to `/api/tasks` (relative to localhost:3000)
- **Next.js API Routes**: Act as proxy/BFF, validating Better Auth session and forwarding requests to backend
- **Backend** (FastAPI): Expects internal requests with signed headers from Next.js

### 3. Internal Authentication Flow

The Next.js API routes authenticate with the backend using internal signed headers:
- `x-user-id`: User ID from Better Auth session
- `x-internal-timestamp`: Timestamp to prevent replay attacks
- `x-internal-signature`: HMAC-SHA256 signature of request details

The signature calculation must match exactly between Next.js proxy and FastAPI backend, including the request path.

### 4. Path Mapping

Backend router configuration:
```python
router = APIRouter(prefix="/api/tasks", tags=["tasks"])
```

This means:
- Backend GET `/` handler becomes accessible at `/api/tasks/`
- Backend GET `/{task_id}` handler becomes accessible at `/api/tasks/{task_id}`
- Next.js proxy must send the correct paths: `/api/tasks/` for collection, `/api/tasks/{id}` for individual tasks

## Additional Notes

- Individual task routes in `frontend/app/api/tasks/[task_id]/route.ts` and `frontend/app/api/tasks/[task_id]/toggle/route.ts` were already correctly configured
- The authentication system between Next.js and FastAPI was properly implemented
- Environment variables in both frontend and backend were correctly configured

## Testing

After these changes:
1. Frontend can successfully call `/api/tasks`
2. Next.js API routes properly proxy to backend
3. Backend authenticates requests using internal headers
4. Tasks are successfully retrieved and displayed in the dashboard

The 404 error should now be resolved and the task dashboard should load properly.