# app/routers/pubsub.py

from fastapi import APIRouter
from app.redis_client import r

router = APIRouter()

@router.post("/publish/")
def publish_msg(message: str):
    r.publish("notifications", message)
    return {"status": "sent", "message": message}
