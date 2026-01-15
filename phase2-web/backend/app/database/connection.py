"""Database connection module for Neon PostgreSQL with SQLModel."""
import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLModel engine for Neon PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600  # Recycle connections every hour
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
