import networkx as nx
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
import requests

# Connect to PostgreSQL
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

# 1. Execute SQL query and return results as a DataFrame
def extract_data(_=None):
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
        return df  # 🔁 No print here
    except psycopg2.Error as e:
        print(f"❌ Error executing the query: {e}")
        return None
    finally:
        cur.close()
        conn.close()
        print("🔒 Connection closed successfully.")

# 2. Fetch current USD to CLP exchange rate
def fetch_usd_to_clp(_=None):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()

        if "rates" in data and "CLP" in data["rates"]:
            rate = data.get('rates', {}).get('CLP')
            print(f"💱 Exchange rate: 1 USD = {rate:.2f} CLP")
            return rate
        else:
            raise ValueError("CLP rate not found in API response.")
    except Exception as e:
        print("❌ Failed to retrieve exchange rate:", e)
        return None

# 3. Enrich report with CLP values
def enrich_report(df_usd, clp_rate):
    if df_usd is not None and clp_rate:
        clp_rate = float(clp_rate)
        df_usd["total"] = df_usd["total"].astype(float)
        df_usd["total_clp"] = df_usd["total"] * clp_rate
        df_usd["total_clp"] = round(df_usd["total_clp"], 0)

        # Set float display format
        pd.options.display.float_format = '{:,.2f}'.format

        print("📊 Enriched report:")
        print(df_usd.head())
        return df_usd
    else:
        print("⚠️ Report enrichment failed.")
        return None

# 4. Export results
def export_results(df):
    df.to_csv("report.csv", index=False)
    print("📤 Exported report to 'report.csv'")

## Simulated DAG with networkx
tasks = {
    "extract": extract_data,
    "fetch_usd_to_clp": fetch_usd_to_clp,
    "enrich_report": enrich_report,
    "export": export_results
}

dag = nx.DiGraph()
dag.add_edges_from([
    ("extract", "fetch_usd_to_clp"),
    ("fetch_usd_to_clp", "enrich_report"),
    ("enrich_report", "export"),
])

# Execute the DAG in topological order
execution_order = list(nx.topological_sort(dag))
print("\n🔁 Execution order:", execution_order)

results = {}

for task in execution_order:
    if task == "extract":
        results["extract"] = tasks[task]()  # Save DataFrame
    elif task == "fetch_usd_to_clp":
        results["fetch_usd_to_clp"] = tasks[task]()  # Save rate
    elif task == "enrich_report":
        results["enrich_report"] = tasks[task](results["extract"], results["fetch_usd_to_clp"])
    elif task == "export":
        tasks[task](results["enrich_report"])
    else:
        tasks[task]()  # e.g., "connect", which needs no arguments
