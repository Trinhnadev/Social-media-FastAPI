from fastapi import APIRouter, HTTPException
from services.transactions import transfer_funds

router = APIRouter()

@router.post("/transfer/")
async def transfer_money(sender_id: str, receiver_id: str, amount: float):
    return await transfer_funds(sender_id, receiver_id, amount)
