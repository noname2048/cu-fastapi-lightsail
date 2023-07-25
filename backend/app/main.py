import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .api.index import router as api_router
from .config import settings
from .index import router as http_router
from .middleware import add_useful_headers
from app.slack import send_deployment_success_to_slack

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_useful_headers)
app.include_router(http_router, tags=["http"], prefix="")
app.include_router(api_router, tags=["api"], prefix="/api")


@app.on_event("startup")
async def startup_event():
    if settings.backend_env != "local":
        asyncio.create_task(send_deployment_success_to_slack())
    else:
        print("Running in local environment")
        from .database import Base, engine

        Base.metadata.create_all(bind=engine)
