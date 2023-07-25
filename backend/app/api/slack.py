from datetime import datetime

import requests
from fastapi import APIRouter

from app.config import settings
from app.slack import get_server_start

router = APIRouter()


@router.get("")
def get_slack_info():
    return {"slack_webhook_url": settings.slack_webhook_url}


@router.post("")
def post_slack():
    if not settings.slack_webhook_url.startswith("https://"):
        return {
            "message": "slack_webhook_url is not valid",
            "slack_webhook_url": settings.slack_webhook_url,
        }

    now_iso = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    payload = get_server_start(
        event_at=now_iso,
        version=settings.version,
        backend_env=settings.backend_env,
    )

    res = requests.post(
        url=settings.slack_webhook_url,
        json=payload,
    )

    return {"res": res.status_code, "message": res.text}
