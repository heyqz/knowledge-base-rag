from fastapi import APIRouter, UploadFile, BackgroundTasks, HTTPException

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
async def upload_document(file: UploadFile, background_tasks: BackgroundTasks,):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Only PDF files are supported"
        )
    
    document = document_service.upload_document(file)
    
    background_tasks.add_task(
        document_service.process_document,
        document.id
    )
    
    return DocumentResponse(
        id=document.id,
        filename=document.original_filename,
        status=document.status,
        uploaded_at=document.uploaded_at,
    )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    
    success = document_service.delete_document(document_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {"message": "Document deleted successfully"}