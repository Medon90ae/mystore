
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any

from ..deps import AIClient, CurrentUser

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    prompt: str
    history: List[ChatMessage]

def get_role_context(user: Dict[str, Any]) -> str:
    """Determines the user's role from Firebase custom claims."""
    claims = user.get("claims", {})
    if claims.get("admin"):
        return "You are speaking to an Admin. Provide detailed system-level insights."
    if claims.get("merchant"):
        return "You are speaking to a Merchant. Focus on sales, products, and order management."
    return "You are speaking to a Customer. Be helpful and focus on product questions and support."

async def stream_gemini_response(model, prompt: str, history: List[ChatMessage], context: str):
    """Generator function to stream responses from Gemini."""
    try:
        # Recreate history in the format expected by the model
        chat_history = [{"role": msg.role, "parts": [{"text": msg.text}]} for msg in history]
        
        # The user's prompt is the last part of the contents
        contents = chat_history + [{"role": "user", "parts": [{"text": prompt}]}]

        # The system instruction provides the role-based context
        system_instruction = [context]

        responses = model.generate_content(
            contents=contents,
            system_instruction=system_instruction,
            stream=True
        )
        for response in responses:
            yield response.text
    except Exception as e:
        print(f"Error streaming from Gemini: {e}")
        yield f"Error: Could not get response from AI. {e}"


@router.post("/")
async def handle_chat(
    request: ChatRequest,
    user: CurrentUser,
    ai_client: AIClient,
):
    """
    Receives a chat prompt, adds user role context, and streams a response from Vertex AI.
    """
    role_context = get_role_context(user)
    
    try:
        return StreamingResponse(
            stream_gemini_response(ai_client, request.prompt, request.history, role_context),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
