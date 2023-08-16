import logging
import os
import time
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from routes import SDXL, dcmj, account
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


class BlockIPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_404=5):
        super().__init__(app)
        self.max_404 = max_404
        self.ip_404_counter = defaultdict(int)
        self.allowed_ips = {"192.168.3.16", "127.0.0.1"}  # 将其他允许的 IP 地址添加到这里

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        # 检查 IP 是否允许
        if client_ip not in self.allowed_ips:
            # 如果 IP 不在允许列表中，直接返回 403 Forbidden 响应
            return Response("IP Blocked", status_code=403)

        response = await call_next(request)

        # 检查响应是否为 404
        if response.status_code == 404:
            self.ip_404_counter[client_ip] += 1
            if self.ip_404_counter[client_ip] >= self.max_404:
                # 可以在这里添加日志或警报
                pass
        else:
            # 如果请求成功，重置计数器
            self.ip_404_counter[client_ip] = 0

        return response


# Add CORS middleware
origins = ["*"]
# app.add_middleware(BlockIPMiddleware)
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
api_router.include_router(account.router)


@app.get("/")
async def root():
    return {"Model": "EZPrompt"}


@app.get("/get_hash")
async def get_hash(key: str):
    try:
        value = redis_client.get_hash(key)
    except Exception as e:
        raise Exception(e)
    return value


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
    res = []
    for img in imgs:
        value = redis_client.get_hash(img)
        prompt = value["prompt"]
        view1 = prompt.split(",")[0]
        view2 = prompt.replace(view1 + ",", "")
        res.append(
            {
                "img": img,
                "url": f"http://192.168.3.16:9527/media/mock/{img}.jpg",
                "view1": view1,
                "view2": view2,
            }
        )
    return res


@app.get("/media/{folder}/{image_name}")
async def show_image(folder: str, image_name: str):
    image_path = os.path.join("/workspace", folder, image_name)
    if os.path.isfile(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}


@app.get("/history")
async def get_history(user_id):
    crud = IntegratedCRUD()
    try:
        history = await crud.read_user_history(user_id)
        return {
            "code": 200,
            "message": "Successfully get images",
            "data": history,
        }
    except Exception as e:
        return {"code": 400, "message": str(e)}


@app.get("/showcase")
async def get_showcase(user_id=""):
    crud = IntegratedCRUD()
    try:
        showcase = await crud.read_showcase(user_id, 40)
        return {
            "code": 200,
            "message": "Successfully get images",
            "data": showcase,
        }
    except Exception as e:
        return {"code": 400, "message": str(e)}


# 定期刪檔案
FOLDER_PATH = "/workspace/output"
DELETE_INTERVAL = timedelta(days=7)


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
    crud = IntegratedCRUD()
    crud.delete_expires()


@app.on_event("startup")
async def start_scheduler():
    delete_old_files(FOLDER_PATH, DELETE_INTERVAL)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        delete_old_files, "interval", days=1, args=[FOLDER_PATH, DELETE_INTERVAL]
    )
    scheduler.start()


app.include_router(api_router)
