import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    # TimescaleDB / Unified DB
    TSDB_HOST: str = os.getenv("TIMESCALE_DB_HOST", "localhost")
    TSDB_PORT: str = os.getenv("TIMESCALE_DB_PORT", "5432")
    TSDB_USER: str = os.getenv("TIMESCALE_DB_USER", "admin")
    TSDB_PASS: str = os.getenv("TIMESCALE_DB_PASS", "admin")
    TSDB_NAME: str = os.getenv("TIMESCALE_DB_NAME", "postgres")

    # Database Postgres
    POSTGRES_DB_HOST: str = os.getenv("POSTGRES_DB_HOST", "postgres")
    POSTGRES_DB_PORT: str = os.getenv("POSTGRES_DB_PORT", "5433")
    POSTGRES_DB_USER: str = os.getenv("POSTGRES_DB_USER", "admin")
    POSTGRES_DB_PASS: str = os.getenv("POSTGRES_DB_PASS", "admin")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME", "postgres")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
