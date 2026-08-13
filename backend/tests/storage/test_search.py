from app.embedding.openai_embedder import OpenAIEmbedder
from app.storage.qdrant_repository import QdrantRepository
from app.core.config import settings


def test_search():
    embedder = OpenAIEmbedder(settings.EMBEDDING_MODEL)
    repo = QdrantRepository()
    query = "What is this document about?"

    vector = embedder.embed([query])[0]

    results = repo.search(
        query_vector=vector,
        limit=3,
    )
    
    
    assert len(results) > 0