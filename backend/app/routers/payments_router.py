import os
import hmac
import hashlib
import json
from fastapi import APIRouter, HTTPException, Request, Depends
from bson import ObjectId
import mercadopago

from ..database import get_db
from ..models import CreatePreferenceRequest
from .auth_router import get_current_user
from ..notifications import send_order_notification

router = APIRouter(prefix="/payments", tags=["payments"])

MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "")
MP_WEBHOOK_SECRET = os.environ.get("MP_WEBHOOK_SECRET", "")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://frontend-silver-wood.reflex.run")
BACKEND_URL = os.environ.get("BACKEND_URL", "https://nurseshop-api.onrender.com")


@router.post("/create-preference")
async def create_preference(
    body: CreatePreferenceRequest,
    current_user: dict = Depends(get_current_user),
):
    if not MP_ACCESS_TOKEN:
        raise HTTPException(503, "Pagos no configurados")

    db = get_db()
    order = await db.orders.find_one({"_id": ObjectId(body.order_id)})
    if not order:
        raise HTTPException(404, "Pedido no encontrado")
    if order["user_id"] != current_user["user_id"]:
        raise HTTPException(403, "Acceso denegado")

    sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

    items = [
        {
            "title": item["name"],
            "quantity": item["qty"],
            "unit_price": float(item["price"]),
            "currency_id": "ARS",
        }
        for item in order["items"]
    ]

    preference_data = {
        "items": items,
        "external_reference": str(order["_id"]),
        "back_urls": {
            "success": f"{FRONTEND_URL}/orders?payment=success",
            "failure": f"{FRONTEND_URL}/orders?payment=failure",
            "pending": f"{FRONTEND_URL}/orders?payment=pending",
        },
        "auto_return": "approved",
        "notification_url": f"{BACKEND_URL}/payments/webhook",
    }

    response = sdk.preference().create(preference_data)
    if response["status"] != 201:
        raise HTTPException(502, "Error al crear preferencia en MercadoPago")

    init_point = response["response"]["init_point"]
    await db.orders.update_one(
        {"_id": order["_id"]},
        {"$set": {"mp_preference_id": response["response"]["id"]}},
    )

    return {"init_point": init_point}


@router.post("/webhook")
async def mp_webhook(request: Request):
    raw_body = await request.body()

    if MP_WEBHOOK_SECRET:
        sig_header = request.headers.get("x-signature", "")
        ts = ""
        received_hash = ""
        for part in sig_header.split(","):
            part = part.strip()
            if part.startswith("ts="):
                ts = part[3:]
            elif part.startswith("v1="):
                received_hash = part[3:]

        manifest = (
            f"id:{request.query_params.get('id', '')};"
            f"request-id:{request.headers.get('x-request-id', '')};"
            f"ts:{ts};"
        )
        expected = hmac.new(
            MP_WEBHOOK_SECRET.encode(),
            manifest.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, received_hash):
            raise HTTPException(400, "Firma inválida")

    payload = json.loads(raw_body) if raw_body else {}
    topic = payload.get("type") or request.query_params.get("topic", "")

    if topic not in ("payment", "merchant_order"):
        return {"ok": True}

    if topic == "payment":
        resource_id = (
            payload.get("data", {}).get("id")
            or request.query_params.get("id")
        )
        if not resource_id or not MP_ACCESS_TOKEN:
            return {"ok": True}

        sdk = mercadopago.SDK(MP_ACCESS_TOKEN)
        payment_response = sdk.payment().get(resource_id)
        if payment_response["status"] != 200:
            return {"ok": True}

        p = payment_response["response"]
        ext_ref = p.get("external_reference")
        mp_status = p.get("status")

        status_map = {
            "approved": "confirmed",
            "rejected": "cancelled",
            "pending": "pending",
            "in_process": "pending",
        }
        new_status = status_map.get(mp_status, "pending")

        if ext_ref:
            db = get_db()
            try:
                order = await db.orders.find_one({"_id": ObjectId(ext_ref)})
            except Exception:
                return {"ok": True}
            if order:
                await db.orders.update_one(
                    {"_id": order["_id"]},
                    {"$set": {"status": new_status, "mp_payment_id": str(resource_id)}},
                )
                order["status"] = new_status
                await send_order_notification(order, f"Pago {mp_status}")

    return {"ok": True}
