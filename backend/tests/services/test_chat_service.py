from app.services.chat_service import ChatService   

def test_chat_service():
    service = ChatService()

    answer = service.chat(
        "What is this document about?"
    )

    print(answer)

    assert len(answer.answer) > 0
    assert answer.retrieved_chunks > 0