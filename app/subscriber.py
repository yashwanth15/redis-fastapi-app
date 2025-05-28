# subscriber.py

import redis
import os
from dotenv import load_dotenv

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True
)

pubsub = r.pubsub()
pubsub.subscribe('notifications')

print("🔔 Listening for messages on 'notifications' channel...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"📩 Received: {message['data'].decode()}")
