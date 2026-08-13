from dataclasses import dataclass

@dataclass
class RetrievedChunk:
    text: str
    score: float
    page: int | None = None
    source: str | None = None
    document_id: str | None = None
