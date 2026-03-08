from __future__ import annotations

import polars as pl

from backend.pipeline.base_step import BaseStep
from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import register_step


@register_step
class CumulativePremiumTestStep(BaseStep):
    name = "s03_cumulative_premium_test"
    order = 30
    output_level = "intermediate"

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        premiums = ctx.frames["premiums"]
        enriched = ctx.frames["policies_enriched"]

        # Aggregate premiums by policy_id and policy_year
        annual = (
            premiums.group_by("policy_id", "policy_year")
            .agg(pl.col("premium_amount").sum().alias("annual_premium"))
            .sort("policy_id", "policy_year")
        )

        # Compute cumulative premium per policy
        annual = annual.with_columns(
            pl.col("annual_premium").cum_sum().over("policy_id").alias("cumulative_premium")
        )

        # Join with enriched policies to get 7-pay limit
        test = annual.join(
            enriched.select("policy_id", "seven_pay_annual_limit"),
            on="policy_id",
            how="left",
        )

        # Compute cumulative limit and whether it is exceeded (strict >)
        test = test.with_columns(
            (pl.col("seven_pay_annual_limit") * pl.col("policy_year")).alias("cumulative_limit"),
        ).with_columns(
            (pl.col("cumulative_premium") > pl.col("cumulative_limit")).alias("exceeds_limit"),
        )

        ctx.frames["premium_test"] = test
        ctx.add_diagnostic(self.name, "Computed cumulative premium test")
        return ctx
