from typing import List

import polars as pl
from data_cli.core.models import CampaignStats


def write_campaign_stats_csv(path: str, stats: List[CampaignStats]) -> None:
    data = []
    for stat in stats:
        row = {
            "campaign_id": stat.campaign_id,
            "total_impressions": stat.total_impressions,
            "total_clicks": stat.total_clicks,
            "total_spend": float(stat.total_spend),
            "total_conversions": stat.total_conversions,
            "CTR": str(stat.ctr),
            "CPA": str(stat.cpa) if stat.cpa is not None else "",
        }
        data.append(row)
    df = pl.DataFrame(data)
    df.write_csv(path)
