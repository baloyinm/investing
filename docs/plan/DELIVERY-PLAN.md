# Delivery plan: investing

Updated 2026-11-26. This repo is PUBLIC: no secrets, no personal data, no account details in git.

## What it is for
Scripts and data engineering for investing research: loading price data, validating it, and computing risk and return metrics. Software only, not advice. No live trades.

## Done on 2026-11-26
| Item | Acceptance check | Status |
| --- | --- | --- |
| Price CSV loader with validation (`investing.load_prices`) | pytest: 6 bad-file cases rejected with a line-numbered message | Verified |
| Metrics: returns, CAGR, volatility, max drawdown, Sharpe (`investing.metrics`) | pytest known-value checks | Verified |
| CLI `python -m investing file.csv` prints a JSON summary | pytest `test_cli` | Verified |
| CI: pytest, pip-audit, gitleaks | workflow present; first run result recorded below | NOT VERIFIED until the Actions result is read |

## Unfinished (each with its acceptance check)
1. Data sources: pick one free, licensed source (for example a broker export or JSE/Yahoo CSV) and write a fetch script that respects its terms. Check: one real CSV loads. Waiting on Ntsakisi to choose the source.
2. Handle splits and dividends (adjusted close). Check: a fixture with a split gives the same return as the adjusted series.
3. Currency conversion to ZAR with dated rates. Check: a USD series converted with fixture rates matches hand calculation.
4. Shared metrics with Stock-Portfolio: one library component (see LIBRARY-TODO.md). Check: both repos import it.
