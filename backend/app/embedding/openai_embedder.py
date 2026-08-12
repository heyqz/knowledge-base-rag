from openai import OpenAI
from app.core.config import settings

class OpenAIEmbedder:
    def __init__(self, model: str):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    def embed(self, texts: list[str]) -> list[list[float]]:

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [ item.embedding for item in response.data]