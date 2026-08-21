from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"
    # API Keys
    OPENAI_API_KEY: str 
    EMBEDDING_MODEL: str
    CHAT_MODEL: str = "gpt-4.1-mini"
    
    #QDRANT settings
    QDRANT_URL: str
    QDRANT_COLLECTION: str = "knowledge-base"
    QDRANT_API_KEY: str
    EMBED_DIM: int =3072
    
    # Storage settings
    SQLITE_PATH: str = "storage/metadata.db"
    UPLOAD_DIR: str = "storage/uploads"
    
    # RAG settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5
    ENABLE_RERANKER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()