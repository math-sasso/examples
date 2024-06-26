from beam import endpoint, Image
from beam import Image, Volume, endpoint, task_queue, Output

from diffusers import AutoPipelineForText2Image
import torch

CACHE_PATH = "./models"
BEAM_OUTPUT_PATH = "/tmp/image_sdx_turbo.png"


image = Image(
    python_version="python3.10",
    python_packages=[
        "diffusers[torch]",
        "transformers",
        "pillow",
    ],
    # commands=["apt-get update -y && apt-get install ffmpeg -y"],
    # base_image="docker.io/nvidia/cuda:12.3.1-runtime-ubuntu20.04",
)


def load_models():
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
    pipe.to("cuda")

    return pipe


@endpoint(
    name="sdxl-turbo",
    image=image,
    on_start=load_models,
    keep_warm_seconds=60,
    cpu=16,
    memory="32Gi",
    gpu="A100-40",
    volumes=[Volume(name="models", mount_path=CACHE_PATH)],
)
def generate(context, prompt):


    pipe = context.on_start_value

    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

    print(f"Saved Image: {image}")

    # Save image file
    image.save(BEAM_OUTPUT_PATH)
    output = Output(path=BEAM_OUTPUT_PATH)
    output.save()
    # Retrieve pre-signed URL for output file
    url = output.public_url()
    print(url)

    return {"image": url}
