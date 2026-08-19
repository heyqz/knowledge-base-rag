from app.storage.qdrant_repository import QdrantRepository


def main():
    repository = QdrantRepository()

    chunks = repository.get_all_chunks()

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print("\n" + "=" * 80)
        print(f"Chunk #{i}")
        print(f"chunk_id: {chunk.chunk_id}")
        print(f"filename: {chunk.filename}")
        print(f"page: {chunk.page}")
        print("-" * 80)
        print(chunk.text)


if __name__ == "__main__":
    main()