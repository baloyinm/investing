"""Plain-Python risk and return metrics. Prices are a list of (date, close)."""
import math

TRADING_DAYS = 252


def simple_returns(prices):
    closes = [c for _, c in prices]
    return [b / a - 1 for a, b in zip(closes, closes[1:])]


def cagr(prices):
    (d0, c0), (d1, c1) = prices[0], prices[-1]
    years = (d1 - d0).days / 365.25
    if years <= 0:
        raise ValueError("series spans no time")
    return (c1 / c0) ** (1 / years) - 1


def annual_volatility(prices, periods=TRADING_DAYS):
    r = simple_returns(prices)
    if len(r) < 2:
        raise ValueError("need at least 3 prices")
    m = sum(r) / len(r)
    var = sum((x - m) ** 2 for x in r) / (len(r) - 1)
    return math.sqrt(var) * math.sqrt(periods)


def max_drawdown(prices):
    """Largest peak-to-trough fall as a negative fraction (0.0 if never fell)."""
    peak = prices[0][1]
    worst = 0.0
    for _, c in prices:
        peak = max(peak, c)
        worst = min(worst, c / peak - 1)
    return worst


def sharpe_ratio(prices, risk_free=0.0, periods=TRADING_DAYS):
    vol = annual_volatility(prices, periods)
    if vol == 0:
        raise ValueError("zero volatility")
    r = simple_returns(prices)
    ann = (sum(r) / len(r)) * periods
    return (ann - risk_free) / vol


def summary(prices, risk_free=0.0):
    return {
        "start": prices[0][0].isoformat(), "end": prices[-1][0].isoformat(), "points": len(prices),
        "cagr": cagr(prices), "volatility": annual_volatility(prices),
        "max_drawdown": max_drawdown(prices), "sharpe": sharpe_ratio(prices, risk_free),
    }
