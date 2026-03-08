from __future__ import annotations

import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.api.dependencies import get_app_settings, get_job_manager
from backend.api.schemas import ReportMeta

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{job_id}", response_model=list[ReportMeta])
async def list_reports(job_id: str) -> list[ReportMeta]:
    manager = get_job_manager()
    job = await manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    manifest_raw = job.get("manifest")
    if not manifest_raw:
        return []

    manifest = json.loads(manifest_raw) if isinstance(manifest_raw, str) else manifest_raw
    return [ReportMeta(**entry) for entry in manifest]


@router.get("/{job_id}/{level}")
async def preview_report(job_id: str, level: str, limit: int = 100) -> dict[str, object]:
    settings = get_app_settings()
    output_dir = settings.paths_output_dir / job_id

    # Find matching file
    matches = list(output_dir.glob(f"*{level}*"))
    if not matches:
        raise HTTPException(status_code=404, detail=f"No output found for level '{level}'")

    path = matches[0]
    if path.suffix == ".parquet":
        df = pl.read_parquet(path)
    elif path.suffix == ".csv":
        df = pl.read_csv(path)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {path.suffix}")

    rows = df.head(limit).to_dicts()
    return {"columns": df.columns, "row_count": len(df), "rows": rows}


@router.get("/{job_id}/{level}/download")
async def download_report(job_id: str, level: str) -> FileResponse:
    settings = get_app_settings()
    output_dir = settings.paths_output_dir / job_id

    matches = list(output_dir.glob(f"*{level}*"))
    if not matches:
        raise HTTPException(status_code=404, detail=f"No output found for level '{level}'")

    path = matches[0]
    return FileResponse(path=str(path), filename=path.name)
