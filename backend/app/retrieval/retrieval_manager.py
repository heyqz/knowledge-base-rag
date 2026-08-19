from app.retrieval.bm25_index import BM25Index
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.hybrid_retriever import HybridRetriever
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

    def refresh(self) -> None:
        chunks = self.repository.get_all_chunks()

        self.bm25_index.build(chunks)

        print(
            f"BM25 index refreshed: {len(chunks)} chunks",
            flush=True,
        )

    def get_retriever(self) -> HybridRetriever:
        return self.hybrid_retriever
    
retrieval_manager = RetrievalManager()