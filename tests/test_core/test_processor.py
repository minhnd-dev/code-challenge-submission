import pytest
from data_cli.core.models import DataRecord, process_record, process_records


class TestProcessor:
    def test_process_record(self):
        record = DataRecord(id=1, value="hello")
        result = process_record(record)
        assert result.value == "HELLO"
        assert result.id == 1

    def test_process_records(self):
        records = [
            DataRecord(id=1, value="hello"),
            DataRecord(id=2, value="world"),
        ]
        results = process_records(records)
        assert len(results) == 2
        assert results[0].value == "HELLO"
        assert results[1].value == "WORLD"