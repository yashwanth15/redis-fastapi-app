from confluent_kafka import Producer, Consumer
import os

from dotenv import load_dotenv
load_dotenv()

# Kafka Configs
conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET")
}

def get_producer():
    return Producer(conf)

def get_consumer(group_id="test-group"):
    return Consumer({
        **conf,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
