from __future__ import annotations

import polars as pl

from backend.core.exceptions import ValidationError
from backend.ingest.schema_registry import get_schema


def validate_schema(frame: pl.LazyFrame, file_type: str) -> list[str]:
    schema = get_schema(file_type)
    if schema is None:
        return []

    errors: list[str] = []
    actual_columns = frame.collect_schema().names()

    for col_name in schema:
        if col_name not in actual_columns:
            errors.append(f"Missing required column: {col_name}")

    return errors


def validate_not_empty(frame: pl.LazyFrame, name: str) -> None:
    row_count = frame.select(pl.len()).collect().item()
    if row_count == 0:
        raise ValidationError(f"Input '{name}' contains no rows")


def validate_no_nulls(frame: pl.LazyFrame, columns: list[str], name: str) -> list[str]:
    errors: list[str] = []
    df = frame.collect()
    for col in columns:
        if col in df.columns:
            null_count = df[col].null_count()
            if null_count > 0:
                errors.append(f"Column '{col}' in '{name}' has {null_count} null values")
    return errors
