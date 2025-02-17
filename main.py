from fastapi import FastAPI
from routes.authentication import router as authentication
from routes.users import router as users
from routes.posts import router as posts
from indexes import create_indexes




# Initialize FastAPI
app = FastAPI()

app.include_router(authentication)
app.include_router(users)
app.include_router(posts)



@app.on_event("startup")
async def startup_event():
    await create_indexes()






