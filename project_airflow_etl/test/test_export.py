# pyright: reportMissingImports=false

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch, MagicMock
import pandas as pd
from etl_modules.export import export_results

@patch("etl_modules.export.os.makedirs")
@patch("etl_modules.export.pd.DataFrame.to_csv")
def test_export_results_calls_to_csv(mock_to_csv, mock_makedirs):
    # Create a dummy DataFrame
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    })

    export_results(df)

    # Check that makedirs was called
    mock_makedirs.assert_called_once_with(os.path.join(os.getcwd(), "project_airflow_etl/data"), exist_ok=True)

    # Check that to_csv was called with the correct path and index=False
    output_path = os.path.join(os.getcwd(), "project_airflow_etl/data", "report.csv")
    mock_to_csv.assert_called_once_with(output_path, index=False)
