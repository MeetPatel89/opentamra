from __future__ import annotations

from pathlib import Path

import polars as pl

from backend.core.exceptions import DataSourceError


def read_file(path: Path) -> pl.LazyFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pl.scan_csv(path)
    elif suffix == ".parquet":
        return pl.scan_parquet(path)
    elif suffix in (".xlsx", ".xls"):
        return pl.read_excel(path).lazy()
    else:
        raise DataSourceError(f"Unsupported file format: {suffix}")


def read_directory(directory: Path, pattern: str = "*.csv") -> dict[str, pl.LazyFrame]:
    frames: dict[str, pl.LazyFrame] = {}
    for path in sorted(directory.glob(pattern)):
        frames[path.stem] = read_file(path)
    return frames
