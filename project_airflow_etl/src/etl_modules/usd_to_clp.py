import requests
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def fetch_usd_to_clp(_=None):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        rate = data.get('rates', {}).get('CLP')
        if not rate:
            raise ValueError("CLP rate not found.")
        logger.info(f"💱 1 USD = {rate:.2f} CLP")
        return rate
    except Exception as e:
        logger.error(f"❌ Failed to fetch exchange rate: {e}")
        return None
