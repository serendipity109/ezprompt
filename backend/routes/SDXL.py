from fastapi import APIRouter
from pydantic import BaseModel
import base64
import requests
import random
from dotenv import load_dotenv
import os
import openai
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
from utils import minioTool
import io
import time


load_dotenv()
sdxl_keys = [os.getenv("SDXL_KEY1"), os.getenv("SDXL_KEY2")]
openai_keys = [
    os.getenv("OPENAI_KEY1"),
    os.getenv("OPENAI_KEY2"),
    os.getenv("OPENAI_KEY3"),
]


router = APIRouter()
minio_client = minioTool.MinioClient()


class xlInput(BaseModel):
    prompt: str = ""
    nprompt: str = "tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"
    hw: int = 1
    n: int = 1
    CFG: float = 7.0
    mock: bool = False


@router.post("/sdxl")
async def sdxl(inp: xlInput):
    if inp.mock:
        urls = [
            "http://192.168.3.16:8087/test/4066560120_u.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20230601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230601T074816Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=432c665b100a6a591f47d935a5fa64e0d7b3c9d40705006bf482d73c6b109ab5",
            "http://127.0.0.1:9000/test/288715164.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HB2R8ZEGJ22ZGLCDXQIQ%2F20230601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230601T084241Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJIQjJSOFpFR0oyMlpHTENEWFFJUSIsImV4cCI6MTY4NTY1MjEyMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.TuRXaJMEGhlD7LAlyD68HdGA09B4JEwkuWV_sWnuuq166siuNnaqgDiztt08JUtpkOr8h-kyhxOMCND-kLCryw&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=5356aa8911790b31903a90491bf6579c6c25799b09fd9abcc7320c5bafd94552",
            "http://127.0.0.1:9000/test/2506940560.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HB2R8ZEGJ22ZGLCDXQIQ%2F20230601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230601T084334Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJIQjJSOFpFR0oyMlpHTENEWFFJUSIsImV4cCI6MTY4NTY1MjEyMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.TuRXaJMEGhlD7LAlyD68HdGA09B4JEwkuWV_sWnuuq166siuNnaqgDiztt08JUtpkOr8h-kyhxOMCND-kLCryw&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=4ec9a0580104f85170e706e1250ecb56984f99e3ed816697dfbfe139c86a032d",
            "http://127.0.0.1:9000/test/4210377865.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HB2R8ZEGJ22ZGLCDXQIQ%2F20230601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230601T084522Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJIQjJSOFpFR0oyMlpHTENEWFFJUSIsImV4cCI6MTY4NTY1MjEyMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.TuRXaJMEGhlD7LAlyD68HdGA09B4JEwkuWV_sWnuuq166siuNnaqgDiztt08JUtpkOr8h-kyhxOMCND-kLCryw&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=023ab4907bc6546276bae329cf7f83c0857bf89a0aa620f5ded90e363120825b",
        ]
        fps = [
            "./output/4066560120_u.png",
            "./output/288715164.png",
            "./output/2506940560.png",
            "./output/4210377865.png",
        ]
        data = []
        for url, file_path in zip(urls, fps):
            data.append(
                {
                    "result": url,
                    "file_path": file_path,
                    "candidates": [],
                    "waste_milliseconds": 666666,
                    "extend_info": "",
                    "type": "image",
                    "recall_details": [],
                }
            )
        return {"code": 200, "message": "", "data": data}
    start = time.time()
    match inp.hw:
        case 0:
            h, w = 512, 640
        case 1:
            h, w = 512, 512
        case 2:
            h, w = 640, 512

    stability_key = random.sample(sdxl_keys, 1)[0]
    stability_api = client.StabilityInference(
        key=stability_key,  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2",  # Set the engine to use for generation.
    )
    answers = await gRPC(stability_api, inp.prompt, inp.nprompt, h, w, inp.n)
    urls = []
    for resp in answers:
        if resp.artifacts[0].finish_reason == 4:
            return {"code": 404, "message": "Invalid prompts detected"}
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                filename = str(artifact.seed) + ".png"
                file_path = os.path.join("output", filename)
                img.save(file_path)
                minio_client.upload_file("test", filename, file_path)
                urls.append(
                    minio_client.share_url("test", filename).replace(
                        "172.17.0.1:9000", "192.168.3.16:8087"
                    )
                )

    waste_milliseconds = (time.time() - start) * 1000
    data = []
    for url in urls:
        data.append(
            {
                "result": url,
                "file_path": file_path,
                "candidates": [],
                "waste_milliseconds": waste_milliseconds,
                "extend_info": "",
                "type": "image",
                "recall_details": [],
            }
        )
    return {"code": 200, "message": "", "data": data}


