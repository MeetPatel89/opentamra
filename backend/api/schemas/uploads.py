from __future__ import annotations

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: str
    filename: str
    row_count: int
