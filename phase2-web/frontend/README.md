# Phase II Frontend - Next.js 16+ App Router

Multi-user todo application frontend with JWT authentication.

## Tech Stack

- **Framework**: Next.js 16.1+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion 12+
- **Icons**: Lucide React
- **Toast Notifications**: Sonner

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create or update `.env.local` file:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=https://hammad224-todo-app-backend.hf.space/

# Authentication Secret (MUST match backend)
BETTER_AUTH_SECRET=your-secure-secret-key-minimum-32-characters
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be:
- Minimum 32 characters
- Identical to backend `.env` file
- Kept secret (never commit to git)

## Running the Application

### Development Server

```bash
npm run dev
```

The app will be available at: **https://hackathon-ii-lyart.vercel.app/**

### Build for Production

```bash
npm run build
npm start
```

### Run Tests

```bash
npm test
```

## Application Structure

### Pages (App Router)

- **/** - Root (redirects to /login)
- **/login** - User login page
- **/signup** - User registration page
- **/dashboard** - Main todo dashboard (protected route)

### Components

**UI Components** (`components/ui/`):
- `button.tsx` - Button component
- `input.tsx` - Input field
- `checkbox.tsx` - Checkbox for task completion
- `dialog.tsx` - Modal dialogs
- `sonner.tsx` - Toast notifications

**Feature Components** (`components/`):
- `Header.tsx` - App header with logout button
- `TaskForm.tsx` - Add new task form
- `TaskList.tsx` - Task list container
- `TaskItem.tsx` - Individual task with edit/delete/toggle

### API Client (`lib/api/client.ts`)

Type-safe API client with automatic JWT token attachment:
- `api.signup()` - Register new user
- `api.login()` - Authenticate user
- `api.logout()` - Logout user
- `api.getTasks()` - Fetch user's tasks
- `api.createTask()` - Create new task
- `api.updateTask()` - Update task description
- `api.toggleTask()` - Toggle completion status
- `api.deleteTask()` - Delete task

## Features

### Authentication

- ✅ User registration with email/password
- ✅ User login with credential verification
- ✅ JWT token storage in localStorage
- ✅ Automatic token attachment to API requests
- ✅ Protected routes (redirect to login if not authenticated)
- ✅ Logout functionality

### Task Management

- ✅ Create new tasks
- ✅ View task list (only user's own tasks)
- ✅ Toggle task completion status
- ✅ Edit task description (inline editing)
- ✅ Delete tasks with confirmation dialog
- ✅ Real-time UI updates
- ✅ Toast notifications for all operations

### User Experience

- ✅ Clean, modern UI with shadcn/ui components
- ✅ Loading states during API calls
- ✅ Error handling with user-friendly messages
- ✅ Form validation
- ✅ Responsive design (basic - full responsive in Phase 5)

## Usage Guide

### First Time Setup

1. **Start backend**: `cd ../backend && uvicorn app.main:app --reload`
2. **Start frontend**: `npm run dev`
3. **Open browser**: https://hackathon-ii-lyart.vercel.app/
4. **Create account**: Click "Sign up" and enter email/password
5. **Add tasks**: Use the form to add your first task
6. **Manage tasks**: Toggle, edit, or delete tasks as needed

### Authentication Flow

1. **Signup**: `/signup` → Enter email/password → Auto-login → Redirect to dashboard
2. **Login**: `/login` → Enter credentials → Receive JWT → Redirect to dashboard
3. **Protected Access**: All API calls include `Authorization: Bearer <token>` header
4. **Logout**: Click logout button → Token cleared → Redirect to login

### Task Operations

- **Add**: Type description → Press "Add Task"
- **Toggle**: Click checkbox to mark complete/incomplete
- **Edit**: Click pencil icon → Modify description → Click "Save"
- **Delete**: Click trash icon → Confirm in dialog → Task removed

## Troubleshooting

### "Authorization header missing" error

- Make sure you're logged in
- Check that JWT token is in localStorage (DevTools → Application → Local Storage)
- Verify backend is accessible at https://hammad224-todo-app-backend.hf.space/

### CORS errors

- Verify backend CORS is configured for https://hackathon-ii-lyart.vercel.app/
- Check `NEXT_PUBLIC_API_URL` in `.env.local` matches backend URL

### Tasks not loading

- Check browser console for errors
- Verify backend is running and accessible
- Test backend directly at https://hammad224-todo-app-backend.hf.space/docs

### Build errors

```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | http://localhost:8000 |
| BETTER_AUTH_SECRET | JWT secret (match backend) | your-32-char-secret |

## Next Steps

- **Phase 5 (US3)**: Add responsive design for mobile/tablet
- **Phase 6 (US4)**: Add Framer Motion animations
- **Phase 7**: Polish with loading states and error boundaries

## Related Documentation

- [Backend README](../backend/README.md)
- [API Specification](../../specs/001-phase2-web-todo/contracts/openapi.yaml)
- [Implementation Plan](../../specs/001-phase2-web-todo/plan.md)
- [Tasks Breakdown](../../specs/001-phase2-web-todo/tasks.md)
