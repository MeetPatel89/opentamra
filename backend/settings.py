from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


def _load_toml(path: Path) -> dict[str, Any]:
    if path.exists():
        with open(path, "rb") as f:
            return tomllib.load(f)
    return {}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _flatten(d: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    items: dict[str, Any] = {}
    for k, v in d.items():
        key = f"{prefix}_{k}" if prefix else k
        if isinstance(v, dict):
            items.update(_flatten(v, key))
        else:
            items[key] = v
    return items


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


class Settings(BaseSettings):
    model_config = {"env_prefix": "OPENTAMRA_"}

    # app
    app_name: str = Field(default="OpenTAMRA")
    app_env: str = Field(default="development")
    app_debug: bool = Field(default=False)

    # paths
    paths_data_dir: Path = Field(default=Path("./data"))
    paths_input_dir: Path = Field(default=Path("./data/input"))
    paths_output_dir: Path = Field(default=Path("./data/output"))
    paths_db_path: Path = Field(default=Path("./opentamra.db"))
    paths_upload_dir: Path = Field(default=Path("./data/uploads"))

    # server
    server_host: str = Field(default="0.0.0.0")
    server_port: int = Field(default=8000)
    server_cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # pipeline
    pipeline_max_workers: int = Field(default=2)
    pipeline_default_output_format: str = Field(default="parquet")

    # datasource
    datasource_type: str = Field(default="local")

    @classmethod
    def from_toml(cls, env: str | None = None) -> Settings:
        defaults = _load_toml(CONFIG_DIR / "default.toml")
        env_name = env or defaults.get("app", {}).get("env", "development")
        overrides = _load_toml(CONFIG_DIR / f"{env_name}.toml")
        merged = _merge(defaults, overrides)
        flat = _flatten(merged)
        return cls(**flat)


def get_settings() -> Settings:
    return Settings.from_toml()
