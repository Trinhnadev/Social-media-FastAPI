from fastapi import FastAPI
from routes.authentication import router as authentication
from routes.users import router as users
from routes.posts import router as posts
from indexes import create_indexes
# from routes.authentication import router as users
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize FastAPI
app = FastAPI()

app.include_router(authentication)
app.include_router(users)
app.include_router(posts)



@app.on_event("startup")
async def startup_event():
    await create_indexes()






