from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from backend.settings import Settings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def sample_policies_path() -> Path:
    return FIXTURES_DIR / "policies.csv"


@pytest.fixture
def policy_filter_path() -> Path:
    return FIXTURES_DIR / "policy_filter_list.csv"


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    return Settings(
        paths_input_dir=FIXTURES_DIR,
        paths_output_dir=tmp_path / "output",
        paths_db_path=tmp_path / "test.db",
        paths_upload_dir=tmp_path / "uploads",
    )


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
