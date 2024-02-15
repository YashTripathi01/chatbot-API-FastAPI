import asyncio
import websockets
from websockets.exceptions import InvalidStatusCode


async def chat():
    try:
        async with websockets.connect(
            "ws://localhost:8000/api/v1/users/1/chat"
        ) as websocket:
            while True:
                message = input("You: ")
                await websocket.send(message)
                response = await websocket.recv()
                print("Bot: " + response)

    except InvalidStatusCode as e:
        print("WebSocket connection failed: HTTP", e.status_code)


asyncio.get_event_loop().run_until_complete(chat())
