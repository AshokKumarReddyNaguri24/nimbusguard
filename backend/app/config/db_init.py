import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import text
from app.config import database
from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger(__name__)


def _check_engine(engine, label: str) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        logger.error("Environment validation failed: %s", label, exc_info=True)
        raise RuntimeError(f"{label} unavailable")


def validate_environment():
    logger.info("Validating environment connectivity...")
    _check_engine(database.engine_inventory, "inventory_db")
    _check_engine(database.engine_metrics, "metrics_db")
    logger.info("Environment validation OK")


def init_inventory():
    """Validates connectivity to Postgres and ensures the devices table exists."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_DB_HOST,
            port=settings.POSTGRES_DB_PORT,
            user=settings.POSTGRES_DB_USER,
            password=settings.POSTGRES_DB_PASS,
            dbname=settings.POSTGRES_DB_NAME
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        logger.info("Checking Inventory DB (Postgres)...")

        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'devices');")
        if not cursor.fetchone()[0]:
            logger.info("Creating 'devices' table...")
            cursor.execute("""
                CREATE TABLE devices (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    ip_address VARCHAR(255),
                    device_type VARCHAR(50),
                    location VARCHAR(255)
                );
            """)
        else:
            logger.info("'devices' table already exists.")

        cursor.close()
        conn.close()
    except Exception:
        logger.error("Inventory DB init failed", exc_info=True)


def init_metrics():
    """Validates connectivity to TimescaleDB and ensures metrics hypertable exists."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.TSDB_HOST,
            port=settings.TSDB_PORT,
            user=settings.TSDB_USER,
            password=settings.TSDB_PASS,
            dbname=settings.TSDB_NAME
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        logger.info("Checking Metrics DB (TimescaleDB)...")

        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'metrics');")
        if not cursor.fetchone()[0]:
            logger.info("Creating 'metrics' table...")
            cursor.execute("""
                CREATE TABLE metrics (
                    id SERIAL PRIMARY KEY,
                    time TIMESTAMPTZ NOT NULL,
                    device_id INTEGER,
                    metric_name TEXT,
                    value DOUBLE PRECISION NOT NULL
                );
            """)
        else:
            logger.info("'metrics' table already exists.")

        cursor.execute("SELECT hypertable_name FROM timescaledb_information.hypertables WHERE hypertable_name = 'metrics';")
        if not cursor.fetchone():
            logger.info("Converting 'metrics' into a hypertable...")
            try:
                cursor.execute("SELECT create_hypertable('metrics', 'time', if_not_exists => TRUE);")
                logger.info("Converted 'metrics' into a hypertable.")
            except Exception:
                logger.warning("Hypertable conversion skipped or failed", exc_info=True)
        else:
            logger.info("'metrics' is already a hypertable.")

        cursor.close()
        conn.close()
    except Exception:
        logger.error("Metrics DB init failed", exc_info=True)


def run_migrations():
    logger.info("Starting migrations...")
    init_inventory()
    init_metrics()
    logger.info("Database init complete.")
