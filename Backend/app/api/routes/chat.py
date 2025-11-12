from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from app.utils.groq import get_groq_chat_response
import re
from app.core.auth import get_current_user_id

router = APIRouter()

# Pydantic schema for request validation
class ChatRequest(BaseModel):
    message: str

# Convert markdown to HTML
def format_response(text: str) -> str:
    if not text:
        return "⚠️ No response received from assistant."
    
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = text.replace("\n", "<br>")
    text = re.sub(r"(?m)^\* ", "• ", text)
    return text

@router.post("/chat")
async def chat(message: ChatRequest, request: Request, user_id: str = Depends(get_current_user_id)):
    user_message = message.message.strip()

    if not user_message:
        return {"response": "⚠️ Please enter a message."}

    # User is authenticated (user_id available). Forward message to Groq model.
    response = get_groq_chat_response(user_message)
    formatted_response = format_response(response)
    return {"response": formatted_response}
