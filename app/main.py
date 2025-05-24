from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import redis
import json
import os
from dotenv import load_dotenv
from app.kafka_client import get_producer, get_consumer

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


@app.post("/produce/{message}")
def produce_message(message: str):
    producer = get_producer()
    topic = os.getenv("KAFKA_TOPIC")
    producer.produce(topic, value=message)
    producer.flush()
    return {"status": "Message sent", "message": message}

@app.get("/consume")
def consume_message():
    consumer = get_consumer()
    topic = os.getenv("KAFKA_TOPIC")
    consumer.subscribe([topic])

    msg = consumer.poll(5.0)
    if msg is None:
        return {"message": "No messages"}
    elif msg.error():
        return {"error": msg.error()}
    else:
        return {"message": msg.value().decode()}