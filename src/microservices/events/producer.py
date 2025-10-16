import os

from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKERS', 'kafka:9092')

def deserialize(data):
    try:
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Deserialization error: {e}")
        return None


class EventProducer:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVER):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=deserialize,
            value_serializer=deserialize
        )

    def send_event(self, topic, event):
        try:
            future = self.producer.send(topic, event)
            result = future.get(timeout=10)
            logger.info(f"Event sent to {topic}: {event}")
            return result
        except KafkaError as e:
            logger.error(f"Failed to send event to {topic}: {e}")
            return None

    def close(self):
        self.producer.close()