import asyncio
import io
import json
import logging
import os
import queue
import time

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import FileResponse
from PIL import Image

from utils.tools import download_image, generate_random_id, style_parser
from utils.worker import post_imagine
from utils.gpt import translator

router = APIRouter()
websocket_connections = set()

n_jobs = os.environ.get("CONCURRENT_JOBS", "3")
job_q = queue.Queue(int(n_jobs))
waiting_q = queue.Queue(1000)
job_map = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERNAL_IP = os.environ.get("INTERNAL_IP", "192.168.3.16:9527")
EXTERNAL_IP = os.environ.get("EXTERNAL_IP", "61.216.75.236:9528")


@router.websocket("/dcmj/imagine")
async def imagine(websocket: WebSocket):
    start = time.time()
    await websocket.accept()
    client_ip = websocket.client.host
    if "192.168" in client_ip:
        IP = INTERNAL_IP
    else:
        IP = EXTERNAL_IP
    websocket_connections.add(websocket)
    msg = {"code": 200, "message": "Waiting to start imagining.", "result": ""}
    await websocket.send_text(json.dumps(msg))
    try:
        await imagine_handler(websocket, start, IP)
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
        await websocket.close()
    websocket_connections.remove(websocket)
    await websocket.close()


async def imagine_handler(websocket, start, IP):
    global job_q, waiting_q, job_map
    data = await websocket.receive_json()
    user_id = data["user_id"]
    prompt = await translator(data["prompt"])
    if "preset" in data.keys():
        prompt = await style_parser(prompt, data["preset"])
    if "image_url" in data.keys() and data["image_url"]:
        prompt = data["image_url"] + " " + prompt
    logger.info(f"prompt: {prompt}")
    job_id = await generate_random_id()
    job_map = {job_id: (websocket, prompt)}
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    res = await job_schedular(job_id)
    taskid = res["id"]
    url = res["imageUrl"]
    image_list = await download_image(user_id, url, IP)
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
    while True:
        if job_q.full():
            if job_id not in list(waiting_q.queue):
                waiting_q.put(job_id)
            n = min(len(waiting_q.queue), n)
            await websocket.send_text(
                json.dumps(
                    {
                        "code": 200,
                        "message": f"Waiting for {n} job(s) to start!",
                        "result": "",
                    }
                )
            )
            await asyncio.sleep(10)
        else:
            if waiting_q.empty():
                # 沒人排
                pass
            elif job_id == waiting_q.queue[0]:
                # 排備取一
                waiting_q.get()
            else:
                # 排後面的讓別人先上
                await asyncio.sleep(10)
                continue
            job_q.put(job_id)
            res = await post_imagine(websocket, prompt)
            job_q.queue.remove(job_id)
            if job_q.empty() and waiting_q.empty():
                job_map = {}
            return res


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
        return {"error": "Image not found"}


@router.post("/dcmj/callback")
async def handle_callback(data: dict):
    if data["progress"] == "100%":
        return {"message": "Callback received"}
