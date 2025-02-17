from database.mongodb import db

# Function to get the top users based on the number of posts they have created
async def get_top_users(limit: int = 10):
    pipeline = [
        # Join (lookup) the "posts" collection to get all posts associated with a user
        {"$lookup": {
            "from": "post",  # Collection to join with
            "localField": "_id",  # Field in the "users" collection
            "foreignField": "user._id",  # Field in the "posts" collection
            "as": "post"  # Alias for the joined data
        }},
        # Project only necessary fields and compute the number of posts per user
        {
            "project": {
                "name": 1,  # Include name
                "email": 1,  # Include email
                "post_count": {"$size": "$post"}  # Count the number of posts per user
            }
        },
        # Sort users in descending order based on post count
        {"$sort": {"post_count": -1}},
        # Limit the results to the top 'limit' users
        {"$limit": limit}
    ]   

    # Execute the aggregation pipeline and return the top users
    return await db.user.aggregate(pipeline).to_list(length=limit) 


# Function to get the most liked posts
async def get_most_liked_posts(limit: int = 5):
    pipeline = [
        # Project only necessary fields and compute the number of likes for each post
        {"$project": {
            "title": 1,  # Include title
            "content": 1,  # Include content
            "like_count": {"$size": "$likes"}  # Count the number of likes per post
        }},
        # Sort posts in descending order based on the number of likes
        {"$sort": {"like_count": -1}},
        # Limit the results to the top 'limit' posts
        {"$limit": limit}
    ]
    # Execute the aggregation pipeline and return the most liked posts
    return await db.posts.aggregate(pipeline).to_list(length=limit) 


# Function to get the most commented posts
async def get_most_commented_posts(limit: int = 10):
    pipeline = [
        # Join (lookup) the "comments" collection to get all comments associated with a post
        {"$lookup": {
            "from": "comments",  # Collection to join with
            "localField": "_id",  # Field in the "posts" collection
            "foreignField": "post_id",  # Field in the "comments" collection
            "as": "comments"  # Alias for the joined data
        }},
        # Project only necessary fields and compute the number of comments per post
        {"$project": {
            "title": 1,  # Include title
            "content": 1,  # Include content
            "comment_count": {"$size": "$comments"}  # Count the number of comments per post
        }},
        # Sort posts in descending order based on the number of comments
        {"$sort": {"comment_count": -1}},
        # Limit the results to the top 'limit' posts
        {"$limit": limit}
    ]
    # Execute the aggregation pipeline and return the most commented posts
    return await db.posts.aggregate(pipeline).to_list(length=limit)
