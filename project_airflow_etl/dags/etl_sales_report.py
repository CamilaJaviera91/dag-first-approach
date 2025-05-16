from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

from etl_modules import extract_data, fetch_usd_to_clp, enrich_report, export_results, export_to_google_sheets

default_args = {
    'owner': 'camila',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id='sales_etl_dag',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    task_fetch = PythonOperator(
        task_id='fetch_usd_to_clp',
        python_callable=fetch_usd_to_clp
    )

    def _enrich_report(**context):
        df_usd = context['ti'].xcom_pull(task_ids='extract_data')
        rate = context['ti'].xcom_pull(task_ids='fetch_usd_to_clp')
        df = enrich_report(pd.DataFrame(df_usd), rate)
        context['ti'].xcom_push(key='enriched', value=df.to_dict())
        return df

    task_enrich = PythonOperator(
        task_id='enrich_report',
        python_callable=_enrich_report
    )

    def _export(**context):
        df_dict = context['ti'].xcom_pull(task_ids='enrich_report', key='enriched')
        df = pd.DataFrame(df_dict)
        export_results(df)

    task_export_csv = PythonOperator(
        task_id='export_csv',
        python_callable=_export
    )

    def _export_gsheet(**context):
        df_dict = context['ti'].xcom_pull(task_ids='enrich_report', key='enriched')
        df = pd.DataFrame(df_dict)
        export_to_google_sheets(df)

    task_export_gsheet = PythonOperator(
        task_id='export_gsheet',
        python_callable=_export_gsheet
    )

    task_extract >> task_fetch >> task_enrich >> task_export_csv >> task_export_gsheet
