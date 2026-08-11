from pydantic import BaseModel
from datetime import datetime


class Document(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    status: str
    uploaded_at: datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
