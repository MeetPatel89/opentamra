"""Azure Data Lake data source — stub for future implementation."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from backend.datasource.base import BaseDataSource


class AzureDataLakeSource(BaseDataSource):
    def __init__(self, **kwargs: object) -> None:
        raise NotImplementedError("Azure Data Lake source is not yet implemented")

    def list_files(self, pattern: str = "*") -> list[Path]:
        raise NotImplementedError

    def read_frame(self, path: Path) -> pl.LazyFrame:
        raise NotImplementedError

    def write_frame(
        self, frame: pl.LazyFrame | pl.DataFrame, path: Path, fmt: str = "parquet"
    ) -> Path:
        raise NotImplementedError
