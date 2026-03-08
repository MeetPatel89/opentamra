from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable

import polars as pl


@runtime_checkable
class DataSource(Protocol):
    def list_files(self, pattern: str = "*") -> list[Path]: ...
    def read_frame(self, path: Path) -> pl.LazyFrame: ...
    def write_frame(
        self, frame: pl.LazyFrame | pl.DataFrame, path: Path, fmt: str = "parquet"
    ) -> Path: ...


class BaseDataSource(ABC):
    @abstractmethod
    def list_files(self, pattern: str = "*") -> list[Path]: ...

    @abstractmethod
    def read_frame(self, path: Path) -> pl.LazyFrame: ...

    @abstractmethod
    def write_frame(
        self, frame: pl.LazyFrame | pl.DataFrame, path: Path, fmt: str = "parquet"
    ) -> Path: ...
