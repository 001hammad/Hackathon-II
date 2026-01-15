# Phase II Backend - FastAPI + SQLModel + Neon PostgreSQL

Multi-user todo application backend with JWT authentication and user isolation.

## Tech Stack

- **Framework**: FastAPI 0.109+
- **ORM**: SQLModel 0.0.14+
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create or update `.env` file with your Neon PostgreSQL credentials:

```bash
# Neon PostgreSQL Connection
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
DATABASE_URL_ASYNC=postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Authentication Secret (MUST match frontend)
BETTER_AUTH_SECRET=your-secure-secret-key-minimum-32-characters

# JWT Configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be:
- Minimum 32 characters
- Identical in both backend and frontend
- Kept secret (never commit to git)

### 4. Initialize Database

The database tables will be created automatically on first run via the startup event in `app/main.py`.

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/signup | Register new user | No |
| POST | /api/auth/login | Login user | No |
| POST | /api/auth/logout | Logout user | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/tasks | List user's tasks | Yes |
| POST | /api/tasks | Create new task | Yes |
| GET | /api/tasks/{id} | Get specific task | Yes |
| PUT | /api/tasks/{id} | Update task description | Yes |
| PATCH | /api/tasks/{id}/toggle | Toggle completion | Yes |
| DELETE | /api/tasks/{id} | Delete task | Yes |

## Project Structure

```
app/
├── models/          # SQLModel ORM models
│   ├── user.py      # User model
│   └── task.py      # Task model
├── routes/          # API endpoints
│   ├── auth.py      # Authentication endpoints
│   └── tasks.py     # Task CRUD endpoints
├── auth/            # Authentication middleware
│   └── dependencies.py  # JWT verification
├── database/        # Database configuration
│   ├── connection.py    # SQLModel engine
│   └── init.py          # Table creation
├── schemas/         # Pydantic request/response schemas
│   ├── auth.py      # Auth schemas
│   └── task.py      # Task schemas
├── core/            # Core configuration
│   ├── config.py    # Environment variables
│   └── security.py  # Password hashing
└── main.py          # FastAPI app instance

tests/
├── conftest.py      # Pytest fixtures
├── test_auth.py     # Auth endpoint tests
├── test_tasks.py    # Task CRUD tests
└── test_user_isolation.py  # Security tests
```

## Security Features

- **Password Hashing**: bcrypt with automatic salt
- **JWT Tokens**: HS256 algorithm with configurable expiry
- **User Isolation**: All queries filter by authenticated user_id
- **CORS**: Configured for frontend (http://localhost:3000)
- **Input Validation**: Pydantic schemas validate all requests

## Development Guidelines

### User Isolation (CRITICAL)

**ALL task queries MUST filter by user_id from JWT**:

```python
# ✅ CORRECT
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == current_user_id  # From JWT
)

# ❌ WRONG - Security vulnerability!
statement = select(Task).where(Task.id == task_id)
```

### Error Handling

- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Task doesn't exist or belongs to another user
- `400 Bad Request`: Validation error (email format, password requirements)
- `409 Conflict`: Email already registered

## Troubleshooting

### Database Connection Errors

```bash
# Verify DATABASE_URL is correct
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_URL'))"

# Test connection manually
from sqlmodel import create_engine
engine = create_engine(DATABASE_URL)
```

### JWT Verification Fails

- Verify `BETTER_AUTH_SECRET` matches in frontend and backend
- Check token is being sent in `Authorization: Bearer <token>` header
- Verify token hasn't expired (default 24 hours)

### Password Validation Fails

Password must meet requirements:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number

## Next Steps

1. Set up Neon PostgreSQL database at https://neon.tech
2. Update `.env` with your database credentials
3. Run the development server
4. Test with API docs at http://localhost:8000/docs
5. Connect frontend at http://localhost:3000

## Related Documentation

- [Frontend README](../frontend/README.md)
- [API Specification](../../specs/001-phase2-web-todo/contracts/openapi.yaml)
- [Data Model](../../specs/001-phase2-web-todo/data-model.md)
- [Implementation Plan](../../specs/001-phase2-web-todo/plan.md)
