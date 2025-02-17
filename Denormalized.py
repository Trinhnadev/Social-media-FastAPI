from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    password: str
    profilePic: Optional[str] = None
    bio: Optional[str] = None
    followers: List[dict] = []  
    following: List[dict] = []  
    recent_posts: List[dict] = []  


class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user: dict  
    title: str
    content: str
    created_at: str
    likes: List[dict] = []  
    comments: List[dict] = []  


class Message(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    sender: dict  
    receiver: dict 
    content: str
    sent_at: str



class Group(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    members: List[dict] = [] 


class Notification(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user: dict 
    type: str
    message: str
    created_at: str


class Report(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    reporter: dict 
    reported_user: dict 
    reason: str
    status: str  
    created_at: str





