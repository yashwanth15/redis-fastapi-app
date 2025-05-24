from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("Redis Host:", os.getenv("REDIS_HOST"))

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True
)


@app.get("/")
def read_root():
    return {"message": "Redis + FastAPI working 🎉"}

@app.post("/set/{key}/{value}")
def set_redis_value(key: str, value: str):
    r.set(key, value)
    return {"status": "Key set", "key": key, "value": value}

@app.get("/get/{key}")
def get_redis_value(key: str):
    value = r.get(key)
    return {"value": value.decode() if value else None}