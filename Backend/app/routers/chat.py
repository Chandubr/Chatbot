from fastapi import APIRouter,WebSocket
from app.services.chatbot_service import get_bot_response

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = get_bot_response(data)
        await websocket.send_text(response)