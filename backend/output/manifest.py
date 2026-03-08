from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class ManifestEntry:
    step: str
    path: str
    row_count: int
    format: str = "parquet"


@dataclass
class JobManifest:
    job_id: str
    entries: list[ManifestEntry] = field(default_factory=list)

    def add(self, step: str, path: Path, row_count: int, fmt: str = "parquet") -> None:
        self.entries.append(ManifestEntry(step=step, path=str(path), row_count=row_count, format=fmt))

    def save(self, output_dir: Path) -> Path:
        manifest_path = output_dir / self.job_id / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w") as f:
            json.dump({"job_id": self.job_id, "outputs": [asdict(e) for e in self.entries]}, f, indent=2)
        return manifest_path

    @classmethod
    def load(cls, path: Path) -> JobManifest:
        with open(path) as f:
            data = json.load(f)
        manifest = cls(job_id=data["job_id"])
        for entry in data["outputs"]:
            manifest.entries.append(ManifestEntry(**entry))
        return manifest
