from app.core.config import settings
from qdrant_client import QdrantClient


def main():
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

    collections = client.get_collections()

    print("Connected to Qdrant Cloud!")
    print(collections)


if __name__ == "__main__":
    main()