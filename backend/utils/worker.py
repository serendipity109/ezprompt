import asyncio
import json
import logging
import os

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERNAL_IP = os.environ.get("INTERNAL_IP", "192.168.3.16:9527")
PROXY_IP = os.environ.get("PROXY_IP", "192.168.3.16:9999")


async def post_imagine(websocket, prompt, callback=False):
    msg = {"code": 200, "message": "Start imagining!", "result": ""}
    await websocket.send_text(json.dumps(msg))
    header = {"content-type": "application/json"}
    if callback:
        payload = {
            "notifyHook": f"http://{INTERNAL_IP}/callback",
            "prompt": prompt,
        }
    else:
        payload = {
            "prompt": prompt,
        }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{PROXY_IP}/mj/submit/imagine", json=payload, headers=header
        )
    id = response.json()["result"]
    progress = 0
    try:
        while progress != 100:
            msg = await get_status(id)
            await websocket.send_text(json.dumps(msg))
            if msg["result"]["status"] in ["SUBMITTED", "IN_PROGRESS", "SUCCESS"]:
                if msg["result"]["progress"] == "Waiting to start":
                    continue
                progress = msg["result"]["progress"].replace("%", "")
                progress = int(progress)
                if progress > 60:
                    await asyncio.sleep(3)
                    continue
                await asyncio.sleep(10)
            elif msg["result"]["status"] == "NOT_START":
                await asyncio.sleep(10)
    except:
        logger.info(f"Error msg: {msg}")
        raise "Account got banned!"
    response = {"id": msg["result"]["id"], "imageUrl": msg["result"]["imageUrl"]}
    return response


async def get_status(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{PROXY_IP}/mj/task/{id}/fetch")
    status = response.json()["status"]
    progress = response.json()["progress"]
    imageUrl = response.json()["imageUrl"]
    msg = {
        "code": 200,
        "message": "Imagining in progress.",
        "result": {
            "status": status,
            "progress": progress,
            "id": id,
            "imageUrl": imageUrl,
        },
    }
    return msg
