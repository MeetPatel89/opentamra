from __future__ import annotations

import polars as pl

from backend.pipeline.base_step import BaseStep
from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import register_step


@register_step
class MECDeterminationStep(BaseStep):
    name = "s04_mec_determination"
    order = 40
    output_level = "final"

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        premium_test = ctx.frames["premium_test"]
        enriched = ctx.frames["policies_enriched"]

        # Find earliest year exceeding limit per policy
        mec_year = (
            premium_test.filter(pl.col("exceeds_limit"))
            .group_by("policy_id")
            .agg(pl.col("policy_year").min().alias("mec_year"))
        )

        # Total premiums paid per policy
        total_premiums = premium_test.group_by("policy_id").agg(
            pl.col("annual_premium").sum().alias("total_premiums_paid")
        )

        # Build final summary from enriched policies
        summary = (
            enriched.select(
                "policy_id",
                "product_type",
                "issue_date",
                "issue_age",
                "gender",
                "face_amount",
                "seven_pay_annual_limit",
            )
            .join(mec_year, on="policy_id", how="left")
            .join(total_premiums, on="policy_id", how="left")
            .with_columns(
                pl.col("mec_year").is_not_null().alias("is_mec"),
                pl.col("total_premiums_paid").fill_null(0.0),
            )
        )

        ctx.frames["mec_summary"] = summary
        ctx.add_diagnostic(self.name, "Determined MEC status for all policies")
        return ctx
