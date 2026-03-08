from __future__ import annotations

from pydantic import BaseModel

from backend.core.types import JobState


class JobCreate(BaseModel):
    policy_filter_id: str | None = None
    input_dir: str | None = None


class JobStatus(BaseModel):
    id: str
    status: JobState
    created_at: str
    updated_at: str


class JobDetail(BaseModel):
    id: str
    status: JobState
    input_dir: str | None = None
    output_dir: str | None = None
    policy_filter_id: str | None = None
    created_at: str
    updated_at: str
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None
    manifest: object | None = None
