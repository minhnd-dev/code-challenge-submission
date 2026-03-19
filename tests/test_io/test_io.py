from decimal import Decimal
from pathlib import Path
import polars as pl

from data_cli.core.models import AdRecord, read_csv_lazy


class TestReader:
    def test_read_csv_lazy(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["camp_1", "camp_2"],
            "date": ["2024-01-01", "2024-01-02"],
            "impressions": [1000, 2000],
            "clicks": [50, 100],
            "spend": [10.50, 20.75],
            "conversions": [5, 10],
        })
        df.write_csv(csv_file)

        records = list(read_csv_lazy(str(csv_file)))

        assert len(records) == 2
        assert records[0].campaign_id == "camp_1"
        assert records[0].date.year == 2024
        assert records[0].impressions == 1000
        assert records[0].clicks == 50
        assert records[0].spend == Decimal("10.50")
        assert records[0].conversions == 5

    def test_read_csv_lazy_decimal_precision(self, tmp_path: Path):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({
            "campaign_id": ["camp_1"],
            "date": ["2024-01-01"],
            "impressions": [100],
            "clicks": [10],
            "spend": [10.123],
            "conversions": [1],
        })
        df.write_csv(csv_file)

        records = list(read_csv_lazy(str(csv_file)))

        assert records[0].spend == Decimal("10.123")


class TestWriter:
    def test_write_csv(self, tmp_path: Path):
        from data_cli.io.writer import write_csv
        from datetime import date

        output_file = tmp_path / "output.csv"
        records = [
            AdRecord(
                campaign_id="camp_1",
                date=date(2024, 1, 1),
                impressions=1000,
                clicks=50,
                spend=Decimal("10.50"),
                conversions=5,
            ),
            AdRecord(
                campaign_id="camp_2",
                date=date(2024, 1, 2),
                impressions=2000,
                clicks=100,
                spend=Decimal("20.75"),
                conversions=10,
            ),
        ]

        write_csv(str(output_file), iter(records))

        df = pl.read_csv(output_file)
        assert len(df) == 2
        assert df["campaign_id"][0] == "camp_1"
        assert df["impressions"][0] == 1000
        assert df["spend"][0] == 10.50
