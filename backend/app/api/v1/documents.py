from fastapi import APIRouter, UploadFile

from app.models.document import DocumentResponse, DocumentListResponse
from app.services.document_service import document_service


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=DocumentListResponse)
async def list_documents():
    documents = document_service.list_documents()
    return DocumentListResponse(
        documents=[
            DocumentResponse(
                id=doc.id,
                filename=doc.original_filename,
                status=doc.status,
                uploaded_at=doc.uploaded_at,
            )
            for doc in documents
        ]
    )


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile):
    document = document_service.upload_document(file)
    return DocumentResponse(
        id=document.id,
        filename=document.original_filename,
        status=document.status,
        uploaded_at=document.uploaded_at,
    )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    success = document_service.delete_document(document_id)
    if success:
        return {"message": "Document deleted successfully"}
    return {"message": "Document not found"}, 404
