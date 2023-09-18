import os
import re
from opencc import OpenCC
import random
import string
import logging
import requests
from PIL import Image
import json
import pickle
from json import JSONDecodeError

from utils.gpt import translator
from utils.mj_styles import apply_style


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = os.environ.get("url", "https://tti-dev.emotibot.com/")

with open("utils/midjourney-banned-prompt.pickle", "rb") as f:
    banned_words = pickle.load(f)
    f.close()


async def imagine_preprocessor(websocket):
    try:
        data = await schema_validator(websocket)
        user_id = data["user_id"]
        prompt = await translator(data["prompt"])
        prompt = await prompt_censorer(prompt)
        if "nprompt" in data.keys():
            nprompt = data["nprompt"]
            nprompt = await translator(nprompt)
        else:
            nprompt = ""
        if "preset" in data.keys():
            prompt = await style_parser(prompt, nprompt, data["preset"])
        if "size" in data.keys():
            size = data["size"]
            prompt += f" --ar {size} "
        else:
            size = "1:1"
        if "mode" in data.keys():
            mode = data["mode"]
            if mode:
                prompt += f" --{mode}"
        else:
            mode = "fast"
        if "iw" in data.keys():
            iw = data["iw"]
            prompt += f" --iw {iw}"
        url = ""
        if "image_urls" in data.keys():
            data["image_url"] = data["image_urls"]
        if "image_url" in data.keys():
            url = data["image_url"]
            prompt = url + " " + prompt
        payload = {
            "prompt": prompt,
            "user_id": user_id,
            "image_url": url,
            "size": size,
            "mode": mode,
        }
    except Exception as e:
        msg = {"code": 404, "message": "URL download error.", "data": str(e)}
        if websocket:
            await websocket.send_text(json.dumps(msg))
        logger.exception(e)
        raise Exception(e)
    logger.info(f"prompt: {prompt}")
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return payload


async def zoom_preprocessor(websocket):
    try:
        data = await schema_validator(websocket)
        user_id = data["user_id"]
        prompt = await translator(data["prompt"])
        prompt = await prompt_censorer(prompt)
        if "nprompt" in data.keys():
            nprompt = data["nprompt"]
            nprompt = await translator(nprompt)
        else:
            nprompt = ""
        if "preset" in data.keys():
            prompt = await style_parser(prompt, nprompt, data["preset"])
        if "size" in data.keys():
            size = data["size"]
        else:
            size = "1:1"
    except Exception as e:
        logger.exception(e)
        raise Exception(e)
    logger.info(f"prompt: {prompt}")
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    payload = {
        "customId": data["customId"],
        "taskId": data["taskId"],
        "prompt": prompt,
        "ar": size,
        "zoom": data["zoom"],
    }
    return user_id, payload


async def inpaint_preprocessor(websocket):
    try:
        data = await schema_validator(websocket)
        user_id = data["user_id"]
        prompt = await translator(data["prompt"])
        prompt = await prompt_censorer(prompt)
        if "nprompt" in data.keys():
            nprompt = data["nprompt"]
            nprompt = await translator(nprompt)
        else:
            nprompt = ""
        if "preset" in data.keys():
            prompt = await style_parser(prompt, nprompt, data["preset"])
    except Exception as e:
        logger.exception(e)
        raise Exception(e)
    logger.info(f"prompt: {prompt}")
    folder = f"/workspace/output/{user_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    payload = {
        "customId": data["customId"],
        "taskId": data["taskId"],
        "prompt": prompt,
        "mask": data["mask"],
    }
    return user_id, payload


async def schema_validator(websocket):
    try:
        data = await websocket.receive_json()
        logger.info(json.dumps(data))
    except JSONDecodeError as e:
        msg = {"code": 404, "message": "Invalid message format!", "result": ""}
        await websocket.send_text(json.dumps(msg))
        raise Exception(e)
    # if "image_url" in data.keys():
    #     if isinstance(data["image_url"], str) and len(data["image_url"]) > 0:
    #         url = data["image_url"].replace("http://20.6.72.133:8889/", "https://tti-dev.emotibot.com/")
    #         async with httpx.AsyncClient() as client:
    #             res = await client.get(url)
    #         if res.status_code == 404:
    #             logger.info("Image url error!")
    #             msg = {"code": 404, "message": "Image url error!", "result": ""}
    #             await websocket.send_text(json.dumps(msg))
    #             raise Exception("Image url error!")
    #         else:
    #             msg = {"code": 200, "message": "Image url is valid!", "result": ""}
    #             await websocket.send_text(json.dumps(msg))
    if "size" in data.keys():
        pattern = r"^[1-9]+\d*:[1-9]+\d*$"
        size = data["size"]
        if isinstance(size, str) and re.match(pattern, size):
            pass
        else:
            msg = {"code": 404, "message": "Invalid size format!", "result": ""}
            await websocket.send_text(json.dumps(msg))
            raise Exception("Size format error!")
    return data


async def style_parser(prompt, nprompt, style):
    cc = OpenCC("t2s")
    try:
        style = cc.convert(style)
        prompt = await apply_style(style, prompt, nprompt)
    except:
        raise Exception("Style Parsing error")
    return prompt


async def prompt_censorer(prompt):
    prompt_list = prompt.split(" ")
    new_prompt_list = []
    for pmt in prompt_list:
        if pmt not in banned_words:
            new_prompt_list.append(pmt)
    prompt = " ".join(new_prompt_list)
    matches = re.findall(r"(--[\w\s\d]+)", prompt)
    for match in matches:
        prompt = prompt.replace(match, "")
    prompt = (
        prompt.replace("-", ",")
        .replace("--", ",")
        .replace("\uff04750", "")
        .replace("$", "")
    )
    return prompt


async def download_image(user_id, url):
    response = requests.get(url)
    logger.info(url)
    file_name = os.path.basename(url)
    file_name = file_name.split("_")[-1]
    file_path = f"/workspace/output/{user_id}/{file_name}"
    file_prefix = file_path.split(".")[0]
    with open(file_path, "wb") as f:
        f.write(response.content)
    top_left, top_right, bottom_left, bottom_right = await split_image(file_path)
    top_left.save(file_prefix + "_1.png")
    top_left.save(file_prefix + "_1.jpg", "JPEG", quality=95)
    top_right.save(file_prefix + "_2.png")
    top_right.save(file_prefix + "_2.jpg", "JPEG", quality=95)
    bottom_left.save(file_prefix + "_3.png")
    bottom_left.save(file_prefix + "_3.jpg", "JPEG", quality=95)
    bottom_right.save(file_prefix + "_4.png")
    bottom_right.save(file_prefix + "_4.jpg", "JPEG", quality=95)
    image_list = [
        file_prefix + "_1.png",
        file_prefix + "_2.png",
        file_prefix + "_3.png",
        file_prefix + "_4.png",
    ]
    return [path.replace("/workspace/output/", "dcmj/media/") for path in image_list]


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
    letters_and_digits = string.digits
    random_id = "".join(random.choice(letters_and_digits) for _ in range(n))
    return random_id
