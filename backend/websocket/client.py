import asyncio
import websockets


async def test():
    uri = "wss://tti-dev.emotibot.com/dcmj/imagine"
    try:
        async with websockets.connect(uri) as websocket:
            message = '{"user_id": "adam","prompt": "柴犬在潛水", "preset": "写实"}'
            await websocket.send(message)
            while True:
                response = await websocket.recv()
                print(response)
                if "201" in response:
                    await websocket.close()

    except Exception as e:
        print(f"Exception: {e}")


asyncio.run(test())
