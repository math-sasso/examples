import asyncio
import aiohttp
from typing import AsyncIterable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from beam_service import BeamService
from pydantic_models import Message

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def fetch_image(url: str) -> AsyncIterable[bytes]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                yield chunk

async def generate_image(content: str) -> AsyncIterable[bytes]:
    beam_service = BeamService(prompt=content)
    json_result = beam_service.call_api()
    image_url = json_result.get('image', "")
    
    # Fetch the image bytes using the image URL
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            image_bytes = await response.read()

    yield image_bytes


@app.post("/sdxl_streaming/")
async def sdxl_streamming(message: Message):
    
    generator = generate_image(content=message.content)
    return StreamingResponse(generator, media_type="image/png")