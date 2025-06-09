# pyright: reportMissingImports=false

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch
from etl_modules.generate_sales_plot import generate_sales_by_year_plot


def get_fake_data():
    return [
        {"year": 2022, "total_clp": 1000},
        {"year": 2023, "total_clp": 2000}
    ]


@patch("etl_modules.generate_sales_plot.plt.savefig")
@patch("etl_modules.generate_sales_plot.Path.mkdir")
def test_generate_sales_by_year_plot_creates_file(mock_mkdir, mock_savefig):
    data = get_fake_data()
    output_path = "tests/tmp/yearly_sales_test.png"

    generate_sales_by_year_plot(data, output_path=output_path)

    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_savefig.assert_called_once_with(output_path)


@patch("etl_modules.generate_sales_plot.plt.savefig")
def test_generate_sales_by_year_plot_raises_with_missing_columns(mock_savefig):
    incomplete_data = [
        {"year": 2022},
        {"total_clp": 2000}
    ]
    try:
        generate_sales_by_year_plot(incomplete_data)
    except ValueError as e:
        assert str(e) == "Null values found in required columns: 'year' and/or 'total_clp'."
