python
import os
import uuid
import asyncio
from fastapi import FastAPI
from fastapi.responses import
FileResponse, JSONResponse
from pydantic import BaseModel
import edge_tts
from groq import Groq
app = FastAPI()
GROQ_API_KEY =
os.getenv("GROQ_API_KEY", "")
client = Groqlapi_key=GROQ_API_KEY)
class VoiceChatin (Base Model):
text: str
voice: str = "uz-UZ-SardorNeural" #
yoki uz-UZ-MadinaNeural
SYSTEM PROMPT = (
"Sen Bibo degan o'zbek tilida
gapiradigan, juda do'stona, hazilkash va
samimiy Al yordamchisan.
"I
"Har doim o'zbek tilida javob ber.
Qisqa va aniq gapir."
async def tts_to_file(text: str, voice: str,
rate: str = "+0%") -> str:
out = f"out_{uuid.uuid4().hex}.mp3"
communicate =
edge_tts.Communicate(text, voice,
rate=rate)
await communicate.save(out)
return out
@app.get("/")
def root():
return {"ok": True, "service":
"bibo-voice-server"}
@app.post("/voice-chat")
def voice_chat(payload: VoiceChatin):
if not GROQ_API_KEY:
return JSONResponse({"error":
"GROQ_API_KEY missing on server"},
status_code=500)
=
user_text (payload.text or "").strip()
if not user_text:
return JSONResponse({"error":
"empty text"}, status_code=400)
completion =
client.chat.completions.create(
model="llama-3.1-70b-versatile",
messages=[
{"role": "system", "content":
SYSTEM PROMPT},
{"role": "user", "content":
user_text},
],
temperature=0.7,
)
(B
=
answer completion.choices[0].mes
sage.content.strip()
try:
mp3_path
=
asyncio.run(tts_to_file(answer,
payload.voice))
# Android app mp3 url'ni olishi
uchun: avval mp3'ni return qilamiz
return FileResponse(mp3_path,
media_type='audio/mpeg"
filename="bibo.mp3")
0,26
KB/S
