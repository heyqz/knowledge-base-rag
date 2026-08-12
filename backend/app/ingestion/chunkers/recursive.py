from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.core.config import settings
from app.ingestion.chunkers.base import BaseChunker


class RecursiveChunker(BaseChunker):
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

    def split(self,documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)