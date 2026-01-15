# Phase II MVP Testing Guide

Complete guide for testing the Phase II Full-Stack Multi-User Web Todo Application.

## Prerequisites

### Backend Setup

1. **Configure Database** (`.env` file already updated with secret)
   - Get Neon PostgreSQL connection string from https://neon.tech
   - Update `DATABASE_URL` and `DATABASE_URL_ASYNC` in `phase2-web/backend/.env`
   - Current secret: `9uleKT09aMwhqTAF6Yh1jnew0z2vu1Su` ✅

2. **Install Backend Dependencies**
   ```bash
   cd phase2-web/backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Update Frontend Secret** - Must match backend
   ```bash
   cd phase2-web/frontend
   # Edit .env.local and set:
   BETTER_AUTH_SECRET=9uleKT09aMwhqTAF6Yh1jnew0z2vu1Su
   ```

## Running the MVP

### Terminal 1: Start Backend

```bash
cd phase2-web/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Expected Output**:
```
✅ Configuration loaded successfully
🚀 Starting Phase II Todo API v1.0.0
📊 Creating database tables...
✅ Database tables created successfully
✅ Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Verify Backend**:
- Open http://localhost:8000 → Should show welcome message
- Open http://localhost:8000/docs → Should show Swagger API docs
- Check for 2 endpoints: `/api/auth` and `/api/tasks`

### Terminal 2: Start Frontend

```bash
cd phase2-web/frontend
npm run dev
```

**Expected Output**:
```
   ▲ Next.js 16.1.1
   - Local:        http://localhost:3000
   - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.3s
