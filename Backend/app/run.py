from uvicorn import run
from fastapi import FastAPI
from dotenv import load_dotenv
from app.core.config import envconfig 
from app.core.logging import logger
from contextlib import asynccontextmanager

load_dotenv()

if __name__ == "__main__":
    run(
        "app.main:app",
        host = envconfig.host,
        port = envconfig.port,
        reload = True
    )
