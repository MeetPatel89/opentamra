from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

from backend.core.types import JobState
from backend.datasource.local import LocalFileSystemSource
from backend.ingest.policy_filter import load_policy_filter
from backend.jobs.manager import JobManager
from backend.pipeline.context import PipelineContext
from backend.pipeline.engine import run_pipeline
from backend.settings import Settings

logger = logging.getLogger(__name__)


def _run_pipeline_sync(
    job_id: str,
    input_dir: str,
    output_dir: str,
    policy_filter_path: str | None,
    settings_dict: dict[str, Any],
) -> dict[str, Any]:
    settings = Settings(**settings_dict)
    policy_filter = None
    if policy_filter_path:
        policy_filter = load_policy_filter(Path(policy_filter_path))

    datasource = LocalFileSystemSource(base_dir=Path(input_dir))

    ctx = PipelineContext(
        job_id=job_id,
        settings=settings,
        input_dir=Path(input_dir),
        output_dir=Path(output_dir),
        policy_filter=policy_filter,
        datasource=datasource,
    )
    ctx = run_pipeline(ctx)
    return {
        "manifest": ctx.manifest,
        "diagnostics": ctx.diagnostics,
    }


class BackgroundWorker:
    def __init__(self, manager: JobManager, settings: Settings) -> None:
        self.manager = manager
        self.settings = settings
        self.executor = ProcessPoolExecutor(max_workers=settings.pipeline_max_workers)

    async def submit(self, job: dict[str, Any]) -> None:
        job_id = job["id"]
        await self.manager.mark_running(job_id)

        loop = asyncio.get_event_loop()
        policy_filter_path = None
        if job.get("policy_filter_id"):
            policy_filter_path = str(self.settings.paths_upload_dir / f"{job['policy_filter_id']}.csv")

        try:
            result = await loop.run_in_executor(
                self.executor,
                _run_pipeline_sync,
                job_id,
                job.get("input_dir", str(self.settings.paths_input_dir)),
                job.get("output_dir", str(self.settings.paths_output_dir)),
                policy_filter_path,
                self.settings.model_dump(),
            )
            await self.manager.mark_completed(job_id, manifest=result.get("manifest"))
        except Exception as e:
            logger.exception("Job %s failed", job_id)
            await self.manager.mark_failed(job_id, str(e))

    def shutdown(self) -> None:
        self.executor.shutdown(wait=False)
