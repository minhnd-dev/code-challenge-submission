# Data CLI

A lightweight data processing CLI tool built with Python.

## Setup

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

## How to Run

```bash
# Run with uv
uv run data-cli --input input.csv --output output/

# Or with short flags
uv run data-cli -i input.csv -o output/

# Get help
uv run data-cli --help
```

## Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| Typer | >=0.15.0 | CLI framework |
| Rich | >=13.0.0 | Terminal output formatting |
| Pydantic | >=2.10.0 | Data validation |
| Polars | >=1.20.0 | Data processing |
| Ruff | >=0.9.0 | Linting/formatting |

## System Info

| Property | Value |
|----------|-------|
| OS | macOS 25.3.0 (Darwin) |
| MacBook | Mac16,1 |
| Chip | Apple M4 |
| Architecture | arm64 |
| RAM | 16.0 GB |
| Storage | Apple SSD AP0512Z (APFS, SSD) |
| Storage Capacity | 494.4 GB |

## Benchmark

### Speed
- Tool: Hyperfine
- Command: hyperfine --runs 10 --warmup 2 --show-output "uv run src/main.py -i input/ad_data.csv -o output"
- Speed (10 times):
    Time (mean ± σ):     512.5 ms ±   9.1 ms    [User: 3128.8 ms, System: 84.7 ms]
    Range (min … max):   499.1 ms … 532.9 ms    10 runs
### Peak usage
- Tool: Scalene
- Command: uv run python -m scalene run src/main.py --- -i input/ad_data.csv -o output
- Peak memory usage: max: 11M, growth: 100.0%
