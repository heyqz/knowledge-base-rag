from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    uploaded_at: str
    
class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]