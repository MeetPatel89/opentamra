# OpenTAMRA

## Quick Start

```bash
uv sync --extra dev          # install deps
uv run pytest -v             # run tests
uv run uvicorn backend.main:app --reload  # start backend
uv run python -m backend run --input-dir data/input --output-dir data/output  # CLI
```

## Architecture

- **Backend**: FastAPI + Polars pipeline for TAMRA tax calculations on life insurance data
- **Frontend**: Create React App (plain JS, plain CSS)
- **Package manager**: uv (not pip)
- **Build**: hatchling

## Pipeline

Steps inherit `BaseStep` and are auto-registered with `@register_step`.
New steps are auto-discovered from `backend/pipeline/steps/` — no manual registration needed.

Steps receive `PipelineContext` which carries:
- `frames` — dict of named DataFrames (Polars LazyFrames by default)
- `datasource` — DataSource protocol instance for all I/O
- `services` — dict for injected dependencies (LLM clients, etc.)
- `settings`, `job_id`, `policy_filter`, `diagnostics`, `manifest`

## Key Conventions

- DataSource protocol (`backend/datasource/base.py`) for all file I/O
- Polars LazyFrame for deferred computation
- Steps access I/O and services through PipelineContext, not direct imports
- Tests in `backend/tests/`, fixtures in `backend/tests/fixtures/`
- Config via TOML files in `config/`, env vars prefixed `OPENTAMRA_`

## Package Management (uv)

- **uv only** — never use pip, poetry, conda, or virtualenv
- Always commit `pyproject.toml` and `uv.lock`; never edit `uv.lock` manually
- Add deps: `uv add <pkg>`, dev deps: `uv add --dev <pkg>`
- Execute all Python through `uv run`

## Backend Conventions

### Python Style
- Every module starts with `from __future__ import annotations`
- Line length: **100 characters** max; break with parenthesised continuation, not backslash
- Ruff rules: `E, F, I, N, W, UP` — run `uv run ruff check .` and `uv run ruff format .`
- Type check: `uvx mypy .`

### Type Annotations
- Use PEP 585/604: `list[str]`, `dict[str, Any]`, `X | Y`, `X | None` — never `List`, `Dict`, `Optional`, `Union`
- Full type annotations on all public function signatures (params + return)
- Use `Field(default_factory=...)` for mutable defaults in Pydantic models and dataclasses
- Pydantic v2: use `.model_dump()` not `.dict()`

### Async & I/O
- All I/O-bound functions must be `async def` with `await`; never block the event loop
- Use `async with pool.acquire() as conn:` for connection management
- Fire-and-forget: `asyncio.create_task()` in route handlers, don't `await` long pipelines

### FastAPI Routes
- Annotate return types on all route handlers
- Use `HTTPException` for expected errors, not `return {"error": ...}`
- Keep handlers thin: parse input → call service → return response
- Wire services through `Depends()`, not inline instantiation

### Logging
- Use `structlog` with `get_logger(__name__)` — never `print()` or `logging.getLogger()`
- Pass structured kwargs: `logger.error("event_name", key=value)` not f-strings

### Testing (pytest)
- `asyncio_mode = "auto"` — do not add `@pytest.mark.asyncio` decorator
- Name tests `test_<behavior>`, not `test_<method_name>`
- Mock at boundary interfaces (ABC/Protocol spec), not deep internals
- Run: `uv run pytest -v`

## Frontend Conventions

### Directory Responsibilities
- `src/api/` — all `fetch` calls; never call `fetch` from components or hooks
- `src/hooks/` — stateful logic, side effects, SSE lifecycle
- `src/components/` — rendering only; no API calls or SSE wiring
- `src/stores/` — shared cross-component state

### React Components
- Default-export a single PascalCase function component per file
- Destructure props inline in the function signature
- Use functional `setState` when new state depends on previous: `setX(prev => ...)`
- Wrap event handlers in `useCallback`
- Do not remove the root `ErrorBoundary`

### Data Flow
- SSE connection/teardown lives in hooks; components only call `send` and `reset`
- Always clear `isLoading` / `thinkingStep` in both `onDone` and `catch`
- API helpers: named exports, one function per endpoint, no state management inside
