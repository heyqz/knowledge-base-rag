from langchain_core.documents import Document
from app.ingestion.loader import pdf_loader


def test_load_pdf():
    docs = pdf_loader.load("test_data/Pelican Welcome Letter.pdf")

    assert len(docs) > 0
    assert isinstance(docs[0], Document)
    assert docs[0].page_content.strip() != ""


    print(docs[0].page_content[:300])
