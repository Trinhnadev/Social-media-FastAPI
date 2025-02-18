
from fastapi import FastAPI, HTTPException, Depends, Body ,Query, APIRouter
from pymongo import MongoClient, ASCENDING, DESCENDING
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from bson import ObjectId
from enum import Enum
from datetime import datetime

from models.post import Post, PostUpdate, PostCreate, PostUpdateResponse
from fastapi.encoders import jsonable_encoder
# from motor.motor_asyncio import AsyncIOMotorClient
from database.mongodb import db, client
from routes.authentication import router as authentication

router = APIRouter(prefix="/api", tags=["Posts"])


@router.post("/posts/", response_model=Post)
async def create_post(post: PostCreate):
    # Chuyển đổi dữ liệu đầu vào
    post_data = post.model_dump()
    post_data["created_at"] = datetime.utcnow()  # Lấy thời gian hiện tại
    post_data["likes"] = []
    post_data["comments"] = []
    post_data["user"] = None

        # Lưu vào MongoDB
    await db.posts.insert_one(post_data)

        # Trả về dữ liệu đã lưu
    return Post(**post_data)

@router.get("/posts/{post_id}",response_model=Post)
async def find_post_by_id(post_id:str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=500,detail="Id is invalid")
    post = await db.posts.find_one({"_id":ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=500, detail="Post not found")
    post["_id"] = str(post["_id"])
    return post

@router.patch("/posts/{post_id}", response_model=PostUpdateResponse)
async def update_post_by_id(post_id: str, update_data: PostUpdate = Body(...)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_fields = {k: v for k, v in update_data.dict(exclude_unset=True).items()}
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": update_fields})

    updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if updated_post:
        updated_post["_id"] = str(updated_post["_id"])  # Chuyển đổi ObjectId về string

    return PostUpdateResponse(
        message="Post updated successfully" if result.modified_count > 0 else "No changes made",
        post=jsonable_encoder(updated_post)
    )

@router.delete("/posts/{post_id}")
async def delete_post_by_id(post_id:str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    
    post = await db.posts.find_one({"_id":ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    result = await db.posts.delete_one({"_id":ObjectId(post_id)})

    if result.deleted_count ==0:
        raise HTTPException(status_code=500, detail="Failed to delete Post")
    
    return {"message": "Post deleted successfully"}



def fix_objectid(doc):
    """Convert ObjectId to string to avoid JSON serialization error"""
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/posts/")
async def get_posts(
    limit: int = Query(10, ge=1, le=100),  
    skip: int = Query(0, ge=0),  
    sort: str = Query("created_at")
):
    # Kiểm tra nếu trường `sort` tồn tại trong MongoDB
    sample_post = await db.posts.find_one()
    if sample_post and sort not in sample_post:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

    # Query dữ liệu và sắp xếp
    cursor = db.posts.find().sort(sort, -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)

    # Convert ObjectId thành string trước khi trả về
    return [fix_objectid(post) for post in posts]
