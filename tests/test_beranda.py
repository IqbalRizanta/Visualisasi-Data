"""Tests for navigation/beranda.py — homepage stats, filtering, and display."""

import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, MagicMock, call


class TestPriceCalculations:
    """Verify the core price / delta computations performed in show_beranda."""

    def test_latest_price(self, sample_df):
        assert sample_df["close"].iloc[-1] == 8000

    def test_previous_price(self, sample_df):
        assert sample_df["close"].iloc[-2] == 7900

    def test_price_difference_positive(self, sample_df):
        selisih = sample_df["close"].iloc[-1] - sample_df["close"].iloc[-2]
        assert selisih == 100

    def test_price_percentage_change(self, sample_df):
        harga_now = sample_df["close"].iloc[-1]
        harga_sebelum = sample_df["close"].iloc[-2]
        pct = (harga_now - harga_sebelum) / harga_sebelum * 100
        assert pytest.approx(pct, rel=1e-4) == (100 / 7900) * 100

    def test_delta_class_up(self, sample_df):
        selisih = sample_df["close"].iloc[-1] - sample_df["close"].iloc[-2]
        delta_class = "up" if selisih >= 0 else "down"
        assert delta_class == "up"

    def test_delta_class_down(self):
        df = pd.DataFrame({"close": [100, 90]})
        selisih = df["close"].iloc[-1] - df["close"].iloc[-2]
        delta_class = "up" if selisih >= 0 else "down"
        assert delta_class == "down"

    def test_arrow_symbol_up(self, sample_df):
        selisih = sample_df["close"].iloc[-1] - sample_df["close"].iloc[-2]
        arrow = "\u25b2" if selisih >= 0 else "\u25bc"
        assert arrow == "\u25b2"

    def test_arrow_symbol_down(self):
        df = pd.DataFrame({"close": [100, 90]})
        selisih = df["close"].iloc[-1] - df["close"].iloc[-2]
        arrow = "\u25b2" if selisih >= 0 else "\u25bc"
        assert arrow == "\u25bc"

    def test_zero_change_is_up(self):
        df = pd.DataFrame({"close": [100, 100]})
        selisih = df["close"].iloc[-1] - df["close"].iloc[-2]
        delta_class = "up" if selisih >= 0 else "down"
        assert delta_class == "up"


class TestATHCalculation:
    """All-Time High value and date."""

    def test_ath_value(self, sample_df):
        assert sample_df["close"].max() == 8000

    def test_ath_date(self, sample_df):
        ath_idx = sample_df["close"].idxmax()
        ath_date = sample_df.loc[ath_idx, "date"]
        assert ath_date == pd.Timestamp("2020-01-10")

    def test_ath_date_format(self, sample_df):
        ath_date = sample_df.loc[sample_df["close"].idxmax(), "date"]
        formatted = ath_date.strftime("%d %b %Y")
        assert formatted == "10 Jan 2020"


class TestMarketCapAndStats:
    """Market cap and aggregate statistic computations."""

    def test_market_cap_formula(self, sample_df):
        harga_now = sample_df["close"].iloc[-1]
        market_cap = harga_now * 19_000_000
        assert market_cap == 8000 * 19_000_000

    def test_volume_latest(self, sample_df):
        volume = sample_df["volume"].iloc[-1]
        expected = 1e9 + 9 * 1e8
        assert volume == expected

    def test_close_min(self, sample_df):
        assert sample_df["close"].min() == 7100

    def test_close_mean(self, sample_df):
        expected = np.mean([7200, 7350, 7100, 7500, 7400, 7600, 7800, 7750, 7900, 8000])
        assert pytest.approx(sample_df["close"].mean()) == expected

    def test_missing_values_count(self, sample_df):
        assert sample_df.isna().sum().sum() == 0

    def test_missing_values_with_nans(self, sample_df):
        df = sample_df.copy()
        df.loc[0, "close"] = np.nan
        df.loc[1, "volume"] = np.nan
        assert df.isna().sum().sum() == 2


