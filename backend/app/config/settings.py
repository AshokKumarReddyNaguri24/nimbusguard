import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Anomaly detection thresholds
    ANOMALY_THRESHOLD_CPU: float = float(os.getenv("ANOMALY_THRESHOLD_CPU", "90"))
    ANOMALY_THRESHOLD_MEMORY: float = float(os.getenv("ANOMALY_THRESHOLD_MEMORY", "90"))

    # TimescaleDB / Unified DB
    TSDB_HOST: str = os.getenv("TIMESCALE_HOST", os.getenv("TIMESCALE_DB_HOST", "localhost"))
    TSDB_PORT: str = os.getenv("TIMESCALE_PORT", os.getenv("TIMESCALE_DB_PORT", "5432"))
    TSDB_USER: str = os.getenv("TIMESCALE_USER", os.getenv("TIMESCALE_DB_USER", "admin"))
    TSDB_PASS: str = os.getenv("TIMESCALE_PASSWORD", os.getenv("TIMESCALE_DB_PASS", "admin"))
    TSDB_NAME: str = os.getenv("TIMESCALE_DB", os.getenv("TIMESCALE_DB_NAME", "postgres"))

    TIMESCALE_HOST: str = TSDB_HOST
    TIMESCALE_PORT: str = TSDB_PORT
    TIMESCALE_USER: str = TSDB_USER
    TIMESCALE_PASSWORD: str = TSDB_PASS
    TIMESCALE_DB: str = TSDB_NAME

    # Database Postgres
    POSTGRES_DB_HOST: str = os.getenv("POSTGRES_HOST", os.getenv("POSTGRES_DB_HOST", "postgres"))
    POSTGRES_DB_PORT: str = os.getenv("POSTGRES_PORT", os.getenv("POSTGRES_DB_PORT", "5433"))
    POSTGRES_DB_USER: str = os.getenv("POSTGRES_USER", os.getenv("POSTGRES_DB_USER", "admin"))
    POSTGRES_DB_PASS: str = os.getenv("POSTGRES_PASSWORD", os.getenv("POSTGRES_DB_PASS", "admin"))
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB", os.getenv("POSTGRES_DB_NAME", "postgres"))

    POSTGRES_HOST: str = POSTGRES_DB_HOST
    POSTGRES_PORT: str = POSTGRES_DB_PORT
    POSTGRES_USER: str = POSTGRES_DB_USER
    POSTGRES_PASSWORD: str = POSTGRES_DB_PASS
    POSTGRES_DB: str = POSTGRES_DB_NAME

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
