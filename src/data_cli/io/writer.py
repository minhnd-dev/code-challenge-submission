import polars as pl
from data_cli.core.models import DataRecord


def write_csv(path: str, records: list[DataRecord]) -> None:
    data = [{"id": r.id, "value": r.value} for r in records]
    df = pl.DataFrame(data)
    df.write_csv(path)