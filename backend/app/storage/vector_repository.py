from abc import ABC, abstractmethod
from app.models.retrieved_chunk import RetrievedChunk

class VectorRepository(ABC):

    @abstractmethod
    def upsert(self,ids: list[str], vectors: list[list[float]], payloads: list[dict]) -> None:
         """Insert or update vectors."""
         raise NotImplementedError
     
    @abstractmethod
    def search(self, query_vector: list[float], limit: int = 5) -> list[RetrievedChunk]:
        """Search for similar vectors."""
        raise NotImplementedError