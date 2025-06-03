import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from src.etl_modules.usd_to_clp import fetch_usd_to_clp

@patch("src.etl_modules.usd_to_clp.requests.get")
def test_usd_to_clp_positive_float(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"USD": 941.06}

    rate = fetch_usd_to_clp()
    
    assert isinstance(rate, float)
    assert rate > 0