from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.models.document import Document, DocumentStatus
from app.storage.document_repository import document_repository
from app.storage.file_storage import file_storage
from app.ingestion.pipeline import IngestionPipeline


class DocumentService:
    def __init__(self):
        self.pipeline = IngestionPipeline()
        
    def upload_document(self, file: UploadFile) -> Document:
        # Save the file to the storage
        saved_file = file_storage.save(file)

        # Create a new document record in the database
        document = Document(
            id=str(uuid4()),
            filename=saved_file.filename,
            original_filename=file.filename,
            file_path=saved_file.file_path,
            file_size=saved_file.file_size,
            status=DocumentStatus.UPLOADED,
            uploaded_at=datetime.utcnow(),
        )
        
        document_repository.create(document)

        try:

            self.pipeline.ingest(document)
            
            document.status = DocumentStatus.INDEXED

            document_repository.update_status(
                document.id,
                DocumentStatus.INDEXED,
            )

        except Exception as e:
            print(e)
        
        return document

    def list_documents(self):
        return document_repository.list_all()

    def get_document(self, document_id: str):
        return document_repository.get_by_id(document_id)

    def delete_document(self, document_id: str):
        document = document_repository.get_by_id(document_id)
        if document:
            # Delete the file from storage
            file_storage.delete(document.file_path)
            # Optionally, you can also delete the record from the database
            document_repository.delete(document_id)
            return True
        return False


document_service = DocumentService()
