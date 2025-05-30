import os
from dotenv import load_dotenv
from confluent_kafka import Consumer

load_dotenv()

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_USERNAME"),
    'sasl.password': os.getenv("KAFKA_PASSWORD"),
    'group.id': 'demo-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topic = os.getenv("KAFKA_TOPIC")

consumer.subscribe([topic])
print(f"Listening to topic '{topic}'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
