from datetime import datetime
from pathlib import Path

from qdrant_client import QdrantClient

from app.embedding.openai_embedder import OpenAIEmbedder
from app.ingestion.chunkers.recursive import RecursiveChunker
from app.ingestion.loader import PDFLoader
from app.ingestion.pipeline import IngestionPipeline
from app.storage.qdrant_repository import QdrantRepository
from app.core.config import settings
from app.models.document import Document


def test_ingestion_pipeline():

    client = QdrantClient(
        url=settings.QDRANT_URL,
    )

    repository = QdrantRepository(client=client)

    pipeline = IngestionPipeline(
        loader=PDFLoader(),
        chunker=RecursiveChunker(),
        embedder=OpenAIEmbedder(settings.EMBEDDING_MODEL),
        repository=repository,
    )

    doc = Document(
        id="test-id",
        filename="sample.pdf",
        original_filename="sample.pdf",
        file_path=str(Path("test_data/Pelican Welcome Letter.pdf")),
        file_size=0,
        status="uploaded",
        uploaded_at=datetime.utcnow(),
    )
    
    

    before_points, _ = client.scroll(
    collection_name=repository.collection_name,
    limit=100,
)

    before = len(before_points) 
    pipeline.ingest(
            document=doc
        )
    
    after_points, _ = client.scroll(
    collection_name=repository.collection_name,
    limit=100,
)

    after = len(after_points)

    assert after > before
    
    assert any(point.payload["document_id"] == "test-id"
               for point in after_points)