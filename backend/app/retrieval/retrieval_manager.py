from app.retrieval.bm25_index import BM25Index
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker
from app.models.retrieved_chunk import RetrievedChunk
from app.storage.qdrant_repository import QdrantRepository


class RetrievalManager:

    def __init__(
        self,
        repository: QdrantRepository | None = None,
    ):
        self.repository = repository or QdrantRepository()

        self.bm25_index = BM25Index()

        self.dense_retriever = DenseRetriever(
            repository=self.repository,
        )

        self.bm25_retriever = BM25Retriever(
            index=self.bm25_index,
        )

        self.hybrid_retriever = HybridRetriever(
            dense_retriever=self.dense_retriever,
            bm25_retriever=self.bm25_retriever,
        )
        self.reranker = Reranker()

    def refresh(self) -> None:
        chunks = self.repository.get_all_chunks()

        self.bm25_index.build(chunks)

        print(
            f"BM25 index refreshed: {len(chunks)} chunks",
            flush=True,
        )

    def get_retriever(self) -> HybridRetriever:
        return self.hybrid_retriever
    
    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        candidate_k: int = 20,
    ) -> list[RetrievedChunk]:
        candidates = self.hybrid_retriever.retrieve(
            question,
            top_k=candidate_k,
            candidate_k=candidate_k,
        )

        return self.reranker.rerank(
            question,
            candidates,
            top_k=top_k,
        )
        
retrieval_manager = RetrievalManager()