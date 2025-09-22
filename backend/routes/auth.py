from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.auth_service import AuthService, get_current_user
from models.user import User, UserProfile
from typing import Optional
from db.mongodb import get_db
import os
import jwt
from datetime import datetime, timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

# Import settings from auth_service
from services.auth_service import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    data: User
    access_token: str
    token_type: str = "bearer"


class UserProfileUpdate(BaseModel):
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    website: Optional[str]
    social_links: Optional[dict[str, str]]
    timezone: Optional[str]
    notification_settings: Optional[dict[str, bool]]


class UserPreferencesUpdate(BaseModel):
    preferred_language: Optional[str]
    preferred_model: Optional[str]


router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> AuthService:
    """Get AuthService instance with database dependency."""
    return AuthService(db)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup", response_model=User)
async def signup(
    request: SignupRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await auth_service.create_user(request.email, request.password)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Create token with consistent payload structure
    token_data = {
        "sub": str(user.id),  # Use ID as subject
        "email": user.email,
        "user_id": str(user.id)
    }
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token, data=user)


@router.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return current_user


@router.patch("/profile", response_model=User)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update the current user's profile information."""
    update_data = profile_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No valid fields to update"
        )

    result = await db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": {"profile": update_data}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Profile not updated"
        )

    updated_user = await db.users.find_one({"_id": ObjectId(current_user.id)})
    if updated_user:
        updated_user["id"] = str(updated_user["_id"])
        return User(**updated_user)
    raise HTTPException(status_code=404, detail="User not found")


@router.patch("/preferences", response_model=User)
async def update_preferences(
    preferences: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update the current user's preferences."""
    update_data = preferences.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No valid preferences to update"
        )

    result = await db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Preferences not updated"
        )

    updated_user = await db.users.find_one({"_id": ObjectId(current_user.id)})
    if updated_user:
        updated_user["id"] = str(updated_user["_id"])
        return User(**updated_user)
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/stats", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user statistics including total videos, storage used, etc."""
    # Get up-to-date video count
    total_videos = await db.videos.count_documents({"user_id": current_user.id})

    # Get total storage used from videos collection
    pipeline = [
        {"$match": {"user_id": current_user.id}},
        {"$group": {
            "_id": None,
            "total_storage": {"$sum": "$storage_used"}
        }}
    ]
    storage_result = await db.videos.aggregate(pipeline).to_list(length=1)
    storage_used = storage_result[0]["total_storage"] if storage_result else 0

    stats = {
        "total_videos": total_videos,
        "storage_used": storage_used,
        "account_type": current_user.account_type,
        "is_verified": current_user.is_verified,
        "member_since": current_user.created_at,
        "last_login": current_user.last_login
    }
    return stats
