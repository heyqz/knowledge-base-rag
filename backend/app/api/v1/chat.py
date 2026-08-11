from fastapi import APIRouter

from backend.app.models.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def chat(request: ChatRequest):
    # Placeholder implementation - replace with actual chat logic
    return ChatResponse(answer="Not implemented yet.", sources=[])
