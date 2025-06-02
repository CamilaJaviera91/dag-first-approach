import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etl_modules.usd_to_clp import fetch_usd_to_clp
from src.etl_modules.extract import extract_data
import pandas as pd

def enrich(data, rate):
    df = pd.DataFrame(data)
    df["total"] = df["total"].astype(float)
    df["total_clp"] = round(df["total"] * float(rate), 0)
    return df

def test_enrich_adds_total_clp():
    data = extract_data()
    rate = fetch_usd_to_clp()
    df = enrich(data, rate)
    
    assert "total_clp" in df.columns
    assert not df["total_clp"].isnull().any()
