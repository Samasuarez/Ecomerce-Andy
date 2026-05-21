from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
import os
from pathlib import Path

_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://joublinsuarez_db_user:Hh95027920@cluster0.dy9csba.mongodb.net/ecommerce?retryWrites=true&w=majority&appName=Cluster0",
)
DB_NAME = os.getenv("DB_NAME", "ecommerce")

_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None


async def connect_db():
    global _client, _db
    _client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=8000)
    _db = _client[DB_NAME]


async def close_db():
    global _client
    if _client:
        _client.close()


def get_db() -> AsyncIOMotorDatabase:
    return _db
