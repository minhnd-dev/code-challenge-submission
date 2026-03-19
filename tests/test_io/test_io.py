import pytest
from pathlib import Path
import polars as pl
from data_cli.io.reader import read_csv
from data_cli.io.writer import write_csv
from data_cli.core.models import DataRecord


class TestReader:
    def test_read_csv(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({"id": [1, 2], "value": ["a", "b"]})
        df.write_csv(csv_file)

        records = read_csv(str(csv_file))
        assert len(records) == 2
        assert records[0].id == 1
        assert records[0].value == "a"


class TestWriter:
    def test_write_csv(self, tmp_path: Path):
        output_file = tmp_path / "output.csv"
        records = [
            DataRecord(id=1, value="test"),
            DataRecord(id=2, value="data"),
        ]

        write_csv(str(output_file), records)

        df = pl.read_csv(output_file)
        assert len(df) == 2
        assert df["value"][0] == "test"