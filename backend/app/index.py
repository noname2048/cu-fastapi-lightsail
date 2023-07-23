from app.config import settings
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <h1>cu.noname2048.com</h1>
    <p>안녕하세요. cu.noname2048.com의 API 서버입니다.</p>
    <p>현재 버전: {settings.version}</p>
    <p>API 문서: <a href="/docs">/docs</a></p>
    <p>서버 시작 시간: {settings.start_at}</p>
    """


@router.get("/health", response_class=HTMLResponse)
async def healtcheck():
    return "<h1>OK</h1>"
