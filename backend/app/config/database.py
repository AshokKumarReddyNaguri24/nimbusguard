from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# --- 1. INVENTORY CONNECTION (PostgreSQL) ---
SQLALCHEMY_DATABASE_URL_INVENTORY = (
    f"postgresql://{settings.POSTGRES_DB_USER}:{settings.POSTGRES_DB_PASS}"
    f"@{settings.POSTGRES_DB_HOST}:{settings.POSTGRES_DB_PORT}/{settings.POSTGRES_DB_NAME}"
)

engine_inventory = create_engine(SQLALCHEMY_DATABASE_URL_INVENTORY)
SessionLocalInventory = sessionmaker(autocommit=False, autoflush=False, bind=engine_inventory)

Base = declarative_base() # Base for ORM models (Inventory)

def get_db_inventory():
    db = SessionLocalInventory()
    try:
        yield db
    finally:
        db.close()

# --- 2. METRICS CONNECTION (TimescaleDB) ---
SQLALCHEMY_DATABASE_URL_METRICS = (
    f"postgresql://{settings.TSDB_USER}:{settings.TSDB_PASS}"
    f"@{settings.TSDB_HOST}:{settings.TSDB_PORT}/{settings.TSDB_NAME}"
)

engine_metrics = create_engine(SQLALCHEMY_DATABASE_URL_METRICS)
SessionLocalMetrics = sessionmaker(autocommit=False, autoflush=False, bind=engine_metrics)

def get_db_metrics():
    db = SessionLocalMetrics()
    try:
        yield db
    finally:
        db.close()

# Backward compatibility & helpers
SessionLocal = SessionLocalInventory
engine = engine_inventory
