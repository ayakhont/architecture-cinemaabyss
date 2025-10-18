import asyncio
import traceback
from time import sleep
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from starlette.requests import Request
from starlette.responses import Response

from multiprocessing import Process
from models import MovieEventRequest, UserEventRequest, PaymentEventRequest

from producer import send_event
from consumer import run_consumer

MOVIE_TOPIC = "movie-events"
USER_TOPIC = "user-events"
PAYMENT_TOPIC = "payment-events"

@asynccontextmanager
async def lifespan(app: FastAPI):
    sleep(5.0) # Wait for Kafka to be ready
    print("Starting background consumer processes...")
    process1 = Process(target=run_consumer, daemon=True)
    process2 = Process(target=run_consumer, daemon=True)
    process1.start()
    process2.start()
    print("Background consumer processes started.")
    yield
    print("Shutdown consumer processes")
    process1.terminate()
    process1.join()
    process2.terminate()
    process2.join()

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except (Exception, asyncio.CancelledError) as e:  # python 3.8 fix
        traceback_string = traceback.format_exc()
        print(f"500 ERROR HANDLING!:\n{traceback_string}")
        return Response(
            f"Internal server error:\n{traceback_string}",
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.middleware("http")(catch_exceptions_middleware)

@app.get("/api/events/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    message = f"Event service is healthy"
    return Response(f"{message}", status_code=200)

@app.post("/api/events/movie")
def create_movie_event(request: MovieEventRequest):
    print(f"Received movie event request: {request}")
    send_event(MOVIE_TOPIC, request)
    message = f"Movie event received"
    return Response(f"{message}", status_code=200)

@app.post("/api/events/user")
def create_user_event(request: UserEventRequest):
    print(f"Received user event request: {request}")
    send_event(USER_TOPIC, request)
    message = f"User event received"
    return Response(f"{message}", status_code=200)

@app.post("/api/events/payment")
def create_payment_event(request: PaymentEventRequest):
    print(f"Received payment event request: {request}")
    send_event(PAYMENT_TOPIC, request)
    message = f"Payment event received"
    return Response(f"{message}", status_code=200)


def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()