import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.etl_modules.extract import extract_data

def test_extract_data_returns_list():
    data = extract_data()
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)
