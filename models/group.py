from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING


class Group(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    members: List[dict] = [] 
