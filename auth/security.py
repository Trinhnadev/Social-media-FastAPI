from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from typing import Annotated, Optional, List
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
import os
from pymongo import ASCENDING
from bson import ObjectId
from database.mongodb import db  # MongoDB connection
from models.user import User, UserInDB, UserResponse  # Import User model

# Load environment variables from .env
load_dotenv()

# 🔑 JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Secret key for signing tokens
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # JWT signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Token expiration time

# 🔐 Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🛡 OAuth2 password authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# 🚀 Initialize FastAPI app
app = FastAPI()
router = APIRouter(prefix="/api", tags=["authentication"])

# 🎯 Function to hash passwords
def get_password_hash(password: str):
    return pwd_context.hash(password)

# 🎯 Function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 🔍 Retrieve a user by email from the database
async def get_user(email: str):
    user = await db.users.find_one({"email": email})
    if user:
        user["id"] = str(user.pop("_id"))  # Convert MongoDB ObjectId to string
        if "role" not in user:
            user["role"] = "user"  # Assign default role if not present
        return UserInDB(**user)
    return None

# 🎫 Generate JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 🔓 Decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None

# 🔑 Get current user from token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await get_user(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# 🛡 Role-based access control (RBAC)
# Define role-based permissions (example)
ROLES_PERMISSIONS = {
    "admin": ["manage_users", "view_reports", "delete_posts"],
    "moderator": ["view_reports", "delete_posts"],
    "user": ["create_posts", "comment"]
}

# 🔒 Function to check user permissions
def check_permissions(required_permissions: List[str]):
    async def permission_checker(user: UserInDB = Depends(get_current_user)):
        role = user.role if hasattr(user, "role") else "user"
        # Check if user has at least one of the required permissions
        if not any(p in ROLES_PERMISSIONS.get(role, []) for p in required_permissions):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return permission_checker




