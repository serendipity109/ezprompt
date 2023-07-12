import logging
import os
import time
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes import SDXL, dcmj
from utils import minioTool, redisTool
from utils.integrated_crud import IntegratedCRUD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
minio_client = minioTool.MinioClient()
redis_client = redisTool.RedisClient()
BUILD_VERSION = os.environ.get("BUILD_VERSION", "internal")
if BUILD_VERSION == "internal":
    FRONTEND_IP = os.environ.get("F_INTERNAL_IP")
    BACKEND_IP = os.environ.get("B_INTERNAL_IP")
else:
    FRONTEND_IP = os.environ.get("F_EXTERNAL_IP")
    BACKEND_IP = os.environ.get("B_EXTERNAL_IP")


# Add CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

api_router.include_router(SDXL.router)
api_router.include_router(dcmj.router)
crud = IntegratedCRUD()


@app.get("/")
async def root():
    return {"Model": "EZPrompt"}


@app.get("/get_images")
async def get_images():
    imgs = [
        "s0",
        "s1",
        "s2",
        "s3",
        "s4",
        "s5",
        "s6",
        "s7",
        "s8",
        "s9",
        "s10",
        "s11",
        "s12",
        "s13",
        "s14",
    ]
    imgs = [img + ".png" for img in imgs]
    res = []
    for img in imgs:
        preview = redis_client.get(img)["prompt"]
        view1 = preview.split(",")[0]
        view2 = preview.replace(view1 + ",", "")
        res.append(
            {
                "img": img,
                "url": f"http://192.168.3.16:9527/media/mock/{img}",
                "view1": view1,
                "view2": view2,
            }
        )
    return res


@app.get("/get_image")
async def get_image(img="s0.png"):
    img_res = []
    pmt_res = redis_client.get(img)
    img_res.append(f"http://192.168.3.16:9527/media/mock/{img}")
    if "batch" in pmt_res.keys():
        for img in pmt_res["batch"]:
            img_res.append(f"http://192.168.3.16:9527/media/mock/{img}")
    return {"img_res": img_res, "pmt_res": pmt_res}


@app.get("/media/{folder}/{image_name}")
async def show_image(folder: str, image_name: str):
    image_path = os.path.join("/workspace", folder, image_name)
    if os.path.isfile(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}


@app.post("/create")
async def create_user(user_id, password, credits):
    try:
        await crud.create_user(user_id, password, credits)
        return {"code": 200, "message": f"Successfully create user {user_id}"}
    except Exception as e:
        return {"code": 400, "message": str(e)}


@app.delete("/delete")
async def delete_user(user_id):
    try:
        await crud.delete_user_by_id(user_id)
        return {"code": 200, "message": f"Successfully delete user {user_id}"}
    except Exception as e:
        return {"code": 400, "message": str(e)}


# 定期刪檔案
FOLDER_PATH = "/workspace/output"
DELETE_INTERVAL = timedelta(days=1)


def delete_old_files(folder_path: str, max_age: timedelta):
    current_time = time.time()
    logger.info("Start cleansing expired files!")
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_modification_time = os.path.getmtime(file_path)
            file_age = current_time - file_modification_time
            if file_age > max_age.total_seconds():
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting file: {file_path}, error: {str(e)}")


@app.on_event("startup")
async def start_scheduler():
    delete_old_files(FOLDER_PATH, DELETE_INTERVAL)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        delete_old_files, "interval", days=1, args=[FOLDER_PATH, DELETE_INTERVAL]
    )
    scheduler.start()


app.include_router(api_router)
