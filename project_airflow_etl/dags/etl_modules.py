# etl_modules.py

import os
import requests
import pandas as pd
import psycopg2
import gspread
from dotenv import load_dotenv
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from airflow.utils.log.logging_mixin import LoggingMixin

# Airflow logger
logger = LoggingMixin().log

# Load environment variables (for local testing only)
load_dotenv()

# PostgreSQL connection
def connection():
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

# Step 1: Extract data
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
        return df.to_dict()  # Return serializable dict for XCom
    except psycopg2.Error as e:
        logger.error(f"❌ Error executing the query: {e}")
        return None
    finally:
        cur.close()
        conn.close()
        logger.info("🔒 PostgreSQL connection closed.")

# Step 2: Fetch exchange rate
def fetch_usd_to_clp(_=None):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        rate = data.get('rates', {}).get('CLP')
        if not rate:
            raise ValueError("CLP rate not found.")
        logger.info(f"💱 1 USD = {rate:.2f} CLP")
        return rate
    except Exception as e:
        logger.error(f"❌ Failed to fetch exchange rate: {e}")
        return None

# Step 3: Enrich report
def enrich_report(df_usd, clp_rate):
    if df_usd is not None and clp_rate:
        df = pd.DataFrame(df_usd)
        df["total"] = df["total"].astype(float)
        df["total_clp"] = round(df["total"] * float(clp_rate), 0)
        logger.info("📊 Enriched report sample:\n%s", df.head().to_string(index=False))
        return df.to_dict()
    logger.warning("⚠️ Report enrichment failed.")
    return None

# Step 4: Export to CSV
def export_results(df_dict):
    df = pd.DataFrame(df_dict)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/report.csv", index=False)
    logger.info("📤 Report exported to data/report.csv")

# Step 5: Export to Google Sheets
def export_to_google_sheets(df_dict, sheet_name="ReportSheet", spreadsheet_name="Sales Report"):
    df = pd.DataFrame(df_dict)
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

    if not credentials_path or not os.path.exists(credentials_path):
        logger.error("❌ Invalid or missing GOOGLE_CREDENTIALS_PATH")
        return

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

        set_with_dataframe(worksheet, df)
        logger.info(f"📤 Data exported to Google Sheets: {spreadsheet_name} -> {sheet_name}")
    except Exception as e:
        logger.error(f"❌ Failed to export to Google Sheets: {e}")

# 🔁 Optional: Local test DAG execution
if __name__ == "__main__":
    import networkx as nx

    tasks = {
        "extract": extract_data,
        "fetch_usd_to_clp": fetch_usd_to_clp,
        "enrich_report": enrich_report,
        "export": export_results,
        "googlesheets": export_to_google_sheets
    }

    dag = nx.DiGraph()
    dag.add_edges_from([
        ("extract", "fetch_usd_to_clp"),
        ("fetch_usd_to_clp", "enrich_report"),
        ("enrich_report", "export"),
        ("export", "googlesheets"),
    ])

    order = list(nx.topological_sort(dag))
    logger.info("🔁 Local test execution order: %s", order)

    results = {}

    for task in order:
        if task == "extract":
            results["extract"] = tasks[task]()
        elif task == "fetch_usd_to_clp":
            results["fetch_usd_to_clp"] = tasks[task]()
        elif task == "enrich_report":
            results["enrich_report"] = tasks[task](
                results["extract"], results["fetch_usd_to_clp"]
            )
        elif task in {"export", "googlesheets"}:
            tasks[task](results["enrich_report"])
