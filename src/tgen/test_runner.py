import pytest
from pytest_jsonreport.plugin import JSONReport

def get_test_results(test_file: str) -> str:
    with open(test_file, 'r') as f:
        json_report = JSONReport()
        pytest.main(['--json-report-file=none', test_file], plugins=[json_report])
        return json_report.report