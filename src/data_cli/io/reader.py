import polars as pl
from data_cli.core.models import DataRecord


def read_csv(path: str) -> list[DataRecord]:
    df = pl.read_csv(path)
    return [DataRecord(id=row["id"], value=row["value"]) for row in df.iter_rows()]