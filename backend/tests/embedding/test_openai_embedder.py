from app.embedding.openai_embedder import OpenAIEmbedder
from app.core.config import settings

def test_embed():
    embedder = OpenAIEmbedder(settings.EMBEDDING_MODEL)
    vectors = embedder.embed(
        ["Hello world","OpenAI"]
    )

    assert len(vectors) == 2
    assert len(vectors[0]) > 100
