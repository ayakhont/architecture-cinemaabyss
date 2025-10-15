from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from multiprocessing import Process
from models import MovieEventRequest, UserEventRequest, PaymentEventRequest

from producer import EventProducer
from consumer import EventConsumer

MOVIE_TOPIC = "movie-events"
USER_TOPIC = "user-events"
PAYMENT_TOPIC = "payment-events"

event_producer: Optional[EventProducer] = None

@asynccontextmanager
async def lifespan(app):
    print("Startup event producer...")
    global event_producer
    event_producer = EventProducer()
    print("Starting background consumer processes...")
    consumer1 = EventConsumer()
    consumer2 = EventConsumer()
    process1 = Process(target=consumer1.consume_events, daemon=True)
    process2 = Process(target=consumer2.consume_events, daemon=True)
    process1.start()
    process2.start()
    print("Background consumer processes started.")
    yield
    print("Shutdown consumer processes")
    process1.close()
    process2.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.get("/api/events/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    return {"status": "ok"}

@app.post("/api/events/movie")
def create_movie_event(request: MovieEventRequest):
    event_producer.send_event(MOVIE_TOPIC, request)
    return {"message": "Event received", "data": request}

@app.post("/api/events/user")
def create_user_event(request: UserEventRequest):
    event_producer.send_event(USER_TOPIC, request)
    return {"message": "User event received", "data": request}

@app.post("/api/events/payment")
def create_payment_event(request: PaymentEventRequest):
    event_producer.send_event(PAYMENT_TOPIC, request)
    return {"message": "Payment event received", "data": request}


def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()