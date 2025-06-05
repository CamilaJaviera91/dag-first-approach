from unittest.mock import patch, MagicMock
import pandas as pd

from etl_modules.enrich import enrich_report
from etl_modules.extract import extract_data

@patch("etl_modules.enrich.fetch_usd_to_clp")
@patch("etl_modules.extract.extract_data")
def test_enrich_adds_total_clp(mock_extract_data, mock_fetch_usd_to_clp):
    mock_extract_data.return_value = [
        {"item": "shoes", "price": 50, "quantity": 2, "total": 100},
        {"item": "shirt", "price": 25, "quantity": 1, "total": 25}
    ]
    mock_fetch_usd_to_clp.return_value = 900.0

    df = enrich_report(mock_extract_data.return_value, mock_fetch_usd_to_clp.return_value)

    assert isinstance(df, pd.DataFrame)
    assert "total_clp" in df.columns
    assert df["total_clp"].iloc[0] == 100 * 900.0
    assert df["total_clp"].iloc[1] == 25 * 900.0


@patch("src.etl_modules.extract.connect_to_postgres")
def test_extract_data_returns_expected_structure(mock_connect):
    fake_rows = [
        (2024, "Santiago-01", 1000),
        (2025, "Temuco-02", 1300)
    ]
    fake_description = [("year",), ("store",), ("total",)]

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fake_rows
    mock_cursor.description = fake_description

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    result = extract_data()

    assert isinstance(result, list)
    assert result == [
        {"year": 2024, "store": "Santiago-01", "total": 1000},
        {"year": 2025, "store": "Temuco-02", "total": 1300}
    ]