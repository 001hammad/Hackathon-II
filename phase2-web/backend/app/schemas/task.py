"""Pydantic schemas for task endpoints."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""

    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task description",
        example="Buy groceries"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy groceries"
            }
        }


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""

    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Updated task description",
        example="Buy groceries and cook dinner"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy groceries and cook dinner"
            }
        }


class TaskResponse(BaseModel):
    """Response schema for task data."""

    id: int = Field(..., description="Unique task identifier", example=1)
    user_id: str = Field(..., description="Owner's user ID (Better Auth string ID)")
    description: str = Field(..., description="Task description", max_length=500)
    completed: bool = Field(..., description="Completion status", example=False)
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "WcpSybz2Ws4QFxad1mIKHf7Dc39rCvdF",
                "description": "Buy groceries",
                "completed": False,
                "created_at": "2026-01-02T10:00:00Z",
                "updated_at": "2026-01-02T10:00:00Z"
            }
        }
