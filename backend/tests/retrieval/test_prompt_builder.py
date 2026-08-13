from app.models.retrieved_chunk import RetrievedChunk
from app.retrieval.prompt_builder import PromptBuilder

def test_prompt_builder():
    builder = PromptBuilder()

    chunks = [
        RetrievedChunk(
            text="Employees receive 20 days of PTO.",
            score=0.95,
        ),
    ]
    
    prompt = builder.build(
        question="How many PTO days do employees receive?",
        chunks=chunks,
    )
    

    assert "20 days of PTO" in prompt
    assert "How many PTO" in prompt