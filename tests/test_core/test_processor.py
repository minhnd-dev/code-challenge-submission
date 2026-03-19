from datetime import date
from decimal import Decimal
from data_cli.core.models import AdRecord, process_record, process_records


class TestProcessor:
    def test_process_record(self):
        record = AdRecord(
            campaign_id="camp_1",
            date=date(2024, 1, 1),
            impressions=1000,
            clicks=50,
            spend=Decimal("10.50"),
            conversions=5,
        )
        result = process_record(record)
        assert result.campaign_id == "camp_1"
        assert result.spend == Decimal("10.50")

    def test_process_records(self):
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
        results = list(process_records(iter(records)))
        assert len(results) == 2
        assert results[0].campaign_id == "camp_1"
        assert results[1].campaign_id == "camp_2"
