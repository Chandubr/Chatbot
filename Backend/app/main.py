from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app = FastAPI()

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