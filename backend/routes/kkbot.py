from fastapi import APIRouter
from typing import Literal
from pydantic import BaseModel
import random
from dotenv import load_dotenv
import os
from utils import minioTool
import requests
import base64
import openai
import time
from io import BytesIO
from PIL import Image


load_dotenv()
MINIO_OUTPUT_URL = os.environ.get("MINIO_OUTPUT_URL", "")
sdxl_keys = [os.getenv('SDXL_KEY1'), os.getenv('SDXL_KEY2')]
openai_keys = [os.getenv('OPENAI_KEY1'), os.getenv('OPENAI_KEY2'), os.getenv('OPENAI_KEY3')]

router = APIRouter() # point!
minio_client = minioTool.MinioClient()

class kbInput(BaseModel):
    prompt: str = ''
    size: Literal['512x512', '256x256', '128x128', '512x640', '640x512'] = '512x512'

@router.post("/ezrender/kkbot")
async def kbot(inp: kbInput):    
    start = time.time()
    h, w = 512, 512
    match inp.size:
        case '512x512':
            type = -1
        case '256x256':
            type = 1
        case '128x128':
            type = 2
        case '512x640':
            type = 3
            h, w = 512, 640
        case '640x512':
            type = 4
            h, w = 640, 512
    f = open('routes/prefix/preset.txt')
    prefix = {"role": "user", "content": f.read()}
    prefix["content"] += str("\t" + inp.prompt + f"in photographic style")
    f.close()
    model = "gpt-4"
    openai.api_key = random.sample(openai_keys, 1)[0]
    messages = [prefix]
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    prompt = completion.choices[0].message.content
    prompt = prompt.replace('"', '')
    prompt = prompt.replace("young girl", "girl")
    
    data = await REST(prompt, h, w)

    for artifact in data["artifacts"]:
        image = artifact["base64"]
        filename = str(artifact["seed"]) + ".png"
        file_path = f"./output/{filename}"
        im_bytes = base64.b64decode(image)
        im_file = BytesIO(im_bytes) 
        img = Image.open(im_file) 
        if type == 1:
            img = img.resize((256, 256))
        elif type == 2:
            img = img.resize((128, 128))
        img.save(file_path)
        minio_client.upload_file('ezrender', filename, file_path)
        url = minio_client.share_url("ezrender", filename).replace('http://172.17.0.1:9000', MINIO_OUTPUT_URL)
   
    waste_milliseconds = (time.time() - start)*1000
    return {
        "code": 200,
        "message": "",
        "data": {
            "result": url,
            "candidates": [],
            "waste_milliseconds": waste_milliseconds,
            "extend_info": "",
            "type": "image",
            "recall_details": []
        }
    }

async def REST(prompt, h, w, style="photographic"):
    stability_key = random.sample(sdxl_keys, 1)[0]
    print(prompt + '\n' + style)        
    if style:
        payload = {
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "clip_guidance_preset": "FAST_BLUE",
                "height": h,
                "width": w,
                "samples": 1,
                "steps": 30,
                "style_preset": style,
        }
    else:
        payload = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1.2
                    },
                    {
                        "text": "tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
                        "weight": -1
                    }
                ],
                "cfg_scale": 7,
                "clip_guidance_preset": "FAST_BLUE",
                "height": 512,
                "width": 512,
                "samples": 4,
                "steps": 30,
        }       
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {stability_key}"
        },
        json=payload
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    
    return response.json()
