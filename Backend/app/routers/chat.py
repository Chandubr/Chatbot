import uuid
from app.db.database import conversation_collection, websocket_conversation_collection
from app.services.conversation_service import get_all_session_ids, get_history_messages, rename_conversation_name
from fastapi import APIRouter, WebSocket, Body, Depends
from app.core.logging import logger
from app.workflows.chatbot_workflow import bot_reply
from starlette.websockets import WebSocketDisconnect

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/chat/sessions")
async def get_chat_sessions(collection = Depends(conversation_collection)):
    sessionIds = await get_all_session_ids(collection)
    return {"session_ids": sessionIds}

@router.get("/chat/sessions/{session_id}")
async def get_chat_session(session_id: str, collection = Depends(conversation_collection)):
    conversation = await get_history_messages(collection, session_id)
    return {"conversation": conversation}

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, collection = Depends(websocket_conversation_collection)):
    await websocket.accept()
    session_id = websocket.query_params.get("session_id") or str(uuid.uuid4())
    while True:
        try:
            data = await websocket.receive_text()
            logger.info(f"Received message: {data} (session_id={session_id})")
            reply = await bot_reply(collection,data, session_id=session_id)
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {session_id}")
            break 
        except Exception as e:
            logger.error(f"Error in websocket_chat: {e}")
            await websocket.send_text("Sorry, an error occurred. Please try again later.")
            
@router.delete("/chat/delete-sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    collection = Depends(conversation_collection),
):
    result = await collection.delete_many({"session_id": session_id})
    return {"deleted_count": result.deleted_count}

@router.put("/chat/rename-session/{session_id}")
async def rename_chat_session(session_id: str, new_name: str = Body(..., embed=True), collection = Depends(conversation_collection)):
    """Rename a conversation session."""
    try:
        await rename_conversation_name(collection, session_id, new_name)
        logger.info(f"Renamed session {session_id} to {new_name}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to rename session {session_id}: {e}")
        return {"error": str(e)}
