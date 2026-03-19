from typing import Iterator

import polars as pl
from data_cli.core.models import AdRecord


def write_csv(path: str, records: Iterator[AdRecord]) -> None:
    data = []
    for record in records:
        row = {
            "campaign_id": record.campaign_id,
            "date": record.date.isoformat(),
            "impressions": record.impressions,
            "clicks": record.clicks,
            "spend": float(record.spend),
            "conversions": record.conversions,
        }
        data.append(row)
    df = pl.DataFrame(data)
    df.write_csv(path)
