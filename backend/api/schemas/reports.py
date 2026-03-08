from __future__ import annotations

from pydantic import BaseModel


class ReportMeta(BaseModel):
    step: str
    path: str
    row_count: int
    format: str = "parquet"


class ReportDownload(BaseModel):
    path: str
    filename: str
