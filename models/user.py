from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Map MongoDB _id to id for better readability
    name: str
    email: EmailStr
    bio: Optional[str] = None
    followers: List[dict] = []  # Stores a list of followers as dictionary objects
    following: List[dict] = []  # Stores a list of users the person is following
    recent_posts: List[dict] = []  # Stores the user's recent posts

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}  # Convert ObjectId to string for JSON serialization

# Model used when creating a new user (password is required)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # Only used for user creation, should be hashed before storing

# Model used for storing user data in the database (includes hashed password)
class UserInDB(User):
    id: str  # Ensuring consistent use of 'id' instead of '_id'
    email: str
    hashed_password: str  # Stores the hashed password instead of raw password
    role: str  # User role field (e.g., admin, user, moderator)

# Response model that hides sensitive data such as the hashed password
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    bio: Optional[str] = None
    followers: List[dict] = []
    following: List[dict] = []
    recent_posts: List[dict] = []

# Model for updating user information (fields are optional)
class UserUpdate(BaseModel):
    name: Optional[str] = None  # Allows updating name
    password: Optional[str] = None  # Allows updating password (should be hashed before storing)
    bio: Optional[str] = None  # Allows updating user bio
