# Prompt 1:
As a senior software engineer with 10 yoe in building performant, extendable, maintainable data processing systems. Help me design the design the architecture of this project: I need to create a small python CLI program that reads from a csv file and generate output files. Suggest me on libraries to use, project structure and the overall architecture, things that I need to avoid

AI
```
It is a classic trap to treat a "small CLI" as a quick script. As you know, small scripts inevitably grow into critical infrastructure. Designing this with a focus on decoupling from day one will save you massive headaches when the requirements inevitably change from "read this CSV" to "read from this S3 bucket and output to a database."

Here is a blueprint for building a performant, extendable, and maintainable Python CLI for data processing.

1. The Overall Architecture
Treat this like a mini-ETL (Extract, Transform, Load) pipeline using a lightweight layered architecture. You want strict boundaries between your I/O, your business logic, and your user interface.

Presentation Layer (CLI): Handles arguments, options, and terminal output (progress bars, error messages). It knows nothing about data transformation.

Orchestration/Core Layer: The "Controller." It takes instructions from the CLI, calls the reader, passes data to the transformer, and hands the result to the writer.

Data Access Layer (I/O): Dedicated modules for reading (CSV) and writing. If you design these to an interface (using Python's Protocol or abc), you can easily swap the CSV reader for an API client later.

Business Logic (Transformation): Pure functions that take data structures, apply your processing rules, and return new data structures. They perform no I/O, making them incredibly easy to unit test.

2. Recommended Libraries
To keep the system performant and the codebase modern, lean heavily on type hinting and fast underlying binaries.

CLI Framework: Typer. It is built on top of Click but uses Python type hints to automatically generate CLI arguments and help text. It enforces clean, typed code at the entry point.

Data Processing: * Polars: If performance is your top priority and the data fits in memory (or can be lazy-evaluated). It is written in Rust, heavily parallelized, and significantly faster than Pandas.

Built-in csv + Generators: If you are dealing with files larger than your RAM and strictly need row-by-row streaming processing to keep a low memory footprint.

Data Validation/Config: Pydantic. Use this to validate the shape of the data coming out of your CSV and to manage application configuration.

Terminal Output: Rich. For beautiful, readable logging, tracebacks, and progress bars without cluttering your logic.

3. Project Structure
Use pyproject.toml for dependency management (via Poetry or uv) and structure the repository to separate concerns.

Plaintext
data_cli/
├── pyproject.toml
├── README.md
├── src/
│   └── data_cli/
│       ├── __init__.py
│       ├── main.py          # Typer app initialization and entry point
│       ├── config.py        # Pydantic settings and env var loading
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py    # Pydantic models defining your data schemas
│       │   └── processor.py # Pure functions for data transformation
│       └── io/
│           ├── __init__.py
│           ├── reader.py    # Abstractions for reading CSVs
│           └── writer.py    # Abstractions for generating output files
└── tests/
    ├── conftest.py
    ├── test_core/         # Fast unit tests for pure logic
    └── test_io/           # Slower tests using mock files/temp directories
4. Things to Avoid (Anti-patterns)
The "God" Function: Do not parse CLI arguments, open the file, transform the data, and write the output all inside def main(). It makes unit testing impossible without mocking the entire file system and terminal.

Eager Loading Large Datasets: Unless using Polars' lazy evaluation, avoid list(reader). Process your data in chunks or as a stream (generators) to ensure the CLI doesn't crash via OOM errors when the client suddenly provides a 10GB CSV.

Silent Failures on Bad Data: CSVs are notoriously messy. Do not assume clean data. Wrap your row parsing in Pydantic validation and explicitly route bad rows to an errors.log file rather than crashing the pipeline or quietly dropping them.

Hardcoded Encoding: Never assume a CSV is UTF-8. Allow the user to pass an --encoding flag at the CLI level, defaulting to utf-8.

Using print() for Information: Use the standard logging library or Rich loggers. If someone pipes your CLI output into another program (my_cli process data.csv > output.txt), stray print() statements will corrupt their data stream. Standardize logs to stderr and data/results to stdout.

Would you like me to write out a boilerplate example of the main.py (CLI layer) and processor.py (Core layer) to show how they interact cleanly?

# Prompt 2:
Help me create the project scaffold for a data processing CLI project in python. Project structure:
├── pyproject.toml
├── README.md
├── src/
│   └── data_cli/
│       ├── __init__.py
│       ├── main.py          # Typer app initialization and entry point
│       ├── config.py        # Pydantic settings and env var loading
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py    # Pydantic models defining your data schemas
│       │   └── processor.py # Pure functions for data transformation
│       └── io/
│           ├── __init__.py
│           ├── reader.py    # Abstractions for reading CSVs
│           └── writer.py    # Abstractions for generating output files
└── tests/
    ├── conftest.py
    ├── test_core/         # Fast unit tests for pure logic
    └── test_io/           # Slower tests using mock files/temp directories The Overall Architecture
Treat this like a mini-ETL (Extract, Transform, Load) pipeline using a lightweight layered architecture. You want strict boundaries between your I/O, your business logic, and your user interface.
Presentation Layer (CLI): Handles arguments, options, and terminal output (progress bars, error messages). It knows nothing about data transformation.
Orchestration/Core Layer: The "Controller." It takes instructions from the CLI, calls the reader, passes data to the transformer, and hands the result to the writer.
Data Access Layer (I/O): Dedicated modules for reading (CSV) and writing. If you design these to an interface (using Python's Protocol or abc), you can easily swap the CSV reader for an API client later.
Business Logic (Transformation): Pure functions that take data structures, apply your processing rules, and return new data structures. They perform no I/O, making them incredibly easy to unit test. populate the code with a minimal hello world example. Make sure to init a git repo, create dockerfile, in the project i want to use uv, python3.12, ruff, libraries: polar, typer, rich, pydantic, loguru
