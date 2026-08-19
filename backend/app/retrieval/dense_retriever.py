from app.embedding.openai_embedder import OpenAIEmbedder
from app.storage.vector_repository import VectorRepository
from app.storage.qdrant_repository import QdrantRepository
from app.core.config import settings
from app.models.retrieved_chunk import RetrievedChunk

class DenseRetriever:

    def __init__(self, embedder: OpenAIEmbedder | None =None, repository: VectorRepository | None =None):
        self.embedder = embedder or OpenAIEmbedder(settings.EMBEDDING_MODEL)
        self.repository = repository or QdrantRepository()

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        # query embedding
        vector = self.embedder.embed([question])[0] # embed() returns a list of embeddings, we take the first one since we only have one question

        return self.repository.search(
            query_vector=vector,
            limit=top_k,
        )
       
      