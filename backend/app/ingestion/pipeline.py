import uuid
from pathlib import Path

from app.core.config import settings
from app.embedding.openai_embedder import OpenAIEmbedder
from app.ingestion.chunkers.recursive import RecursiveChunker
from app.ingestion.loader import PDFLoader
from app.storage.qdrant_repository import QdrantRepository
from app.models.document import Document
from app.core.config import settings


class IngestionPipeline:

    def __init__(
        self,
        loader: PDFLoader | None = None,
        chunker: RecursiveChunker | None = None,
        embedder: OpenAIEmbedder | None = None,
        repository: QdrantRepository | None = None,
    ):
        self.loader = loader or PDFLoader()
        self.chunker = chunker or RecursiveChunker()
        self.embedder = embedder or OpenAIEmbedder(settings.EMBEDDING_MODEL)
        self.repository = repository or QdrantRepository()
        
    def ingest(
        self,
        document: Document,
    ) -> None:
        """Ingest a PDF file into the vector repository."""

        # Load the PDF
        loaded_document = self.loader.load(document.file_path)

        # Chunk the document
        chunks = self.chunker.split(loaded_document)
        
        texts = [chunk.page_content for chunk in chunks]
        
        # Embed the texts
        vectors = self.embedder.embed(texts)
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        payloads = []

        for chunk in chunks:

            payloads.append(
                {
                    "document_id": document.id,
                    "filename": document.original_filename,
                    "text": chunk.page_content,
                    **chunk.metadata,
                }
            )
            
            
        self.repository.upsert(
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        )
        
        return 
