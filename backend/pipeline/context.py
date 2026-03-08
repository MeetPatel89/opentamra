from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from backend.settings import Settings

if TYPE_CHECKING:
    from backend.datasource.base import DataSource


@dataclass
class PipelineContext:
    job_id: str
    settings: Settings
    frames: dict[str, Any] = field(default_factory=dict)
    datasource: DataSource | None = None
    services: dict[str, Any] = field(default_factory=dict)
    policy_filter: list[str] | None = None
    diagnostics: list[dict[str, object]] = field(default_factory=list)
    manifest: list[dict[str, object]] = field(default_factory=list)
    input_dir: Path | None = None
    output_dir: Path | None = None

    def add_diagnostic(self, step: str, message: str, **extra: object) -> None:
        self.diagnostics.append({"step": step, "message": message, **extra})

    def add_to_manifest(self, step: str, path: Path, row_count: int) -> None:
        self.manifest.append({"step": step, "path": str(path), "row_count": row_count})
