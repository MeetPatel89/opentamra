from pathlib import Path

from backend.datasource.local import LocalFileSystemSource
from backend.pipeline.context import PipelineContext
from backend.pipeline.engine import run_pipeline
from backend.settings import Settings

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_pipeline_runs(tmp_path: Path) -> None:
    settings = Settings(
        paths_input_dir=FIXTURES,
        paths_output_dir=tmp_path / "output",
        paths_db_path=tmp_path / "test.db",
    )
    datasource = LocalFileSystemSource(base_dir=FIXTURES)
    ctx = PipelineContext(
        job_id="test-001",
        settings=settings,
        input_dir=FIXTURES,
        output_dir=tmp_path / "output",
        datasource=datasource,
    )
    result = run_pipeline(ctx)
    assert len(result.frames) > 0
    assert len(result.diagnostics) > 0
