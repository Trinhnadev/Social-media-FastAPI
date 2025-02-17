from pymongo import ASCENDING, DESCENDING
from database.mongodb import db





async def create_indexes():
    """Creates necessary MongoDB indexes for optimized queries."""
    
    # Ensure unique email for users
    await db.users.create_index([("email", ASCENDING)], unique=True)

    # Index for fast lookup of posts by user
    await db.posts.create_index([("user._id", ASCENDING)])

    # Index for sorting posts by creation date (newest first)
    await db.posts.create_index([("created_at", DESCENDING)])

    # Index for fast retrieval of comments by post_id
    await db.comments.create_index([("post_id", ASCENDING)])

    print("Indexes created successfully")
