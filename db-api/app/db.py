import os
import psycopg2
import psycopg2.extras

# Grab env vars for DB config
DB_CONFIG = {
    "host":     os.getenv("POSTGRES_HOST", "postgres"),
    "port":     int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname":   os.getenv("POSTGRES_DB", "mydb"),
    "user":     os.getenv("POSTGRES_USER", "myuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "mypassword"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_table_if_not_exists():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS string_store (
                    id         SERIAL PRIMARY KEY,
                    key        TEXT UNIQUE NOT NULL,
                    value      TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        conn.commit()