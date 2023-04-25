import io
import os
import random
from typing import Literal
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from PIL import Image
from pydantic import BaseModel
from stability_sdk import client
import time
from minioTool import MinioClient

load_dotenv()
keys = [os.getenv('KEY1'), os.getenv('KEY2'), os.getenv('KEY3')]

app = FastAPI()
minio_client = MinioClient()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class mwInput(BaseModel):
    user_id: str
    prompt: str = ''
    nprompt: str = "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"
    drawingstyle: Literal['油画', '水彩画', '国画', '简笔画'] = '油画'
    mood: Literal['平静', '高兴', '阴郁'] = '平静'
    style: Literal['清新', '文艺', '时尚', '黑白'] = '清新'
    height: int = '512'
    width: int = '512'
    n: int = 1
    steps: int = 30
    CFG: float = 7.0

@app.post("/mw")
async def mw(inp: mwInput):    
    stability_key = random.sample(keys, 1)[0]
    stability_api = client.StabilityInference(
        key=stability_key, # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
    )
    hint = ""
    match inp.drawingstyle:
        case '油画':
            drawingstyle = "oil painting"
            hint = "o"
        case '水彩画':
            drawingstyle = "aquarelle style"
            hint = "a"
        case '国画':
            drawingstyle = "traditional Chinese painting"
            hint = "t"
        case '简笔画':
            drawingstyle = "minimalist sketch style"
            hint = "m"
        case _:
            return {"code": 404, "message": f"Invalid drawingstyle!"}
    match inp.mood:
        case '平静':
            mood = "serene"
        case '高兴':
            mood = "joyful"
        case '阴郁':
            mood = "melancholic"
        case _:
            return {"code": 404, "message": f"Invalid mood!"}
    match inp.style:
        case '清新':
            style = "refreshing style"
        case '文艺':
            style = "artsy photography"
        case '时尚':
            style = "stylish"
        case '黑白':
            style = "monochrome"
        case _:
            return {"code": 404, "message": f"Invalid style!"}
    pmt = f"{drawingstyle} of {inp.prompt}, {mood} atmosphere, {style}"
    answers = stability_api.generate(
        prompt= [generation.Prompt(text=pmt,parameters=generation.PromptParameters(weight=1.2)),
        # generation.Prompt(text="serene",parameters=generation.PromptParameters(weight=1)),
        # generation.Prompt(text="oil painting",parameters=generation.PromptParameters(weight=1)),
        # generation.Prompt(text="monochrome",parameters=generation.PromptParameters(weight=1)),
        generation.Prompt(text=inp.nprompt,parameters=generation.PromptParameters(weight=-1))], # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        # In the example above we are combining a mountain landscape with the style of thomas kinkade, and we are negative prompting trees out of the resulting concept.
        # When determining prompt weights, the total possible range is [-10, 10] but we recommend staying within the range of [-2, 2].
        # seed=9080980, # If a seed is provided, the resulting generated image will be deterministic.
                        # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                        # Note: This is only true for non-CLIP Guided generations.
        steps=inp.steps, # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=inp.CFG, # Influences how strongly your generation is guided to match your prompt.
                    # Setting this value higher increases the strength in which it tries to match your prompt.
                    # Defaults to 7.0 if not specified.
        width=inp.width, # Generation width, defaults to 512 if not included.
        height=inp.height, # Generation height, defaults to 512 if not included.
        samples=inp.n, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                    # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                    # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )
    print(f"Prompt: {pmt} \nnPrompt: {inp.nprompt}")
    return_datas = []

    for resp in answers:
        for artifact in resp.artifacts:
            # if artifact.finish_reason == generation.FILTER:
            #     warnings.warn(
            #         "Your request activated the API's safety filters and could not be processed."
            #         "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                file_path = os.path.join("output", hint + str(artifact.seed)+ ".png")
                img.save(file_path)
                return FileResponse(file_path, media_type="image/jpeg")

class kbInput(BaseModel):
    prompt: str = ''
    size: Literal['512x512', '256x256', '128x128', '512x640', '640x512'] = '512x512'

@app.post("/kkbot")
async def kbot(inp: kbInput):    
    start = time.time()
    
    stability_key = random.sample(keys, 1)[0]
    stability_api = client.StabilityInference(
        key=stability_key, # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
    )
    answers = await generate(stability_api, inp.prompt)
    for resp in answers:
        for artifact in resp.artifacts:
           if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                filename = str(artifact.seed)+ ".png"
                file_path = os.path.join("output", filename)
                img.save(file_path)
                break
    
    waste_milliseconds = (time.time() - start)*1000
    return {
        "code": 200,
        "message": "",
        "data": {
            "result": f"http://192.168.3.20/api/v1/download/image/{filename}",
            "candidates": [],
            "waste_milliseconds": waste_milliseconds,
            "extend_info": "",
            "type": "image",
            "recall_details": []
        }
    }

async def generate(stability_api, pmt):
    answers = stability_api.generate(
        prompt= [generation.Prompt(text=pmt,parameters=generation.PromptParameters(weight=1.2)),
                 generation.Prompt(text="ugly",parameters=generation.PromptParameters(weight=-2)),
                 generation.Prompt(text="tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",parameters=generation.PromptParameters(weight=-1))], # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        steps=30, # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=7, # Influences how strongly your generation is guided to match your prompt.
                    # Setting this value higher increases the strength in which it tries to match your prompt.
                    # Defaults to 7.0 if not specified.
        width=512, # Generation width, defaults to 512 if not included.
        height=512, # Generation height, defaults to 512 if not included.
        samples=1, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                    # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                    # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )
    return answers

@app.get("/show")
async def get_image(user_id, filename):
    image_path = os.path.join("images", user_id, filename)
    return FileResponse(image_path, media_type="image/jpeg")
