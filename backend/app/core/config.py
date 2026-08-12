from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str 
    EMBEDDING_MODEL: str
    CHAT_MODEL: str = "gpt-4.1-mini"
    
    #QDRANT settings
    QDRANT_URL: str
    QDRANT_COLLECTION: str
    EMBED_DIM: int
    
    # Storage settings
    SQLITE_PATH: str = "storage/metadata.db"
    UPLOAD_DIR: str = "storage/uploads"
    
    # RAG settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()