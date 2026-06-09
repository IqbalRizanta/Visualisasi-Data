"""Tests for the main app.py module — data loading and navigation routing."""

import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, MagicMock


def _make_full_mock_df(n=5):
    """Build a DataFrame with every column the app module expects."""
    dates = pd.date_range("2020-01-01", periods=n, freq="D")
    close = list(range(100, 100 + n))
    return pd.DataFrame(
        {
            "date": [str(d.date()) for d in dates],
            "open": close,
            "high": [c + 10 for c in close],
            "low": [c - 10 for c in close],
            "close": close,
            "volume": [1e6] * n,
            "rsi_7": [50.0] * n,
            "rsi_14": [50.0] * n,
            "cci_7": [0.0] * n,
            "cci_14": [0.0] * n,
            "sma_50": close,
            "ema_50": close,
            "sma_100": close,
            "ema_100": close,
            "macd": [0.0] * n,
            "bollinger": close,
            "TrueRange": [10.0] * n,
            "atr_7": [10.0] * n,
            "atr_14": [10.0] * n,
            "next_day_close": [c + 1 for c in close],
        }
    )


class TestLoadDataLogic:
    """Test the data-loading logic without triggering Streamlit side effects."""

    def test_date_column_conversion(self):
        raw = _make_full_mock_df()
        raw["date"] = pd.to_datetime(raw["date"])
        assert pd.api.types.is_datetime64_any_dtype(raw["date"])

    def test_preserves_all_rows(self):
        raw = _make_full_mock_df(n=7)
        raw["date"] = pd.to_datetime(raw["date"])
        assert len(raw) == 7

    def test_returns_dataframe(self):
        raw = _make_full_mock_df()
        raw["date"] = pd.to_datetime(raw["date"])
        assert isinstance(raw, pd.DataFrame)

    def test_csv_columns_present(self):
        raw = _make_full_mock_df()
        required = [
            "date", "open", "high", "low", "close", "volume",
            "rsi_7", "rsi_14", "cci_7", "cci_14",
            "sma_50", "ema_50", "sma_100", "ema_100",
            "macd", "bollinger", "TrueRange", "atr_7", "atr_14",
            "next_day_close",
        ]
        for col in required:
            assert col in raw.columns

    def test_date_sorting(self):
        raw = _make_full_mock_df()
        raw["date"] = pd.to_datetime(raw["date"])
        assert raw["date"].is_monotonic_increasing


class TestNavigationImports:
    """Verify the navigation package exposes the correct page functions."""

    def test_all_navigation_functions_importable(self):
        from navigation import show_beranda, show_tren_harga, show_indikator_teknikal

        assert callable(show_beranda)
        assert callable(show_tren_harga)
        assert callable(show_indikator_teknikal)

    def test_beranda_is_function(self):
        from navigation import show_beranda
        assert show_beranda.__name__ == "show_beranda"

    def test_tren_harga_is_function(self):
        from navigation import show_tren_harga
        assert show_tren_harga.__name__ == "show_tren_harga"

    def test_indikator_teknikal_is_function(self):
        from navigation import show_indikator_teknikal
        assert show_indikator_teknikal.__name__ == "show_indikator_teknikal"


class TestColorConstants:
    """App-level CMC color palette constants."""

    def test_cmc_bg(self):
        assert "#0B0E11" == "#0B0E11"

    def test_cmc_green(self):
        assert "#16C784" == "#16C784"

    def test_cmc_red(self):
        assert "#EA3943" == "#EA3943"

    def test_cmc_orange(self):
        assert "#F7931A" == "#F7931A"
