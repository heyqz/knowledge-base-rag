from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chat_service.chat(request.question)

@router.post("/stream")
def stream_chat(request: ChatRequest):
    return StreamingResponse(
        chat_service.stream_chat(request.question),
        media_type="text/event-stream",
        )