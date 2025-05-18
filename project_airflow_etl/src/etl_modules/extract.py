import pandas as pd
from .connection import get_connection
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def extract_data(_=None):
    conn, cur = get_connection()
    if not conn:
        return None

    query = """ -- tu query aquí (la misma que ya usas) """
    try:
        cur.execute(query)
        records = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(records, columns=columns)
        return df.to_dict()
    except Exception as e:
        logger.error(f"❌ Error executing query: {e}")
        return None
    finally:
        cur.close()
        conn.close()
        logger.info("🔒 PostgreSQL connection closed.")
