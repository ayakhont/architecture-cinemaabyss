import random
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import MovieEventRequest, UserEventRequest, PaymentEventRequest

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MOVIE_TOPIC = "movie-events"
USER_TOPIC = "user-events"
PAYMENT_TOPIC = "payment-events"

app.get("/api/events/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    return {"status": "ok"}

@app.post("/api/events/movie")
def create_movie_event(request: MovieEventRequest):
    # Process the request here
    return {"message": "Event received", "data": request}

@app.post("/api/events/user")
def create_user_event(request: UserEventRequest):
    # Process the request here
    return {"message": "User event received", "data": request}

@app.post("/api/events/payment")
def create_payment_event(request: PaymentEventRequest):
    # Process the request here
    return {"message": "Payment event received", "data": request}


def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()