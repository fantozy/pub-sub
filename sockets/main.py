import json
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketException

from pubsubmanager import PubSubManager


app = FastAPI()
pubsubmanager = PubSubManager()

websockets = []

async def pubsub_data_reader(subscriber):
    while True:
        message = await subscriber.get_message(ignore_subscribe_messages=True)

        if message is not None:
            msg = json.loads(message["data"].decode("utf-8"))

            for ws in websockets:
                await ws.send_text(msg["message"])

@app.websocket("/ws")
async def web_socket_endpoint(websocket: WebSocket):
    await pubsubmanager.connect()

    await websocket.accept()
    websockets.append(websocket)
    print(websockets)

    subscriber = await pubsubmanager.subscribe()
    asyncio.create_task(pubsub_data_reader(subscriber))
    try:        
        while True:
            data = await websocket.receive_text()
    except WebSocketException as wsEx:
        websockets.remove(websocket)
    

