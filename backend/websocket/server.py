import asyncio
import openai
import websockets
import ssl


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_cert = "/home/adamwang/localhost.crt"
ssl_key = "/home/adamwang/localhost.key"
ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

openai.api_key = "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"

f = open('prefix.txt')
prefix = {"role": "user", "content": f.read()}
f.close()

answer = {"role": "system", "content": "Yes, I'm ready. Please provide me with a keyword, and I will generate a detailed prompt based on the given structure and guidelines."}
messages = [prefix, answer]

async def chatgpt(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4",
            messages=messages
        )
        chat_response = completion
        answer = chat_response.choices[0].message.content
        await websocket.send({"code": 200, "message": "", "data": answer})

start_server = websockets.serve(chatgpt, "0.0.0.0", 8765, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()