import uuid
from app.core.config import settings
from qdrant_client import QdrantClient
from app.storage.qdrant_repository import QdrantRepository


def test_upsert():

    client = QdrantClient(":memory:")

    repo = QdrantRepository(client)

    ids = [str(uuid.uuid4())]

    vectors = [[0.1] * settings.EMBED_DIM]

    payloads = [
        {
            "text": "Hello",
            "page": 1,
        }
    ]

    repo.upsert(
        ids,
        vectors,
        payloads,
    )

    result = client.scroll(
        collection_name=repo.collection_name,
        limit=10,
    )

    assert len(result[0]) == 1