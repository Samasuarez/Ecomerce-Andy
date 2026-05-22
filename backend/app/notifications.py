import os
import httpx

NOTIFY_CHANNEL = os.environ.get("NOTIFY_CHANNEL", "")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

TWILIO_SID = os.environ.get("TWILIO_SID", "")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "")
TWILIO_FROM = os.environ.get("TWILIO_FROM", "")
NOTIFY_TO = os.environ.get("NOTIFY_TO", "")


async def send_order_notification(order: dict, event: str):
    if not NOTIFY_CHANNEL:
        return

    order_id = str(order.get("_id", order.get("id", "?")))
    items_lines = "\n".join(
        f"  • {item['name']} x{item['qty']}"
        for item in order.get("items", [])
    )
    address = order.get("delivery_address", order.get("address", "—"))

    msg = (
        f"🛒 *{event} #{order_id[:8]}*\n"
        f"👤 {order.get('user_email', '')}\n"
        f"📦\n{items_lines}\n"
        f"💰 Total: ${order.get('total', 0)}\n"
        f"📍 {address}\n"
        f"Estado: {order.get('status', '')}"
    )

    if NOTIFY_CHANNEL == "telegram":
        await _send_telegram(msg)
    elif NOTIFY_CHANNEL == "whatsapp":
        await _send_whatsapp(msg)


async def _send_telegram(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
            }, timeout=5)
        except Exception:
            pass


async def _send_whatsapp(text: str):
    if not TWILIO_SID or not TWILIO_TOKEN:
        return
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                url,
                data={"From": TWILIO_FROM, "To": NOTIFY_TO, "Body": text},
                auth=(TWILIO_SID, TWILIO_TOKEN),
                timeout=5,
            )
        except Exception:
            pass
