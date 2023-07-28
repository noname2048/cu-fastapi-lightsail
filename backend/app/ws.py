import asyncio
import random

from fastapi import APIRouter, Path, WebSocket

router = APIRouter()

topics = {}


def subscribe(topic: str, ws):
    if topic in topics:
        topics[topic].append(ws)
    else:
        topics[topic] = [ws]


def unsubscribe(topic: str, ws):
    if topic in topics:
        if ws in topics[topic]:
            topics[topic].remove(ws)


async def publish(topic: str, data: dict):
    await asyncio.gather(*[send_data(topic, ws, data) for ws in topics[topic]])


async def send_data(topic: str, ws: WebSocket, data: dict):
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


@router.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str = Path(...)):
    print("Accepting client connection...")
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
