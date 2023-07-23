import time

from fastapi import Request, Response

from .config import settings


async def add_useful_headers(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Content-Language"] = "ko"
    if settings.version:
        response.headers["X-Backend-Version"] = settings.version
    return response
