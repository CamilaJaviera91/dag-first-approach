from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etl_modules.extract import extract_data
from src.etl_modules.usd_to_clp import fetch_usd_to_clp
from src.etl_modules.export import export_results
from src.etl_modules.google_sheets import export_to_google_sheets
from src.etl_modules.generate_sales_plot import generate_sales_by_year_plot

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
    
    @task()
    def generate_plot(data):
        import logging
        output_path = '/home/camilajaviera/Documentos/github/dag-first-approach/project_airflow_etl/data/sales.png'
        
        logging.info(f"Generating plot at: {output_path}")
        logging.info(f"Data sample (first 3 rows): {data[:3]}")
        
        from pathlib import Path
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            generate_sales_by_year_plot(data, output_path)
            logging.info("Plot generated successfully")
        except Exception as e:
            logging.error(f"Failed to generate plot: {e}")
            raise

    @task()
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
    generate_plot(enriched_data)
    export(enriched_data)
    export_gsheet(enriched_data)

# DAG instance
sales_etl_pipeline()