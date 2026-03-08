from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiosqlite

from backend.core.types import JobState

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'pending',
    input_dir TEXT,
    output_dir TEXT,
    policy_filter_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    error TEXT,
    manifest TEXT
)
"""


class JobStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(CREATE_TABLE)
            await db.commit()

    async def create(self, job_id: str, input_dir: str | None = None, output_dir: str | None = None, policy_filter_id: str | None = None) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        row = {
            "id": job_id,
            "status": JobState.PENDING,
            "input_dir": input_dir,
            "output_dir": output_dir,
            "policy_filter_id": policy_filter_id,
            "created_at": now,
            "updated_at": now,
        }
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO jobs (id, status, input_dir, output_dir, policy_filter_id, created_at, updated_at) VALUES (:id, :status, :input_dir, :output_dir, :policy_filter_id, :created_at, :updated_at)",
                row,
            )
            await db.commit()
        return row

    async def get(self, job_id: str) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = await cursor.fetchone()
            if row is None:
                return None
            return dict(row)

    async def list_jobs(self, status: str | None = None) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if status:
                cursor = await db.execute("SELECT * FROM jobs WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor = await db.execute("SELECT * FROM jobs ORDER BY created_at DESC")
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def update_status(self, job_id: str, status: JobState, error: str | None = None, manifest: dict[str, Any] | None = None) -> None:
        now = datetime.now(timezone.utc).isoformat()
        fields = ["status = ?", "updated_at = ?"]
        values: list[Any] = [status, now]

        if status == JobState.RUNNING:
            fields.append("started_at = ?")
            values.append(now)
        elif status in (JobState.COMPLETED, JobState.FAILED):
            fields.append("completed_at = ?")
            values.append(now)

        if error is not None:
            fields.append("error = ?")
            values.append(error)

        if manifest is not None:
            fields.append("manifest = ?")
            values.append(json.dumps(manifest))

        values.append(job_id)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?", values)
            await db.commit()

    async def delete(self, job_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            await db.commit()
            return cursor.rowcount > 0
