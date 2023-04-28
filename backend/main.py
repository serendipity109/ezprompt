import os
import time
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes import kkbot, magicwriter, t2i, minioTool


app = FastAPI()
minio_client = minioTool.MinioClient()

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

api_router.include_router(kkbot.router)
api_router.include_router(magicwriter.router)
api_router.include_router(t2i.router)

@app.get("/")
async def root():
    return {"Model": "SDXL"}

@app.get("/show")
async def get_image(user_id, filename):
    image_path = os.path.join("images", user_id, filename)
    return FileResponse(image_path, media_type="image/jpeg")

@app.get("/get_images")
async def get_images(keyword):
    print(keyword)
    imgs = ["s0", "s1","s2","s3","s4","s5","s6","s7","s8","s9","s10",]
    imgs = [img + ".png" for img in imgs]
    res = []
    for img in imgs:
        res.append(minio_client.share_url("test", img).replace('172.17.0.1:9000', '192.168.3.16:7777'))
        # res.append(minio_client.share_url("test", img))
    return res

# 定期刪檔案
FOLDER_PATH = '/home/adamwang/stabilityaixl/output'  
DELETE_INTERVAL = timedelta(days=1)

def delete_old_files(folder_path: str, max_age: timedelta):
    current_time = time.time()
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_access_time = os.path.getatime(file_path)
            file_age = current_time - file_access_time
            if file_age > max_age.total_seconds():
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

@app.on_event("startup")
async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_old_files, 'interval', days=1, args=[FOLDER_PATH, DELETE_INTERVAL])
    scheduler.start()

app.include_router(api_router)   