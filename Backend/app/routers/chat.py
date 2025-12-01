import uuid
from fastapi import APIRouter, WebSocket
from app.core.logging import logger
from app.workflows.chatbot_workflow import bot_reply

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

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
        except Exception as e:
            logger.error(f"Error in websocket_chat: {e}")
            await websocket.send_text("Sorry, an error occurred. Please try again later.")