"""Generate synthetic test data for OpenTAMRA."""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import polars as pl


def generate_policies(n: int = 100) -> pl.DataFrame:
    random.seed(42)
    base_date = date(2015, 1, 1)
    product_types = ["whole_life", "universal_life", "variable_life"]
    genders = ["M", "F"]
    rows = []
    for i in range(n):
        issue_date = base_date + timedelta(days=random.randint(0, 3000))
        face = random.choice([100_000, 250_000, 500_000, 750_000, 1_000_000])
        rows.append(
            {
                "policy_id": f"POL{i + 1:05d}",
                "product_type": random.choice(product_types),
                "issue_date": issue_date,
                "issue_age": random.randint(20, 75),
                "gender": random.choice(genders),
                "face_amount": round(face, 2),
                "smoker_status": random.choice(["NS", "S"]),
            }
        )
    return pl.DataFrame(rows)


def main() -> None:
    output = Path("data/input")
    output.mkdir(parents=True, exist_ok=True)

    df = generate_policies(100)
    path = output / "policies.csv"
    df.write_csv(path)
    print(f"Wrote {len(df)} policies to {path}")


if __name__ == "__main__":
    main()
