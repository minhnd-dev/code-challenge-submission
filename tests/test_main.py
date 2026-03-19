from pathlib import Path
from unittest.mock import patch, MagicMock
import polars as pl
import pytest

from data_cli.main import validate_params, process_data, generate_output, ValidationError
from data_cli.core.models import DataRecord


class TestValidateParams:
    def test_happy_case_new_output_dir(self, tmp_path: Path):
        input_file = tmp_path / "input.csv"
        input_file.write_text("id,value\n1,a")
        output_dir = tmp_path / "output"

        validate_params(input_file, output_dir)

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_happy_case_existing_output_dir(self, tmp_path: Path):
        input_file = tmp_path / "input.csv"
        input_file.write_text("id,value\n1,a")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        validate_params(input_file, output_dir)

        assert output_dir.exists()

    def test_missing_input_file(self, tmp_path: Path):
        input_file = tmp_path / "nonexistent.csv"
        output_dir = tmp_path / "output"

        with pytest.raises(ValidationError) as exc_info:
            validate_params(input_file, output_dir)

        assert "does not exist" in str(exc_info.value.args[0])
        assert exc_info.value.args[1] == "File Not Found"

    def test_input_path_is_directory(self, tmp_path: Path):
        input_file = tmp_path / "input_dir"
        input_file.mkdir()
        output_dir = tmp_path / "output"

        with pytest.raises(ValidationError) as exc_info:
            validate_params(input_file, output_dir)

        assert "not a file" in str(exc_info.value.args[0])
        assert exc_info.value.args[1] == "Invalid Input"

    def test_input_file_not_csv(self, tmp_path: Path):
        input_file = tmp_path / "input.txt"
        input_file.write_text("some content")
        output_dir = tmp_path / "output"

        with pytest.raises(ValidationError) as exc_info:
            validate_params(input_file, output_dir)

        assert "CSV file" in str(exc_info.value.args[0])
        assert exc_info.value.args[1] == "Invalid File Type"

    def test_input_file_csv_uppercase(self, tmp_path: Path):
        input_file = tmp_path / "input.CSV"
        input_file.write_text("id,value\n1,a")
        output_dir = tmp_path / "output"

        validate_params(input_file, output_dir)

        assert output_dir.exists()

    def test_output_path_exists_but_is_file(self, tmp_path: Path):
        input_file = tmp_path / "input.csv"
        input_file.write_text("id,value\n1,a")
        output_dir = tmp_path / "output"
        output_dir.write_text("this is a file, not a dir")

        with pytest.raises(ValidationError) as exc_info:
            validate_params(input_file, output_dir)

        assert "not a directory" in str(exc_info.value.args[0])
        assert exc_info.value.args[1] == "Invalid Output"

    @patch("data_cli.main.os.access")
    def test_output_dir_not_writable(self, mock_access: MagicMock, tmp_path: Path):
        mock_access.return_value = False
        input_file = tmp_path / "input.csv"
        input_file.write_text("id,value\n1,a")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with pytest.raises(ValidationError) as exc_info:
            validate_params(input_file, output_dir)

        assert "not writable" in str(exc_info.value.args[0])
        assert exc_info.value.args[1] == "Permission Error"


class TestProcessData:
    def test_happy_case(self, tmp_path: Path, capsys):
        csv_file = tmp_path / "test.csv"
        df = pl.DataFrame({"id": [1, 2, 3], "value": ["a", "b", "c"]})
        df.write_csv(csv_file)

        records = process_data(csv_file)

        assert len(records) == 3
        assert all(isinstance(r, DataRecord) for r in records)
        assert records[0].id == 1
        assert records[0].value == "A"
        assert records[1].value == "B"
        assert records[2].value == "C"

    def test_empty_file(self, tmp_path: Path):
        csv_file = tmp_path / "empty.csv"
        df = pl.DataFrame({"id": [], "value": []})
        df.write_csv(csv_file)

        records = process_data(csv_file)

        assert len(records) == 0


class TestGenerateOutput:
    def test_happy_case(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        input_file = Path("test.csv")
        records = [
            DataRecord(id=1, value="hello"),
            DataRecord(id=2, value="world"),
        ]

        output_file = generate_output(records, output_dir, input_file)

        assert output_file == output_dir / "test_processed.csv"
        assert output_file.exists()

        df = pl.read_csv(output_file)
        assert len(df) == 2
        assert df["value"][0] == "hello"
        assert df["value"][1] == "world"


class TestCliIntegration:
    def test_missing_input_argument(self):
        from typer.testing import CliRunner
        from data_cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["--output", "output"])

        assert result.exit_code == 2
        assert "Missing option" in result.output
        assert "--input" in result.output

    def test_missing_output_argument(self):
        from typer.testing import CliRunner
        from data_cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["--input", "input.csv"])

        assert result.exit_code == 2
        assert "Missing option" in result.output
        assert "--output" in result.output

    def test_invalid_input_file(self):
        from typer.testing import CliRunner
        from data_cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["--input", "nonexistent.csv", "--output", "output"])

        assert result.exit_code == 1
        assert "does not exist" in result.output

    def test_invalid_input_type(self, tmp_path: Path):
        from typer.testing import CliRunner
        from data_cli.main import app

        input_file = tmp_path / "input.txt"
        input_file.write_text("data")

        runner = CliRunner()
        result = runner.invoke(app, ["--input", str(input_file), "--output", "output"])

        assert result.exit_code == 1
        assert "CSV file" in result.output

    def test_successful_processing(self, tmp_path: Path):
        from typer.testing import CliRunner
        from data_cli.main import app

        input_file = tmp_path / "input.csv"
        df = pl.DataFrame({"id": [1, 2], "value": ["a", "b"]})
        df.write_csv(input_file)
        output_dir = tmp_path / "output"

        runner = CliRunner()
        result = runner.invoke(app, ["--input", str(input_file), "--output", str(output_dir)])

        assert result.exit_code == 0
        assert "Successfully processed data" in result.output
        assert (output_dir / "input_processed.csv").exists()

    def test_successful_processing_with_short_flags(self, tmp_path: Path):
        from typer.testing import CliRunner
        from data_cli.main import app

        input_file = tmp_path / "data.csv"
        df = pl.DataFrame({"id": [1], "value": ["test"]})
        df.write_csv(input_file)
        output_dir = tmp_path / "out"

        runner = CliRunner()
        result = runner.invoke(app, ["-i", str(input_file), "-o", str(output_dir)])

        assert result.exit_code == 0
        assert (output_dir / "data_processed.csv").exists()
