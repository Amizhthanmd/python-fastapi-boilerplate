import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from middleware.middleware import AuthMiddleware
from api.v1.endpoints import auth
from database.db import init_db
from config.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    init_db()
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Fast api boilerplate",
    description="Python fast api boilerplate",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

app.include_router(auth.auth_router, prefix="/api/v1/auth", tags=["users"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
