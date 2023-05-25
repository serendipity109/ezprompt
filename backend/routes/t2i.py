from fastapi import APIRouter
from pydantic import BaseModel
import random
from dotenv import load_dotenv
import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from fastapi.responses import FileResponse
from PIL import Image
import io


load_dotenv()
keys = [os.getenv("KEY1"), os.getenv("KEY2")]

router = APIRouter()  # point!


class t2iInput(BaseModel):
    prompt: str = ""
    nprompt: str = "tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"
    height: int = "512"
    width: int = "512"
    n: int = 1
    steps: int = 30
    CFG: float = 7.0


@router.post("/t2i")
async def t2i(inp: t2iInput):
    stability_key = random.sample(keys, 1)[0]
    stability_api = client.StabilityInference(
        key=stability_key,  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2",  # Set the engine to use for generation.
    )
    answers = stability_api.generate(
        prompt=[
            generation.Prompt(
                text=inp.prompt, parameters=generation.PromptParameters(weight=1.2)
            ),
            generation.Prompt(
                text="ugly", parameters=generation.PromptParameters(weight=-2)
            ),
            generation.Prompt(
                text=inp.nprompt, parameters=generation.PromptParameters(weight=-1)
            ),
        ],  # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        # In the example above we are combining a mountain landscape with the style of thomas kinkade, and we are negative prompting trees out of the resulting concept.
        # When determining prompt weights, the total possible range is [-10, 10] but we recommend staying within the range of [-2, 2].
        # seed=9080980, # If a seed is provided, the resulting generated image will be deterministic.
        # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
        # Note: This is only true for non-CLIP Guided generations.
        steps=inp.steps,  # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=inp.CFG,  # Influences how strongly your generation is guided to match your prompt.
        # Setting this value higher increases the strength in which it tries to match your prompt.
        # Defaults to 7.0 if not specified.
        width=inp.width,  # Generation width, defaults to 512 if not included.
        height=inp.height,  # Generation height, defaults to 512 if not included.
        samples=inp.n,  # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )
    print(f"Prompt: {inp.prompt} \nnPrompt: {inp.nprompt}")

    for resp in answers:
        if resp.artifacts[0].finish_reason == 4:
            return {"code": 404, "message": "Invalid prompts detected"}
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                file_path = os.path.join("output", str(artifact.seed) + ".png")
                img.save(file_path)
                return FileResponse(file_path, media_type="image/jpeg")
