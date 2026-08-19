from app.retrieval.retrieval_manager import retrieval_manager


question = "How often is potty training encouraged?"

results = retrieval_manager.retrieve(
    question,
    top_k=5,
    candidate_k=20,
)

for rank, chunk in enumerate(results, start=1):
    print()
    print(f"{rank}.")
    print("chunk_id:", chunk.chunk_id)
    print("score:", chunk.score)
    print("filename:", chunk.filename)
    print("page:", chunk.page)
    print(chunk.text[:300])