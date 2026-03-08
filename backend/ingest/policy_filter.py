from __future__ import annotations

from pathlib import Path

import polars as pl


def load_policy_filter(path: Path) -> list[str]:
    df = pl.read_csv(path)
    # Expect a single column with policy IDs, or a column named "policy_id"
    if "policy_id" in df.columns:
        return df["policy_id"].cast(pl.Utf8).to_list()
    # Fall back to first column
    return df[df.columns[0]].cast(pl.Utf8).to_list()


def apply_policy_filter(
    frame: pl.LazyFrame, policy_ids: list[str], column: str = "policy_id"
) -> pl.LazyFrame:
    return frame.filter(pl.col(column).cast(pl.Utf8).is_in(policy_ids))
