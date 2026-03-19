# Project Overview
A Python CLI tool for data processing using Typer, Polars, Pydantic, and Rich. The project follows a layered ETL-style architecture:

# General Principles
- Write clean, readable code. Prefer explicit over implicit.
- Follow the existing patterns in the codebase.
- Use TDD: write tests first (Red), implement minimal logic to pass (Green), then refactor (Refactor).

# Error Handling
- Handle exceptions carefully. Never silently swallow errors.
- Use Pydantic validation for data schema enforcement.
- Route invalid rows explicitly rather than dropping them silently.

# Logging (Loguru)
- Configure loguru in the main entry point.

# Business Logic
- Pure transformation functions must have NO I/O side effects.
- Keep functions small and focused. A function should do one thing well.
- Use generators for memory-efficient streaming of large datasets.
- Never assume clean data — validate with Pydantic.

# I/O Layer
- Abstract reading and writing behind interface functions.
- Never hardcode file encodings. Default to UTF-8.
- Process large files in chunks/streaming mode to avoid OOM.
- Use Polars for fast, parallelized data operations.
