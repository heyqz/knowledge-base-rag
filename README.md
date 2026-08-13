✅ Backend Foundation
FastAPI
Project Structure
Config
Logging
✅ Document Management
Upload PDF
File Storage
SQLite Metadata
Document Repository
✅ Ingestion Pipeline
PDF Loader
Recursive Chunking
OpenAI Embeddings
Qdrant Indexing
✅ Retrieval
Vector Search
Retriever
Prompt Builder
✅ Chat
Chat Service
OpenAI Integration
Chat API


## 🏗️ System Architecture

```mermaid
flowchart TD

    FE["Frontend (React + Assistant UI)"]

    API["FastAPI Backend"]

    FE --> API

    API --> UploadAPI["Upload API"]
    API --> ChatAPI["Chat API"]

    UploadAPI --> DocumentService["Document Service"]
    ChatAPI --> ChatService["Chat Service"]

    DocumentService --> SQLite[(SQLite Metadata)]
    DocumentService --> Pipeline["Ingestion Pipeline"]

    Pipeline --> Loader["PDF Loader"]
    Pipeline --> Chunker["Recursive Chunker"]
    Pipeline --> Embedder["OpenAI Embedder"]
    Pipeline --> Qdrant[(Qdrant Vector DB)]

    ChatService --> Retriever["Retriever"]
    Retriever --> Embedder
    Retriever --> Qdrant

    ChatService --> PromptBuilder["Prompt Builder"]
    PromptBuilder --> OpenAI["OpenAI Chat API"]
```
## 📄 Document Ingestion Pipeline

```mermaid
flowchart LR

PDF["PDF File"]
Loader["PDF Loader"]
Chunker["Recursive Chunker"]
Embedder["OpenAI Embeddings"]
Qdrant[(Qdrant)]

PDF --> Loader
Loader --> Chunker
Chunker --> Embedder
Embedder --> Qdrant
```

## 🔍 Retrieval Flow

```mermaid
flowchart LR

Question["User Question"]
Embed["Query Embedding"]
Search["Vector Search"]
Chunks["Retrieved Chunks"]

Question --> Embed
Embed --> Search
Search --> Chunks
```

## 💬 RAG Chat Flow

```mermaid
flowchart LR

Question["User Question"]

Retriever["Retriever"]

Prompt["Prompt Builder"]

LLM["OpenAI Chat API"]

Answer["AI Answer"]

Question --> Retriever
Retriever --> Prompt
Prompt --> LLM
LLM --> Answer
```

## 📁 Project Structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── embedding/
│   ├── ingestion/
│   ├── models/
│   ├── retrieval/
│   ├── services/
│   └── storage/
│
├── tests/
└── pyproject.toml

frontend/
├── src/
├── public/
└── package.json
```


