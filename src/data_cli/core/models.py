from datetime import date
from decimal import Decimal
from typing import Iterator

import polars as pl
from pydantic import BaseModel


class AdRecord(BaseModel):
    campaign_id: str
    date: date
    impressions: int
    clicks: int
    spend: Decimal
    conversions: int

    def model_post_init(self, __context) -> None:
        if isinstance(self.spend, float):
            self.spend = Decimal(str(self.spend))


def process_record(record: AdRecord) -> AdRecord:
    return record


def process_records(records: Iterator[AdRecord]) -> Iterator[AdRecord]:
    for record in records:
        yield process_record(record)


def read_csv_lazy(path: str) -> Iterator[AdRecord]:
    lf = pl.scan_csv(path)
    df = lf.collect()
    for record in df.iter_rows(named=True):
        record["date"] = date.fromisoformat(record["date"])
        record["spend"] = Decimal(str(record["spend"]))
        yield AdRecord(**record)
