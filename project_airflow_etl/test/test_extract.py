from unittest.mock import patch, MagicMock
import pandas as pd

from etl_modules.extract import extract_data

@patch("etl_modules.extract.get_connection")
def test_extract_data_returns_expected_structure(mock_get_connection):
    fake_rows = [
        (2024, "Santiago-01", 1000),
        (2025, "Temuco-02", 1300)
    ]
    fake_description = [("year",), ("store",), ("total",)]

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fake_rows
    mock_cursor.description = fake_description

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Además, extract_data hace cur.close() y conn.close(), el mock debe tenerlos:
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    mock_get_connection.return_value = (mock_conn, mock_cursor)

    result = extract_data()

    assert isinstance(result, list)
    assert result == [
        {"year": 2024, "store": "Santiago-01", "total": 1000},
        {"year": 2025, "store": "Temuco-02", "total": 1300}
    ]