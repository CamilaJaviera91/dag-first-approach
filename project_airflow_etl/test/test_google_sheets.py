# pyright: reportMissingImports=false

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pandas as pd
from unittest.mock import patch, MagicMock
from etl_modules.google_sheets import export_to_google_sheets

@patch("etl_modules.google_sheets.set_with_dataframe")
@patch("etl_modules.google_sheets.gspread")
@patch("etl_modules.google_sheets.ServiceAccountCredentials")
@patch("etl_modules.google_sheets.os.path.exists")
@patch("etl_modules.google_sheets.os.getenv")
def test_export_to_google_sheets_success(
    mock_getenv, mock_exists, mock_creds, mock_gspread, mock_set_with_df
):
    # Setup fakes
    mock_getenv.return_value = "/fake/credentials.json"
    mock_exists.return_value = True

    mock_client = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()

    # Simular abrir el spreadsheet y worksheet correctamente
    mock_client.open.return_value = mock_spreadsheet
    mock_spreadsheet.worksheet.return_value = mock_worksheet

    # Service account y autorización
    mock_creds.from_json_keyfile_name.return_value = "fake_creds"
    mock_gspread.authorize.return_value = mock_client

    df_dict = [{"name": "Camila", "sales": 1000}]

    export_to_google_sheets(df_dict)

    mock_creds.from_json_keyfile_name.assert_called_once()
    mock_client.open.assert_called_once()
    mock_spreadsheet.worksheet.assert_called_once()
    mock_worksheet.clear.assert_called_once()
    mock_set_with_df.assert_called_once_with(mock_worksheet, pd.DataFrame(df_dict))

@patch("etl_modules.google_sheets.os.getenv")
@patch("etl_modules.google_sheets.os.path.exists")
def test_export_to_google_sheets_invalid_credentials(mock_exists, mock_getenv):
    mock_getenv.return_value = None
    mock_exists.return_value = False

    df_dict = [{"year": 2024, "sales": 2000}]
    export_to_google_sheets(df_dict)

    mock_exists.assert_called_once()
