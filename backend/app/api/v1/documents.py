from fastapi import APIRouter


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get("/")
async def list_documents():
    return []

@router.post("/upload")
async def upload_document():
    raise NotImplementedError("Document upload functionality is not implemented yet.")
