from rank_bm25 import BM25Okapi

from app.models.retrieved_chunk import RetrievedChunk
from app.retrieval.bm25_index import BM25Index

class BM25Retriever:
    def __init__(self, index: BM25Index):
        self.index = index

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        if not self.index.is_ready():
            return []

        tokenized_query = self._tokenize(query)

        scores = self.index.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:
            score = scores[index]
            if score <=0:
                continue
            
            chunk = self.index.chunks[index]

            results.append(
                RetrievedChunk(
                    text=chunk.text,
                    score=float(score),
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