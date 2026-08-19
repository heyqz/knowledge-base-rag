from rank_bm25 import BM25Okapi

from app.models.retrieved_chunk import RetrievedChunk

class BM25Retriever:
    def __init__(self, chunks: list[RetrievedChunk]):
        self.chunks = chunks

        tokenized_chunks = [
            self._tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:

        tokenized_query = self._tokenize(query)

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:
            if scores[index] <=0:
                continue
            chunk = self.chunks[index]

            results.append(
                RetrievedChunk(
                    text=chunk.text,
                    score=float(scores[index]),
                    page=chunk.page,
                    filename=chunk.filename,
                    document_id=chunk.document_id,
                )
            )
            if len(results) >= top_k:
                break

        return results

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()