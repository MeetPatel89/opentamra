from __future__ import annotations

import polars as pl

from backend.pipeline.base_step import BaseStep
from backend.pipeline.context import PipelineContext
from backend.pipeline.registry import register_step


@register_step
class EnrichPoliciesStep(BaseStep):
    name = "s02_enrich_policies"
    order = 20
    output_level = "intermediate"

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        policies = ctx.frames["policies"]
        factors = ctx.frames["seven_pay_factors"]

        # Rename factor columns to avoid suffix collisions on join
        factors_renamed = factors.rename(
            {
                "product_type": "factor_product_type",
                "gender": "factor_gender",
            }
        )

        # Cross-join then filter to match product_type, gender, and age band
        enriched = (
            policies.join(factors_renamed, how="cross")
            .filter(
                (pl.col("product_type") == pl.col("factor_product_type"))
                & (pl.col("gender") == pl.col("factor_gender"))
                & (pl.col("issue_age") >= pl.col("age_low"))
                & (pl.col("issue_age") <= pl.col("age_high"))
            )
            .with_columns(
                (pl.col("face_amount") / 1000.0 * pl.col("seven_pay_factor")).alias(
                    "seven_pay_annual_limit"
                )
            )
            .drop("factor_product_type", "factor_gender", "age_low", "age_high")
        )

        ctx.frames["policies_enriched"] = enriched
        ctx.add_diagnostic(self.name, "Enriched policies with 7-pay annual limits")
        return ctx
