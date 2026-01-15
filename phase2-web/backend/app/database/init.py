"""Database initialization module - creates all tables."""
from sqlmodel import SQLModel
from .connection import engine


def create_tables():
    """
    Create all database tables defined in SQLModel models.

    This function should be called on application startup to ensure
    all tables exist in the database.

    Usage:
        from app.database.init import create_tables
        create_tables()
    """
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def drop_tables():
    """
    Drop all database tables.

    WARNING: This will delete all data. Use only for testing/development.
    """
    SQLModel.metadata.drop_all(bind=engine)
    print("All database tables dropped")
