from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from ..database import get_db
from ..models import UserPublic, UserUpdate
from .auth_router import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


def _to_public(user: dict) -> UserPublic:
    return UserPublic(
        id=str(user["_id"]),
        email=user.get("email", ""),
        full_name=user.get("full_name", ""),
        first_name=user.get("first_name", ""),
        last_name=user.get("last_name", ""),
        phone=user.get("phone", ""),
        address=user.get("address", ""),
        dni=user.get("dni", ""),
        profession=user.get("profession", ""),
        province=user.get("province", ""),
        city=user.get("city", ""),
        is_admin=user.get("is_admin", False),
        created_at=user.get("created_at", ""),
    )


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return _to_public(user)


@router.put("/me", response_model=UserPublic)
async def update_me(body: UserUpdate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    oid = ObjectId(current_user["user_id"])
    update_data = {k: v for k, v in body.model_dump().items() if v != ""}
    if update_data:
        await db.users.update_one({"_id": oid}, {"$set": update_data})
    user = await db.users.find_one({"_id": oid})
    return _to_public(user)
