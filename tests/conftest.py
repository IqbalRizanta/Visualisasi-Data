import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_df():
    """Minimal DataFrame that mirrors the real btc_2015_2024.csv schema."""
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    np.random.seed(42)
    close = [7200, 7350, 7100, 7500, 7400, 7600, 7800, 7750, 7900, 8000]
    open_ = [7100, 7200, 7350, 7100, 7500, 7400, 7600, 7800, 7750, 7900]
    high = [c + 100 for c in close]
    low = [c - 100 for c in close]
    volume = [1e9 + i * 1e8 for i in range(10)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "rsi_7": np.random.uniform(20, 80, 10),
            "rsi_14": np.random.uniform(20, 80, 10),
            "cci_7": np.random.uniform(-100, 100, 10),
            "cci_14": np.random.uniform(-100, 100, 10),
            "sma_50": np.random.uniform(7000, 8000, 10),
            "ema_50": np.random.uniform(7000, 8000, 10),
            "sma_100": np.random.uniform(7000, 8000, 10),
            "ema_100": np.random.uniform(7000, 8000, 10),
            "macd": np.random.uniform(-50, 50, 10),
            "bollinger": np.random.uniform(7500, 8500, 10),
            "TrueRange": np.random.uniform(50, 300, 10),
            "atr_7": np.random.uniform(100, 200, 10),
            "atr_14": np.random.uniform(100, 200, 10),
            "next_day_close": [7350, 7100, 7500, 7400, 7600, 7800, 7750, 7900, 8000, 8100],
        }
    )


@pytest.fixture
def multi_year_df():
    """DataFrame spanning multiple years for year-range filter tests."""
    rows = []
    for year in range(2015, 2025):
        for month in [1, 6]:
            d = pd.Timestamp(f"{year}-{month:02d}-15")
            base = 300 + (year - 2015) * 5000
            rows.append(
                {
                    "date": d,
                    "open": base,
                    "high": base + 200,
                    "low": base - 200,
                    "close": base + 100,
                    "volume": 1e9,
                    "rsi_7": 50.0,
                    "rsi_14": 50.0,
                    "cci_7": 0.0,
                    "cci_14": 0.0,
                    "sma_50": base,
                    "ema_50": base,
                    "sma_100": base,
                    "ema_100": base,
                    "macd": 0.0,
                    "bollinger": base + 300,
                    "TrueRange": 100.0,
                    "atr_7": 100.0,
                    "atr_14": 100.0,
                    "next_day_close": base + 150,
                }
            )
    return pd.DataFrame(rows)
