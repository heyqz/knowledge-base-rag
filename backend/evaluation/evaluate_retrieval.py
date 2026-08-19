import json
from pathlib import Path

from app.retrieval.retrieval_manager import retrieval_manager


# ============================================================
# Configuration
# ============================================================

QUESTIONS_FILE = (
    Path(__file__).resolve().parent / "questions.json"
)

TOP_K_VALUES = [1, 3, 5]

HYBRID_TOP_K = 5
HYBRID_CANDIDATE_K = 20

RERANKER_TOP_K = 5
RERANKER_CANDIDATE_K = 20


# ============================================================
# Load Questions
# ============================================================

def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Ground Truth
# ============================================================

def chunk_matches_source(chunk, source):
    """
    Check whether a retrieved chunk matches a ground-truth source.
    """

    if chunk.filename != source["filename"]:
        return False

    if chunk.page != source["page"]:
        return False

    text_contains = source.get("text_contains", [])

    if not text_contains:
        return True

    chunk_text = chunk.text.lower()

    return all(
        phrase.lower() in chunk_text
        for phrase in text_contains
    )


def resolve_ground_truth(question, all_chunks):
    """
    Resolve ground-truth source definitions to actual chunk IDs.
    """

    relevant_chunk_ids = set()

    for source in question.get("relevant_sources", []):
        for chunk in all_chunks:

            if chunk_matches_source(chunk, source):
                relevant_chunk_ids.add(chunk.chunk_id)

    return relevant_chunk_ids


def resolve_all_ground_truth(questions):
    """
    Resolve all questions against the current indexed corpus.
    """

    all_chunks = retrieval_manager.repository.get_all_chunks()

    print("\n" + "=" * 60)
    print("Resolving Ground Truth")
    print("=" * 60)

    ground_truth = {}

    for question in questions:
        question_id = question["id"]

        relevant_chunk_ids = resolve_ground_truth(
            question,
            all_chunks,
        )

        ground_truth[question_id] = relevant_chunk_ids

        if relevant_chunk_ids:
            print(
                f"{question_id}: "
                f"{len(relevant_chunk_ids)} relevant chunk(s)"
            )
        else:
            print(
                f"WARNING: {question_id} "
                f"could not resolve any relevant chunks."
            )

    return ground_truth


# ============================================================
# Ranking Helpers
# ============================================================

def get_rank(results, relevant_chunk_ids):
    """
    Return the 1-based rank of the first relevant chunk.

    Returns None if no relevant chunk is found.
    """

    for rank, chunk in enumerate(results, start=1):
        if chunk.chunk_id in relevant_chunk_ids:
            return rank

    return None


def calculate_recall(results_by_question, ground_truth, k):
    """
    Recall@K for retrieval evaluation.

    A question counts as successful if at least one
    relevant chunk appears in the top K results.
    """

    evaluated_questions = 0
    hits = 0

    for question_id, results in results_by_question.items():

        relevant_chunk_ids = ground_truth.get(
            question_id,
            set(),
        )

        # Skip questions whose ground truth could not
        # be resolved against the current indexed corpus.
        if not relevant_chunk_ids:
            continue

        evaluated_questions += 1

        retrieved_ids = {
            chunk.chunk_id
            for chunk in results[:k]
        }

        if retrieved_ids & relevant_chunk_ids:
            hits += 1

    if evaluated_questions == 0:
        return 0.0

    return hits / evaluated_questions


def calculate_metrics(results_by_question, ground_truth):
    return {
        f"Recall@{k}": calculate_recall(
            results_by_question,
            ground_truth,
            k,
        )
        for k in TOP_K_VALUES
    }


# ============================================================
# Retriever Evaluation
# ============================================================

def evaluate_dense(questions):
    results = {}

    for question in questions:
        question_id = question["id"]

        retrieved = retrieval_manager.dense_retriever.retrieve(
            question["question"],
            top_k=5,
        )

        results[question_id] = retrieved

    return results


def evaluate_bm25(questions):
    results = {}

    for question in questions:
        question_id = question["id"]

        retrieved = retrieval_manager.bm25_retriever.retrieve(
            question["question"],
            top_k=5,
        )

        results[question_id] = retrieved

    return results


def evaluate_hybrid(questions):
    results = {}

    for question in questions:
        question_id = question["id"]

        retrieved = retrieval_manager.hybrid_retriever.retrieve(
            question["question"],
            top_k=HYBRID_TOP_K,
            candidate_k=HYBRID_CANDIDATE_K,
        )

        results[question_id] = retrieved

    return results


def evaluate_hybrid_reranker(questions):
    results = {}

    for question in questions:
        question_id = question["id"]

        retrieved = retrieval_manager.retrieve(
            question["question"],
            top_k=RERANKER_TOP_K,
            candidate_k=RERANKER_CANDIDATE_K,
        )

        results[question_id] = retrieved

    return results


# ============================================================
# Print Metrics
# ============================================================

