from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.core.config import settings
from app.storage.vector_repository import VectorRepository
from app.models.retrieved_chunk import RetrievedChunk


class QdrantRepository(VectorRepository):
    """Qdrant implementation of the vector repository."""

    def __init__(self, client: QdrantClient | None = None):
        self.client = client or QdrantClient(
            url=settings.QDRANT_URL,
        )

        self.collection_name = settings.QDRANT_COLLECTION

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Create the collection if it does not exist."""

        if self.client.collection_exists(
            collection_name=self.collection_name
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=settings.EMBED_DIM,
                distance=Distance.COSINE,
            ),
        )

    def upsert(self,ids: list[str],vectors: list[list[float]], payloads: list[dict]) -> None:
        if not (len(ids) == len(vectors) == len(payloads)):
            raise ValueError("ids, vectors and payloads must have the same length.")

        points = []
        for point_id, vector, payload in zip(ids, vectors, payloads):
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            )
        result = self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    

    def search(self,query_vector: list[float],limit: int = 5):
        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        )
        
        chunks = []
        for point in result.points:
            payload = point.payload or {}
            chunk = RetrievedChunk(
                text=payload["text"],
                score=point.score,
                filename=payload.get("filename"),
                page=payload.get("page"),
                document_id=payload.get("document_id"),
                # chunk_id =str(point.id),
            )
            chunks.append(chunk)
        return chunks
    
    def get_all_chunks(self) -> list[RetrievedChunk]:
        chunks = []
        offset = None
        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
                
            for point in points:
                payload = point.payload or {}
                chunk = RetrievedChunk(
                    text=payload["text"],
                    score=0.0,
                    filename=payload.get("filename"),
                    page=payload.get("page"),
                    document_id=payload.get("document_id")
                )
                
                chunks.append(chunk)
                
            if offset is None:
                break
        
        return chunks
    
    def delete_by_document_id(self, document_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )