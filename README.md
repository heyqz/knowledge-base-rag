# AI Knowledge Base

A production-style document question-answering application that allows users to upload PDF documents, ask natural-language questions, and receive answers grounded in the uploaded documents with source attribution.

The system combines dense vector retrieval, BM25 lexical retrieval, hybrid ranking, and cross-encoder reranking to improve retrieval quality before generating the final answer with an LLM.

---

## Features

- PDF document upload and management
- OCR support for scanned and image-based PDFs
- Asynchronous background document ingestion
- Document lifecycle tracking:
  `uploaded → processing → indexed / failed`
- Dense vector retrieval with Qdrant
- BM25 lexical retrieval
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- BGE cross-encoder reranking
- Streaming LLM responses
- Source attribution with document and page information
- Document deletion with Qdrant and BM25 cleanup
- Retrieval evaluation across multiple retrieval strategies
- Dockerized backend and Qdrant

---

## Architecture

```text
                           User
                            │
                            ▼
                    React Frontend
                            │
                            ▼
                     FastAPI Backend
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      Document Management            Chat Service
              │                           │
              ▼                           ▼
      Background Ingestion        Retrieval Manager
              │                           │
       ┌──────┴──────┐          ┌─────────┴─────────┐
       │             │          │                   │
       ▼             ▼          ▼                   ▼
   PDF Parsing      OCR      Dense Retrieval      BM25
       │                        │                   │
       └─────────────┬──────────┘                   │
                     ▼                              │
                  Qdrant                            │
                     │                              │
                     └───────────┬──────────────────┘
                                 ▼
                            RRF Fusion
                                 │
                                 ▼
                         Candidate Retrieval
                                 │
                                 ▼
                          BGE Reranker
                                 │
                                 ▼
                           Top-K Context
                                 │
                                 ▼
                         Prompt Builder
                                 │
                                 ▼
                              OpenAI
                                 │
                                 ▼
                       Streaming Answer
                                 │
                                 ▼
                            Sources

Document Ingestion

Documents are processed asynchronously after upload so the upload request does not need to wait for the entire indexing pipeline to complete.

Upload PDF
    │
    ▼
Save file + create document record
    │
    ▼
Status: uploaded
    │
    ▼
Background processing
    │
    ├── PDF parsing / OCR
    ├── Chunking
    ├── Embedding generation
    └── Qdrant indexing
    │
    ▼
Refresh BM25 index
    │
    ▼
Status: indexed


On failure:
    processing → failed

Document deletion removes the associated file, metadata, Qdrant chunks, and refreshes the BM25 index so deleted documents are no longer retrievable.

Retrieval Pipeline

The retrieval layer combines semantic and lexical retrieval.

Dense Retrieval

User questions are embedded using OpenAI embeddings and searched against Qdrant using vector similarity.

BM25 Retrieval

BM25 provides lexical matching for exact terms, names, numbers, and phrases that may not be ranked highly by semantic retrieval.

Hybrid Retrieval

Dense and BM25 results are combined using Reciprocal Rank Fusion (RRF).

Reranking

The top hybrid candidates are reranked with a BGE cross-encoder before the final context is passed to the LLM.

Question
   │
   ├── Dense Retrieval ──┐
   │                     │
   └── BM25 Retrieval ───┤
                         ▼
                      RRF Fusion
                         │
                   Candidate Set
                         │
                         ▼
                    BGE Reranker
                         │
                         ▼
                      Top 5
                         │
                         ▼
                        LLM
Retrieval Evaluation

A manually curated evaluation set is used to compare different retrieval strategies.

Current evaluation results:

Retriever	Recall@1	Recall@3	Recall@5
Dense	73.2%	92.7%	95.1%
BM25	43.9%	63.4%	85.4%
Hybrid (RRF)	63.4%	85.4%	90.2%
Hybrid + Reranker	73.2%	92.7%	100.0%

The evaluation showed that reranking improved the final ranking quality of hybrid retrieval, particularly when the relevant chunk was already present in the candidate set but ranked lower by RRF.

Note: the current metrics are calculated from evaluation questions whose ground-truth chunks were successfully resolved against the indexed corpus.

Tech Stack
Backend
Python
FastAPI
Pydantic Settings
Uvicorn
OpenAI API
Qdrant
BM25 (rank-bm25)
Sentence Transformers / BGE Reranker
SQLite
Frontend
React
TypeScript
Vite
TanStack Query
Tailwind CSS
shadcn/ui
Infrastructure
Docker
Docker Compose
Qdrant
Project Structure
knowledge-rag/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── ingestion/
│   │   ├── models/
│   │   ├── retrieval/
│   │   ├── services/
│   │   └── storage/
│   ├── evaluation/
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
└── README.md
Local Development
Prerequisites
Python
uv
Node.js
Docker
OpenAI API key
Backend
cd backend


uv sync

Create a local .env file based on .env.example and configure the required environment variables.

Start the backend:

uv run uvicorn app.main:app --reload

Backend:

http://localhost:8000

API documentation:

http://localhost:8000/docs
Frontend
cd frontend


npm install
npm run dev

Frontend:

http://localhost:5173
Docker

The backend and Qdrant can be started with:

docker compose up --build

The backend is available at:

http://localhost:8000

The application uses persistent local storage for document metadata and uploaded files during Docker-based development.

Environment Variables
Backend
OPENAI_API_KEY=
EMBEDDING_MODEL=
CHAT_MODEL=


QDRANT_URL=
QDRANT_COLLECTION=
EMBED_DIM=


SQLITE_PATH=storage/metadata.db
UPLOAD_DIR=storage/uploads


CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5


ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173
Frontend
VITE_API_BASE_URL=http://localhost:8000

Do not commit .env files or API credentials.

Current Limitations
SQLite and local file storage are intended for a lightweight deployment/demo environment.
BM25 is maintained in memory and refreshed after document ingestion and deletion.
The current deployment is designed for a relatively small number of documents and users.
Retrieval evaluation uses a manually curated dataset.
Future Improvements

Potential future work includes:

PostgreSQL for production metadata storage
Object storage such as S3 for uploaded documents
Dedicated background workers for large-scale ingestion
Authentication and per-user document isolation
Conversation history
Retrieval latency and observability metrics
Automated retrieval evaluation in CI/CD
License

This project is for educational and portfolio purposes.



### 你现在直接这样做


打开：


```text
knowledge-rag/README.md