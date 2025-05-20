# main.py

import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.etl_modules.extract import extract_data
from src.etl_modules.fx import fetch_usd_to_clp
from src.etl_modules.enrich import enrich_report
from src.etl_modules.export import export_results
from src.etl_modules.google_sheets import export_to_google_sheets


def run_etl():
    # Step 1: Extract
    print("Extracting data...")
    df = extract_data()
    print("Data extracted:")
    print(df.head())

    # Step 2: Fetch FX rate
    print("Fetching USD to CLP rate...")
    rate = fetch_usd_to_clp()
    print(f"Exchange rate: {rate}")

    # Step 3: Enrich
    print("Enriching report...")
    df_enriched = enrich_report(df, rate)
    print("Enriched data:")
    print(df_enriched.head())

    # Step 4: Export CSV
    print("Exporting to CSV...")
    export_results(df_enriched)
    print("Exported to CSV.")

    # Step 5: Export to Google Sheets
    print("Exporting to Google Sheets...")
    export_to_google_sheets(df_enriched)
    print("Exported to Google Sheets.")

if __name__ == "__main__":
    run_etl()
