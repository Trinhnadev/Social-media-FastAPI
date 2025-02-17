from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    password: str
    followers: List[str] = []
    followeing: List[str] = []
    profilePic: List[str] =[]
    bio: str


class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    content: str
    created_at: str
    comments: List[str] = []
    likes: int = 0

class Comment(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: ObjectId
    post_id: ObjectId
    content: str
    created_at: str

class Message(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    sender_id: str
    receiver_id: str
    content: str
    sent_at: str

class Notification(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    message: str
    created_at: str


class Categories(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str

class Likes(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    post_id: ObjectId
    user_id:ObjectId

class Followers(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    followers_id: ObjectId
    following_id: ObjectId

class Messages(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    sender_id: ObjectId
    receiver_id: ObjectId
    message: str
    created_at: str

class Groups(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str
    members: List[ObjectId] = []

class Notifications(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: ObjectId
    type: List[str] = []
    message: str
    created_at: str

class ReportStatus(str, Enum):
    pending = "Pending"
    in_review = "In Review"
    resolved = "Resolved"
    rejected = "Rejected"

class Reports(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    reporter_id: ObjectId
    reported_user_id: ObjectId
    reason: str
    status: ReportStatus = ReportStatus.pending  
    created_at: str