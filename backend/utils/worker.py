import asyncio
import json
import logging

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERNAL_IP = "192.168.3.16:9527"


async def post_imagine(websocket, prompt, job_id, proxy="proxy1"):
    PROXY_IP = ""
    match proxy:
        case "proxy1":
            PROXY_IP = "192.168.2.16:9999"
        case "proxy2":
            PROXY_IP = "192.168.2.16:9998"
        case _:
            raise Exception("Proxy selection error!")
    msg = {
        "code": 200,
        "message": "Start imagining!",
        "data": {"job_id": job_id, "PROXY_IP": PROXY_IP},
    }
    await websocket.send_text(json.dumps(msg))
    header = {"content-type": "application/json"}
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
            msg = await get_status(id, PROXY_IP)
            await websocket.send_text(json.dumps(msg))
            if msg["result"]["status"] in [
                "SUBMITTED",
                "IN_PROGRESS",
                "SUCCESS",
                "NOT_START",
            ]:
                if msg["result"]["progress"] is None or msg["result"]["progress"] in [
                    "Waiting Midjourney to start.",
                    "paused",
                ]:
                    await asyncio.sleep(10)
                    continue
                progress = msg["result"]["progress"].replace("%", "")
                progress = int(progress)
                if progress > 0:
                    await asyncio.sleep(5)
                    continue
                await asyncio.sleep(10)
            elif msg["result"]["status"] == "FAILURE":
                raise MidjourneyProxyError("Midjourney proxy error!")
            else:
                await asyncio.sleep(10)
    except Exception as e:
        logger.info(f"Exception {str(e)}")
        raise Exception(e)
    response = {"id": msg["result"]["id"], "imageUrl": msg["result"]["imageUrl"]}
    return response


async def get_status(id: str, PROXY_IP: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{PROXY_IP}/mj/task/{id}/fetch")
    status = response.json()["status"]
    progress = response.json()["progress"]
    if progress == "Waiting to start":
        progress = "Waiting Midjourney to start."
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


class MidjourneyProxyError(Exception):
    pass
