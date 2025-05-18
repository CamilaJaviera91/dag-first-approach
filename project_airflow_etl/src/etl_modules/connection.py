import os
import psycopg2
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        schema = os.getenv("DB_SCHEMA")
        if schema:
            cur.execute(f'SET search_path TO {schema};')
        logger.info("✅ Successfully connected to PostgreSQL.")
        return conn, cur
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        return None, None
