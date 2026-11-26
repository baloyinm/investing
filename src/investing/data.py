"""Load and validate a price CSV with columns date (YYYY-MM-DD) and close."""
import csv
import math
from datetime import date


class PriceDataError(ValueError):
    """The price file is malformed. The message says which line and why."""


def load_prices(path):
    """Return a list of (date, close) sorted by date. Rejects bad rows instead of guessing."""
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = [f.strip().lower() for f in (reader.fieldnames or [])]
        if "date" not in fields or "close" not in fields:
            raise PriceDataError("header must contain 'date' and 'close'")
        for n, raw in enumerate(reader, start=2):
            row = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if k}
            try:
                d = date.fromisoformat(row["date"])
            except ValueError:
                raise PriceDataError(f"line {n}: bad date {row['date']!r}") from None
            try:
                c = float(row["close"])
            except ValueError:
                raise PriceDataError(f"line {n}: bad close {row['close']!r}") from None
            if not math.isfinite(c) or c <= 0:
                raise PriceDataError(f"line {n}: close must be a positive number")
            rows.append((d, c))
    if len(rows) < 2:
        raise PriceDataError("need at least 2 rows")
    rows.sort(key=lambda r: r[0])
    for a, b in zip(rows, rows[1:]):
        if a[0] == b[0]:
            raise PriceDataError(f"duplicate date {a[0]}")
    return rows
