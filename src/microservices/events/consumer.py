import traceback

from kafka import KafkaConsumer
from kafka.errors import KafkaError

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventConsumer:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='event-consumers'):
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            key_deserializer=lambda k: json.loads(k.decode('utf-8')),
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

    def subscribe(self, topics):
        self.consumer.subscribe(topics)
        logger.info(f"Subscribed to topics: {topics}")

    def consume_events(self):
        while True:
            try:
                messages = self.consumer.poll(timeout_ms=1000)
                logger.info("Polling for events...")
                for tp, msgs in messages.items():
                    logger.info(f"Received {len(msgs)} messages from topic partition {tp}")
                    for message in msgs:
                        logger.info(f"Received event from {message.topic}: "
                                    f"key={message.key} value={message.value} offset={message.offset}")
                        # Process the event here
                self.consumer.commit()
            except KafkaError as e:
                logger.error(f"Error consuming events: {e}")
                logger.error(traceback.format_exc())

    def close(self):
        self.consumer.commit()
        self.consumer.close()