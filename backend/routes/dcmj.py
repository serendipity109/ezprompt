import asyncio
import io
import json
import logging
import os
import time

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    UploadFile,
    WebSocket,
)
from starlette.websockets import WebSocketState
from fastapi.responses import FileResponse
from multiprocessing import Manager
from PIL import Image

from utils.tools import (
    download_image,
    generate_random_id,
    style_parser,
    prompt_censorer,
    schema_validator,
)
from utils.worker import post_imagine
from utils.gpt import translator

router = APIRouter()
websocket_connections = set()
manager = Manager()

n_jobs = os.environ.get("CONCURRENT_JOBS", "6")
job_q = manager.list()
jq1 = manager.list()
jq2 = manager.list()
waiting_q = manager.list()
job_map = manager.dict()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERNAL_IP = "192.168.3.16:9527"
EXTERNAL_IP = "61.216.75.236:9528"
BUILD_VERSION = os.environ.get("BUILD_VERSION", "internal")
if BUILD_VERSION == "internal":
    FRONTEND_IP = os.environ.get("F_INTERNAL_IP")
    BACKEND_IP = os.environ.get("B_INTERNAL_IP")
else:
    FRONTEND_IP = os.environ.get("F_EXTERNAL_IP")
    BACKEND_IP = os.environ.get("B_EXTERNAL_IP")


@router.websocket("/dcmj/imagine")
async def imagine(websocket: WebSocket):
    global job_q, waiting_q, job_map
    start = time.time()
    await websocket.accept()
    websocket_connections.add(websocket)
    msg = {"code": 200, "message": "Waiting to start imagining.", "result": ""}
    await websocket.send_text(json.dumps(msg))
    job_id = await generate_random_id()
    try:
        await imagine_handler(websocket, start, job_id)
    except Exception as e:
        await kill_zombie(job_id)
        if e == "Midjourney proxy error!":
            await imagine_handler(websocket, start, job_id)
        else:
            msg = {
                "code": 400,
                "message": str(e),
                "result": "",
            }
            logger.info(json.dumps(msg))
    finally:
        websocket_connections.remove(websocket)
        await websocket.close()


async def imagine_handler(websocket, start, job_id):
    global job_q, waiting_q, job_map
    try:
        data = await schema_validator(websocket)
        user_id = data["user_id"]
        prompt = await translator(data["prompt"])
        if "preset" in data.keys():
            prompt = await style_parser(prompt, data["preset"])
        if "image_url" in data.keys():
            prompt = data["image_url"] + " " + prompt
        prompt = await prompt_censorer(prompt)
    except Exception as e:
        logger.info(e)
        raise Exception(e)
    logger.info(f"prompt: {prompt}")
    job_map = {job_id: (websocket, prompt)}
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    res = await job_schedular(job_id)
    taskid = res["id"]
    url = res["imageUrl"]
    image_list = await download_image(user_id, url)
    image_list.insert(0, image_list[0].replace("_1.png", ".png"))
    elapsed_time = time.time() - start
    return_msg = {
        "code": 201,
        "message": "Successfully create images!",
        "data": {
            "result": image_list,
            "elapsed_time": elapsed_time,
            "task_id": taskid,
        },
    }
    await websocket.send_text(json.dumps(return_msg))


async def job_schedular(job_id):
    global job_q, waiting_q, job_map
    websocket, prompt = job_map[job_id]
    n = 1000
    while websocket.client_state == WebSocketState.CONNECTED:
        state = websocket.client_state
        logger.info(f"State: {state}, job_q: {len(job_q)}, waiting_q: {len(waiting_q)}")
        if len(job_q) == int(n_jobs):
            if job_id not in waiting_q:
                waiting_q.append(job_id)
            n = min(len(waiting_q), n)
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_text(
                    json.dumps(
                        {
                            "code": 200,
                            "message": f"Waiting for {n} job(s) to start!",
                            "result": "",
                        }
                    )
                )
            else:
                waiting_q.remove(job_id)
                raise Exception("Connection dropped out!")
            await asyncio.sleep(10)
        else:
            if len(waiting_q) == 0:
                # 沒人排
                pass
            elif job_id == waiting_q[0]:
                # 排備取一
                waiting_q.remove(job_id)
            else:
                # 排後面的讓別人先上
                await asyncio.sleep(10)
                continue
            if websocket.client_state == WebSocketState.CONNECTED:
                res = await job_handler(websocket, prompt, job_id)
            else:
                raise Exception("Connection Error!")
            if job_id in waiting_q:
                waiting_q.remove(job_id)
            if len(job_q) + len(waiting_q) == 0:
                job_map.clear()
                logger.info(
                    f"cleansing! wq: {str(waiting_q)}, jq: {str(job_q)}, job_map: {job_map}"
                )
            return res


async def job_handler(websocket, prompt, job_id):
    global job_q, jq1, jq2
    job_q.append(job_id)
    if len(jq1) < int(n_jobs) // 2:
        jq1.append(job_id)
        res = await post_imagine(websocket, prompt, job_id, "proxy1")
        jq1.remove(job_id)
    elif len(jq2) < int(n_jobs) // 2:
        jq2.append(job_id)
        res = await post_imagine(websocket, prompt, job_id, "proxy2")
        jq2.remove(job_id)
    else:
        raise Exception(f"Job queue error! jq1: {jq1}, jq2: {jq2}, jq: {job_q}")
    job_q.remove(job_id)
    return res


async def kill_zombie(job_id):
    global job_q, waiting_q, jq1, jq2
    logger.info(
        f"Before: wq: {str(waiting_q)}, jq: {str(job_q)}, jq1: {str(jq1)}, jq2: {str(jq2)}, job_id: {job_id}"
    )
    for queue in [job_q, waiting_q, jq1, jq2]:
        if job_id in queue:
            queue.remove(job_id)
    logger.info(
        f"After: wq: {str(waiting_q)}, jq: {str(job_q)}, q1: {str(jq1)}, jq2: {str(jq2)}, job_id: {job_id}"
    )


@router.post("/dcmj/upload")
async def upload_file(request: Request, user_id: str, file: UploadFile):
    client_ip = request.client.host
    if "192.168" in client_ip:
        IP = INTERNAL_IP
    else:
        IP = EXTERNAL_IP
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image.save(os.path.join(folder, file.filename))
    except:
        raise HTTPException(status_code=400, detail="Invalid image file.")
    return {
        "code": 200,
        "message": "Successfully uploaded image!",
        "data": f"http://{IP}/dcmj/media/{user_id}/{file.filename}",
    }


@router.get("/dcmj/media/{user_id}/{image_name}")
async def show_image(user_id: str, image_name: str):
    image_path = os.path.join("/workspace/output", user_id, image_name)
    if os.path.isfile(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")


@router.post("/dcmj/callback")
async def handle_callback(data: dict):
    if data["progress"] == "100%":
        return {"message": "Callback received"}
