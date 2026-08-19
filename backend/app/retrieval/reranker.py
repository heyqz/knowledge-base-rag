from sentence_transformers import CrossEncoder

from app.models.retrieved_chunk import RetrievedChunk


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:

        if not chunks:
            return []

        pairs = [
            [query, chunk.text]
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        scored_chunks = []

        for chunk, score in zip(chunks, scores):
            scored_chunks.append(
                RetrievedChunk(
                    text=chunk.text,
                    score=float(score),
                    filename=chunk.filename,
                    page=chunk.page,
                    document_id=chunk.document_id,
                    chunk_id=chunk.chunk_id,
                )
            )

        scored_chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )

        return scored_chunks[:top_k]