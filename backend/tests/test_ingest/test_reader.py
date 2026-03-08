from pathlib import Path

from backend.ingest.reader import read_directory, read_file

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_read_csv_file() -> None:
    frame = read_file(FIXTURES / "policies.csv")
    df = frame.collect()
    assert len(df) == 12
    assert "policy_id" in df.columns


def test_read_directory() -> None:
    frames = read_directory(FIXTURES, pattern="*.csv")
    assert len(frames) >= 1
    assert "policies" in frames
