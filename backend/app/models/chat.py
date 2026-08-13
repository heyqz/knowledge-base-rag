from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: str
    page: int

class ChatResponse(BaseModel):
    answer: str
    retrieved_chunks: int    
    # sources: list[Source]
