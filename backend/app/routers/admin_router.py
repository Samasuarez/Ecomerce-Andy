from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bson import ObjectId
from ..database import get_db
from ..models import UserPublic, OrderPublic, ProductModel, ProductCreate, AdminStats
from .auth_router import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


async def get_admin_user(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    if not user or not user.get("is_admin", False):
        raise HTTPException(403, "Acceso denegado. Se requieren permisos de administrador.")
    return current_user


# ── Stats ─────────────────────────────────────────────────────────────────── #

@router.get("/stats", response_model=AdminStats)
async def get_stats(_: dict = Depends(get_admin_user)):
    db = get_db()
    total_users = await db.users.count_documents({})
    total_orders = await db.orders.count_documents({})
    pending_orders = await db.orders.count_documents({"status": "pending"})

    pipeline = [
        {"$match": {"status": {"$ne": "cancelled"}}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}}},
    ]
    result = await db.orders.aggregate(pipeline).to_list(1)
    total_revenue = result[0]["total"] if result else 0.0

    return AdminStats(
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        pending_orders=pending_orders,
    )


# ── Usuarios ─────────────────────────────────────────────────────────────── #

@router.get("/users", response_model=List[UserPublic])
async def list_users(skip: int = 0, limit: int = 100, _: dict = Depends(get_admin_user)):
    db = get_db()
    cursor = db.users.find({}, {"hashed_password": 0}).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    return [
        UserPublic(
            id=str(u["_id"]),
            email=u.get("email", ""),
            first_name=u.get("first_name", ""),
            last_name=u.get("last_name", ""),
            phone=u.get("phone", ""),
            address=u.get("address", ""),
            is_admin=u.get("is_admin", False),
            created_at=u.get("created_at", ""),
        )
        for u in users
    ]


# ── Pedidos ───────────────────────────────────────────────────────────────── #

@router.get("/orders", response_model=List[OrderPublic])
async def list_orders(skip: int = 0, limit: int = 100, _: dict = Depends(get_admin_user)):
    db = get_db()
    cursor = db.orders.find({}).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    return [
        OrderPublic(
            id=str(o["_id"]),
            user_id=o["user_id"],
            user_email=o["user_email"],
            items=o["items"],
            total=o["total"],
            status=o["status"],
            created_at=o["created_at"],
        )
        for o in orders
    ]


@router.patch("/orders/{order_id}/status")
async def update_order_status(
    order_id: str, status: str, _: dict = Depends(get_admin_user)
):
    valid = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
    if status not in valid:
        raise HTTPException(400, f"Estado inválido. Opciones: {valid}")
    db = get_db()
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)}, {"$set": {"status": status}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Pedido no encontrado")
    return {"ok": True}


# ── Productos ─────────────────────────────────────────────────────────────── #

@router.get("/products", response_model=List[ProductModel])
async def list_products_admin(_: dict = Depends(get_admin_user)):
    db = get_db()
    cursor = db.products.find({}, {"_id": 0}).sort("id", 1)
    return await cursor.to_list(length=200)


@router.post("/products", response_model=ProductModel)
async def create_product(body: ProductCreate, _: dict = Depends(get_admin_user)):
    db = get_db()
    last = await db.products.find_one({}, {"id": 1}, sort=[("id", -1)])
    new_id = (last["id"] + 1) if last else 1

    doc = {
        "id": new_id,
        "name": body.name,
        "price": body.price,
        "description": body.description,
        "category": body.category,
        "sizes": body.sizes,
        "image": body.image or f"assets/products/{body.category}-{new_id}.jpg",
        "stock": body.stock,
    }
    await db.products.insert_one(doc)
    return ProductModel(**{k: v for k, v in doc.items() if k != "_id"})


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, _: dict = Depends(get_admin_user)):
    db = get_db()
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Producto no encontrado")
    return {"ok": True}
