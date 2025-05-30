import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def export_results(df):
    # Crear carpeta 'data' si no existe
    output_dir = os.path.join(os.getcwd(), "./data") 
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "report.csv")
    df.to_csv(output_file, index=False)
    logger.info(f"📤 Report exported to {output_file}")