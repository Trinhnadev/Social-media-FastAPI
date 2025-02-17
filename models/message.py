from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING


class Message(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    sender: dict  
    receiver: dict 
    content: str
    sent_at: str
