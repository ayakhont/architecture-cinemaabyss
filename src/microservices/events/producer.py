import os

from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKERS', 'kafka:9092')

def serialize(data):
    try:
        return data.model_dump().encode('utf-8')
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Serialization error: {e}")
        return None

def send_event(topic, event):
    producer = EventProducer()
    result = producer.send_event(topic, event)
    producer.close()
    return result


class EventProducer:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVER):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=serialize
        )

    def send_event(self, topic, event):
        try:
            print(f"Event sending to {topic}: {event}")
            future = self.producer.send(topic, event)
            result = future.get(timeout=10)
            print(f"Event sent to {topic}: {event}")
            return result
        except KafkaError as e:
            print(f"Failed to send event to {topic}: {e}")
            return None

    def close(self):
        self.producer.close()