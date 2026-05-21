from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..database import get_db
from ..models import ProductModel

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductModel])
async def get_products(category: Optional[str] = None):
    db = get_db()
    query = {"category": category} if category else {}
    cursor = db.products.find(query, {"_id": 0})
    return await cursor.to_list(length=200)


@router.get("/{product_id}", response_model=ProductModel)
async def get_product(product_id: int):
    db = get_db()
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    return product
