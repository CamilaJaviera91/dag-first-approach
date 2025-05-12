import networkx as nx
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_batch
import os
import pandas as pd

def connection():

    load_dotenv()
    
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SCHEMA = os.getenv("DB_SCHEMA")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        if DB_SCHEMA:
            cur.execute(f'SET search_path TO {DB_SCHEMA};')
        print("✅ Successfully connected to PostgreSQL.")
        return conn, cur
    except Exception as e:
        print("❌ Failed to connect to PostgreSQL:", e)
        return None, None

def extract_data(_=None) -> pd.DataFrame | None:
    # Ejecuta una consulta y devuelve los resultados como DataFrame
    conn, cur = connection()
    if not conn:
        return None

    query = '''
        WITH resume AS (
            SELECT 
                o.order_date AS date,
                CONCAT(s.city, '-', s.store_id) AS store,
                p."name",
                p.category,
                p.price,
                o.quantity,
                (p.price * o.quantity) AS total,
                sm."name" AS salesman,
                c."name" AS client
            FROM test.orders o 
            JOIN test.store s ON o.store_id = s.store_id 
            JOIN test.product p ON o.product_id = p.product_id
            JOIN test.salesman sm ON o.salesman_id = sm.salesman_id
            JOIN test.client c ON o.client_id = c.client_id
            ORDER BY o.order_date DESC
        )
        SELECT 
            EXTRACT(YEAR FROM DATE(date)) AS year,
            store,
            SUM(total) AS total
        FROM resume
        GROUP BY year, store
        ORDER BY year, total ASC
    '''

    try:
        cur.execute(query)
        records = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(records, columns=columns)
        print(df)
        return df
    except psycopg2.Error as e:
        print(f"❌ Error executing the query: {e}")
        return None
    finally:
        cur.close()
        conn.close()
        print("🔒 Connection closed successfully.")

# DAG definition with NetworkX
tasks = {
    "connect": connection,
    "extract": extract_data
}

dag = nx.DiGraph()
dag.add_edges_from([
    ("connect", "extract"),
])

execution_order = list(nx.topological_sort(dag))
print("📋 Execution order:", execution_order)

for task in execution_order:
    tasks[task]()
