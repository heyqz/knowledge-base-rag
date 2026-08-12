from app.ingestion.loader import pdf_loader
from app.ingestion.chunkers.recursive import RecursiveChunker


def test_recursive_chunker():
    docs = pdf_loader.load("test_data/Pelican Welcome Letter.pdf")

    chunker = RecursiveChunker()

    chunks = chunker.split(docs)

    assert len(chunks) > 0

    assert len(chunks) >= len(docs)

    assert chunks[0].page_content.strip() != ""

    assert "page" in chunks[0].metadata

    print(f"Pages: {len(docs)}")

    print(f"Chunks: {len(chunks)}")