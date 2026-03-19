from data_cli.core.models import DataRecord, process_records


def run_pipeline(records: list[DataRecord]) -> list[DataRecord]:
    return process_records(records)