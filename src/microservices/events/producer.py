from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
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