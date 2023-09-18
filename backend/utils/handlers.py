import os
import asyncio
import json
import logging
import httpx
from utils.exp_dict import ExpiringDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROXY_IP = os.environ.get("proxy")
SECRET = os.environ.get("mj-api-secret")
header = {"content-type": "application/json", "mj-api-secret": SECRET}
upsample_map = ExpiringDict()


async def job_handler(websocket, task, payload, job_id):
    try:
        if task == "imagine":
            return await imagine_handler(websocket, payload, job_id)
        elif task == "zoom":
            return await zoom_handler(websocket, payload, job_id)
        elif task == "inpaint":
            return await inpaint_handler(websocket, payload, job_id)
    except MidjourneyProxyError as e:
        raise e from None


async def imagine_handler(websocket, payload, job_id):
    prompt = payload["prompt"]
    if "base64Array" in payload.keys():
        base64Array = payload["base64Array"]
        task_id = await post_imagine(prompt, base64Array)
    else:
        task_id = await post_imagine(prompt)
    await send_start_message(websocket, task_id, job_id, "Imagine")
    try:
        msg = await pool_status(websocket, "Imagine", task_id)
    except Exception as e:
        raise Exception(e)
    response = {
        "task_id": msg["result"]["task_id"],
        "imageUrl": msg["result"]["imageUrl"],
        "buttons": msg["result"]["buttons"],
    }
    return response


async def zoom_handler(websocket, payload, job_id):
    if payload["customId"] in upsample_map.keys():
        msg = upsample_map[payload["customId"]]
    else:
        task_id = await post_action(payload["customId"], payload["taskId"])  # Upsample
        await send_start_message(websocket, task_id, job_id, "Zoom")
        try:
            msg = await pool_status(websocket, "Upsample", task_id)
            upsample_map[payload["customId"]] = msg
        except Exception as e:
            raise Exception(e)
    task_id = msg["result"]["task_id"]
    buttons = msg["result"]["buttons"]
    customId = ""
    for button in buttons:
        if button.startswith("MJ::CustomZoom"):
            customId = button
            break
    task_id = await post_action(customId, task_id)  # CustomZoom
    prompt = payload["prompt"] + " --ar " + payload["ar"] + " --zoom " + payload["zoom"]
    task_id = await post_modal(prompt, task_id)
    try:
        msg = await pool_status(websocket, "Zoom", task_id)
        response = {
            "task_id": msg["result"]["task_id"],
            "imageUrl": msg["result"]["imageUrl"],
            "buttons": msg["result"]["buttons"],
        }
        return response
    except Exception as e:
        raise Exception(e)


async def inpaint_handler(websocket, payload, job_id):
    logger.info(upsample_map.keys())
    if payload["customId"] in upsample_map.keys():
        msg = upsample_map[payload["customId"]]
    else:
        task_id = await post_action(payload["customId"], payload["taskId"])  # Upsample
        await send_start_message(websocket, task_id, job_id, "Inpaint")
        try:
            msg = await pool_status(websocket, "Upsample", task_id)
            upsample_map[payload["customId"]] = msg
        except Exception as e:
            raise Exception(e)
    task_id = msg["result"]["task_id"]
    buttons = msg["result"]["buttons"]
    customId = ""
    for button in buttons:
        if button.startswith("MJ::Inpaint"):
            customId = button
            break
    task_id = await post_action(customId, task_id)  # Inpaint
    prompt = payload["prompt"]
    mask = payload["mask"]
    task_id = await post_modal(prompt, task_id, mask)
    try:
        msg = await pool_status(websocket, "Inpaint", task_id)
        response = {
            "task_id": msg["result"]["task_id"],
            "imageUrl": msg["result"]["imageUrl"],
            "buttons": msg["result"]["buttons"],
        }
        return response
    except Exception as e:
        raise Exception(e)


async def send_start_message(websocket, task_id, job_id, task):
    msg = {
        "code": 200,
        "message": f"Start {task}!",
        "data": {"task_id": task_id, "job_id": job_id},
    }
    await websocket.send_text(json.dumps(msg))


async def post_imagine(prompt, base64Array=None):
    payload = {
        "prompt": prompt,
    }
    if base64Array:
        payload["base64Array"] = base64Array
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{PROXY_IP}/mj/submit/imagine", json=payload, headers=header
        )
    task_id = response.json()["result"]
    return task_id


async def post_action(customId: str, taskId: str):
    payload = {"customId": customId, "taskId": taskId}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{PROXY_IP}/mj/submit/action", json=payload, headers=header
        )
        taskId = response.json()["result"]
    return taskId


async def post_modal(prompt: str, taskId: str, mask: str = None):
    payload = {"prompt": prompt, "taskId": taskId}
    if mask:
        payload["maskBase64"] = mask
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{PROXY_IP}/mj/submit/modal", json=payload, headers=header
        )
        taskId = response.json()["result"]
    return taskId


async def post_describe(base64_str: str):
    payload = {"base64": base64_str}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{PROXY_IP}/mj/submit/describe", json=payload, headers=header
        )
    taskId = response.json()["result"]
    return taskId


async def get_status(task: str, task_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://{PROXY_IP}/mj/task/{task_id}/fetch", headers=header
        )
    status = response.json()["status"]
    progress = response.json()["progress"]
    if progress == "Waiting to start":
        progress = "Waiting Midjourney to start."
    imageUrl = response.json()["imageUrl"]
    msg = {
        "code": 200,
        "message": f"{task} in progress.",
        "result": {
            "status": status,
            "progress": progress,
            "task_id": task_id,
            "imageUrl": imageUrl,
        },
    }
    if response.json()["buttons"]:
        msg["result"]["buttons"] = [
            button["customId"] for button in response.json()["buttons"]
        ]
    if task == "Describe":
        if response.json()["properties"]:
            msg["result"]["properties"] = response.json()["properties"]
    if status == "FAILURE":
        failReason = response.json()["failReason"]
        msg["result"]["failReason"] = failReason
    return msg


async def pool_status(websocket, task: str, task_id: str):
    progress = 0
    patience = 0
    while progress != 100:
        msg = await get_status(task, task_id)
        if websocket:
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
            if failReason == "可能包含违规信息":
                msg = {
                    "code": 404,
                    "message": "Prompt contains inappropriate content.",
                    "result": "break",
                }
                if websocket:
                    await websocket.send_text(json.dumps(msg))
                raise Exception("Prompt contains inappropriate content.")
            if patience < 5:
                if failReason.startswith("You've run out of hours"):
                    msg = {
                        "code": 404,
                        "message": "Run out of hours!",
                        "result": "Switch to another proxy.",
                    }
                    if websocket:
                        await websocket.send_text(json.dumps(msg))
                    raise MidjourneyProxyError("Run out of hours!")
                else:
                    msg = {
                        "code": 404,
                        "message": failReason,
                        "data": {"patience": patience},
                    }
                    if websocket:
                        await websocket.send_text(json.dumps(msg))
                    await asyncio.sleep(5)
                    patience += 1
                    continue
            else:
                raise MidjourneyProxyError(msg["result"]["failReason"])
        else:
            await asyncio.sleep(10)
    return msg


class MidjourneyProxyError(Exception):
    pass
