from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field
import redis
import json
import os
from dotenv import load_dotenv
from app.routes import users, reports, pubsub

load_dotenv()

print("Redis Host:", os.getenv("REDIS_HOST"))

app = FastAPI()
app.include_router(users.router,prefix="/users", tags=["Users"])
app.include_router(reports.router,prefix="/reports", tags=["Shift Reports (Cache)"])
app.include_router(pubsub.router,prefix="/pubsub", tags=["PubSub"])

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True
)

# Ratelimiting
@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    user_ip = request.client.host
    key = f"rate_limit:{user_ip}"
    
    count = r.incr(key)
    if count == 1:
        r.expire(key, 60)  # 60 seconds window

    if count > 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    return await call_next(request)

@app.get("/")
def read_root():
    return {"message": "Redis + FastAPI working 🎉"}

