from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

class PDFLoader:

    def load(self, pdf_path: str | Path):
        loader = PyPDFLoader(pdf_path)
        return loader.load()


pdf_loader = PDFLoader()