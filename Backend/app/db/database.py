from fastapi import Request, WebSocket
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import envconfig

def create_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(envconfig.mongodb_uri)

def get_conversation_collection(client: AsyncIOMotorClient):
    return client[envconfig.mongodb_db][envconfig.mongodb_conversations_collection]


def conversation_collection(request: Request):
    return get_conversation_collection(request.app.state.mongo_client)

def websocket_conversation_collection(websocket: WebSocket):
    return get_conversation_collection(websocket.app.state.mongo_client)
