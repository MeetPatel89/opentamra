# OpenTAMRA

OpenTAMRA is a TAMRA tax calculation pipeline for life insurance policy data.
The project includes:

- a FastAPI backend
- a CLI for running the pipeline on local input files
- a React frontend

## Requirements

- Python 3.13+
- `uv` for Python dependency management
- Node.js and npm for the frontend

## Quick Start

### 1. Install backend dependencies

```bash
uv sync --extra dev
```

### 2. Start the backend

```bash
uv run uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 3. Start the frontend

```bash
cd frontend
npm install
npm start
```

The frontend is configured to proxy API requests to `http://localhost:8000`.

## Run the CLI Pipeline

Run the pipeline against local input files:

```bash
uv run python -m backend run --input-dir data/input --output-dir data/output
```

You can also use the installed script entrypoint:

```bash
uv run opentamra run --input-dir data/input --output-dir data/output
```

Optional arguments:

- `--policy-list <path>` to filter by policy IDs from a CSV file
- `--job-id <id>` to provide a custom job ID
- `--log-level <level>` to set logging verbosity

## Testing

Run the backend test suite:

```bash
uv run pytest -v
```

## Development Checks

Lint and format Python code:

```bash
uv run ruff check .
uv run ruff format .
```

Run type checking:

```bash
uvx mypy .
```

## Project Structure

```text
backend/   FastAPI app, pipeline engine, CLI, datasource layer
frontend/  React app
config/    TOML configuration files
data/      Local input and output data
```

## Architecture Notes

- Backend: FastAPI + Polars pipeline
- Frontend: Create React App
- Package management: `uv` for Python dependencies
- Pipeline steps live in `backend/pipeline/steps/` and are auto-discovered
- File I/O goes through the datasource layer

## Useful Commands

```bash
uv sync --extra dev
uv run uvicorn backend.main:app --reload
uv run pytest -v
uv run python -m backend run --input-dir data/input --output-dir data/output
```
