# pyright: reportMissingImports=false

from etl_modules.enrich import enrich_report

def test_enrich_report_success():
    input_data = [
        {"item": "shoes", "price": 50, "quantity": 2, "total": 100},
        {"item": "shirt", "price": 25, "quantity": 1, "total": 25}
    ]
    clp_rate = 900

    result = enrich_report(input_data, clp_rate)

    assert isinstance(result, list)
    assert all("total_clp" in row for row in result)
    assert result[0]["total_clp"] == round(100 * 900)
    assert result[1]["total_clp"] == round(25 * 900)


def test_enrich_report_empty_list():
    result = enrich_report([], 900)
    assert result is None


def test_enrich_report_missing_total_field():
    input_data = [
        {"item": "hat", "price": 10, "quantity": 1}  # sin campo "total"
    ]
    result = enrich_report(input_data, 900)
    assert result is None


def test_enrich_report_total_as_string():
    input_data = [
        {"item": "gloves", "price": 15, "quantity": 2, "total": "30"}
    ]
    clp_rate = 900

    result = enrich_report(input_data, clp_rate)

    assert isinstance(result, list)
    assert result[0]["total_clp"] == round(30 * 900)
