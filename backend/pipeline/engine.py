from __future__ import annotations

import logging
import time

import polars as pl

from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import get_ordered_steps

logger = logging.getLogger(__name__)


def run_pipeline(ctx: PipelineContext) -> PipelineContext:
    steps = get_ordered_steps()
    logger.info("Starting pipeline for job %s with %d steps", ctx.job_id, len(steps))

    for step in steps:
        logger.info("Running step: %s (order=%d)", step.name, step.order)
        start = time.perf_counter()

        ctx = step.execute(ctx)

        elapsed = time.perf_counter() - start
        logger.info("Step %s completed in %.2fs", step.name, elapsed)

        if step.output_level and ctx.output_dir and ctx.datasource:
            for frame_name, frame in ctx.frames.items():
                out_path = ctx.output_dir / ctx.job_id / f"{step.name}_{frame_name}"
                fmt = ctx.settings.pipeline_default_output_format
                # Collect once to avoid double-materialization
                df = frame.collect() if isinstance(frame, pl.LazyFrame) else frame
                written = ctx.datasource.write_frame(df, out_path, fmt=fmt)
                ctx.add_to_manifest(step.name, written, len(df))
                logger.info("Wrote %s (%d rows)", written, len(df))

    logger.info("Pipeline complete for job %s", ctx.job_id)
    return ctx
