
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["social_media"]  # Use "fastapi_db" database