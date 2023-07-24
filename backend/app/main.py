import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .api.index import router as api_router
from .config import send_deployment_success_to_slack, settings
from .index import router as http_router
from .middleware import add_useful_headers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "https://cu.noname2048.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_useful_headers)
app.include_router(http_router, tags=["http"], prefix="")
app.include_router(api_router, tags=["api"], prefix="/api")


@app.on_event("startup")
async def startup_event():
    if settings.backend_env != "local":
        asyncio.create_task(send_deployment_success_to_slack, delay=60)
    else:
        print("Running in local environment")
        from .database import Base, engine

        Base.metadata.create_all(bind=engine)
