from pydantic import BaseModel, EmailStr
from typing import Optional, Literal, List


class MovieEventRequest(BaseModel):
    movie_id: int
    title: str
    action: str
    user_id: int
    rating: float
    genres: List[str]
    description: Optional[str] = None

class UserEventRequest(BaseModel):
    user_id: int
    action: str
    timestamp: str
    username: str
    email: EmailStr

class PaymentEventRequest(BaseModel):
    payment_id: int
    user_id: int
    amount: float
    status: Literal["completed", "pending", "failed"]
    timestamp: str
    method_type: str