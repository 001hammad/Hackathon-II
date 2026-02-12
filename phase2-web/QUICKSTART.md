# Phase 2 Web Todo App - Quick Start Guide

## 🚀 Your Application is Ready!

Both your backend and frontend are running successfully:
- **Backend API**: http://localhost:8001
- **Frontend App**: http://localhost:3000
- **Database**: Neon PostgreSQL (Connected ✅)

---

## 📋 Quick Access

### Login to Your App
1. Open your browser and go to: **http://localhost:3000/login**
2. Use the test account:
   - **Email**: `test@example.com`
   - **Password**: `TestPass123`
3. Click "Sign In"

### Create a New Account
1. Go to: **http://localhost:3000/signup**
2. Enter your email and password
   - Password must have: min 8 chars, 1 uppercase, 1 lowercase, 1 number
3. Click "Sign Up"

---

## 🎯 What You Can Do

### Task Management
- ✅ **Add Tasks**: Type in the input field and press Enter
- ✅ **Complete Tasks**: Click the checkbox next to any task
- ✅ **Edit Tasks**: Click the edit icon to modify task description
- ✅ **Delete Tasks**: Click the delete icon to remove a task
- ✅ **Filter Tasks**: Use "All", "Active", or "Completed" buttons
- ✅ **Search Tasks**: Use the search bar to find specific tasks

### User Features
- ✅ **Secure Login**: JWT-based authentication
- ✅ **Data Isolation**: Each user only sees their own tasks
- ✅ **Persistent Storage**: All data saved to Neon PostgreSQL
- ✅ **Responsive Design**: Works on mobile, tablet, and desktop

---

## 🔧 If You Need to Restart

### Start Backend
```bash
cd D:/hackathone_2/phase2-web/backend
python main.py
```
The backend will start on **port 8001** (not 8000 to avoid conflicts)

### Start Frontend
```bash
cd D:/hackathone_2/phase2-web/frontend
npm run dev
```
The frontend will start on **port 3000**

---

## 📊 API Documentation

Visit **http://localhost:8001/docs** to see interactive API documentation (Swagger UI)

### Available Endpoints

**Authentication:**
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout

**Tasks (requires authentication):**
- `GET /api/tasks/` - Get all your tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task description
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete task

---

## 🗄️ Database Information

**Provider**: Neon Serverless PostgreSQL
**Connection**: Configured in `.env` file
**Tables**:
- `users` - User accounts with hashed passwords
- `tasks` - Todo items linked to users

---

## 🔐 Security Features

✅ **Password Hashing**: bcrypt with 12 rounds
✅ **JWT Tokens**: Secure authentication tokens
✅ **User Isolation**: Database-level filtering by user_id
✅ **Protected Routes**: Middleware redirects unauthenticated users
✅ **CORS Configuration**: Proper cross-origin setup

---

## 🎨 UI Features

✅ **Modern Design**: Tailwind CSS + shadcn/ui components
✅ **Smooth Animations**: Framer Motion transitions
✅ **Dark Mode Support**: Automatic theme detection
✅ **Loading States**: Skeleton loaders and spinners
✅ **Error Handling**: User-friendly error messages
✅ **Toast Notifications**: Success/error feedback

---

## 📁 Project Structure

```
phase2-web/
├── backend/                 # FastAPI Backend (Port 8001)
│   ├── app/
│   │   ├── models/         # Database models (User, Task)
│   │   ├── routes/         # API endpoints (auth, tasks)
│   │   ├── auth/           # JWT authentication
│   │   ├── database/       # Neon PostgreSQL connection
│   │   └── core/           # Configuration & security
│   ├── main.py             # Entry point
│   └── .env                # Backend config
│
└── frontend/                # Next.js Frontend (Port 3000)
    ├── app/
    │   ├── (auth)/         # Login & Signup pages
    │   ├── (dashboard)/    # Main dashboard
    │   ├── api/            # BFF proxy routes
    │   ├── components/     # React components
    │   └── lib/            # API client & utilities
    └── .env                # Frontend config
```

---

## 🐛 Troubleshooting

### Backend won't start
- **Check port**: Make sure port 8001 is available
- **Check database**: Verify DATABASE_URL in `.env`
- **Install dependencies**: Run `pip install -r requirements.txt`

### Frontend won't start
- **Check port**: Make sure port 3000 is available
- **Check API URL**: Verify NEXT_PUBLIC_API_URL=http://localhost:8001
- **Install dependencies**: Run `npm install`

### Can't login
- **Check backend**: Make sure backend is running on port 8001
- **Check secrets**: Ensure BETTER_AUTH_SECRET matches in both .env files
- **Check browser console**: Look for error messages

### Tasks not loading
- **Check authentication**: Make sure you're logged in
- **Check API**: Visit http://localhost:8001/docs to test endpoints
- **Check browser console**: Look for network errors

---

## 📝 Test Account

A test account has been created for you:
- **Email**: test@example.com
- **Password**: TestPass123

You can use this immediately to test the application!

---

## 🚀 Next Steps

### Recommended Enhancements
1. Add password reset functionality
2. Implement email verification
3. Add task categories and tags
4. Add due dates and reminders
5. Implement task sharing
6. Add export/import functionality
7. Deploy to production (Vercel + Railway)

### Testing
- Write unit tests for backend (pytest)
- Write component tests for frontend (Jest)
- Add E2E tests (Playwright)

---

## 📚 Additional Resources

- **Full Documentation**: See `SETUP_COMPLETE.md`
- **API Docs**: http://localhost:8001/docs
- **Specs**: Check `specs/001-phase2-web-todo/` folder

---

## ✅ Status Check

Run this command to verify everything is working:

```bash
# Check backend
curl http://localhost:8001/health

# Check frontend
curl http://localhost:3000/
```

---

**Last Updated**: 2026-02-12
**Status**: ✅ All systems operational
**Backend**: Running on port 8001
**Frontend**: Running on port 3000
**Database**: Neon PostgreSQL connected

---

## 🎉 You're All Set!

Your Phase 2 multi-user todo application is ready to use. Open http://localhost:3000/login and start managing your tasks!
