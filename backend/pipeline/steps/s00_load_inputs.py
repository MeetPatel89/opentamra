from __future__ import annotations

from backend.core.exceptions import PipelineError
from backend.datasource.local import LocalFileSystemSource
from backend.ingest.policy_filter import apply_policy_filter
from backend.pipeline.base_step import BaseStep
from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import register_step


@register_step
class LoadInputsStep(BaseStep):
    name = "s00_load_inputs"
    order = 0
    output_level = "raw"

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        input_dir = ctx.input_dir or ctx.settings.paths_input_dir
        ds = ctx.datasource or LocalFileSystemSource(base_dir=input_dir)

        files = ds.list_files(pattern="*.csv")
        if not files:
            raise PipelineError(f"No CSV files found in {input_dir}")

        frames = {f.stem: ds.read_frame(f) for f in files}

        if ctx.policy_filter:
            for name, frame in frames.items():
                schema_cols = frame.collect_schema().names()
                if "policy_id" in schema_cols:
                    frames[name] = apply_policy_filter(frame, ctx.policy_filter)

        ctx.frames = frames
        ctx.add_diagnostic(self.name, f"Loaded {len(frames)} file(s) from {input_dir}")
        return ctx
