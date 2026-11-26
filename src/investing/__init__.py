"""Investing helpers: price-series loading and risk/return metrics. Software only, not advice."""
from .data import load_prices, PriceDataError
from .metrics import simple_returns, cagr, annual_volatility, max_drawdown, sharpe_ratio, summary

__all__ = ["load_prices", "PriceDataError", "simple_returns", "cagr", "annual_volatility",
           "max_drawdown", "sharpe_ratio", "summary"]
