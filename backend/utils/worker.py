import os
import time
import json
import logging
from datetime import datetime
from utils.tools import download_image, imagine_preprocessor
from utils.handlers import job_handler
from utils.crud import MJImg
from utils.monitor import SQLAlchemyMon
from utils.integrated_crud import IntegratedCRUD


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

crud = IntegratedCRUD()
monitor = SQLAlchemyMon()
IP = os.environ.get("IP")
BACKEND_IP = f"{IP}:9527"


async def imagine_worker(websocket, start, job_id):
    payload = await imagine_preprocessor(websocket)
    res = await job_handler(websocket, "imagine", payload, job_id)
    taskid, url, buttons = res["task_id"], res["imageUrl"], res["buttons"]
    image_list = await download_image(user_id=payload["user_id"], url=url)
    image_list = [f"http://{BACKEND_IP}/{url}" for url in image_list]
    image_list.insert(0, image_list[0].replace("_1.png", ".png"))
    elapsed_time = time.time() - start
    return_msg = {
        "code": 201,
        "message": "Successfully create images!",
        "data": {
            "result": image_list,
            "elapsed_time": elapsed_time,
            "task_id": taskid,
            "buttons": buttons,
        },
    }
    await websocket.send_text(json.dumps(return_msg))
    payload["image_list"] = image_list[1:]
    payload["start"] = start
    await storage_worker(payload)


async def storage_worker(payload):
    if payload["image_url"]:
        mjimg = MJImg(
            user_id=payload["user_id"],
            prompt=payload["prompt"],
            source_url=payload["image_url"],
            size=payload["size"],
            images=payload["image_list"],
        )
    else:
        mjimg = MJImg(
            user_id=payload["user_id"],
            prompt=payload["prompt"],
            size=payload["size"],
            images=payload["image_list"],
        )
    await crud.insert_mjimage(mjimg)
    monitor.create(
        user_id=payload["user_id"],
        prompt=payload["prompt"],
        mode=payload["mode"],
        create_time=datetime.fromtimestamp(payload["start"]),
    )


class MidjourneyProxyError(Exception):
    pass
