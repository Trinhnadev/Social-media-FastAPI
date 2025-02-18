
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING
from datetime import datetime


class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))  # ID lưu dưới dạng string
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Tạo thời gian tự động
    likes: List[dict] = []
    comments: List[dict] = []
    user: Optional[dict] = None  # Người dùng tạo bài viết

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class PostCreate(BaseModel):
    title: str
    content: str


# Model cho yêu cầu cập nhật bài viết
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Model phản hồi sau khi cập nhật
class PostUpdateResponse(BaseModel):
    message: str
    post: Post