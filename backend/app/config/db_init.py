import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.config.settings import settings

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

        print("Checking Inventory DB (Postgres)...")
        # Check/Create Device Table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'devices');")
        if not cursor.fetchone()[0]:
            print("Creating 'devices' table...")
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
            print("'devices' table already exists.")

        # Check/Create Alerts Table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alerts');")
        if not cursor.fetchone()[0]:
            print("Creating 'alerts' table...")
            cursor.execute("""
                CREATE TABLE alerts (
                    id SERIAL PRIMARY KEY,
                    device_id INTEGER,
                    metric_type VARCHAR(50),
                    value DOUBLE PRECISION,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    description TEXT,
                    resolved BOOLEAN DEFAULT FALSE
                );
            """)
        else:
            print("'alerts' table already exists.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Inventory DB init failed: {e}")

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

        print("Checking Metrics DB (TimescaleDB)...")
        
        # Check/Create Metrics Table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'metrics');")
        if not cursor.fetchone()[0]:
            print("Creating 'metrics' table...")
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
            print("'metrics' table already exists.")

        # Convert to Hypertable
        cursor.execute("SELECT hypertable_name FROM timescaledb_information.hypertables WHERE hypertable_name = 'metrics';")
        if not cursor.fetchone():
            print("Converting 'metrics' into a hypertable...")
            try:
                # Note: 'time' column used here to match table schema above
                cursor.execute("SELECT create_hypertable('metrics', 'time', if_not_exists => TRUE);")
                print("Converted 'metrics' into a hypertable.")
            except Exception as e:
                print(f"Hypertable conversion skipped or failed: {e}")
        else:
            print("'metrics' is already a hypertable.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Metrics DB init failed: {e}")

def run_migrations():
    print("Starting migrations...")
    init_inventory()
    init_metrics()
    print("Database init complete.\n")
