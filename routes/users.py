from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from database.mongodb import db
from models.user import UserCreate, UserInDB, UserResponse, UserUpdate
from passlib.context import CryptContext

router = APIRouter(prefix="/api/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_objectid(doc):
    """Convert ObjectId to string to avoid JSON serialization error"""
    if not doc:
        return None
    doc["id"] = str(doc["_id"])  # Đảm bảo có field 'id'
    del doc["_id"]  # Xóa `_id` nếu không cần thiết
    return doc

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")  
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict(exclude={"password"})
    user_dict["hashed_password"] = hashed_password
    user_dict["_id"] = ObjectId()
    user_dict["followers"] = []
    user_dict["following"] = []
    user_dict["recent_posts"] = []
    
    await db.users.insert_one(user_dict)
    return UserResponse(**fix_objectid(user_dict))

@router.get("/{user_id}", response_model=UserResponse)
async def find_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return fix_objectid(user)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_by_id(user_id: str, update_data: UserUpdate = Body(...)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_fields = {k: v for k, v in update_data.dict(exclude_unset=True).items()}
    if "password" in update_fields:
        update_fields["hashed_password"] = pwd_context.hash(update_fields.pop("password"))
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    return UserResponse(**fix_objectid(updated_user))

@router.delete("/{user_id}")
async def delete_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return {"message": "User deleted successfully"}
