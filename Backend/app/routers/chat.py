import uuid
from app.db.database import get_conversation_collection
from app.services.conversation_service import get_all_session_ids, get_history_messages
from fastapi import APIRouter, WebSocket
from app.core.logging import logger
from app.workflows.chatbot_workflow import bot_reply
from starlette.websockets import WebSocketDisconnect

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/chat/sessions")
async def get_chat_sessions():
    sessionIds = await get_all_session_ids()
    return {"session_ids": sessionIds}

@router.get("/chat/sessions/{session_id}")
async def get_chat_session(session_id: str):
    conversation = await get_history_messages(session_id)
    return {"conversation": conversation}

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    while True:
        try:
            data = await websocket.receive_text()
            logger.info(f"Received message: {data} (session_id={session_id})")
            reply = await bot_reply(data, session_id=session_id)
            logger.info(f"Bot reply: {reply} (session_id={session_id})")
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {session_id}")
        except Exception as e:
            logger.error(f"Error in websocket_chat: {e}")
            await websocket.send_text("Sorry, an error occurred. Please try again later.")
            
@router.delete("/chat/delete-sessions/{session_id}")            
async def delete_chat_session(session_id: str):
    """Delete all messages for a given session ID."""
    collection = get_conversation_collection()
    result = await collection.delete_many({"session_id": session_id})
    logger.debug(f"Deleted {result.deleted_count} messages from MongoDB for session_id={session_id}")