from fastapi import APIRouter
from typing import Literal
from pydantic import BaseModel
import random
from dotenv import load_dotenv
import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
import time

load_dotenv()
keys = [os.getenv("SDXL_KEY1"), os.getenv("SDXL_KEY2")]

router = APIRouter()  # point!


class kbInput(BaseModel):
    prompt: str = ""
    size: Literal["512x512", "256x256", "128x128", "512x640", "640x512"] = "512x512"


@router.post("/kkbot")
async def kbot(inp: kbInput):
    start = time.time()
    h, w = 512, 512
    match inp.size:
        case "512x512":
            type = -1
        case "256x256":
            type = 1
        case "128x128":
            type = 2
        case "512x640":
            type = 3
            h, w = 512, 640
        case "640x512":
            type = 4
            h, w = 640, 512
    stability_key = random.sample(keys, 1)[0]
    stability_api = client.StabilityInference(
        key=stability_key,  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2",  # Set the engine to use for generation.
    )
    answers = await generate(stability_api, inp.prompt, h, w)
    for resp in answers:
        if resp.artifacts[0].finish_reason == 4:
            return {"code": 404, "message": "Invalid prompts detected"}
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                filename = str(artifact.seed) + ".png"
                file_path = os.path.join("output", filename)
                if type == 1:
                    img = img.resize((256, 256))
                elif type == 2:
                    img = img.resize((128, 128))
                img.save(file_path)
                break

    waste_milliseconds = (time.time() - start) * 1000
    return {
        "code": 200,
        "message": "",
        "data": {
            "result": f"http://192.168.3.16/api/v1/download/image/{filename}",
            "candidates": [],
            "waste_milliseconds": waste_milliseconds,
            "extend_info": "",
            "type": "image",
            "recall_details": [],
        },
    }


async def generate(stability_api, pmt, h, w):
    answers = stability_api.generate(
        prompt=[
            generation.Prompt(
                text=pmt, parameters=generation.PromptParameters(weight=1.2)
            ),
            generation.Prompt(
                text="ugly", parameters=generation.PromptParameters(weight=-2)
            ),
            generation.Prompt(
                text="tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
                parameters=generation.PromptParameters(weight=-1),
            ),
        ],  # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        steps=30,  # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=7,  # Influences how strongly your generation is guided to match your prompt.
        # Setting this value higher increases the strength in which it tries to match your prompt.
        # Defaults to 7.0 if not specified.
        width=w,  # Generation width, defaults to 512 if not included.
        height=h,  # Generation height, defaults to 512 if not included.
        samples=1,  # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )
    return answers
