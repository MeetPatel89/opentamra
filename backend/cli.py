from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Optional

import typer

from backend.datasource.local import LocalFileSystemSource
from backend.ingest.policy_filter import load_policy_filter
from backend.pipeline.context import PipelineContext
from backend.pipeline.engine import run_pipeline
from backend.settings import get_settings

app = typer.Typer(name="opentamra", help="OpenTAMRA CLI")


@app.callback()
def main() -> None:
    """OpenTAMRA — TAMRA tax calculation pipeline."""


@app.command("run")
def run_pipeline_cmd(
    input_dir: Path = typer.Option(..., help="Directory containing input CSV files"),
    output_dir: Path = typer.Option(..., help="Directory for output files"),
    policy_list: Optional[Path] = typer.Option(None, help="Path to policy filter CSV"),
    job_id: Optional[str] = typer.Option(None, help="Job ID (auto-generated if not set)"),
    log_level: str = typer.Option("INFO", help="Logging level"),
) -> None:
    """Run the TAMRA calculation pipeline."""
    logging.basicConfig(level=getattr(logging, log_level.upper()))

    settings = get_settings()
    jid = job_id or uuid.uuid4().hex[:12]

    policy_filter = None
    if policy_list:
        policy_filter = load_policy_filter(policy_list)
        typer.echo(f"Loaded {len(policy_filter)} policy IDs from filter")

    datasource = LocalFileSystemSource(base_dir=input_dir)

    ctx = PipelineContext(
        job_id=jid,
        settings=settings,
        input_dir=input_dir,
        output_dir=output_dir,
        policy_filter=policy_filter,
        datasource=datasource,
    )

    typer.echo(f"Starting pipeline (job_id={jid})")
    ctx = run_pipeline(ctx)
    typer.echo(f"Pipeline complete. Outputs: {len(ctx.manifest)} files")

    for entry in ctx.manifest:
        typer.echo(f"  {entry['path']} ({entry['row_count']} rows)")


if __name__ == "__main__":
    app()
