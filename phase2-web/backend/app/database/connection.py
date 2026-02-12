"""Database connection module for SQLModel."""
import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLModel engine
# Check if it's a SQLite database for different connect_args
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Set to False in production
        connect_args={"check_same_thread": False},  # Required for SQLite with threading
    )
else:
    # PostgreSQL specific configuration (Neon)
    # Note: sslmode is already in the DATABASE_URL connection string
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Set to False in production
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections every hour
        pool_size=5,  # Reduced for Neon's connection limits
        max_overflow=10,
    )


def get_session():
    """
    Dependency that provides a database session.
    Use with FastAPI Depends for automatic session management.

    Usage:
        @app.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            tasks = session.query(Task).all()
            return tasks
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
