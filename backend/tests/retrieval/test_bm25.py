from app.storage.qdrant_repository import QdrantRepository
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.bm25_index import BM25Index

repository = QdrantRepository()

chunks = repository.get_all_chunks()

print("Total chunks:", len(chunks))
index = BM25Index()
index.build(chunks)
bm25_retriever = BM25Retriever(index)

results = bm25_retriever.retrieve(
    "What time is lunch?",
    top_k=5,
)

for result in results:
    print("\n----")
    print("score:", result.score)
    print("filename:", result.filename)
    print("page:", result.page)
    print(result.text[:500])