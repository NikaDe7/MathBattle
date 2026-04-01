import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
import httpx

from dotenv import load_dotenv
from backend import game
load_dotenv()

# Middleware для COOP/COEP
class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        return response

app = FastAPI()
app.add_middleware(SecurityMiddleware)

# Статика і шаблони
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend")

# MongoDB
client = AsyncIOMotorClient(os.getenv("MONGO_DETAILS"))
db = client.math_game

# ------------------------------
class AuthToken(BaseModel):
    token: str

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"google_client_id": os.getenv("GOOGLE_CLIENT_ID")}
    )

@app.post("/auth/google")
async def google_auth(auth: AuthToken):
    if not auth.token:
        return {"status": "error", "message": "No token provided"}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": auth.token},
                timeout=10
            )
            if r.status_code != 200:
                return {"status": "error", "message": "Invalid Google token"}
            info = r.json()
            return {"name": info.get("name", "Гість"), "email": info.get("email"), "status": "ok"}
    except Exception as e:
        print("Ошибка /auth/google:", e)
        return {"status": "error", "message": str(e)}

@app.get("/leaderboard")
async def get_leaderboard():
    cursor = db.results.find({"user_id":{"$not":{"$regex":"^guest_|test|example"}}}).sort("score",-1).limit(10)
    results = await cursor.to_list(length=10)
    return [{"name": r.get("user_id"), "score": r.get("score"), "level": r.get("level","-"), "time": r.get("duration","-")} for r in results]

@app.websocket("/ws/battle/{user_id}/{level}/{duration}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, level: int, duration: int):
    await websocket.accept()
    current_score = 0
    try:
        while True:
            problem, answer = game.generate_math_problem(level)
            await websocket.send_json({"problem": problem, "score": current_score})
            data = await websocket.receive_text()
            try:
                if int(data) == answer:
                    current_score += 1
                    await websocket.send_json({"status": "correct", "score": current_score})
                else:
                    await websocket.send_json({"status": "wrong", "answer": answer})
            except ValueError:
                await websocket.send_json({"status": "invalid"})
    except WebSocketDisconnect:
        if current_score>0 and user_id and not user_id.startswith("guest_"):
            await db.results.update_one(
                {"user_id": user_id},
                {"$set":{"score":current_score,"level":f"{level} клас","duration":f"{duration//60} хв","timestamp":datetime.utcnow()}},
                upsert=True
            )

@app.get("/clear_db")
async def clear_db():
    await db.results.delete_many({"user_id":{"$regex":"^guest_|test|example"}})
    return {"status":"cleaned"}