from openai import OpenAI
import json

from app.core.config import settings
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.storage.qdrant_repository import QdrantRepository
from app.retrieval.prompt_builder import PromptBuilder
from app.models.chat import ChatResponse, Source

class ChatService:
    def __init__(self, retriever: HybridRetriever | None = None, prompt_builder: PromptBuilder | None = None):
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.retriever = retriever or self._create_hybrid_retriever()
        self.prompt_builder = prompt_builder or PromptBuilder()
        
    def _create_hybrid_retriever(self) -> HybridRetriever:
        repository = QdrantRepository()
       
        dense_retriever = DenseRetriever(repository=repository)
        chunks = repository.get_all_chunks()
        bm25_retriever = BM25Retriever(chunks=chunks)
        
        return HybridRetriever(
            dense_retriever=dense_retriever,
            bm25_retriever=bm25_retriever
        )
        
        
    def chat(self, question: str) -> ChatResponse:
        # Retrieve relevant documents based on user input
        chunks = self.retriever.retrieve(question)

        # Build a prompt using the retrieved documents and user input
        prompt = self.prompt_builder.build(question, chunks)
        
        # add sources into chat response
        sources = [
            Source(
                filename=chunk.filename or "Unknown",
                page=chunk.page or 1,
                score=chunk.score,
            )
            for chunk in chunks     
        ]
            
        # Generate a response using the OpenAI API
        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            # max_tokens=150,
            # temperature=0.7,
        )

        return ChatResponse(
                answer=response.choices[0].message.content or "",
                sources= sources
        )
        
    def stream_chat(self, question: str):
        chunks = self.retriever.retrieve(question)
        
        prompt = self.prompt_builder.build(question, chunks)  
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
            messages=[{"role": "user", "content": prompt}],
            stream=True

        )
        for chunk in response:
            delta = chunk.choices[0].delta.content
            
            if delta:
                yield f"data: {json.dumps({'token': delta})}\n\n"
        
        yield f"data: {json.dumps({
            'done': True, 
            'sources':sources
            })}\n\n"