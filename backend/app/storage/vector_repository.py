from abc import ABC, abstractmethod


class VectorRepository(ABC):

    @abstractmethod
    def upsert(self,ids: list[str], vectors: list[list[float]], payloads: list[dict]) -> None:
         """Insert or update vectors."""
         raise NotImplementedError