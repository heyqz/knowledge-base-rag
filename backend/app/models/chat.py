from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    filename: str
    page: int
    score: float

class ChatResponse(BaseModel):
    answer: str
    # retrieved_chunks: int    
    sources: list[Source]
