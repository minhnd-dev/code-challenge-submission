import polars as pl
from data_cli.core.models import DataRecord


def read_csv(path: str) -> list[DataRecord]:
    df = pl.read_csv(path)
    return [DataRecord(id=row[0], value=row[1]) for row in df.iter_rows()]