import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def export_results(df_dict):
    df = pd.DataFrame(df_dict)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/report.csv", index=False)
    logger.info("📤 Report exported to ./data/report.csv")
