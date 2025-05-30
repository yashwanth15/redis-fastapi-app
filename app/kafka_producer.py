import os
from dotenv import load_dotenv
from confluent_kafka import Producer

load_dotenv()

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_USERNAME"),
    'sasl.password': os.getenv("KAFKA_PASSWORD")
}

producer = Producer(conf)
topic = os.getenv("KAFKA_TOPIC")

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed:', err)
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

while True:
    value = input("Enter message to publish (or 'exit'): ")
    if value.lower() == 'exit':
        break
    producer.produce(topic, value.encode('utf-8'), callback=delivery_report)
    producer.flush()
