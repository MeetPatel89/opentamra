from __future__ import annotations

from backend.core.exceptions import ValidationError
from backend.ingest.validator import validate_not_empty, validate_schema
from backend.pipeline.base_step import BaseStep
from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import register_step


@register_step
class ValidateInputsStep(BaseStep):
    name = "s01_validate_inputs"
    order = 10

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        all_errors: list[str] = []

        for name, frame in ctx.frames.items():
            validate_not_empty(frame, name)
            errors = validate_schema(frame, name)
            all_errors.extend(errors)

        if all_errors:
            msg = "Validation errors:\n" + "\n".join(f"  - {e}" for e in all_errors)
            ctx.add_diagnostic(self.name, msg)
            raise ValidationError(msg)

        ctx.add_diagnostic(self.name, f"Validated {len(ctx.frames)} frame(s)")
        return ctx
