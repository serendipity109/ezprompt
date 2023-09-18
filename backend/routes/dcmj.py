import io
import json
import logging
import os
import time

from fastapi import APIRouter, HTTPException, UploadFile, WebSocket
from fastapi.responses import FileResponse
from PIL import Image
from starlette.websockets import WebSocketState
from utils.tools import generate_random_id
from utils.worker import imagine_worker
from utils.integrated_crud import IntegratedCRUD


router = APIRouter()
crud = IntegratedCRUD()

PROXY_IP = os.environ.get("proxy")
URL = os.environ.get("url")
SECRET = os.environ.get("mj-api-secret")
header = {"content-type": "application/json", "mj-api-secret": SECRET}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.websocket("/dcmj/imagine")
async def imagine(websocket: WebSocket):
    start = time.time()
    await websocket.accept()
    msg = {"code": 200, "message": "Waiting to start imagining.", "result": ""}
    await websocket.send_text(json.dumps(msg))
    job_id = await generate_random_id()
    try:
        await imagine_worker(websocket, start, job_id)
    except Exception as e:
        msg = {
            "code": 404,
            "message": str(e),
            "result": "",
        }
        logger.exception(json.dumps(msg))
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()


@router.post("/dcmj/upload")
async def upload_file(user_id: str, file: UploadFile):
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image.save(os.path.join(folder, file.filename))
    except:
        raise HTTPException(status_code=404, detail="Invalid image file.")
    return {
        "code": 200,
        "message": "Successfully uploaded image!",
        "data": f"{URL}dcmj/media/{user_id}/{file.filename}",
    }


@router.get("/dcmj/media/{user_id}/{image_name}")
async def show_image(user_id: str, image_name: str):
    image_path = os.path.join("/workspace/output", user_id, image_name)
    if os.path.isfile(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
