import asyncio
import json
import logging

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def post_imagine(websocket, prompt, job_id, proxy="proxy1"):
    PROXY_IP = ""
    match proxy:
        case "proxy1":
            PROXY_IP = "192.168.2.16:9998"
        case "proxy2":
            PROXY_IP = "192.168.2.16:9999"
        case _:
            raise Exception("Proxy selection error!")
    msg = {
        "code": 200,
        "message": "Start imagining!",
        "data": {"job_id": job_id, "PROXY_IP": proxy},
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
    patience = 0
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
            failReason = msg["result"]["failReason"]
            if patience < 5:
                if failReason.startswith("You've run out of hours"):
                    msg = {
                        "code": 400,
                        "message": f"{proxy} run out of hours!",
                        "result": "Switch to another proxy.",
                    }
                    await websocket.send_text(json.dumps(msg))
                    raise MidjourneyProxyError(f"{proxy} run out of hours!")
                elif failReason == "可能包含违规信息":
                    msg = {
                        "code": 400,
                        "message": "Input message contains controversial issues. Reach out to the backend team.",
                        "result": "",
                    }
                    await websocket.send_text(json.dumps(msg))
                    raise MidjourneyProxyError(
                        "Input message contains controversial issues. Reach out to the backend team."
                    )
                else:
                    msg = {
                        "code": 400,
                        "message": failReason,
                        "data": {"patience": patience},
                    }
                    await websocket.send_text(json.dumps(msg))
                    await asyncio.sleep(5)
                    patience += 1
                    continue
            else:
                raise MidjourneyProxyError(msg["result"]["failReason"])
        else:
            await asyncio.sleep(10)
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
    if status == "FAILURE":
        failReason = response.json()["failReason"]
        msg["result"]["failReason"] = failReason
    return msg


class MidjourneyProxyError(Exception):
    pass
