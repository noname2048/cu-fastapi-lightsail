import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.index import router as api_router
from app.config import settings
from app.index import router as http_router
from app.middleware import add_useful_headers
from app.slack import send_deployment_success_to_slack
from app.ws import router as ws_router

app = FastAPI()
allow_origins: list[str] = settings.allow_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_useful_headers)
app.include_router(http_router, tags=["http"], prefix="")
app.include_router(api_router, tags=["api"], prefix="/api")
app.include_router(ws_router, tags=["ws"], prefix="")


@app.on_event("startup")
async def startup_event():
    if settings.backend_env != "local":
        asyncio.create_task(send_deployment_success_to_slack())
    else:
        print("Running in local environment")
        from .database import Base, engine

        Base.metadata.create_all(bind=engine)
