# Database Connection Template
# Copy to app/database.py

import os
from typing import Generator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Import models for metadata
from app.models import SQLModel  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.task import Task  # noqa: F401


# ============== CONFIGURATION ==============

# Get connection string from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

DATABASE_URL_ASYNC = os.getenv(
    "DATABASE_URL_ASYNC",
    "postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
)


# ============== SYNC ENGINE (for migrations) ==============

# Sync engine - use for Alembic migrations, seeds, CLI scripts
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections hourly
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    }
)

# Sync session factory
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)


# ============== ASYNC ENGINE (for API) ==============

# Async engine - use for FastAPI endpoints
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=False,  # Set to True for debugging SQL
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,          # Base pool size
    max_overflow=10,      # Max additional connections
    pool_recycle=3600,    # Recycle connections hourly
    pool_reset_on_return="commit",
    connect_args={
        "ssl": "require",
        "timeout": 10,
        "command_timeout": 60
    }
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keep object accessible after commit
    autocommit=False,
    autoflush=False
)


# ============== DEPENDENCIES ==============

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> Generator[AsyncSession, None, None]:
    """
    FastAPI dependency that provides an async database session.

    Usage:
        @router.get("/tasks")
        async def list_tasks(
            session: AsyncSession = Depends(get_async_session)
        ):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_sync_session():
    """
    Context manager for sync sessions (CLI scripts, etc.)

    Usage:
        async with get_sync_session() as session:
            result = session.query(Task).all()
    """
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ============== INITIALIZATION ==============

def create_tables():
    """
    Create all database tables based on SQLModel metadata.

    Call this on application startup.
    """
    SQLModel.metadata.create_all(bind=sync_engine)
    print("Database tables created successfully")


async def create_tables_async():
    """
    Create all database tables asynchronously.

    Alternative to create_tables() for async contexts.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def drop_tables():
    """
    Drop all database tables.

    WARNING: This deletes all data! Use only for testing.
    """
    SQLModel.metadata.drop_all(bind=sync_engine)
    print("Database tables dropped")


async def drop_tables_async():
    """
    Drop all database tables asynchronously.

    WARNING: This deletes all data! Use only for testing.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# ============== HEALTH CHECK ==============

async def check_database_connection() -> bool:
    """
    Verify database is reachable and responsive.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


async def get_database_info() -> dict:
    """
    Get database version and connection info.

    Returns:
        Dict with database information
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()

            result = await session.execute(
                text("SELECT current_database()")
            )
            database = result.scalar()

            return {
                "connected": True,
                "database": database,
                "version": version,
                "pool": {
                    "size": async_engine.pool.size(),
                    "checked_out": async_engine.pool.checkedout(),
                    "overflow": async_engine.pool.overflow()
                }
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }


# ============== CLEANUP ==============

async def close_connections():
    """
    Close all database connections.

    Call this on application shutdown.
    """
    await async_engine.dispose()
    sync_engine.dispose()
    print("Database connections closed")


# ============== SETUP FUNCTION ==============

def setup_database():
    """
    Initialize database on application startup.

    Call this in main.py or lifespan handler.
    """
    import asyncio

    # Create tables
    create_tables()
    print("Database initialized")


async def setup_database_async():
    """
    Initialize database asynchronously.

    Call this in FastAPI lifespan.
    """
    await create_tables_async()
    print("Database initialized (async)")


# ============== USAGE ==============

"""
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import (
    setup_database_async,
    close_connections,
    check_database_connection
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await setup_database_async()
    connected = await check_database_connection()
    print(f"Database connected: {connected}")
    yield
    # Shutdown
    await close_connections()

app = FastAPI(lifespan=lifespan)


# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_async_session
from app.models import Task, TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return [TaskResponse.from_orm(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
):
    task = Task(**task_data.model_dump(), user_id="current-user-id")
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return TaskResponse.from_orm(task)
"""