def print_metrics(
    dense_metrics,
    bm25_metrics,
    hybrid_metrics,
    reranker_metrics,
):
    print("\n" + "=" * 60)
    print("Retrieval Evaluation")
    print("=" * 60)

    print(
        f"Questions: "
        f"{len(dense_metrics.get('_evaluated_questions', []))}"
    )

    print()

    print(
        f"{'Retriever':<22}"
        f"{'Recall@1':>10}"
        f"{'Recall@3':>10}"
        f"{'Recall@5':>10}"
    )

    print("-" * 60)

    rows = [
        ("Dense", dense_metrics),
        ("BM25", bm25_metrics),
        ("Hybrid", hybrid_metrics),
        ("Hybrid + Reranker", reranker_metrics),
    ]

    for name, metrics in rows:
        print(
            f"{name:<22}"
            f"{metrics['Recall@1'] * 100:>9.1f}%"
            f"{metrics['Recall@3'] * 100:>9.1f}%"
            f"{metrics['Recall@5'] * 100:>9.1f}%"
        )


# ============================================================
# Per-question Results
# ============================================================

def print_per_question(
    questions,
    ground_truth,
    dense_results,
    bm25_results,
    hybrid_results,
    reranker_results,
):
    print("\n" + "=" * 60)
    print("Per-question Results")
    print("=" * 60)

    for question in questions:
        question_id = question["id"]
        question_text = question["question"]

        relevant_chunk_ids = ground_truth.get(
            question_id,
            set(),
        )

        if not relevant_chunk_ids:
            continue

        dense_rank = get_rank(
            dense_results.get(question_id, []),
            relevant_chunk_ids,
        )

        bm25_rank = get_rank(
            bm25_results.get(question_id, []),
            relevant_chunk_ids,
        )

        hybrid_rank = get_rank(
            hybrid_results.get(question_id, []),
            relevant_chunk_ids,
        )

        reranker_rank = get_rank(
            reranker_results.get(question_id, []),
            relevant_chunk_ids,
        )

        print()
        print(f"{question_id}: {question_text}")

        print(
            f"  Dense:              "
            f"{dense_rank if dense_rank is not None else '✗'}"
        )

        print(
            f"  BM25:               "
            f"{bm25_rank if bm25_rank is not None else '✗'}"
        )

        print(
            f"  Hybrid:             "
            f"{hybrid_rank if hybrid_rank is not None else '✗'}"
        )

        print(
            f"  Hybrid + Reranker:  "
            f"{reranker_rank if reranker_rank is not None else '✗'}"
        )


# ============================================================
# Main
# ============================================================

def main():

    questions = load_questions()

    # --------------------------------------------------------
    # Refresh BM25
    # --------------------------------------------------------

    retrieval_manager.refresh()

    # --------------------------------------------------------
    # Resolve ground truth against current indexed chunks
    # --------------------------------------------------------

    ground_truth = resolve_all_ground_truth(
        questions
    )

    # --------------------------------------------------------
    # Run retrievers
    # --------------------------------------------------------

    dense_results = evaluate_dense(
        questions
    )

    bm25_results = evaluate_bm25(
        questions
    )

    hybrid_results = evaluate_hybrid(
        questions
    )

    reranker_results = evaluate_hybrid_reranker(
        questions
    )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    dense_metrics = calculate_metrics(
        dense_results,
        ground_truth,
    )

    bm25_metrics = calculate_metrics(
        bm25_results,
        ground_truth,
    )

    hybrid_metrics = calculate_metrics(
        hybrid_results,
        ground_truth,
    )

    reranker_metrics = calculate_metrics(
        reranker_results,
        ground_truth,
    )

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Retrieval Evaluation")
    print("=" * 60)

    evaluated_questions = [
        question_id
        for question_id, relevant_ids
        in ground_truth.items()
        if relevant_ids
    ]

    print(
        f"Questions: {len(evaluated_questions)}"
    )

    print()

    print(
        f"{'Retriever':<22}"
        f"{'Recall@1':>10}"
        f"{'Recall@3':>10}"
        f"{'Recall@5':>10}"
    )

    print("-" * 60)

    rows = [
        ("Dense", dense_metrics),
        ("BM25", bm25_metrics),
        ("Hybrid", hybrid_metrics),
        (
            "Hybrid + Reranker",
            reranker_metrics,
        ),
    ]

    for name, metrics in rows:
        print(
            f"{name:<22}"
            f"{metrics['Recall@1'] * 100:>9.1f}%"
            f"{metrics['Recall@3'] * 100:>9.1f}%"
            f"{metrics['Recall@5'] * 100:>9.1f}%"
        )

    # --------------------------------------------------------
    # Per-question results
    # --------------------------------------------------------

    print_per_question(
        questions,
        ground_truth,
        dense_results,
        bm25_results,
        hybrid_results,
        reranker_results,
    )



if __name__ == "__main__":
    main()