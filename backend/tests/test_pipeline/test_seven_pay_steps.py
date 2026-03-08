from __future__ import annotations

from pathlib import Path

import polars as pl

from backend.pipeline.context import PipelineContext
from backend.pipeline.steps.s02_enrich_policies import EnrichPoliciesStep
from backend.pipeline.steps.s03_cumulative_premium_test import CumulativePremiumTestStep
from backend.pipeline.steps.s04_mec_determination import MECDeterminationStep
from backend.settings import Settings


def _make_ctx(tmp_path: Path, frames: dict[str, pl.LazyFrame]) -> PipelineContext:
    settings = Settings(
        paths_input_dir=tmp_path,
        paths_output_dir=tmp_path / "output",
        paths_db_path=tmp_path / "test.db",
    )
    return PipelineContext(job_id="test", settings=settings, frames=frames)


def _policies_frame() -> pl.LazyFrame:
    return pl.LazyFrame(
        {
            "policy_id": ["P1", "P2"],
            "product_type": ["whole_life", "whole_life"],
            "issue_date": ["2020-01-01", "2020-01-01"],
            "issue_age": [35, 60],
            "gender": ["M", "F"],
            "face_amount": [500_000.0, 200_000.0],
            "smoker_status": ["NS", "NS"],
        }
    )


def _factors_frame() -> pl.LazyFrame:
    return pl.LazyFrame(
        {
            "product_type": ["whole_life", "whole_life"],
            "gender": ["M", "F"],
            "age_low": [30, 60],
            "age_high": [39, 69],
            "seven_pay_factor": [5.20, 11.80],
        }
    )


# --- s02: Enrich Policies ---


def test_enrich_policies_adds_seven_pay_limit(tmp_path: Path) -> None:
    frames = {"policies": _policies_frame(), "seven_pay_factors": _factors_frame()}
    ctx = _make_ctx(tmp_path, frames)

    result = EnrichPoliciesStep().execute(ctx)
    df = result.frames["policies_enriched"].collect()

    assert "seven_pay_annual_limit" in df.columns
    assert len(df) == 2

    p1 = df.filter(pl.col("policy_id") == "P1")
    assert p1["seven_pay_annual_limit"][0] == 500_000.0 / 1000 * 5.20  # 2600.0

    p2 = df.filter(pl.col("policy_id") == "P2")
    assert p2["seven_pay_annual_limit"][0] == 200_000.0 / 1000 * 11.80  # 2360.0


def test_enrich_policies_handles_age_band_boundaries(tmp_path: Path) -> None:
    policies = pl.LazyFrame(
        {
            "policy_id": ["A29", "A30", "A59", "A60", "A70"],
            "product_type": ["whole_life"] * 5,
            "issue_date": ["2020-01-01"] * 5,
            "issue_age": [29, 30, 59, 60, 70],
            "gender": ["M"] * 5,
            "face_amount": [100_000.0] * 5,
            "smoker_status": ["NS"] * 5,
        }
    )
    factors = pl.LazyFrame(
        {
            "product_type": ["whole_life"] * 4,
            "gender": ["M"] * 4,
            "age_low": [20, 30, 50, 60],
            "age_high": [29, 39, 59, 69],
            "seven_pay_factor": [4.50, 5.20, 9.10, 12.50],
        }
    )
    ctx = _make_ctx(tmp_path, {"policies": policies, "seven_pay_factors": factors})

    result = EnrichPoliciesStep().execute(ctx)
    df = result.frames["policies_enriched"].collect().sort("policy_id")

    assert len(df) == 4  # A70 has no matching band
    ids = df["policy_id"].to_list()
    assert "A29" in ids
    assert "A30" in ids
    assert "A59" in ids
    assert "A60" in ids
    assert "A70" not in ids


# --- s03: Cumulative Premium Test ---


