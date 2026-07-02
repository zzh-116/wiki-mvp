from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Wiki MVP"
    app_version: str = "0.1.0"

    # Database (SQLite by default)
    database_url: str = "sqlite+aiosqlite:///./data/wiki.db"

    # Milvus
    milvus_host: str = "localhost"
    milvus_port: int = 19530

    # Data directory
    data_dir: Path = Path("data")
    upload_dir: Path = data_dir / "uploads"
    chunk_dir: Path = data_dir / "chunks"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
