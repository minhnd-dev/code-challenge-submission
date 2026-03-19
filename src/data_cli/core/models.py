from decimal import Decimal
from typing import Optional
from dataclasses import dataclass

import polars as pl


@dataclass
class CampaignStats:
    campaign_id: str
    total_impressions: int
    total_clicks: int
    total_spend: Decimal
    total_conversions: int
    ctr: Decimal
    cpa: Optional[Decimal]


def compute_campaign_stats_lazy(path: str) -> list[CampaignStats]:
    lf = pl.scan_csv(path)

    aggregated = lf.group_by("campaign_id").agg(
        pl.col("impressions").sum().alias("total_impressions"),
        pl.col("clicks").sum().alias("total_clicks"),
        pl.col("spend").sum().alias("total_spend"),
        pl.col("conversions").sum().alias("total_conversions"),
    )

    df = aggregated.collect(engine="streaming")

    results = []
    for row in df.iter_rows(named=True):
        total_impressions = row["total_impressions"]
        total_clicks = row["total_clicks"]
        total_spend = Decimal(str(row["total_spend"]))
        total_conversions = row["total_conversions"]

        if total_impressions > 0:
            ctr = Decimal(total_clicks) / Decimal(total_impressions)
        else:
            ctr = Decimal("0")

        if total_conversions > 0:
            cpa = total_spend / Decimal(total_conversions)
        else:
            cpa = None

        results.append(CampaignStats(
            campaign_id=row["campaign_id"],
            total_impressions=total_impressions,
            total_clicks=total_clicks,
            total_spend=total_spend,
            total_conversions=total_conversions,
            ctr=ctr,
            cpa=cpa,
        ))

    return results


def get_top_ctr_campaigns(stats: list[CampaignStats], n: int = 10) -> list[CampaignStats]:
    return sorted(stats, key=lambda x: x.ctr, reverse=True)[:n]


def get_top_cpa_campaigns(stats: list[CampaignStats], n: int = 10) -> list[CampaignStats]:
    valid_stats = [s for s in stats if s.cpa is not None]
    return sorted(valid_stats, key=lambda x: x.cpa)[:n]
