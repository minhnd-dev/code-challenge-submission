from decimal import Decimal
from pathlib import Path
import polars as pl
import pytest

from src.processor import (
    CampaignStats,
    compute_campaign_stats_lazy,
    get_top_ctr_campaigns,
    get_top_cpa_campaigns,
    write_campaign_stats_csv,
)


class TestComputeCampaignStats:
    def test_single_campaign(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["camp_1", "camp_1"],
            "date": ["2024-01-01", "2024-01-02"],
            "impressions": [1000, 2000],
            "clicks": [50, 100],
            "spend": [10.50, 20.75],
            "conversions": [5, 10],
        })
        df.write_csv(csv_file)

        stats = compute_campaign_stats_lazy(str(csv_file))

        assert len(stats) == 1
        assert stats[0].campaign_id == "camp_1"
        assert stats[0].total_impressions == 3000
        assert stats[0].total_clicks == 150
        assert stats[0].total_spend == Decimal("31.25")
        assert stats[0].total_conversions == 15
        assert stats[0].ctr == Decimal("150") / Decimal("3000")
        assert stats[0].cpa == Decimal("31.25") / Decimal("15")

    def test_multiple_campaigns(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["camp_a", "camp_b", "camp_a"],
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "impressions": [1000, 500, 1500],
            "clicks": [100, 25, 150],
            "spend": [10.00, 5.00, 15.00],
            "conversions": [10, 0, 20],
        })
        df.write_csv(csv_file)

        stats = compute_campaign_stats_lazy(str(csv_file))

        assert len(stats) == 2

        camp_a = next(s for s in stats if s.campaign_id == "camp_a")
        assert camp_a.total_impressions == 2500
        assert camp_a.total_clicks == 250
        assert camp_a.total_spend == Decimal("25.00")
        assert camp_a.total_conversions == 30
        assert camp_a.ctr == Decimal("250") / Decimal("2500")
        assert camp_a.cpa == Decimal("25.00") / Decimal("30")

        camp_b = next(s for s in stats if s.campaign_id == "camp_b")
        assert camp_b.total_conversions == 0
        assert camp_b.cpa is None

    def test_zero_impressions(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["camp_1"],
            "date": ["2024-01-01"],
            "impressions": [0],
            "clicks": [0],
            "spend": [0],
            "conversions": [0],
        })
        df.write_csv(csv_file)

        stats = compute_campaign_stats_lazy(str(csv_file))

        assert stats[0].ctr == Decimal("0")
        assert stats[0].cpa is None


class TestGetTopCtrCampaigns:
    def test_top_ctr(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["low", "high", "medium"],
            "date": ["2024-01-01", "2024-01-01", "2024-01-01"],
            "impressions": [1000, 100, 500],
            "clicks": [10, 10, 25],
            "spend": [10, 10, 10],
            "conversions": [1, 1, 1],
        })
        df.write_csv(csv_file)

        stats = compute_campaign_stats_lazy(str(csv_file))
        top_ctr = get_top_ctr_campaigns(stats, n=2)

        assert len(top_ctr) == 2
        assert top_ctr[0].campaign_id == "high"
        assert top_ctr[0].ctr == Decimal("10") / Decimal("100")
        assert top_ctr[1].campaign_id == "medium"
        assert top_ctr[1].ctr == Decimal("25") / Decimal("500")


class TestGetTopCpaCampaigns:
    def test_top_cpa_ignores_zero_conversions(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["zero_conv", "best", "worst"],
            "date": ["2024-01-01", "2024-01-01", "2024-01-01"],
            "impressions": [1000, 1000, 1000],
            "clicks": [100, 100, 100],
            "spend": [100, 10, 100],
            "conversions": [0, 10, 5],
        })
        df.write_csv(csv_file)

        stats = compute_campaign_stats_lazy(str(csv_file))
        top_cpa = get_top_cpa_campaigns(stats, n=2)

        assert len(top_cpa) == 2
        assert all(s.cpa is not None for s in top_cpa)
        assert top_cpa[0].campaign_id == "best"
        assert top_cpa[1].campaign_id == "worst"


class TestWriter:
    def test_write_campaign_stats_csv(self, tmp_path: Path):

        output_file = tmp_path / "output.csv"
        stats = [
            CampaignStats(
                campaign_id="camp_1",
                total_impressions=1000,
                total_clicks=50,
                total_spend=Decimal("10.50"),
                total_conversions=5,
                ctr=Decimal("50") / Decimal("1000"),
                cpa=Decimal("10.50") / Decimal("5"),
            ),
            CampaignStats(
                campaign_id="camp_2",
                total_impressions=2000,
                total_clicks=100,
                total_spend=Decimal("20.75"),
                total_conversions=10,
                ctr=Decimal("100") / Decimal("2000"),
                cpa=Decimal("20.75") / Decimal("10"),
            ),
        ]

        write_campaign_stats_csv(str(output_file), stats)

        df = pl.read_csv(output_file)
        assert len(df) == 2
        assert "CTR" in df.columns
        assert "CPA" in df.columns
        assert df["campaign_id"][0] == "camp_1"
        assert float(df["CTR"][0]) == pytest.approx(0.05, rel=0.001)