```

**Verify Frontend**:
- Open http://localhost:3000 → Should redirect to http://localhost:3000/login
- Login page should display with email/password form

## MVP Testing Checklist

### User Story 1: Authentication (P1) ✅

#### Test 1.1: User Registration

**Steps**:
1. Navigate to http://localhost:3000 (should redirect to /login)
2. Click "Sign up" link
3. Enter email: `test@example.com`
4. Enter password: `TestPass123` (meets requirements: 8+ chars, 1 upper, 1 lower, 1 number)
5. Click "Sign Up"

**Expected Results**:
- ✅ Account created successfully
- ✅ Automatically logged in
- ✅ Redirected to /dashboard
- ✅ JWT token stored in localStorage

**Verify**:
- Open DevTools → Application → Local Storage → `auth_token` should exist

#### Test 1.2: User Login

**Steps**:
1. Click logout button
2. Should redirect to /login
3. Enter email: `test@example.com`
4. Enter password: `TestPass123`
5. Click "Sign In"

**Expected Results**:
- ✅ Login successful
- ✅ Redirected to /dashboard
- ✅ JWT token refreshed in localStorage

#### Test 1.3: Invalid Credentials

**Steps**:
1. Logout
2. Try to login with wrong password: `WrongPass123`

**Expected Results**:
- ✅ Error message: "Invalid email or password"
- ✅ Stays on login page
- ✅ No token stored

#### Test 1.4: Duplicate Email

**Steps**:
1. Go to /signup
2. Try to register with existing email: `test@example.com`

**Expected Results**:
- ✅ Error message: "Email already registered"
- ✅ Stays on signup page

#### Test 1.5: Weak Password

**Steps**:
1. Go to /signup
2. Enter email: `test2@example.com`
3. Enter weak password: `weak` (too short, no numbers)
4. Click "Sign Up"

**Expected Results**:
- ✅ Error message about password requirements
- ✅ Account not created

#### Test 1.6: Session Persistence

**Steps**:
1. Login successfully
2. Close browser tab
3. Open new tab and navigate to http://localhost:3000

**Expected Results**:
- ✅ Token still in localStorage
- ✅ Redirected to /dashboard (not /login)
- ✅ Session persists

#### Test 1.7: Logout

**Steps**:
1. Click "Logout" button in header

**Expected Results**:
- ✅ Token cleared from localStorage
- ✅ Redirected to /login
- ✅ Cannot access /dashboard without logging in again

---

### User Story 2: Task Management (P1) ✅

#### Test 2.1: Create Task

**Steps**:
1. Login to account
2. In task form, enter: "Buy groceries"
3. Click "Add Task"

**Expected Results**:
- ✅ Toast notification: "Task created successfully!"
- ✅ Task appears in list immediately
- ✅ Task shows as incomplete (checkbox unchecked)
- ✅ Character counter shows "14/500 characters"

#### Test 2.2: View Task List

**Steps**:
1. Create multiple tasks:
   - "Buy groceries"
   - "Finish project"
   - "Call mom"
2. Refresh page

**Expected Results**:
- ✅ All 3 tasks visible
- ✅ Tasks persist after refresh
- ✅ Only user's own tasks visible (test with 2nd user account)

#### Test 2.3: User Isolation

**Steps**:
1. Create tasks as User A (`test@example.com`)
2. Logout
3. Create new account as User B (`test2@example.com`)
4. Login as User B

**Expected Results**:
- ✅ User B sees empty task list
- ✅ User B cannot see User A's tasks
- ✅ Database queries filter by user_id

#### Test 2.4: Toggle Task Completion

**Steps**:
1. Click checkbox next to "Buy groceries"

**Expected Results**:
- ✅ Checkbox becomes checked
- ✅ Text shows strikethrough
- ✅ Task marked as completed
2. Click checkbox again

**Expected Results**:
- ✅ Checkbox unchecked
- ✅ Strikethrough removed
- ✅ Task marked as incomplete

#### Test 2.5: Edit Task Description

**Steps**:
1. Click pencil (edit) icon next to task
2. Modify description: "Buy groceries and cook dinner"
3. Click "Save"

**Expected Results**:
- ✅ Toast: "Task updated!"
- ✅ Description updated in list
- ✅ Edit mode exits
- ✅ Changes persist

#### Test 2.6: Cancel Edit

**Steps**:
1. Click edit icon
2. Change description
3. Click "Cancel"

**Expected Results**:
- ✅ Edit mode exits
- ✅ Original description restored
- ✅ No changes saved

#### Test 2.7: Delete Task

**Steps**:
1. Click trash (delete) icon next to task
2. Confirmation dialog appears
3. Click "Delete"

**Expected Results**:
- ✅ Confirmation dialog: "Are you sure you want to delete...?"
- ✅ Toast: "Task deleted!"
- ✅ Task removed from list immediately
- ✅ Task permanently deleted from database

#### Test 2.8: Cancel Delete

**Steps**:
1. Click delete icon
2. Click "Cancel" in dialog

**Expected Results**:
- ✅ Dialog closes
- ✅ Task remains in list
- ✅ No deletion occurs

#### Test 2.9: Empty Description Validation

**Steps**:
1. Try to add task with empty description
2. Try to edit task to empty description

**Expected Results**:
- ✅ Add button disabled when input empty
- ✅ Toast error: "Please enter a task description"
- ✅ Save button disabled when description empty

#### Test 2.10: Description Length Limit

**Steps**:
1. Enter description with 501+ characters

**Expected Results**:
- ✅ Character counter shows "501/500 characters" (red)
- ✅ Toast error: "Description must be 500 characters or less"
- ✅ Task not created/updated

---

## Backend API Testing

### Using Swagger UI (http://localhost:8000/docs)

#### Test Auth Endpoints

**1. POST /api/auth/signup**
```json
{
  "email": "api-test@example.com",
  "password": "ApiTest123"
}
```

**Expected Response (201)**:
```json
{
  "message": "User created successfully",
  "user": {
    "id": "uuid-here",
    "email": "api-test@example.com"
  },
  "token": "eyJhbGc..."
}
```

**2. POST /api/auth/login**
```json
{
  "email": "api-test@example.com",
  "password": "ApiTest123"
}
```

**Expected Response (200)**:
```json
{
  "message": "Login successful",
  "user": { ... },
  "token": "eyJhbGc..."
}
```

#### Test Task Endpoints (Requires JWT)

**1. Click "Authorize" button in Swagger UI**
- Enter: `Bearer <your-token-from-login>`
- Click "Authorize"

**2. GET /api/tasks**

**Expected Response (200)**:
```json
{
  "tasks": []
}
```

**3. POST /api/tasks**
```json
{
  "description": "API test task"
}
```

**Expected Response (201)**:
```json
{
  "id": 1,
  "user_id": "uuid",
  "description": "API test task",
  "completed": false,
  "created_at": "2026-01-02T...",
  "updated_at": "2026-01-02T..."
}
```

**4. PATCH /api/tasks/1/toggle**

**Expected Response (200)**:
```json
{
  "id": 1,
  "completed": true,
  ...
}
```

**5. DELETE /api/tasks/1**

**Expected Response (200)**:
```json
{
  "message": "Task deleted successfully"
}
```

---

## Error Testing

### Authentication Errors

**Missing Token**:
```bash
curl http://localhost:8000/api/tasks
```
Expected: `401 Unauthorized - Authorization header missing`

**Invalid Token**:
```bash
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/tasks
```
Expected: `401 Unauthorized - Invalid token`

**Wrong Format**:
```bash
curl -H "Authorization: invalid-format" http://localhost:8000/api/tasks
```
Expected: `401 Unauthorized - Invalid authorization format`

### Validation Errors

**Invalid Email**:
```bash
POST /api/auth/signup
{ "email": "not-an-email", "password": "TestPass123" }
```
Expected: `400 Bad Request - Invalid email format`

**Weak Password**:
```bash
POST /api/auth/signup
{ "email": "test@example.com", "password": "weak" }
```
Expected: `400 Bad Request - Password must be at least 8 characters`

**Empty Description**:
```bash
POST /api/tasks
{ "description": "" }
```
Expected: `400 Bad Request - Description cannot be empty`

---

## Performance Testing

### Response Time Targets (from SC-002, SC-003)

```bash
# Test task creation time (should be < 2 seconds)
time curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"description":"Test task"}'

