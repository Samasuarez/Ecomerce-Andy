from pydantic import BaseModel, field_validator
from typing import List, Optional


# ── Usuarios ─────────────────────────────────────────────────────────────── #

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = ""
    phone: str = ""
    dni: str = ""
    profession: str = ""
    province: str = ""
    city: str = ""
    address: str = ""

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.strip().lower()


class UserLogin(BaseModel):
    email: str
    password: str


class UserPublic(BaseModel):
    id: str
    email: str
    full_name: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    address: str = ""
    dni: str = ""
    profession: str = ""
    province: str = ""
    city: str = ""
    is_admin: bool = False
    created_at: str = ""


class UserUpdate(BaseModel):
    full_name: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    address: str = ""
    dni: str = ""
    profession: str = ""
    province: str = ""
    city: str = ""


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


# ── Productos ─────────────────────────────────────────────────────────────── #

class ProductModel(BaseModel):
    id: int
    name: str
    price: float
    image: str
    description: str
    sizes: List[str]
    category: str
    stock: int = 0


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    sizes: List[str]
    image: str = ""
    stock: int = 0


# ── Pedidos ───────────────────────────────────────────────────────────────── #

class OrderItem(BaseModel):
    product_id: int
    name: str
    price: float
    qty: int


class OrderCreate(BaseModel):
    items: List[OrderItem]


class OrderPublic(BaseModel):
    id: str
    user_id: str
    user_email: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: str


# ── Pagos ─────────────────────────────────────────────────────────────────── #

class CreatePreferenceRequest(BaseModel):
    order_id: str


# ── Admin stats ───────────────────────────────────────────────────────────── #

class AdminStats(BaseModel):
    total_users: int
    total_orders: int
    total_revenue: float
    pending_orders: int
