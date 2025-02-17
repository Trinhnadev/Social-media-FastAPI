from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING



class Notification(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user: dict 
    type: str
    message: str
    created_at: str