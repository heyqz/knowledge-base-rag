from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"

class Document(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    status: DocumentStatus
    uploaded_at: datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: DocumentStatus
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