class ezInput(BaseModel):
    prompt: str = ""
    style: str = "creative"
    upscale: bool = False
    mock: bool = False


@router.post("/ezpmt")
async def ezpmt(inp: ezInput):
    if inp.mock:
        urls = [
            "http://192.168.3.16:8087/test/4066560120_u.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20230601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230601T074816Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=432c665b100a6a591f47d935a5fa64e0d7b3c9d40705006bf482d73c6b109ab5",
            "http://127.0.0.1:9000/test/288715164.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=WEHJ3R3TOYU653G4YGQI%2F20230602%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230602T035853Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJXRUhKM1IzVE9ZVTY1M0c0WUdRSSIsImV4cCI6MTY4NTcyMTIwMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.QXXGTJy12J7fsv3oNw-CWCfQEYjLDYDc9AT-mJeMRGwkkGmzxXmH_3Klz7DkFK5Nm0wX5SGkvOYHj9OYyGwtoA&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=ce48902f6f541b746cf3534a0bb286bc2b71faeb195f1b60961c8ee141899976",
            "http://127.0.0.1:9000/test/2506940560.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=WEHJ3R3TOYU653G4YGQI%2F20230602%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230602T035912Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJXRUhKM1IzVE9ZVTY1M0c0WUdRSSIsImV4cCI6MTY4NTcyMTIwMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.QXXGTJy12J7fsv3oNw-CWCfQEYjLDYDc9AT-mJeMRGwkkGmzxXmH_3Klz7DkFK5Nm0wX5SGkvOYHj9OYyGwtoA&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=94a78705692fa492e34cc356d85c301cc309ad05d0d47933a3804470f412f789",
            "http://127.0.0.1:9000/test/4210377865.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=WEHJ3R3TOYU653G4YGQI%2F20230602%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230602T035936Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJXRUhKM1IzVE9ZVTY1M0c0WUdRSSIsImV4cCI6MTY4NTcyMTIwMiwicGFyZW50IjoibWluaW9hZG1pbiJ9.QXXGTJy12J7fsv3oNw-CWCfQEYjLDYDc9AT-mJeMRGwkkGmzxXmH_3Klz7DkFK5Nm0wX5SGkvOYHj9OYyGwtoA&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=bdb9e3fa072dffb7457ee761254590dce67f20558811c675fcaf0778918bb4eb",
        ]
        fps = [
            "./output/4066560120_u.png",
            "./output/288715164.png",
            "./output/2506940560.png",
            "./output/4210377865.png",
        ]
        data = []
        for url, file_path in zip(urls, fps):
            data.append(
                {
                    "result": url,
                    "file_path": file_path,
                    "candidates": [],
                    "waste_milliseconds": 666666,
                    "extend_info": "",
                    "type": "image",
                    "recall_details": [],
                }
            )
        return {"code": 200, "message": "", "data": data}
    start = time.time()
    if inp.style == "creative":
        f = open("routes/prefix/creative.txt")
        prefix = {"role": "user", "content": f.read()}
        prefix["content"] += str("\n" + inp.prompt)
        f.close()
        style = ""
        model = "gpt-4"
    elif inp.style == "fantasy-art":
        prefix = {
            "role": "user",
            "content": f"Translate {inp.prompt} into English. If there are more than three objects, the translation must be ordered from small objects to big objects.",
        }
        style = inp.style
        model = "gpt-3.5-turbo"
    else:
        f = open("routes/prefix/preset.txt")
        prefix = {"role": "user", "content": f.read()}
        prefix["content"] += str("\t" + inp.prompt + f"in {inp.style} style")
        f.close()
        style = inp.style
        model = "gpt-4"
    openai.api_key = random.sample(openai_keys, 1)[0]
    messages = [prefix]
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    prompt = completion.choices[0].message.content
    prompt = prompt.replace('"', "")
    prompt = prompt.replace("young girl", "girl")

    data = await REST(prompt, style)
    urls = []
    fps = []
    for artifact in data["artifacts"]:
        image = artifact["base64"]
        filename = str(artifact["seed"]) + ".png"
        file_path = f"./output/{filename}"
        fps.append(file_path)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image))
            minio_client.upload_file("test", filename, file_path)
            urls.append(
                minio_client.share_url("test", filename).replace(
                    "172.17.0.1:9000", "192.168.3.16:8087"
                )
            )

    waste_milliseconds = (time.time() - start) * 1000
    data = []
    for url, file_path in zip(urls, fps):
        data.append(
            {
                "result": url,
                "file_path": file_path,
                "candidates": [],
                "waste_milliseconds": waste_milliseconds,
                "extend_info": "",
                "type": "image",
                "recall_details": [],
            }
        )
    return {"code": 200, "message": "", "data": data}


