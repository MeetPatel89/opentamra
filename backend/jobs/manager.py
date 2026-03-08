from __future__ import annotations

import uuid
from typing import Any

from backend.core.types import JobState
from backend.jobs.store import JobStore
from backend.settings import Settings


class JobManager:
    def __init__(self, store: JobStore, settings: Settings) -> None:
        self.store = store
        self.settings = settings

    async def create_job(
        self, policy_filter_id: str | None = None, input_dir: str | None = None
    ) -> dict[str, Any]:
        job_id = uuid.uuid4().hex[:12]
        return await self.store.create(
            job_id=job_id,
            input_dir=input_dir or str(self.settings.paths_input_dir),
            output_dir=str(self.settings.paths_output_dir),
            policy_filter_id=policy_filter_id,
        )

    async def get_job(self, job_id: str) -> dict[str, Any] | None:
        return await self.store.get(job_id)

    async def list_jobs(self, status: str | None = None) -> list[dict[str, Any]]:
        return await self.store.list_jobs(status)

    async def mark_running(self, job_id: str) -> None:
        await self.store.update_status(job_id, JobState.RUNNING)

    async def mark_completed(self, job_id: str, manifest: dict[str, Any] | None = None) -> None:
        await self.store.update_status(job_id, JobState.COMPLETED, manifest=manifest)

    async def mark_failed(self, job_id: str, error: str) -> None:
        await self.store.update_status(job_id, JobState.FAILED, error=error)

    async def cancel_job(self, job_id: str) -> None:
        await self.store.update_status(job_id, JobState.CANCELLED)

    async def delete_job(self, job_id: str) -> bool:
        return await self.store.delete(job_id)
