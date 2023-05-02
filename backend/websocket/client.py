import asyncio
import time
import websockets
import ssl


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_cert = "/home/adamwang/localhost.crt"
ssl_key = "/home/adamwang/localhost.key"
ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

async def send_message():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        message = input("Enter your message: ")

        await websocket.send(message)
        print(f"Sent message: {message}")
        start = time.time()
        response = await websocket.recv()
        print(time.time()- start, " seconds")
        print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(send_message())