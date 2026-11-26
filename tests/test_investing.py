import json
from datetime import date
import pytest
from investing import load_prices, PriceDataError, simple_returns, cagr, max_drawdown, annual_volatility, summary
from investing.__main__ import main

P = [(date(2024, 1, 1), 100.0), (date(2024, 1, 2), 110.0), (date(2024, 1, 3), 99.0), (date(2025, 1, 1), 121.0)]


def test_returns():
    assert simple_returns(P)[:2] == pytest.approx([0.10, -0.10])


def test_cagr_doubling_in_one_year():
    s = [(date(2024, 1, 1), 100.0), (date(2025, 1, 1), 200.0)]
    assert cagr(s) == pytest.approx(1.0, abs=0.01)


def test_max_drawdown():
    assert max_drawdown(P) == pytest.approx(-0.10)
    assert max_drawdown([(date(2024, 1, 1), 1.0), (date(2024, 1, 2), 2.0)]) == 0.0


def test_volatility_zero_for_constant_growth_is_nonnegative():
    assert annual_volatility(P) > 0


def write(tmp_path, text):
    f = tmp_path / "p.csv"
    f.write_text(text)
    return f


def test_load_sorts_and_validates(tmp_path):
    f = write(tmp_path, "Date,Close\n2024-01-02,11\n2024-01-01,10\n")
    assert [r[1] for r in load_prices(f)] == [10.0, 11.0]


@pytest.mark.parametrize("text,msg", [
    ("date,price\n2024-01-01,1\n", "header"),
    ("date,close\n2024-01-01,1\n", "at least 2"),
    ("date,close\n2024-01-01,1\n2024-01-01,2\n", "duplicate"),
    ("date,close\n2024-01-01,1\nbad,2\n", "bad date"),
    ("date,close\n2024-01-01,1\n2024-01-02,-3\n", "positive"),
    ("date,close\n2024-01-01,1\n2024-01-02,abc\n", "bad close"),
])
def test_load_rejects_bad_files(tmp_path, text, msg):
    with pytest.raises(PriceDataError, match=msg):
        load_prices(write(tmp_path, text))


def test_cli(tmp_path, capsys):
    f = write(tmp_path, "date,close\n2024-01-01,100\n2024-01-02,101\n2024-01-03,99\n2025-01-01,120\n")
    assert main([str(f)]) == 0
    assert "max_drawdown" in json.loads(capsys.readouterr().out)
    assert main([str(tmp_path / "missing.csv")]) == 1