@router.post("/upscale")
async def upscale(file_path: str):
    start = time.time()
    data = await UPscale(file_path)
    file_path = file_path.replace(".png", "_u.png")
    filename = file_path.split("/")[-1]
    with open(file_path, "wb") as f:
        f.write(data)
    minio_client.upload_file("test", filename, file_path)
    url = minio_client.share_url("test", filename).replace(
        "172.17.0.1:9000", "192.168.3.16:8087"
    )

    waste_milliseconds = (time.time() - start) * 1000
    data = [
        {
            "result": url,
            "file_path": file_path,
            "candidates": [],
            "waste_milliseconds": waste_milliseconds,
            "extend_info": "",
            "type": "image",
            "recall_details": [],
        }
    ]

    return {"code": 200, "message": "", "data": data}


async def gRPC(stability_api, pmt, npmt, h, w, n):
    answers = stability_api.generate(
        prompt=[
            generation.Prompt(
                text=pmt, parameters=generation.PromptParameters(weight=1.2)
            ),
            generation.Prompt(
                text="ugly", parameters=generation.PromptParameters(weight=-2)
            ),
            generation.Prompt(
                text=npmt, parameters=generation.PromptParameters(weight=-1)
            ),
        ],  # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        steps=30,  # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=7,  # Influences how strongly your generation is guided to match your prompt.
        # Setting this value higher increases the strength in which it tries to match your prompt.
        # Defaults to 7.0 if not specified.
        width=w,  # Generation width, defaults to 512 if not included.
        height=h,  # Generation height, defaults to 512 if not included.
        samples=n,  # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )
    return answers


async def REST(prompt, style):
    stability_key = random.sample(sdxl_keys, 1)[0]
    print(prompt + "\n" + style)
    if style:
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 4,
            "steps": 30,
            "style_preset": style,
        }
    else:
        payload = {
            "text_prompts": [
                {"text": prompt, "weight": 1.2},
                {
                    "text": "tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
                    "weight": -1,
                },
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
            "Authorization": f"Bearer {stability_key}",
        },
        json=payload,
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    return response.json()


async def UPscale(file_path):
    img = Image.open(file_path)
    h = img.size[1]
    stability_key = random.sample(sdxl_keys, 1)[0]
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-x4-latent-upscaler/image-to-image/upscale",
        headers={"Accept": "image/png", "Authorization": f"Bearer {stability_key}"},
        files={"image": open(file_path, "rb")},
        data={
            "height": h * 2,
        },
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    return response.content
