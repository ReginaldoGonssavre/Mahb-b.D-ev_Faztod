from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    text: str

class MessageCreate(MessageBase):
    sender_id: int

class Message(MessageBase):
    id: int
    sender_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