class TestDatasetMetadata:
    """Period range, row/col count used in the 'Tentang Dataset' section."""

    def test_date_range_days(self, sample_df):
        days = (sample_df["date"].max() - sample_df["date"].min()).days
        assert days == 9

    def test_row_count(self, sample_df):
        assert len(sample_df) == 10

    def test_column_count(self, sample_df):
        assert len(sample_df.columns) == 20

    def test_date_min_format(self, sample_df):
        assert sample_df["date"].min().strftime("%d %b %Y") == "01 Jan 2020"


class TestDataFiltering:
    """Year, price-range, volume-range, and search-text filters from beranda."""

    def test_year_filter(self, multi_year_df):
        tahun_pilih = [2020, 2021]
        filtered = multi_year_df[multi_year_df["date"].dt.year.isin(tahun_pilih)]
        assert all(filtered["date"].dt.year.isin(tahun_pilih))
        assert len(filtered) == 4  # 2 rows per year

    def test_price_range_filter(self, sample_df):
        harga_min, harga_max = 7300, 7600
        filtered = sample_df[
            (sample_df["close"] >= harga_min) & (sample_df["close"] <= harga_max)
        ]
        assert all(filtered["close"] >= harga_min)
        assert all(filtered["close"] <= harga_max)

    def test_volume_range_filter(self, sample_df):
        vol_min, vol_max = 1.0e9, 1.4e9
        filtered = sample_df[
            (sample_df["volume"] >= vol_min) & (sample_df["volume"] <= vol_max)
        ]
        assert all(filtered["volume"] >= vol_min)
        assert all(filtered["volume"] <= vol_max)

    def test_search_text_filter(self, sample_df):
        cari = "7200"
        mask = (
            sample_df.astype(str)
            .apply(lambda x: x.str.contains(cari, case=False, na=False))
            .any(axis=1)
        )
        filtered = sample_df[mask]
        assert len(filtered) > 0

    def test_search_text_no_match(self, sample_df):
        cari = "ZZZZZ_NOMATCH"
        mask = (
            sample_df.astype(str)
            .apply(lambda x: x.str.contains(cari, case=False, na=False))
            .any(axis=1)
        )
        filtered = sample_df[mask]
        assert len(filtered) == 0

    def test_combined_filters(self, multi_year_df):
        tahun_pilih = [2020]
        harga_min, harga_max = 0, 100_000
        filtered = multi_year_df[multi_year_df["date"].dt.year.isin(tahun_pilih)]
        filtered = filtered[
            (filtered["close"] >= harga_min) & (filtered["close"] <= harga_max)
        ]
        assert len(filtered) == 2


class TestShowBerandaIntegration:
    """Call show_beranda with mocked Streamlit to ensure no runtime errors."""

    @patch("navigation.beranda.st")
    def test_show_beranda_runs_without_error(self, mock_st, sample_df):
        mock_st.text_input.return_value = ""
        mock_st.multiselect.return_value = sorted(
            sample_df["date"].dt.year.unique()
        )
        mock_st.slider.side_effect = [
            (float(sample_df["close"].min()), float(sample_df["close"].max())),
            (float(sample_df["volume"].min()), float(sample_df["volume"].max())),
        ]
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

        from navigation.beranda import show_beranda

        show_beranda(sample_df)
        assert mock_st.markdown.called

    @patch("navigation.beranda.st")
    def test_show_beranda_with_search_text(self, mock_st, sample_df):
        mock_st.text_input.return_value = "7200"
        mock_st.multiselect.return_value = sorted(
            sample_df["date"].dt.year.unique()
        )
        mock_st.slider.side_effect = [
            (float(sample_df["close"].min()), float(sample_df["close"].max())),
            (float(sample_df["volume"].min()), float(sample_df["volume"].max())),
        ]
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

        from navigation.beranda import show_beranda

        show_beranda(sample_df)
        assert mock_st.dataframe.called

    @patch("navigation.beranda.st")
    def test_show_beranda_calls_divider(self, mock_st, sample_df):
        mock_st.text_input.return_value = ""
        mock_st.multiselect.return_value = sorted(
            sample_df["date"].dt.year.unique()
        )
        mock_st.slider.side_effect = [
            (float(sample_df["close"].min()), float(sample_df["close"].max())),
            (float(sample_df["volume"].min()), float(sample_df["volume"].max())),
        ]
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

        from navigation.beranda import show_beranda

        show_beranda(sample_df)
        mock_st.divider.assert_called()
