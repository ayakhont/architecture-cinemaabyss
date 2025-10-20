from pydantic import BaseModel, EmailStr
from typing import Optional, List


class MovieEventRequest(BaseModel):
    movie_id: int
    title: str
    action: str
    user_id: int
    rating: Optional[float] = None
    genres: Optional[List[str]] = None
    description: Optional[str] = None

class UserEventRequest(BaseModel):
    user_id: int
    action: str
    timestamp: str
    username: str
    email: Optional[EmailStr] = None

class PaymentEventRequest(BaseModel):
    payment_id: int
    user_id: int
    amount: float
    status: str
    timestamp: str
    method_type: str