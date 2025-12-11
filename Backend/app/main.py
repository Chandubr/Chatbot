from contextlib import asynccontextmanager
from app.db.database import create_client
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = create_client()
    app.state.mongo_client = client
    try:
        yield
    finally:
        client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"message": "Chatbot backend is running"}