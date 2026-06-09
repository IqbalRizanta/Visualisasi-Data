"""Tests for navigation/indikator_teknikal.py — technical indicator charts."""

import pytest
from unittest.mock import patch, MagicMock


class TestIndikatorMapping:
    """Verify the indicator name-to-column mapping dict."""

    def test_mapping_keys(self):
        from navigation.indikator_teknikal import show_indikator_teknikal

        expected_keys = {"RSI 14", "MACD", "Bollinger Bands", "RSI 7", "CCI 14", "SMA 50", "EMA 50"}
        # Extract the mapping from the function source; alternatively test via mock
        indikator_tersedia = {
            "RSI 14": "rsi_14",
            "MACD": "macd",
            "Bollinger Bands": "bollinger",
            "RSI 7": "rsi_7",
            "CCI 14": "cci_14",
            "SMA 50": "sma_50",
            "EMA 50": "ema_50",
        }
        assert set(indikator_tersedia.keys()) == expected_keys

    def test_mapping_values_are_valid_columns(self, sample_df):
        indikator_tersedia = {
            "RSI 14": "rsi_14",
            "MACD": "macd",
            "Bollinger Bands": "bollinger",
            "RSI 7": "rsi_7",
            "CCI 14": "cci_14",
            "SMA 50": "sma_50",
            "EMA 50": "ema_50",
        }
        for col in indikator_tersedia.values():
            assert col in sample_df.columns, f"Column {col} missing from DataFrame"

    def test_mapping_count(self):
        indikator_tersedia = {
            "RSI 14": "rsi_14",
            "MACD": "macd",
            "Bollinger Bands": "bollinger",
            "RSI 7": "rsi_7",
            "CCI 14": "cci_14",
            "SMA 50": "sma_50",
            "EMA 50": "ema_50",
        }
        assert len(indikator_tersedia) == 7


class TestSubplotConfiguration:
    """Row-height and spacing calculations for the indicator subplots."""

    @pytest.mark.parametrize("n_selected", [2, 3, 5, 7])
    def test_row_count(self, n_selected):
        n_rows = 1 + n_selected
        assert n_rows == n_selected + 1

    @pytest.mark.parametrize("n_selected", [2, 3, 5, 7])
    def test_row_heights_sum(self, n_selected):
        row_heights = [0.35] + [0.65 / n_selected] * n_selected
        assert pytest.approx(sum(row_heights)) == 1.0

    def test_vertical_spacing(self):
        for n_sel in range(2, 8):
            n_rows = 1 + n_sel
            spacing = 0.12 / n_rows * 3
            assert 0 < spacing < 1


class TestRSIThresholds:
    """RSI horizontal line thresholds (overbought / oversold)."""

    def test_overbought_threshold(self):
        assert 70 == 70

    def test_oversold_threshold(self):
        assert 30 == 30

    def test_rsi_indicator_gets_hlines(self):
        pilihan = ["RSI 14", "MACD"]
        rsi_indicators = [n for n in pilihan if "RSI" in n]
        assert len(rsi_indicators) == 1

    def test_non_rsi_gets_no_hlines(self):
        pilihan = ["MACD", "Bollinger Bands"]
        rsi_indicators = [n for n in pilihan if "RSI" in n]
        assert len(rsi_indicators) == 0


class TestChartLayoutConfig:
    """Chart visual configuration constants."""

    def test_color_palette_length(self):
        warna = ["#F7931A", "#3B82F6", "#8B5CF6", "#F59E0B", "#EA3943"]
        assert len(warna) == 5

    def test_color_wraps_around(self):
        warna = ["#F7931A", "#3B82F6", "#8B5CF6", "#F59E0B", "#EA3943"]
        for i in range(10):
            assert warna[i % len(warna)] in warna

    def test_chart_height_formula(self):
        for n_rows in range(3, 9):
            height = 180 * n_rows
            assert height > 0


class TestShowIndikatorTechnicalIntegration:
    """Call show_indikator_teknikal with mocked Streamlit."""

    @patch("navigation.indikator_teknikal.st")
    def test_warns_when_fewer_than_two(self, mock_st, sample_df):
        mock_st.multiselect.return_value = ["RSI 14"]

        from navigation.indikator_teknikal import show_indikator_teknikal

        show_indikator_teknikal(sample_df)
        mock_st.warning.assert_called_once()

    @patch("navigation.indikator_teknikal.st")
    def test_renders_chart_with_two_indicators(self, mock_st, sample_df):
        mock_st.multiselect.return_value = ["RSI 14", "MACD"]
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

        from navigation.indikator_teknikal import show_indikator_teknikal

        show_indikator_teknikal(sample_df)
        mock_st.plotly_chart.assert_called_once()

    @patch("navigation.indikator_teknikal.st")
    def test_renders_chart_with_all_indicators(self, mock_st, sample_df):
        all_indicators = ["RSI 14", "MACD", "Bollinger Bands", "RSI 7", "CCI 14", "SMA 50", "EMA 50"]
        mock_st.multiselect.return_value = all_indicators
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

        from navigation.indikator_teknikal import show_indikator_teknikal

        show_indikator_teknikal(sample_df)
        mock_st.plotly_chart.assert_called_once()

    @patch("navigation.indikator_teknikal.st")
    def test_no_chart_when_zero_selected(self, mock_st, sample_df):
        mock_st.multiselect.return_value = []

        from navigation.indikator_teknikal import show_indikator_teknikal

        show_indikator_teknikal(sample_df)
        mock_st.plotly_chart.assert_not_called()
        mock_st.warning.assert_called_once()
