"""Tests for navigation/tren_harga.py — price trend charts and computations."""

import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, MagicMock, PropertyMock


class TestYearRangeFiltering:
    """Date-range filtering used by the Tren Harga page."""

    def test_year_min_max(self, multi_year_df):
        tahun_min = int(multi_year_df["date"].dt.year.min())
        tahun_max = int(multi_year_df["date"].dt.year.max())
        assert tahun_min == 2015
        assert tahun_max == 2024

    def test_filter_by_year_range(self, multi_year_df):
        batas_awal = pd.Timestamp("2018-01-01")
        batas_akhir = pd.Timestamp("2020-12-31")
        df_f = multi_year_df[
            (multi_year_df["date"] >= batas_awal) & (multi_year_df["date"] <= batas_akhir)
        ]
        years = df_f["date"].dt.year.unique()
        assert set(years) == {2018, 2019, 2020}

    def test_filter_single_year(self, multi_year_df):
        batas_awal = pd.Timestamp("2022-01-01")
        batas_akhir = pd.Timestamp("2022-12-31")
        df_f = multi_year_df[
            (multi_year_df["date"] >= batas_awal) & (multi_year_df["date"] <= batas_akhir)
        ]
        assert all(df_f["date"].dt.year == 2022)

    def test_filter_full_range(self, multi_year_df):
        batas_awal = pd.Timestamp("2015-01-01")
        batas_akhir = pd.Timestamp("2024-12-31")
        df_f = multi_year_df[
            (multi_year_df["date"] >= batas_awal) & (multi_year_df["date"] <= batas_akhir)
        ]
        assert len(df_f) == len(multi_year_df)


class TestDrawdownCalculation:
    """Drawdown from ATH calculation."""

    def test_drawdown_at_ath_is_zero(self, sample_df):
        ath = sample_df["close"].max()
        df = sample_df.copy()
        df["drawdown"] = (df["close"] - ath) / ath * 100
        ath_row = df.loc[df["close"] == ath]
        assert pytest.approx(ath_row["drawdown"].iloc[0]) == 0.0

    def test_drawdown_always_nonpositive(self, sample_df):
        ath = sample_df["close"].max()
        df = sample_df.copy()
        df["drawdown"] = (df["close"] - ath) / ath * 100
        assert all(df["drawdown"] <= 0)

    def test_drawdown_min_value(self, sample_df):
        ath = sample_df["close"].max()
        df = sample_df.copy()
        df["drawdown"] = (df["close"] - ath) / ath * 100
        expected_min = (sample_df["close"].min() - ath) / ath * 100
        assert pytest.approx(df["drawdown"].min()) == expected_min

    def test_drawdown_formula_specific(self):
        df = pd.DataFrame({"close": [100, 80, 60, 100]})
        ath = df["close"].max()
        df["drawdown"] = (df["close"] - ath) / ath * 100
        assert pytest.approx(df["drawdown"].iloc[2]) == -40.0


class TestPerformanceCalculation:
    """Period performance (% change) calculation."""

    def test_positive_performance(self, sample_df):
        perf = (
            (sample_df["close"].iloc[-1] - sample_df["close"].iloc[0])
            / sample_df["close"].iloc[0]
            * 100
        )
        expected = (8000 - 7200) / 7200 * 100
        assert pytest.approx(perf, rel=1e-4) == expected

    def test_negative_performance(self):
        df = pd.DataFrame({"close": [100, 80]})
        perf = (df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100
        assert pytest.approx(perf) == -20.0

    def test_zero_performance(self):
        df = pd.DataFrame({"close": [100, 100]})
        perf = (df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100
        assert perf == 0.0


class TestVolumeColorLogic:
    """Volume bar color assignment (green if close >= open, else red)."""

    def test_green_when_close_ge_open(self, sample_df):
        CMC_GREEN = "#16C784"
        CMC_RED = "#EA3943"
        colors = [
            CMC_GREEN if sample_df["close"].iloc[i] >= sample_df["open"].iloc[i] else CMC_RED
            for i in range(len(sample_df))
        ]
        for i in range(len(sample_df)):
            if sample_df["close"].iloc[i] >= sample_df["open"].iloc[i]:
                assert colors[i] == CMC_GREEN

    def test_red_when_close_lt_open(self):
        CMC_GREEN = "#16C784"
        CMC_RED = "#EA3943"
        df = pd.DataFrame({"close": [90, 110], "open": [100, 100]})
        colors = [
            CMC_GREEN if df["close"].iloc[i] >= df["open"].iloc[i] else CMC_RED
            for i in range(len(df))
        ]
        assert colors[0] == CMC_RED
        assert colors[1] == CMC_GREEN

    def test_volume_color_length_matches_df(self, sample_df):
        colors = [
            "#16C784" if sample_df["close"].iloc[i] >= sample_df["open"].iloc[i] else "#EA3943"
            for i in range(len(sample_df))
        ]
        assert len(colors) == len(sample_df)


class TestMetricOutputs:
    """Open / Close / Change / Drawdown metric cards."""

    def test_open_metric(self, sample_df):
        batas_awal = pd.Timestamp("2020-01-01")
        batas_akhir = pd.Timestamp("2020-12-31")
        df_f = sample_df[
            (sample_df["date"] >= batas_awal) & (sample_df["date"] <= batas_akhir)
        ]
        assert df_f["open"].iloc[0] == 7100

    def test_close_metric(self, sample_df):
        batas_awal = pd.Timestamp("2020-01-01")
        batas_akhir = pd.Timestamp("2020-12-31")
        df_f = sample_df[
            (sample_df["date"] >= batas_awal) & (sample_df["date"] <= batas_akhir)
        ]
        assert df_f["close"].iloc[-1] == 8000

    def test_drawdown_max_metric(self, sample_df):
        ath = sample_df["close"].max()
        df_f = sample_df.copy()
        df_f["drawdown"] = (df_f["close"] - ath) / ath * 100
        assert df_f["drawdown"].min() < 0


class TestShowTrenHargaIntegration:
    """Call show_tren_harga with mocked Streamlit."""

    @patch("navigation.tren_harga.st")
    def test_show_tren_harga_runs(self, mock_st, sample_df):
        mock_st.slider.return_value = (2020, 2020)
        mock_st.checkbox.return_value = False
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]

        from navigation.tren_harga import show_tren_harga

        show_tren_harga(sample_df)
        assert mock_st.plotly_chart.called

    @patch("navigation.tren_harga.st")
    def test_show_tren_harga_log_scale(self, mock_st, sample_df):
        mock_st.slider.return_value = (2020, 2020)
        mock_st.checkbox.return_value = True
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]

        from navigation.tren_harga import show_tren_harga

        show_tren_harga(sample_df)
        assert mock_st.plotly_chart.call_count == 2
