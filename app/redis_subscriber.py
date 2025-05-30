# subscriber.py

import redis
import os
from dotenv import load_dotenv
from redis_client import r

pubsub = r.pubsub()
pubsub.subscribe('notifications')

print("Listening for messages on 'notifications' channel...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data'].decode()}")
