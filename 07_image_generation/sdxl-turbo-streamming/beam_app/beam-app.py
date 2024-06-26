from beam import endpoint, Image
from beam import Image, Volume, endpoint, Output

CACHE_PATH = "./models"
BEAM_OUTPUT_PATH = "/tmp/image_sdx_turbo.png"
BASE_MODEL = "stabilityai/sdxl-turbo"

image = Image(
    python_version="python3.10",
    python_packages=[
        "diffusers[torch]",
        "transformers",
        "pillow",
        "safetensors",
        "pandas"
    ],
)


def load_models():
    import torch
    from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file

    base = "stabilityai/stable-diffusion-xl-base-1.0"
    repo = "ByteDance/SDXL-Lightning"
    ckpt = "sdxl_lightning_4step_unet.safetensors" # Use the correct ckpt for your step setting!


    # Load model.
    pipe = StableDiffusionXLPipeline.from_pretrained(base, torch_dtype=torch.float16, variant="fp16").to("cuda")
    pipe.load_lora_weights(hf_hub_download(repo, ckpt))
    pipe.fuse_lora()

    # Ensure sampler uses "trailing" timesteps.
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")

    pipe.to("cuda")

    return pipe

@endpoint(
    name="sdxl-lightning-streamming",
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

    image = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0.0).images[0]

    print(f"Saved Image: {image}")

    # Save image file
    image.save(BEAM_OUTPUT_PATH)
    output = Output(path=BEAM_OUTPUT_PATH)
    output.save()
    # Retrieve pre-signed URL for output file
    url = output.public_url()
    print(url)

    return {"image": url}
