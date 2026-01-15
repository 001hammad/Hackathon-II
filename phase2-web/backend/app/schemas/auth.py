"""Pydantic schemas for authentication endpoints."""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class SignupRequest(BaseModel):
    """
    Request schema for user registration.

    Validates:
    - Email format (RFC 5322)
    - Password requirements: min 8 chars, 1 upper, 1 lower, 1 number
    """

    email: EmailStr = Field(
        ...,
        description="User's email address (must be unique)",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        description="Password (min 8 chars, 1 upper, 1 lower, 1 number)",
        example="SecurePass123"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123"
            }
        }


class LoginRequest(BaseModel):
    """Request schema for user login."""

    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="User's password",
        example="SecurePass123"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123"
            }
        }


class UserResponse(BaseModel):
    """User data included in authentication responses."""

    id: UUID = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for successful authentication (signup/login)."""

    message: str = Field(
        ...,
        description="Success message",
        example="User created successfully"
    )
    user: UserResponse = Field(..., description="User information")
    token: str = Field(
        ...,
        description="JWT token for authentication",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MDQ0NTYwMDB9.signature"
            }
        }
