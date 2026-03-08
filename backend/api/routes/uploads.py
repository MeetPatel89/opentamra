from __future__ import annotations

import uuid

import polars as pl
from fastapi import APIRouter, UploadFile

from backend.api.dependencies import get_app_settings
from backend.api.schemas import UploadResponse

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/policy-list", response_model=UploadResponse, status_code=201)
async def upload_policy_list(file: UploadFile) -> UploadResponse:
    settings = get_app_settings()
    upload_dir = settings.paths_upload_dir
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex[:12]
    dest = upload_dir / f"{file_id}.csv"

    content = await file.read()
    dest.write_bytes(content)

    df = pl.read_csv(dest)
    return UploadResponse(
        id=file_id,
        filename=file.filename or "unknown.csv",
        row_count=len(df),
    )
