import os
from pathlib import Path
from typing import Iterator

import typer
from rich.console import Console
from rich.panel import Panel

from data_cli.io.reader import read_csv_lazy
from data_cli.io.writer import write_csv
from data_cli.core.models import AdRecord, process_records

app = typer.Typer(help="Data CLI - A data processing tool")
console = Console()


class ValidationError(Exception):
    pass


def validate_params(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise ValidationError(f"Input file '{input_path}' does not exist", "File Not Found")

    if not input_path.is_file():
        raise ValidationError(f"'{input_path}' is not a file", "Invalid Input")

    if input_path.suffix.lower() != ".csv":
        raise ValidationError("Input file must be a CSV file (.csv)", "Invalid File Type")

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]Created output directory: {output_path}[/green]")
        return

    if not output_path.is_dir():
        raise ValidationError(f"Output path '{output_path}' exists but is not a directory", "Invalid Output")

    if not os.access(output_path, os.W_OK):
        raise ValidationError(f"Output directory '{output_path}' is not writable", "Permission Error")


def process_data(input_file: Path) -> Iterator[AdRecord]:
    console.print(f"[blue]Reading data from: {input_file}[/blue]")
    records = read_csv_lazy(str(input_file))

    console.print("[blue]Processing data...[/blue]")
    yield from process_records(records)


def generate_output(records: Iterator[AdRecord], output_dir: Path, input_file: Path) -> Path:
    output_file = output_dir / f"{input_file.stem}_processed.csv"
    console.print(f"[blue]Writing output to: {output_file}[/blue]")
    write_csv(str(output_file), records)
    return output_file


@app.command()
def main(
    input: str = typer.Option(..., "--input", "-i", help="Input CSV file path", is_eager=True),
    output: str = typer.Option(..., "--output", "-o", help="Output directory path", is_eager=True),
) -> None:
    input_path = Path(input)
    output_path = Path(output)

    try:
        validate_params(input_path, output_path)
        processed = process_data(input_path)
        output_file = generate_output(processed, output_path, input_path)
        console.print(Panel(f"[green]Successfully processed data![/green]\nInput: {input}\nOutput: {output_file}", title="Success"))

    except ValidationError as e:
        message, title = e.args[0], e.args[1]
        console.print(Panel(f"[red]Error: {message}[/red]", title=title))
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(Panel(f"[red]Error during processing: {e}[/red]", title="Processing Error"))
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
