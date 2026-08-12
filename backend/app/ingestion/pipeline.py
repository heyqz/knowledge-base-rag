import uuid
from pathlib import Path

from app.core.config import settings
from app.embedding.openai_embedder import OpenAIEmbedder
from app.ingestion.chunkers.recursive import RecursiveChunker
from app.ingestion.loader import PDFLoader
from app.storage.qdrant_repository import QdrantRepository


class IngestionPipeline:

    def __init__(
        self,
        loader: PDFLoader | None = None,
        chunker: RecursiveChunker | None = None,
        embedder: OpenAIEmbedder | None = None,
        repository: QdrantRepository | None = None,
    ):
        self.loader = loader or PDFLoader()
        self.chunker = chunker or RecursiveChunker(...)
        self.embedder = embedder or OpenAIEmbedder()
        self.repository = repository or QdrantRepository()
        
    def ingest(
        self,
        pdf_path: str | Path,
    ):
        """Ingest a PDF file into the vector repository."""

        # Load the PDF
        document = self.loader.load(pdf_path)

        # Chunk the document
        chunks = self.chunker.split(document)
        
        texts = [chunk.page_content for chunk in chunks]
        
        # Embed the texts
        vectors = self.embedder.embed(texts)
        
        print(f"Generated {len(vectors)} embeddings")

        ids = [str(uuid.uuid4()) for _ in chunks]
        
        payloads = []

        for chunk in chunks:

            payloads.append(
                {
                    "text": chunk.page_content,

                    **chunk.metadata,
                }
            )
            
        print("Calling repository.upsert...")
            
        self.repository.upsert(
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        )
        
        print("Upsert finished!")
        
        return len(chunks)
