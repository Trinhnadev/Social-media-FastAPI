
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING
from datetime import datetime


class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Alias cho MongoDB
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Tự động tạo ngày
    likes: List[dict] = []
    comments: List[dict] = []
    user: Optional[dict] = None  # Người dùng tạo bài viết (ẩn khi trả về)

    class Config:
        from_attributes = True  # Hỗ trợ MongoDB
        json_encoders = {datetime: lambda v: v.isoformat()}  # Chuyển datetime thành ISO string
        populate_by_name = True  # Cho phép sử dụng alias khi serialize
        arbitrary_types_allowed = True  # Cho phép sử dụng ObjectId

class PostResponse(BaseModel):
    title: str
    content: str
    created_at: datetime


class PostUpdate(BaseModel):
    title: str = Field(...)
    content: str = Field(...)