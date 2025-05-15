# Import required libraries
import networkx as nx
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# Establish connection with PostgreSQL database
def connection():
    load_dotenv()  # Load environment variables from .env file

    # Retrieve database connection parameters
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SCHEMA = os.getenv("DB_SCHEMA")

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        # Set the default schema if provided
        if DB_SCHEMA:
            cur.execute(f'SET search_path TO {DB_SCHEMA};')
        print("✅ Successfully connected to PostgreSQL.")
        return conn, cur
    except Exception as e:
        print("❌ Failed to connect to PostgreSQL:", e)
        return None, None

# Step 1: Extract data from PostgreSQL and return it as a DataFrame
def extract_data(_=None):
    conn, cur = connection()
    if not conn:
        return None

    # Define SQL query with joins and aggregation
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
        # Execute query and convert result into a DataFrame
        cur.execute(query)
        records = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(records, columns=columns)
        return df
    except psycopg2.Error as e:
        print(f"❌ Error executing the query: {e}")
        return None
    finally:
        # Close DB connection
        cur.close()
        conn.close()
        print("🔒 Connection closed successfully.")

# Step 2: Fetch USD to CLP exchange rate from an external API
def fetch_usd_to_clp(_=None):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()

        # Extract CLP rate from API response
        if "rates" in data and "CLP" in data["rates"]:
            rate = data.get('rates', {}).get('CLP')
            print(f"💱 Exchange rate: 1 USD = {rate:.2f} CLP")
            return rate
        else:
            raise ValueError("CLP rate not found in API response.")
    except Exception as e:
        print("❌ Failed to retrieve exchange rate:", e)
        return None

# Step 3: Enrich the report with CLP values
def enrich_report(df_usd, clp_rate):
    if df_usd is not None and clp_rate:
        clp_rate = float(clp_rate)
        df_usd["total"] = df_usd["total"].astype(float)
        df_usd["total_clp"] = df_usd["total"] * clp_rate
        df_usd["total_clp"] = round(df_usd["total_clp"], 0)

        # Format float display for better readability
        pd.options.display.float_format = '{:,.2f}'.format

        print("📊 Enriched report:")
        print(df_usd.head())
        return df_usd
    else:
        print("⚠️ Report enrichment failed.")
        return None

# Step 4: Export results as CSV
def export_results(df):
    df.to_csv("data/report.csv", index=False)
    print("📤 Exported report to 'report.csv'")

# Step 5: Export the results to a Google Sheet
def export_to_google_sheets(df, sheet_name="ReportSheet", spreadsheet_name="Sales Report"):
    
    load_dotenv()
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

    # Validate credentials path
    if not credentials_path or not os.path.exists(credentials_path):
        print("❌ Google credentials path is invalid or not set.")
        return

    try:
        # Define scope for Google Sheets API access
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        # Authorize client
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        # Open or create spreadsheet
        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)

        # Open or create worksheet
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

        # Write DataFrame to Google Sheet
        set_with_dataframe(worksheet, df)
        print(f"📤 Data exported to Google Sheets: {spreadsheet_name} -> {sheet_name}")

    except Exception as e:
        print("❌ Failed to export to Google Sheets:", e)

# Define a DAG (Directed Acyclic Graph) to represent task dependencies
tasks = {
    "extract": extract_data,
    "fetch_usd_to_clp": fetch_usd_to_clp,
    "enrich_report": enrich_report,
    "export": export_results,
    "googlesheets": export_to_google_sheets
}

dag = nx.DiGraph()
dag.add_edges_from([
    ("extract", "fetch_usd_to_clp"),       # Step 1 -> Step 2
    ("fetch_usd_to_clp", "enrich_report"), # Step 2 -> Step 3
    ("enrich_report", "export"),           # Step 3 -> Step 4
    ("export", "googlesheets"),            # Step 4 -> Step 5
])

# Execute tasks based on topological sorting of the DAG
execution_order = list(nx.topological_sort(dag))
print("\n🔁 Execution order:", execution_order)

# Dictionary to store intermediate results
results = {}

# Loop through the tasks and execute them in order
for task in execution_order:
    if task == "extract":
        results["extract"] = tasks[task]()
    elif task == "fetch_usd_to_clp":
        results["fetch_usd_to_clp"] = tasks[task]()
    elif task == "enrich_report":
        results["enrich_report"] = tasks[task](results["extract"], results["fetch_usd_to_clp"])
    elif task == "export":
        tasks[task](results["enrich_report"])
    elif task == "googlesheets":
        tasks[task](results["enrich_report"])
    else:
        tasks[task]()  # Generic fallback for functions without arguments