# Test task toggle time (should be < 1 second)
time curl -X PATCH http://localhost:8000/api/tasks/1/toggle \
  -H "Authorization: Bearer <token>"
```

---

## Manual Test Results Template

### User Story 1: Authentication

- [ ] 1.1 User Registration ✅/❌
- [ ] 1.2 User Login ✅/❌
- [ ] 1.3 Invalid Credentials ✅/❌
- [ ] 1.4 Duplicate Email ✅/❌
- [ ] 1.5 Weak Password ✅/❌
- [ ] 1.6 Session Persistence ✅/❌
- [ ] 1.7 Logout ✅/❌

### User Story 2: Task Management

- [ ] 2.1 Create Task ✅/❌
- [ ] 2.2 View Task List ✅/❌
- [ ] 2.3 User Isolation ✅/❌
- [ ] 2.4 Toggle Task Completion ✅/❌
- [ ] 2.5 Edit Task Description ✅/❌
- [ ] 2.6 Cancel Edit ✅/❌
- [ ] 2.7 Delete Task ✅/❌
- [ ] 2.8 Cancel Delete ✅/❌
- [ ] 2.9 Empty Description Validation ✅/❌
- [ ] 2.10 Description Length Limit ✅/❌

### Success Criteria Verification

- [ ] SC-001: Registration + login < 90 seconds ✅/❌
- [ ] SC-002: Task creation < 2 seconds ✅/❌
- [ ] SC-003: Task toggle < 1 second ✅/❌
- [ ] SC-008: User isolation enforced ✅/❌

---

## Known Issues / Notes

(Document any issues found during testing)

---

## MVP Status

**Phases 1-4 Complete**: 59/59 tasks ✅

- ✅ Phase 1: Setup (10 tasks)
- ✅ Phase 2: Foundational (19 tasks)
- ✅ Phase 3: User Story 1 - Authentication (11 tasks)
- ✅ Phase 4: User Story 2 - Task Management (19 tasks)

**MVP Ready for Testing**: Yes ✅

**Next**: Test with Neon database, verify all user stories work independently
