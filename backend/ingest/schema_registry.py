from __future__ import annotations

import polars as pl
from polars.datatypes import DataTypeClass

# Maps file type/name to expected column schemas.
# Each entry is a dict of column_name -> polars dtype.
# Extend this as more input files are defined.
SCHEMAS: dict[str, dict[str, DataTypeClass]] = {
    "policies": {
        "policy_id": pl.Utf8,
        "product_type": pl.Utf8,
        "issue_date": pl.Date,
        "issue_age": pl.Int64,
        "gender": pl.Utf8,
        "face_amount": pl.Float64,
        "smoker_status": pl.Utf8,
    },
    "premiums": {
        "policy_id": pl.Utf8,
        "payment_date": pl.Date,
        "premium_amount": pl.Float64,
        "policy_year": pl.Int64,
    },
    "seven_pay_factors": {
        "product_type": pl.Utf8,
        "gender": pl.Utf8,
        "age_low": pl.Int64,
        "age_high": pl.Int64,
        "seven_pay_factor": pl.Float64,
    },
}


def get_schema(file_type: str) -> dict[str, DataTypeClass] | None:
    return SCHEMAS.get(file_type)
