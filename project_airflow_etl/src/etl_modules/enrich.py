import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def enrich_report(df_usd, clp_rate):
    if isinstance(df_usd, list) and df_usd and "total" in df_usd[0]:
        df = pd.DataFrame(df_usd)
        df["total"] = df["total"].astype(float)
        df["total_clp"] = round(df["total"] * float(clp_rate), 0)
        logger.info("📊 Enriched report sample:\n%s", df.head().to_string(index=False))
        return df.to_dict(orient='records')  
    logger.warning("⚠️ Report enrichment failed.")
    return None

