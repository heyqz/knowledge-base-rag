from collections import defaultdict

from app.models.retrieved_chunk import RetrievedChunk
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever


class HybridRetriever:

    def __init__(
        self,
        dense_retriever: DenseRetriever,
        bm25_retriever: BM25Retriever,
    ):
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 10,
    ) -> list[RetrievedChunk]:

        dense_results = self.dense_retriever.retrieve(
            query,
            top_k=candidate_k,
        )

        bm25_results = self.bm25_retriever.retrieve(
            query,
            top_k=candidate_k,
        )

        return self._rrf(
            dense_results,
            bm25_results,
            top_k=top_k,
        )

    def _rrf(
        self,
        dense_results: list[RetrievedChunk],
        bm25_results: list[RetrievedChunk],
        top_k: int,
        k: int = 60,
    ) -> list[RetrievedChunk]:

        scores = defaultdict(float)
        chunks = {}

        print("\n===== DENSE RESULTS =====")

        for rank, chunk in enumerate(dense_results, start=1):
            key = self._chunk_key(chunk)

            scores[key] += 1 / (k + rank)
            chunks[key] = chunk
            
            print(
                rank,
                chunk.filename,
                chunk.page,
                chunk.score,
            )

        print("\n===== BM25 RESULTS =====")
        for rank, chunk in enumerate(bm25_results, start=1):
            key = self._chunk_key(chunk)

            scores[key] += 1 / (k + rank)
            chunks[key] = chunk
            
            print(
                rank,
                chunk.filename,
                chunk.page,
                chunk.score,
            )

        ranked_keys = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        results = []

        for key in ranked_keys[:top_k]:
            chunk = chunks[key]

            results.append(
                RetrievedChunk(
                    text=chunk.text,
                    score=scores[key],
                    filename=chunk.filename,
                    page=chunk.page,
                    document_id=chunk.document_id,
                )
            )

        return results

    @staticmethod
    def _chunk_key(chunk: RetrievedChunk) -> str:
        return (
            f"{chunk.document_id}:"
            f"{chunk.page}:"
            f"{chunk.text}"
        )