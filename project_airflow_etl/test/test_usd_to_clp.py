import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.etl_modules.usd_to_clp import fetch_usd_to_clp

def test_usd_to_clp_positive_float():
    rate = fetch_usd_to_clp()
    assert isinstance(rate, float)
    assert rate > 0
