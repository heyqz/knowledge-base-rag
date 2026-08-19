from openai import OpenAI
import json

from app.core.config import settings
from app.retrieval.retrieval_manager import retrieval_manager
from app.retrieval.prompt_builder import PromptBuilder
from app.models.chat import ChatResponse, Source


class ChatService:

    def __init__(
        self,
        prompt_builder: PromptBuilder | None = None,
    ):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.retrieval_manager = retrieval_manager
        self.retrieval_manager.refresh()

        self.prompt_builder = (
            prompt_builder or PromptBuilder()
        )

    def chat(self, question: str) -> ChatResponse:
        chunks = self.retrieval_manager.retrieve(
            question,
            top_k=5,
            candidate_k=20,
        )

        prompt = self.prompt_builder.build(
            question,
            chunks,
        )

        sources = [
            Source(
                filename=chunk.filename or "Unknown",
                page=chunk.page or 1,
                score=chunk.score,
            )
            for chunk in chunks
        ]

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return ChatResponse(
            answer=response.choices[0].message.content or "",
            sources=sources,
        )

    def stream_chat(self, question: str):
        chunks = self.retrieval_manager.retrieve(
            question,
            top_k=5,
            candidate_k=20,
        )

        prompt = self.prompt_builder.build(
            question,
            chunks,
        )

        sources = [
            {
                "filename": chunk.filename or "Unknown",
                "page": chunk.page or 0,
                "score": chunk.score,
            }
            for chunk in chunks
        ]

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
        )

        for chunk in response:
            delta = chunk.choices[0].delta.content

            if delta:
                yield (
                    f"data: "
                    f"{json.dumps({'token': delta})}\n\n"
                )

        yield (
            f"data: "
            f"{json.dumps({
                'done': True,
                'sources': sources,
            })}\n\n"
        )