from pydantic import BaseModel


class DataRecord(BaseModel):
    id: int
    value: str


def process_record(record: DataRecord) -> DataRecord:
    return DataRecord(id=record.id, value=record.value.upper())


def process_records(records: list[DataRecord]) -> list[DataRecord]:
    return [process_record(r) for r in records]