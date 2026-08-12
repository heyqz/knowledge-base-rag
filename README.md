✅ Backend Foundation
FastAPI project structure
Configuration management (.env + Settings)
Logging
Health API

✅ Document Management
File upload
SQLite metadata storage
Document repository
Document service

✅ Ingestion Pipeline
PDF Loader
Recursive Character Chunking
OpenAI Embeddings
Qdrant Vector Store
End-to-End Pipeline
Integration Tests

                Upload API
                     │
                     ▼
              Save Document
                     │
                     ▼
            Ingestion Pipeline
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 PDF Loader   Recursive Chunker   OpenAI Embedder
                                         │
                                         ▼
                                   Qdrant Index