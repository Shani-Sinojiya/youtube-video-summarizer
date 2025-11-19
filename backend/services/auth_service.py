import os
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import Optional
from bson.objectid import ObjectId
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from db.mongodb import get_db
from dotenv import load_dotenv

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Security settings
load_dotenv()

# Get settings from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Configure CryptContext with explicit bcrypt settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b",
    bcrypt__min_rounds=4,
    bcrypt__max_rounds=31,
)


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize AuthService with database instance.

        Args:
            db: AsyncIOMotorDatabase instance
        """
        self.db = db
        self.users = self.db.users

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        # Bcrypt has a 72-byte limit, so we truncate the password if necessary
        # This is a standard practice and doesn't significantly reduce security
        password_bytes = password.encode('utf-8')[:72]
        return pwd_context.hash(password_bytes)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # Apply the same truncation for verification
        password_bytes = plain_password.encode('utf-8')[:72]
        return pwd_context.verify(password_bytes, hashed_password)

    async def create_user(self, email: str, password: str) -> User:
        password_hash = self.hash_password(password)
        user = {
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),  # Initialize last_login
            "active_chats": [],  # Initialize active_chats as empty list
            "preferred_language": "en",
            "preferred_model": "gemini-pro",
            "account_type": "free",
            "is_verified": False,
            "total_videos": 0,
            "storage_used": 0,
            "profile": {
                "display_name": None,
                "bio": None,
                "avatar_url": None,
                "website": None,
                "social_links": {},
                "timezone": None,
                "notification_settings": {"email_notifications": True}
            }
        }
        result = await self.users.insert_one(user)
        user["id"] = str(result.inserted_id)
        return User(**user)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.users.find_one({"email": email})
        if user and self.verify_password(password, user["password_hash"]):
            # Convert ObjectId to string for the id field
            user["id"] = str(user["_id"])
            current_time = datetime.utcnow()

            # Ensure required fields exist with defaults
            if "active_chats" not in user:
                user["active_chats"] = []
            if "last_login" not in user:
                user["last_login"] = current_time
            if "profile" not in user:
                user["profile"] = {
                    "display_name": None,
                    "bio": None,
                    "avatar_url": None,
                    "website": None,
                    "social_links": {},
                    "timezone": None,
                    "notification_settings": {"email_notifications": True}
                }

            # Update last login
            await self.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": current_time}}
            )
            return User(**user)
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> User:
    """FastAPI dependency to get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Get user ID from the subject claim
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception

        # Find user in database
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise credentials_exception

        # Add string ID and ensure default fields
        user["id"] = str(user["_id"])

        # Ensure required fields exist
        if "profile" not in user:
            user["profile"] = {
                "display_name": None,
                "bio": None,
                "avatar_url": None,
                "website": None,
                "social_links": {},
                "timezone": None,
                "notification_settings": {"email_notifications": True}
            }

        if "active_chats" not in user:
            user["active_chats"] = []

        if "last_login" not in user:
            user["last_login"] = datetime.utcnow()

        return User(**user)

    except (JWTError, ValueError):
        raise credentials_exception


async def get_api_key() -> str:
    """Get the Google API key for Gemini and other services."""
    return GOOGLE_API_KEY
