import os
import re
from opencc import OpenCC
import random
import string
import logging
import httpx
import requests
from PIL import Image
import json
import pickle
from json import JSONDecodeError

from utils.gpt import translator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERNAL_IP = "192.168.3.16:9527"
EXTERNAL_IP = "61.216.75.236:9528"
BUILD_VERSION = os.environ.get("BUILD_VERSION", "internal")
if BUILD_VERSION == "internal":
    BACKEND_IP = os.environ.get("B_INTERNAL_IP")
else:
    BACKEND_IP = os.environ.get("B_EXTERNAL_IP")

with open("utils/midjourney-banned-prompt.pickle", "rb") as f:
    banned_words = pickle.load(f)
    f.close()


async def schema_validator(websocket):
    try:
        data = await websocket.receive_json()
        logger.info(json.dumps(data))
    except JSONDecodeError as e:
        msg = {"code": 400, "message": "Invalid message format!", "result": ""}
        await websocket.send_text(json.dumps(msg))
        raise Exception(e)
    if "image_url" in data.keys():
        if isinstance(data["image_url"], str) and len(data["image_url"]) > 0:
            url = data["image_url"].replace("61.216.75.236:9528", "192.168.3.16:9527")
            async with httpx.AsyncClient() as client:
                res = await client.get(url)
            if res.status_code == 404:
                logger.error("Image url error!")
                msg = {"code": 400, "message": "Image url error!", "result": ""}
                await websocket.send_text(json.dumps(msg))
                raise Exception("Image url error!")
            else:
                msg = {"code": 200, "message": "Image url is valid!", "result": ""}
                await websocket.send_text(json.dumps(msg))
    if "size" in data.keys():
        pattern = r"^[1-9]+\d*:[1-9]+\d*$"
        size = data["size"]
        if isinstance(size, str) and re.match(pattern, size):
            pass
        else:
            msg = {"code": 400, "message": "Invalid size format!", "result": ""}
            await websocket.send_text(json.dumps(msg))
            raise Exception("Size format error!")
    if "mode" in data.keys():
        mode = data["mode"]
        match mode:
            case "turbo":
                pass
            case "fast":
                pass
            case "relax":
                pass
            case _:
                msg = {"code": 400, "message": f"Mode {mode} is not valid!", "result": ""}
                await websocket.send_text(json.dumps(msg))
                raise Exception(f"Mode {mode} is not valid!")
    return data


async def style_parser(prompt, style):
    cc = OpenCC("t2s")
    try:
        style = cc.convert(style)
        match style:
            case "漫画":
                prompt += ", anime --niji 5"
            case "电影":
                prompt += (
                    ", photorealistic, cinematic, shot on kodak detailed cinematic hbo"
                )
            case "水墨画":
                prompt += ", chinese ink painting"
            case "油画":
                prompt += ", oil painting"
            case "水彩画":
                prompt += ", watercolor painting"
            case "铅笔画":
                prompt += ", pencil drawing"
            case "写实":
                prompt += ", realistic, DSLR, depth of field"
            case _:
                postfix = await translator(style)
                prompt += f", {postfix}"
    except:
        raise Exception("Style Parsing error")
    return prompt


async def prompt_censorer(prompt):
    prompt_list = prompt.split(" ")
    new_prompt_list = []
    for pmt in prompt_list:
        if pmt not in banned_words:
            new_prompt_list.append(pmt)
    return " ".join(new_prompt_list)


async def download_image(user_id, url):
    response = requests.get(url)
    file_name = os.path.basename(url)
    file_name = file_name.split("_")[1] + ".png"
    file_path = f"/workspace/output/{user_id}/{file_name}"
    file_prefix = file_path.split(".")[0]
    with open(file_path, "wb") as f:
        f.write(response.content)
    top_left, top_right, bottom_left, bottom_right = await split_image(file_path)
    top_left.save(file_prefix + "_1.png")
    top_right.save(file_prefix + "_2.png")
    bottom_left.save(file_prefix + "_3.png")
    bottom_right.save(file_prefix + "_4.png")
    image_list = [
        file_prefix + "_1.png",
        file_prefix + "_2.png",
        file_prefix + "_3.png",
        file_prefix + "_4.png",
    ]
    return [
        path.replace("/workspace/output/", f"http://{BACKEND_IP}/dcmj/media/")
        for path in image_list
    ]


async def split_image(image_file):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right


async def generate_random_id(n=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))
