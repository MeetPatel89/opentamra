from __future__ import annotations

from pathlib import Path

from backend.datasource.local import LocalFileSystemSource
from backend.pipeline.context import PipelineContext
from backend.pipeline.engine import run_pipeline
from backend.settings import Settings

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_full_pipeline_mec_determination(tmp_path: Path) -> None:
    """Run full pipeline against fixture data and verify MEC/non-MEC for all 12 policies."""
    settings = Settings(
        paths_input_dir=FIXTURES,
        paths_output_dir=tmp_path / "output",
        paths_db_path=tmp_path / "test.db",
    )
    datasource = LocalFileSystemSource(base_dir=FIXTURES)
    ctx = PipelineContext(
        job_id="integration-001",
        settings=settings,
        input_dir=FIXTURES,
        output_dir=tmp_path / "output",
        datasource=datasource,
    )

    result = run_pipeline(ctx)

    assert "mec_summary" in result.frames
    df = result.frames["mec_summary"]
    # Collect if lazy
    import polars as pl

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    assert len(df) == 12

    # Build lookup: policy_id -> (is_mec, mec_year)
    lookup = {}
    for row in df.iter_rows(named=True):
        lookup[row["policy_id"]] = (row["is_mec"], row["mec_year"])

    # Expected MEC status per plan
    # Non-MEC policies
    for pol_id in ["POL001", "POL003", "POL005", "POL007", "POL009", "POL011"]:
        is_mec, mec_year = lookup[pol_id]
        assert is_mec is False, f"{pol_id} should be non-MEC"
        assert mec_year is None, f"{pol_id} should have no mec_year"

    # MEC year 1 policies
    for pol_id in ["POL002", "POL006", "POL008", "POL010"]:
        is_mec, mec_year = lookup[pol_id]
        assert is_mec is True, f"{pol_id} should be MEC"
        assert mec_year == 1, f"{pol_id} should be MEC in year 1"

    # POL004: MEC year 2
    assert lookup["POL004"][0] is True
    assert lookup["POL004"][1] == 2

    # POL012: MEC year 3
    assert lookup["POL012"][0] is True
    assert lookup["POL012"][1] == 3
