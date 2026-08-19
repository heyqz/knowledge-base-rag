from app.storage.qdrant_repository import QdrantRepository
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.hybrid_retriever import HybridRetriever


repository = QdrantRepository()

dense_retriever = DenseRetriever(
    repository=repository,
)

chunks = repository.get_all_chunks()

bm25_retriever = BM25Retriever(chunks)

hybrid_retriever = HybridRetriever(
    dense_retriever=dense_retriever,
    bm25_retriever=bm25_retriever,
)

results = hybrid_retriever.retrieve(
    "What time is lunch?",
    top_k=5,
    candidate_k=10,
)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("RRF score:", result.score)
    print("filename:", result.filename)
    print("page:", result.page)
    print(result.text[:500])