def test_cumulative_premium_test_computes_correctly(tmp_path: Path) -> None:
    enriched = pl.LazyFrame(
        {
            "policy_id": ["P1"],
            "product_type": ["whole_life"],
            "issue_date": ["2020-01-01"],
            "issue_age": [35],
            "gender": ["M"],
            "face_amount": [100_000.0],
            "smoker_status": ["NS"],
            "seven_pay_factor": [5.20],
            "seven_pay_annual_limit": [520.0],
        }
    )
    premiums = pl.LazyFrame(
        {
            "policy_id": ["P1", "P1", "P1"],
            "payment_date": ["2020-01-01", "2021-01-01", "2022-01-01"],
            "premium_amount": [500.0, 500.0, 600.0],
            "policy_year": [1, 2, 3],
        }
    )
    ctx = _make_ctx(tmp_path, {"policies_enriched": enriched, "premiums": premiums})

    result = CumulativePremiumTestStep().execute(ctx)
    df = result.frames["premium_test"].collect().sort("policy_year")

    assert len(df) == 3
    # Year 1: 500 cumul, limit 520 → not exceeded
    assert df["exceeds_limit"][0] is False
    # Year 2: 1000 cumul, limit 1040 → not exceeded
    assert df["exceeds_limit"][1] is False
    # Year 3: 1600 cumul, limit 1560 → exceeded
    assert df["exceeds_limit"][2] is True


# --- s04: MEC Determination ---


def test_mec_determination_identifies_mec(tmp_path: Path) -> None:
    enriched = pl.LazyFrame(
        {
            "policy_id": ["P1"],
            "product_type": ["whole_life"],
            "issue_date": ["2020-01-01"],
            "issue_age": [35],
            "gender": ["M"],
            "face_amount": [100_000.0],
            "seven_pay_annual_limit": [520.0],
        }
    )
    premium_test = pl.LazyFrame(
        {
            "policy_id": ["P1", "P1", "P1"],
            "policy_year": [1, 2, 3],
            "annual_premium": [500.0, 500.0, 600.0],
            "cumulative_premium": [500.0, 1000.0, 1600.0],
            "seven_pay_annual_limit": [520.0, 520.0, 520.0],
            "cumulative_limit": [520.0, 1040.0, 1560.0],
            "exceeds_limit": [False, False, True],
        }
    )
    ctx = _make_ctx(tmp_path, {"policies_enriched": enriched, "premium_test": premium_test})

    result = MECDeterminationStep().execute(ctx)
    df = result.frames["mec_summary"].collect()

    assert len(df) == 1
    assert df["is_mec"][0] is True
    assert df["mec_year"][0] == 3
    assert df["total_premiums_paid"][0] == 1600.0


def test_mec_determination_identifies_non_mec(tmp_path: Path) -> None:
    enriched = pl.LazyFrame(
        {
            "policy_id": ["P1"],
            "product_type": ["whole_life"],
            "issue_date": ["2020-01-01"],
            "issue_age": [35],
            "gender": ["M"],
            "face_amount": [100_000.0],
            "seven_pay_annual_limit": [520.0],
        }
    )
    premium_test = pl.LazyFrame(
        {
            "policy_id": ["P1", "P1"],
            "policy_year": [1, 2],
            "annual_premium": [400.0, 400.0],
            "cumulative_premium": [400.0, 800.0],
            "seven_pay_annual_limit": [520.0, 520.0],
            "cumulative_limit": [520.0, 1040.0],
            "exceeds_limit": [False, False],
        }
    )
    ctx = _make_ctx(tmp_path, {"policies_enriched": enriched, "premium_test": premium_test})

    result = MECDeterminationStep().execute(ctx)
    df = result.frames["mec_summary"].collect()

    assert len(df) == 1
    assert df["is_mec"][0] is False
    assert df["mec_year"][0] is None
    assert df["total_premiums_paid"][0] == 800.0


def test_mec_determination_exact_limit_is_not_mec(tmp_path: Path) -> None:
    enriched = pl.LazyFrame(
        {
            "policy_id": ["P1"],
            "product_type": ["whole_life"],
            "issue_date": ["2020-01-01"],
            "issue_age": [35],
            "gender": ["M"],
            "face_amount": [100_000.0],
            "seven_pay_annual_limit": [520.0],
        }
    )
    premium_test = pl.LazyFrame(
        {
            "policy_id": ["P1"],
            "policy_year": [1],
            "annual_premium": [520.0],
            "cumulative_premium": [520.0],
            "seven_pay_annual_limit": [520.0],
            "cumulative_limit": [520.0],
            "exceeds_limit": [False],  # 520 == 520 → strict > means NOT exceeded
        }
    )
    ctx = _make_ctx(tmp_path, {"policies_enriched": enriched, "premium_test": premium_test})

    result = MECDeterminationStep().execute(ctx)
    df = result.frames["mec_summary"].collect()

    assert len(df) == 1
    assert df["is_mec"][0] is False
    assert df["mec_year"][0] is None
