import networkx as nx
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_batch
import os

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA")

# Configure PostgreSQL connection
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    print("✅ Successfully connected to PostgreSQL.")
except Exception as e:
    print("❌ Failed to connect to PostgreSQL:", e)
    exit()