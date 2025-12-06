from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import envconfig
from app.core.logging import logger


client = AsyncIOMotorClient(envconfig.mongodb_uri)
db = client[envconfig.mongodb_db]
collection = db[envconfig.mongodb_conversations_collection]

def get_conversation_collection():
    """Return the MongoDB collection used to store chat conversations."""
    return collection