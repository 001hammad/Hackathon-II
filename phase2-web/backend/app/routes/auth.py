"""Authentication endpoints for user registration and login."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from jose import jwt
from datetime import datetime, timedelta
from uuid import UUID

from ..database.connection import get_session
from ..models.user import User
from ..schemas.auth import SignupRequest, LoginRequest, AuthResponse, UserResponse
from ..core.security import hash_password, verify_password, validate_password_strength
from ..core.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])


def create_access_token(user_id: UUID) -> str:
    """
    Create JWT access token for authenticated user.

    Args:
        user_id: User's unique identifier

    Returns:
        str: JWT token
    """
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "sub": str(user_id),  # User ID in 'sub' claim
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(
    signup_data: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Validates:
    - Email format (done by Pydantic EmailStr)
    - Email uniqueness
    - Password strength (min 8 chars, 1 upper, 1 lower, 1 number)

    Returns JWT token for automatic login after signup.
    """
    # Validate password strength
    is_valid, error_msg = validate_password_strength(signup_data.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Check if email already exists
    statement = select(User).where(User.email == signup_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(signup_data.password)

    # Create new user
    new_user = User(
        email=signup_data.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    token = create_access_token(new_user.id)

    return AuthResponse(
        message="User created successfully",
        user=UserResponse(id=new_user.id, email=new_user.email),
        token=token
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user with email and password.

    Returns JWT token for accessing protected endpoints.
    """
    # Find user by email
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token(user.id)

    return AuthResponse(
        message="Login successful",
        user=UserResponse(id=user.id, email=user.email),
        token=token
    )


@router.post("/logout")
async def logout():
    """
    Logout user.

    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token from storage. This endpoint provides a
    standardized logout flow and can be extended with token blacklisting
    if needed in the future.
    """
    return {"message": "Logout successful"}
