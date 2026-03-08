from pathlib import Path

import polars as pl

from backend.ingest.policy_filter import apply_policy_filter, load_policy_filter

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_load_policy_filter() -> None:
    ids = load_policy_filter(FIXTURES / "policy_filter_list.csv")
    assert ids == ["POL001", "POL003", "POL005"]


def test_apply_policy_filter() -> None:
    df = pl.DataFrame({"policy_id": ["POL001", "POL002", "POL003"], "value": [1, 2, 3]})
    filtered = apply_policy_filter(df.lazy(), ["POL001", "POL003"]).collect()
    assert len(filtered) == 2
    assert filtered["policy_id"].to_list() == ["POL001", "POL003"]
