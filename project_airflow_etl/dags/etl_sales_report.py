from airflow.decorators import dag, task
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

@dag(dag_id="sales_etl_dag", default_args=default_args, schedule_interval="@daily", catchup=False)
def etl_pipeline():

    @task()
    def _extract():
        return extract_data()

    @task()
    def _fetch_rate():
        return fetch_usd_to_clp()

    @task()
    def _enrich(data, rate):
        df = enrich_report(pd.DataFrame(data), rate)
        return df.to_dict(orient='records')

    @task()
    def _export_csv(data):
        df = pd.DataFrame(data)
        export_results(df)

    @task()
    def _export_gsheet(data):
        df = pd.DataFrame(data)
        export_to_google_sheets(df)

    data = _extract()
    rate = _fetch_rate()
    enriched = _enrich(data, rate)
    _export_csv(enriched)
    _export_gsheet(enriched)

etl_pipeline()