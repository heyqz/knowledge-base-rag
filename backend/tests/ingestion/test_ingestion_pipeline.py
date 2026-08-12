from pathlib import Path

from qdrant_client import QdrantClient

from app.embedding.openai_embedder import OpenAIEmbedder
from app.ingestion.chunkers.recursive import RecursiveChunker
from app.ingestion.loader import PDFLoader
from app.ingestion.pipeline import IngestionPipeline
from app.storage.qdrant_repository import QdrantRepository
from app.core.config import settings


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

    chunk_count = pipeline.ingest(
        Path("test_data/Pelican Welcome Letter.pdf")
    )

    assert chunk_count > 0
    
    points, _ = client.scroll(
        collection_name=repository.collection_name,
        limit=100,
    )

    assert len(points) == chunk_count