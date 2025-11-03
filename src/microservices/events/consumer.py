import os
import traceback

from kafka import KafkaConsumer
from kafka.errors import KafkaError

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKERS', 'kafka:9092')
MOVIE_TOPIC = "movie-events"
USER_TOPIC = "user-events"
PAYMENT_TOPIC = "payment-events"

def run_consumer():
    consumer = EventConsumer()
    consumer.subscribe([MOVIE_TOPIC, USER_TOPIC, PAYMENT_TOPIC])
    consumer.consume_events()

# def deserialize(data):
#     try:
#         return json.loads(data)
#     except (json.JSONDecodeError, AttributeError) as e:
#         print(f"Deserialization error: {e}")
#         return None

class EventConsumer:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVER, group_id='event-consumers'):
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

    def subscribe(self, topics):
        self.consumer.subscribe(topics)
        print(f"Subscribed to topics: {topics}")

    def consume_events(self):
        while True:
            try:
                messages = self.consumer.poll(timeout_ms=1000)
                for tp, msgs in messages.items():
                    print(f"Received {len(msgs)} messages from topic partition {tp}")
                    for message in msgs:
                        print(f"Received event from {message.topic}: "
                                    f"key={message.key} value={message.value} offset={message.offset}")
            except KafkaError as e:
                print(f"Error consuming events: {e}")
                print(traceback.format_exc())

    def close(self):
        self.consumer.commit()
        self.consumer.close()