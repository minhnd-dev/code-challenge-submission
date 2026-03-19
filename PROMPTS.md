# Prompt 1:
As a senior software engineer with 10 yoe in building performant, extendable, maintainable data processing systems. Help me design the design the architecture of this project: I need to create a small python CLI program that reads from a csv file and generate output files. Suggest me on libraries to use, project structure and the overall architecture, things that I need to avoid

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

# Prompt 3:
Update the CLI to recieve 2 arguments: input <file_name>.csv --output <directory>. For example: uv run data-cli --input ad_data.csv --output output. Make sure to handle errors, check for file existence, directory existence, etc

# Prompt 4: 
Separate the code into modular functions: parameter validation, data processing, generate output

# Prompt 5: 
Writ unit tests for each function, handle all cases: happy case, missing required arguments, input file existence, input file type csv, invalid output path, etc. Make sure it all tests are passed

# Prompt 6:
Help me implement reading data from the csv file. Here's the expected input file columns: 
Column	Type	Description
campaign_id	string	Campaign ID
date	string	Date in YYYY-MM-DD format
impressions	integer	Number of impressions
clicks	integer	Number of clicks
spend	float	Advertising cost (USD)
conversions	integer	Number of conversions 
For float, make sure to use Decimal for precision. I want to read the file lazily with stream.

# Prompt 7:
Implement data processing: For each campaign_id, compute:
total_impressions
total_clicks
total_spend
total_conversions
CTR = total_clicks / total_impressions
CPA = total_spend / total_conversions
If conversions = 0, ignore or return null for CPA