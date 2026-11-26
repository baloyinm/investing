import argparse
import json
import sys
from . import load_prices, summary, PriceDataError


def main(argv=None):
    p = argparse.ArgumentParser(prog="investing", description="Risk/return summary of a price CSV (not advice).")
    p.add_argument("csv")
    p.add_argument("--risk-free", type=float, default=0.0)
    a = p.parse_args(argv)
    try:
        print(json.dumps(summary(load_prices(a.csv), a.risk_free), indent=2))
    except (PriceDataError, ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
