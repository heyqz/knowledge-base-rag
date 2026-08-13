from openai import OpenAI

from app.core.config import settings
from app.retrieval.retriever import Retriever
from app.retrieval.prompt_builder import PromptBuilder
from app.models.chat import ChatResponse

class ChatService:
    def __init__(self, retriever: Retriever | None = None, prompt_builder: PromptBuilder | None = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.retriever = retriever or Retriever()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def chat(self, question: str) -> ChatResponse:
        # Retrieve relevant documents based on user input
        chunks = self.retriever.retrieve(question)

        # Build a prompt using the retrieved documents and user input
        prompt = self.prompt_builder.build(question, chunks)

        # Generate a response using the OpenAI API
        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            # max_tokens=150,
            # temperature=0.7,
        )

        return ChatResponse(
                answer=response.choices[0].message.content or "",
                retrieved_chunks=len(chunks),
    )