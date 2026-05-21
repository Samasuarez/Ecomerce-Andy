from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from ..database import get_db
from ..models import OrderCreate, OrderPublic
from .auth_router import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


def _order_to_public(o: dict) -> OrderPublic:
    return OrderPublic(
        id=str(o["_id"]),
        user_id=o["user_id"],
        user_email=o["user_email"],
        items=o["items"],
        total=o["total"],
        status=o["status"],
        created_at=o["created_at"],
    )


@router.post("", response_model=OrderPublic)
async def create_order(body: OrderCreate, current_user: dict = Depends(get_current_user)):
    if not body.items:
        raise HTTPException(400, "El pedido no puede estar vacío")

    db = get_db()
    total = round(sum(item.price * item.qty for item in body.items), 2)

    doc = {
        "user_id": current_user["user_id"],
        "user_email": current_user["sub"],
        "items": [item.model_dump() for item in body.items],
        "total": total,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    result = await db.orders.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _order_to_public(doc)


@router.get("/mine", response_model=List[OrderPublic])
async def get_my_orders(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.orders.find({"user_id": current_user["user_id"]}).sort("created_at", -1)
    orders = await cursor.to_list(length=50)
    return [_order_to_public(o) for o in orders]
