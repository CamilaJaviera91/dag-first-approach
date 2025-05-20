import os
import psycopg2
from airflow.utils.log.logging_mixin import LoggingMixin
from dotenv import load_dotenv
load_dotenv() 

logger = LoggingMixin().log

def get_connection():
    try:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        schema = os.getenv("DB_SCHEMA")

        logger.info(f"Trying to connect to DB at {host}:{port} with user {user} and db {dbname}")

        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        cur = conn.cursor()
        if schema:
            cur.execute(f'SET search_path TO {schema};')
        logger.info("✅ Successfully connected to PostgreSQL.")
        return conn, cur
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        return None, None