import os
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def export_to_google_sheets(df_dict, sheet_name="ReportSheet", spreadsheet_name="Sales Report"):
    df = pd.DataFrame(df_dict)
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

    if not credentials_path or not os.path.exists(credentials_path):
        logger.error("❌ Invalid or missing GOOGLE_CREDENTIALS_PATH")
        return

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

        set_with_dataframe(worksheet, df)
        logger.info(f"📤 Data exported to Google Sheets: {spreadsheet_name} -> {sheet_name}")
    except Exception as e:
        logger.error(f"❌ Failed to export to Google Sheets: {e}")
