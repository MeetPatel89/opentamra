from __future__ import annotations

from pathlib import Path

import polars as pl

from backend.core.exceptions import DataSourceError
from backend.datasource.base import BaseDataSource


class LocalFileSystemSource(BaseDataSource):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)

    def list_files(self, pattern: str = "*") -> list[Path]:
        return sorted(self.base_dir.glob(pattern))

    def read_frame(self, path: Path) -> pl.LazyFrame:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pl.scan_csv(path)
        elif suffix == ".parquet":
            return pl.scan_parquet(path)
        elif suffix in (".xlsx", ".xls"):
            return pl.read_excel(path).lazy()
        else:
            raise DataSourceError(f"Unsupported file format: {suffix}")

    def write_frame(
        self, frame: pl.LazyFrame | pl.DataFrame, path: Path, fmt: str = "parquet"
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        df = frame.collect() if isinstance(frame, pl.LazyFrame) else frame
        if fmt == "parquet":
            out = path.with_suffix(".parquet")
            df.write_parquet(out)
        elif fmt == "csv":
            out = path.with_suffix(".csv")
            df.write_csv(out)
        elif fmt == "xlsx":
            out = path.with_suffix(".xlsx")
            df.write_excel(out)
        else:
            raise DataSourceError(f"Unsupported output format: {fmt}")
        return out
