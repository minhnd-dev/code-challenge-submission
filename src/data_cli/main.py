import os
from pathlib import Path
from typing import List

import typer
from rich.console import Console
from rich.panel import Panel

from data_cli.io.writer import write_campaign_stats_csv
from data_cli.core.models import (
    CampaignStats,
    compute_campaign_stats_lazy,
    get_top_ctr_campaigns,
    get_top_cpa_campaigns,
)

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


def process_data(input_file: Path) -> List[CampaignStats]:
    console.print(f"[blue]Reading and computing statistics from: {input_file}[/blue]")
    console.print("[blue]Using streaming mode for memory efficiency...[/blue]")
    stats = compute_campaign_stats_lazy(str(input_file))
    console.print(f"[blue]Computed statistics for {len(stats)} campaigns[/blue]")
    return stats


def generate_top_ctr_output(stats: List[CampaignStats], output_dir: Path) -> Path:
    top_ctr = get_top_ctr_campaigns(stats)
    output_file = output_dir / "top10_ctr.csv"
    console.print(f"[blue]Writing top CTR campaigns to: {output_file}[/blue]")
    write_campaign_stats_csv(str(output_file), top_ctr)
    return output_file


def generate_top_cpa_output(stats: List[CampaignStats], output_dir: Path) -> Path:
    top_cpa = get_top_cpa_campaigns(stats)
    output_file = output_dir / "top10_cpa.csv"
    console.print(f"[blue]Writing top CPA campaigns to: {output_file}[/blue]")
    write_campaign_stats_csv(str(output_file), top_cpa)
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
        stats = process_data(input_path)
        top_ctr_file = generate_top_ctr_output(stats, output_path)
        top_cpa_file = generate_top_cpa_output(stats, output_path)
        console.print(Panel(
            f"[green]Successfully processed data![/green]\nInput: {input}\nTop CTR: {top_ctr_file}\nTop CPA: {top_cpa_file}",
            title="Success",
        ))

    except ValidationError as e:
        message, title = e.args[0], e.args[1]
        console.print(Panel(f"[red]Error: {message}[/red]", title=title))
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(Panel(f"[red]Error during processing: {e}[/red]", title="Processing Error"))
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
