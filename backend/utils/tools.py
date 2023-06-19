import os
from opencc import OpenCC
import random
import string

import requests
from PIL import Image

from utils.gpt import translator


async def style_parser(prompt, style):
    cc = OpenCC("t2s")
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
    return prompt


async def download_image(user_id, url, IP):
    response = requests.get(url)
    file_name = os.path.basename(url)
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
        path.replace("/workspace/output/", f"http://{IP}/dcmj/media/")
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
    letters_and_digits = string.digits
    random_id = "".join(random.choice(letters_and_digits) for _ in range(n))
    return random_id
