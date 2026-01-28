from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from datetime import timedelta
from ..database.database import get_session
from ..models.user import User, UserCreate, UserRead
from ..services.auth_service import (
    authenticate_user,
    get_user_by_email,
    create_access_token
)
from ..services.user_service import create_user as create_user_service
from ..config import settings

router = APIRouter()

@router.post("/signup", response_model=UserRead)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """Create a new user account"""
    # Check if user already exists
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Create new user
    db_user = create_user_service(session, user_create)
    return db_user

@router.post("/signin")
def signin(user_create: UserCreate, session: Session = Depends(get_session)):
    """Authenticate user and return token"""
    user = authenticate_user(session, user_create.email, user_create.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": str(user.id),
            "email": user.email
        },
        "token": access_token
    }

@router.post("/signout")
def signout():
    """Sign out current user"""
    return {"message": "Signed out successfully"}