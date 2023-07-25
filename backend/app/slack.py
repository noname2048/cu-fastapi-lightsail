import asyncio
from datetime import datetime

import requests
from pytz import timezone

from app.config import settings


def get_server_start(event_at: str, version: str, backend_env: str):
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":white_check_mark: 새로운 서버가 시작되었습니다.",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*일시:* {event_at} | *버전*: {version} | *환경*: {backend_env}",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🏠 *INDEX* | https://cu.noname2048.com",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "바로가기",
                        "emoji": True,
                    },
                    "url": "https://cu.noname2048.com",
                    "value": "go_to_index",
                    "action_id": "go_to_index",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🚀 *API 문서* | https://cu.noname2048.com/docs",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "바로가기",
                        "emoji": True,
                    },
                    "url": "https://cu.noname2048.com/docs",
                    "value": "go_to_docs",
                    "action_id": "go_to_docs",
                },
            },
        ],
    }


async def send_deployment_success_to_slack(delay: int = 60):
    if not settings.slack_webhook_url.startswith("https://"):
        return

    event_at = datetime.now(tz=timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    payload = get_server_start(
        event_at=event_at,
        version=settings.version,
        backend_env=settings.backend_env,
    )

    for _ in range(60):
        await asyncio.sleep(delay)
        res = requests.post(
            url=settings.slack_webhook_url,
            json=payload,
            timeout=5,
        )
        if res.status_code == 200:
            return
        else:
            print(f"failed to send slack, {res.status_code}, {res.text}")
