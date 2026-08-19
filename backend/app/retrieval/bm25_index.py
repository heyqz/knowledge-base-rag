from rank_bm25 import BM25Okapi

from app.models.retrieved_chunk import RetrievedChunk


class BM25Index:

    def __init__(self):
        self.chunks: list[RetrievedChunk] = []
        self.bm25: BM25Okapi | None = None

    def build(self, chunks: list[RetrievedChunk]) -> None:
        self.chunks = chunks

        tokenized_chunks = [
            self._tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def is_ready(self) -> bool:
        return self.bm25 is not None

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()