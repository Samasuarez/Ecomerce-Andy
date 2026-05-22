from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
from bson import ObjectId
from ..database import get_db
from ..models import UserCreate, UserLogin, UserPublic, TokenResponse
from ..auth import hash_password, verify_password, create_access_token, decode_token
from ..limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def _user_to_public(user: dict) -> UserPublic:
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


@router.post("/register", response_model=TokenResponse)
@limiter.limit("5/minute")
async def register(request: Request, body: UserCreate):
    db = get_db()
    if await db.users.find_one({"email": body.email}):
        raise HTTPException(400, "El email ya está registrado")

    doc = {
        "email": body.email,
        "hashed_password": hash_password(body.password),
        "full_name": body.full_name,
        "first_name": "",
        "last_name": "",
        "phone": body.phone,
        "address": body.address,
        "dni": body.dni,
        "profession": body.profession,
        "province": body.province,
        "city": body.city,
        "is_admin": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = await db.users.insert_one(doc)
    doc["_id"] = result.inserted_id

    token = create_access_token({"sub": body.email, "user_id": str(result.inserted_id)})
    return TokenResponse(access_token=token, user=_user_to_public(doc))


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: UserLogin):
    db = get_db()
    user = await db.users.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(401, "Email o contraseña incorrectos")

    token = create_access_token({"sub": body.email, "user_id": str(user["_id"])})
    return TokenResponse(access_token=token, user=_user_to_public(user))


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        return decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(401, "Token inválido o expirado")
