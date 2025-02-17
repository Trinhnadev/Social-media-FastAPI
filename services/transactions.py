from fastapi import HTTPException
from database.mongodb import db, client


# service transactions
async def transfer_funds(sender_id: str, receiver_id:str,amount:float):
    async with await client.start_session() as session:
        async with session.start_transaction():
            sender = await db.users.find_one({"_id":sender_id})
            receiver = await db.users.find_one({"_id":receiver_id})


            if not sender or not receiver:
                raise HTTPException(status_code=404, detail="User not found")
            
            if sender["balance"]< amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            
            #deduct amount from sender
            await db.users.update_one(
                {"_id":sender_id},{"$inc":{"blance":-amount}},session=session
            )

            # Add amount to receiver
            await db.users.update_one(
                {"_id": receiver_id}, {"$inc": {"balance": amount}}, session=session
            )

            await session.commit_transaction()
            return {"message": "Transaction successful"}
        
