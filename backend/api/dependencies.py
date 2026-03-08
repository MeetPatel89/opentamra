from __future__ import annotations

from functools import lru_cache

from backend.datasource.base import BaseDataSource
from backend.datasource.registry import create_datasource
from backend.jobs.manager import JobManager
from backend.jobs.store import JobStore
from backend.jobs.worker import BackgroundWorker
from backend.settings import Settings, get_settings


@lru_cache
def get_app_settings() -> Settings:
    return get_settings()


def get_datasource(settings: Settings | None = None) -> BaseDataSource:
    s = settings or get_app_settings()
    return create_datasource(s)


def get_job_store(settings: Settings | None = None) -> JobStore:
    s = settings or get_app_settings()
    return JobStore(db_path=s.paths_db_path)


def get_job_manager(settings: Settings | None = None) -> JobManager:
    s = settings or get_app_settings()
    return JobManager(store=get_job_store(s), settings=s)


def get_worker(settings: Settings | None = None) -> BackgroundWorker:
    s = settings or get_app_settings()
    return BackgroundWorker(manager=get_job_manager(s), settings=s)
