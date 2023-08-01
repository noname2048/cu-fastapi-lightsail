import asyncio
import random

from fastapi import APIRouter, Path, WebSocket

router = APIRouter()

topic2ws_list: dict[str, list[WebSocket]] = {}
BROADCAST = "broadcast"


def subscribe(topic: str, ws):
    """ws이 해당 topic을 구독한 것을 기록합니다."""
    if topic in topic2ws_list:
        topic2ws_list[topic].append(ws)
    else:
        topic2ws_list[topic] = [ws]


def unsubscribe(topic: str, ws):
    """ws이 해당 topic에 대해 구독 취소한 것을 기록합니다."""
    if topic in topic2ws_list:
        if ws in topic2ws_list[topic]:
            topic2ws_list[topic].remove(ws)


async def publish(topic: str, data: dict):
    """topic에 해당하는 모든 구독자에게 data를 전송합니다."""
    if topic != BROADCAST:
        target_ws_list = topic2ws_list.get(topic, [])
        await asyncio.gather(
            *[send_data(ws=ws, data=data, topic=topic) for ws in target_ws_list]
        )
    # broadcast
    target_ws_list = topic2ws_list.get(BROADCAST, [])
    await asyncio.gather(
        send_data(ws=ws, data=data, topic=BROADCAST) for ws in target_ws_list
    )


async def send_data(ws: WebSocket, data: dict, topic: str):
    """ws에 data를 전송합니다.
    실패할 경우 해당 토픽에서 ws를 구독 취소합니다."""
    try:
        await ws.send_json(data)
    except Exception as err:
        print("error:", err)
        await ws.close()
        unsubscribe(topic, ws)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Accepting client connection...")
    await websocket.accept()
    while True:
        try:
            await websocket.receive_text()
            resp = {"value": random.uniform(0, 1)}
            await websocket.send_json(resp)
        except Exception as err:
            print("error:", err)
            break
    print("Bye..")


@router.websocket("/ws/topic/{topic}")
async def websocket_topic(websocket: WebSocket, topic: str = Path(...)):
    if topic == BROADCAST:
        await websocket.close()
        return

    await websocket.accept()
    subscribe(topic, websocket)
    while True:
        try:
            resp = await websocket.receive_json()
            await publish(topic, resp)
        except Exception as err:
            print("error:", err)
            break
    unsubscribe(topic, websocket)
    print("Bye..")


@router.websocket("/ws/broadcast")
async def websocket_broadcast(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            resp = await websocket.receive_json()
            await publish(BROADCAST, resp)
        except Exception as err:
            print("error:", err)
            break
    print("Bye..")
