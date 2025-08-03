from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db, get_current_user
from backend.app.models.user import User
from backend.app.models.message import Message
from backend.app.schemas.message import MessageCreate, Message as MessageSchema
from backend.app.schemas.user import User as UserSchema

# Placeholder para integração de IA (LangChain, etc.)
# Em um estágio posterior, isso se conectaria ao AgenticRAGFramework
class SimpleAI:
    def generate_response(self, text: str) -> str:
        return f"AI says: You asked '{text}'. I am learning..."

ai_model = SimpleAI()
router = APIRouter()

@router.post("/", response_model=MessageSchema)
def send_message(
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save user message
    user_message = Message(text=message_in.text, sender_id=current_user.id)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Generate AI response
    ai_response_text = ai_model.generate_response(message_in.text)
    ai_message = Message(text=ai_response_text, sender_id=current_user.id) # AI also sends from current user for simplicity
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message

@router.get("/", response_model=list[MessageSchema])
def get_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(Message.sender_id == current_user.id).all()
    return messages
