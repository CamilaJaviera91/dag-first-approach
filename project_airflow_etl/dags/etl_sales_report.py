from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etl_modules.extract import extract_data
from project_airflow_etl.src.etl_modules.usd_to_clp import fetch_usd_to_clp
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
    schedule='@daily',
    catchup=False,
    description="Sales ETL: PostgreSQL -> Enrichment -> CSV and Google Sheets"
)

def sales_etl_pipeline():

    @task()
    def extract() -> list[dict]:
        return extract_data()

    @task()
    def fetch_fx_rate() -> float:
        return fetch_usd_to_clp()

    @task()
    def enrich(data, rate):
        df = pd.DataFrame(data)
        df["total"] = df["total"].astype(float)
        df["total_clp"] = round(df["total"] * float(rate), 0)
        return df.to_dict(orient='records')

    @task
    def export(df_dict):
        df = pd.DataFrame(df_dict)
        export_results(df)

    @task()
    def export_gsheet(data):
        df = pd.DataFrame(data)
        export_to_google_sheets(df)

    # Task pipeline
    raw_data = extract()
    rate = fetch_fx_rate()
    enriched_data = enrich(raw_data, rate)
    export(enriched_data)
    export_gsheet(enriched_data)

# DAG instance
sales_etl_pipeline()