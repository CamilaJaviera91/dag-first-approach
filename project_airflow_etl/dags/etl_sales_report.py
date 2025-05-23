from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime
import pandas as pd

from src.etl_modules.extract import extract_data
from src.etl_modules.fx import fetch_usd_to_clp
from src.etl_modules.enrich import enrich_report
from src.etl_modules.export import export_results
from src.etl_modules.google_sheets import export_to_google_sheets

default_args = {
    'owner': 'camila',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

@dag(
    dag_id='sales_etl_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description="Sales ETL: PostgreSQL -> Enrichment -> CSV and Google Sheets"
)
def sales_etl_pipeline():

    @task()
    def extract():
        return extract_data()

    @task()
    def fetch_fx_rate():
        return fetch_usd_to_clp()

    @task()
    def enrich(data, rate):
        df = pd.DataFrame(data)
        df["total"] = df["total"].astype(float)
        df["total_clp"] = round(df["total"] * float(rate), 0)
        return df.to_dict(orient='records')

    @task()
    def export_csv(data):
        df = pd.DataFrame(data)
        export_results(df)

    @task()
    def export_gsheet(data):
        df = pd.DataFrame(data)
        export_to_google_sheets(df)

    # Task pipeline
    raw_data = extract()
    rate = fetch_fx_rate()
    enriched_data = enrich(raw_data, rate)
    export_csv(enriched_data)
    export_gsheet(enriched_data)

# DAG instance
sales_etl_pipeline()