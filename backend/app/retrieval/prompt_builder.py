from app.models.retrieved_chunk import RetrievedChunk

class PromptBuilder:
    def build(self, question: str, chunks: list[RetrievedChunk]) -> str:
        
        context = "\n\n".join([chunk.text for chunk in chunks])
        
        
        prompt = f"""
        You are a helpful AI assistant.

        Answer the user's question using ONLY the provided context.

        If the answer cannot be found in the context, say "I don't know based on the provided documents."

        Context:

        {context}

        Question:

        {question}

        Answer:
        """
        
        return prompt.strip()