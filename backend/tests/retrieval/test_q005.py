from app.retrieval.retrieval_manager import retrieval_manager


QUESTION = "How often is potty training encouraged?"

EXPECTED_CHUNK_ID = (
    "bf10e05b-bb57-4bda-a70e-f727a60eb3e5"
)


def print_results(name, results):
    print(f"\n===== {name} TOP 10 =====")

    for rank, chunk in enumerate(results, start=1):
        marker = "  <-- EXPECTED" if chunk.chunk_id == EXPECTED_CHUNK_ID else ""

        print(
            f"{rank}. "
            f"chunk_id={chunk.chunk_id} "
            f"score={chunk.score:.6f} "
            f"file={chunk.filename} "
            f"page={chunk.page}"
            f"{marker}"
        )

        print(f"   {chunk.text[:300]}")


def main():
    retrieval_manager.refresh()

    dense_results = (
        retrieval_manager.dense_retriever.retrieve(
            QUESTION,
            top_k=10,
        )
    )

    bm25_results = (
        retrieval_manager.bm25_retriever.retrieve(
            QUESTION,
            top_k=10,
        )
    )

    print(f"\nQuestion: {QUESTION}")
    print(f"Expected chunk: {EXPECTED_CHUNK_ID}")

    print_results("DENSE", dense_results)
    print_results("BM25", bm25_results)


if __name__ == "__main__":
    main()