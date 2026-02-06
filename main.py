from fastapi import FastAPI, HTTPException
from pyrogram import Client
from pyrogram.errors import FloodWait
import os
import asyncio

app = FastAPI()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")   # session رو اینجا بذار

client = Client(
    "clock_bio",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session_string
)

@app.on_event("startup")
async def startup():
    await client.start()

@app.post("/update-bio")
async def update_bio(data: dict):
    bio = data.get("bio")
    if not bio:
        raise HTTPException(400, "bio لازم است")

    try:
        await client.update_profile(bio=bio)
        return {"ok": True, "bio": bio}
    except FloodWait as e:
        return {"ok": False, "error": f"flood wait {e.value} ثانیه"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# برای تست
@app.get("/")
def root():
    return {"status": "running"}
