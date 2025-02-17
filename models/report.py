
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from pymongo import ASCENDING, DESCENDING



class Report(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    reporter: dict 
    reported_user: dict 
    reason: str
    status: str  
    created_at: str
