from app.retrieval.dense_retriever import DenseRetriever


def test_retriever():
    retriever = DenseRetriever()

    results = retriever.retrieve(
        "What is this PDF about?"
    )

    assert len(results) > 0
    
    first = results[0]
    print(f"Text: {first.text}")
    print(f"Score: {first.score}")
    print(f"Page: {first.page}")
    print(f"Source: {first.source}")
    print(f"Document ID: {first.document_id}")
    assert first.text is not None
    assert first.score > 0
    
    