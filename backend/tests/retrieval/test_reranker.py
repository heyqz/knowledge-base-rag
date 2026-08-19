from app.retrieval.reranker import Reranker
from app.retrieval.retrieval_manager import retrieval_manager


def main():

    question = "How often is potty training encouraged?"

    # First get candidates from Hybrid
    candidates = retrieval_manager.hybrid_retriever.retrieve(
        question,
        top_k=20,
        candidate_k=20,
    )

    print("\n" + "=" * 60)
    print("HYBRID RESULTS")
    print("=" * 60)

    for rank, chunk in enumerate(candidates, start=1):
        print(
            f"\n{rank}. "
            f"chunk_id={chunk.chunk_id}"
        )
        print(
            f"score={chunk.score}"
        )
        print(
            f"{chunk.filename} "
            f"page={chunk.page}"
        )
        print(chunk.text[:300])

    # Rerank
    reranker = Reranker()

    reranked = reranker.rerank(
        question,
        candidates,
        top_k=5,
    )

    print("\n" + "=" * 60)
    print("RERANKED RESULTS")
    print("=" * 60)

    for rank, chunk in enumerate(reranked, start=1):
        print(
            f"\n{rank}. "
            f"chunk_id={chunk.chunk_id}"
        )
        print(
            f"reranker_score={chunk.score}"
        )
        print(
            f"{chunk.filename} "
            f"page={chunk.page}"
        )
        print(chunk.text[:300])


if __name__ == "__main__":
    main()