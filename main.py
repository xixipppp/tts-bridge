import os
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel

import edge_tts

app = FastAPI(title="tts-bridge", description="Edge-TTS bridge service")


class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    rate: str = "+0%"


@app.get("/")
def root():
    return {"service": "tts-bridge", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tts")
async def tts(req: TTSRequest):
    communicate = edge_tts.Communicate(req.text, req.voice, rate=req.rate)
    audio = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
    return Response(content=bytes(audio), media_type="audio/mpeg")
