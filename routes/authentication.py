from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import Annotated
from database.mongodb import db
from models.user import User, UserInDB  # Importing user models

from auth.security import (
    get_current_user,  # Function to get the currently authenticated user
    get_user,  # Function to retrieve a user from the database
    get_password_hash,  # Function to hash passwords securely
    verify_password,  # Function to verify a password against its hashed version
    create_access_token  # Function to create a JWT access token
)

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Defining OAuth2 authentication scheme with a token URL for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Creating a FastAPI instance
app = FastAPI()

# Creating an API router with a prefix "/api" and a tag for better documentation
router = APIRouter(prefix="/api", tags=["authentication"])

# async def get_user(username: str):
#     user = await db.users.find_one({"email": username})  # Fetch user by email from database
#     return user

# 🎯 Endpoint for user authentication and token generation
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
