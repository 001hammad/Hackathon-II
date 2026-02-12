---
title: Phase 2 Todo API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Phase 2 Todo API

FastAPI backend for multi-user todo application with Better Auth integration and Neon PostgreSQL.

## Features

- 🔐 JWT Authentication with Better Auth
- ✅ Full CRUD operations for tasks
- 👥 Multi-user support with data isolation
- 🗄️ PostgreSQL database (Neon)
- 🚀 FastAPI with automatic API docs
- 🔒 Secure password hashing with bcrypt

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Tasks (Authenticated)
- `GET /api/tasks/` - List all user's tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

## Documentation

Interactive API documentation available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## Tech Stack

- FastAPI 0.109.0
- SQLModel 0.0.14
- PostgreSQL (Neon)
- Python 3.11
- Uvicorn
