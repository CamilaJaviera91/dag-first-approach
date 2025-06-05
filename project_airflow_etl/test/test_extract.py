from unittest.mock import patch, MagicMock
from etl_modules.extract import extract_data

@patch("etl_modules.extract.connect_to_postgres")
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