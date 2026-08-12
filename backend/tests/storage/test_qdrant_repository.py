from qdrant_client import QdrantClient

from app.storage.qdrant_repository import QdrantRepository


def test_repository_initialization():
    """Repository should initialize successfully."""

    client = QdrantClient(":memory:")

    repo = QdrantRepository(client=client)

    assert repo.client is not None
    assert repo.collection_name == "knowledge-base"
    assert client.collection_exists(repo.collection_name)