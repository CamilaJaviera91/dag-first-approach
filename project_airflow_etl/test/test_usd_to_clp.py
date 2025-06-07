# pyright: reportMissingImports=false

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch, MagicMock
from etl_modules.usd_to_clp import fetch_usd_to_clp

@patch("etl_modules.usd_to_clp.requests.get")
def test_fetch_usd_to_clp_returns_correct_rate(mock_get):
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "rates": {
            "CLP": 925.37
        }
    }
    mock_get.return_value = fake_response

    result = fetch_usd_to_clp()

    assert isinstance(result, float)
    assert result == 925.37

@patch("etl_modules.usd_to_clp.requests.get")
def test_fetch_usd_to_clp_missing_rate_returns_none(mock_get):
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "rates": {
            # CLP intentionally missing
            "EUR": 0.92
        }
    }
    mock_get.return_value = fake_response

    result = fetch_usd_to_clp()

    assert result is None

@patch("etl_modules.usd_to_clp.requests.get")
def test_fetch_usd_to_clp_raises_exception_returns_none(mock_get):
    mock_get.side_effect = Exception("API down")

    result = fetch_usd_to_clp()

    assert result is None