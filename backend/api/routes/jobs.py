from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException

from backend.api.dependencies import get_job_manager, get_worker
from backend.api.schemas import JobCreate, JobDetail, JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobDetail, status_code=201)
async def create_job(body: JobCreate) -> JobDetail:
    manager = get_job_manager()
    job = await manager.create_job(
        policy_filter_id=body.policy_filter_id,
        input_dir=body.input_dir,
    )

    # Launch pipeline in background
    worker = get_worker()
    asyncio.create_task(worker.submit(job))

    return JobDetail(**job)


@router.get("", response_model=list[JobStatus])
async def list_jobs(status: str | None = None) -> list[JobStatus]:
    manager = get_job_manager()
    jobs = await manager.list_jobs(status=status)
    return [JobStatus(**j) for j in jobs]


@router.get("/{job_id}", response_model=JobDetail)
async def get_job(job_id: str) -> JobDetail:
    manager = get_job_manager()
    job = await manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobDetail(**job)


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: str) -> None:
    manager = get_job_manager()
    deleted = await manager.delete_job(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")
