FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY tests/ ./tests/

ENV PYTHONPATH=/app

CMD ["uv", "run", "data-cli"]