import logging

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

CMC_BG = "#0B0E11"
CMC_CARD = "#1E2329"
CMC_GREEN = "#16C784"
CMC_RED = "#EA3943"
CMC_TEXT = "#FFFFFF"
CMC_TEXT2 = "#848E9C"
CMC_BORDER = "#2B3139"
CMC_ORANGE = "#F7931A"


def show_indikator_teknikal(df):
    st.markdown(f'<p style="color:{CMC_TEXT}; font-size:1.3rem; font-weight:700;">Analisis Indikator Teknikal</p>', unsafe_allow_html=True)

    indikator_tersedia = {
        "RSI 14": "rsi_14",
        "MACD": "macd",
        "Bollinger Bands": "bollinger",
        "RSI 7": "rsi_7",
        "CCI 14": "cci_14",
        "SMA 50": "sma_50",
        "EMA 50": "ema_50",
    }

    pilihan = st.multiselect(
        "Pilih indikator (minimal 2):",
        options=list(indikator_tersedia.keys()),
        default=["RSI 14", "Bollinger Bands"],
    )

    if len(pilihan) < 2:
        st.warning("Pilih minimal 2 indikator.")
    else:
        missing_cols = [
            nama for nama in pilihan
            if indikator_tersedia[nama] not in df.columns
        ]
        if missing_cols:
            st.error(
                f"The dataset is missing columns for: {', '.join(missing_cols)}. "
                "These indicators cannot be displayed."
            )
            logger.error("Missing indicator columns: %s", missing_cols)
            pilihan = [p for p in pilihan if p not in missing_cols]
            if len(pilihan) < 2:
                st.warning("Not enough valid indicators remaining (need at least 2).")
                return

        n_rows = 1 + len(pilihan)
        fig = make_subplots(
            rows=n_rows, cols=1,
            shared_xaxes=False,
            vertical_spacing=0.12 / n_rows * 3,
            row_heights=[0.35] + [0.65 / len(pilihan)] * len(pilihan),
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"], y=df["close"],
                mode="lines", name="Harga Close",
                line=dict(color=CMC_GREEN, width=2),
            ),
            row=1, col=1,
        )
        fig.update_xaxes(dtick="M12", tickformat="%Y", row=1, col=1)

        warna = [CMC_ORANGE, "#3B82F6", "#8B5CF6", "#F59E0B", CMC_RED]
        for i, nama in enumerate(pilihan):
            kolom = indikator_tersedia[nama]
            fig.add_trace(
                go.Scatter(
                    x=df["date"], y=df[kolom],
                    mode="lines", name=nama,
                    line=dict(color=warna[i % len(warna)], width=2),
                ),
                row=i + 2, col=1,
            )
            fig.update_xaxes(dtick="M12", tickformat="%Y", row=i + 2, col=1)
            if "RSI" in nama:
                fig.add_hline(y=70, line=dict(color=CMC_RED, width=1, dash="dash"), row=i + 2, col=1)
                fig.add_hline(y=30, line=dict(color=CMC_GREEN, width=1, dash="dash"), row=i + 2, col=1)

        fig.update_layout(
            hovermode="x unified",
            height=180 * n_rows,
            margin=dict(t=20, b=30, l=30, r=30),
            plot_bgcolor=CMC_CARD,
            paper_bgcolor=CMC_BG,
            font=dict(family="Inter, sans-serif", color=CMC_TEXT2),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1, font=dict(color=CMC_TEXT2)),
        )
        for i in range(1, n_rows + 1):
            fig.update_xaxes(showgrid=True, gridcolor=CMC_BORDER, row=i, col=1)
            fig.update_yaxes(showgrid=True, gridcolor=CMC_BORDER, row=i, col=1)

        st.plotly_chart(fig, config={'responsive': True})

        with st.expander("Penjelasan Indikator"):
            st.markdown(
                f"""
                <p style="color:{CMC_TEXT2};">
                - <b style="color:{CMC_TEXT};">RSI</b> — Mengukur kecepatan & perubahan harga. &gt;70 = overbought, &lt;30 = oversold.<br>
                - <b style="color:{CMC_TEXT};">MACD</b> — Menunjukkan hubungan dua EMA. Golden cross = tren naik.<br>
                - <b style="color:{CMC_TEXT};">Bollinger Bands</b> — Mengukur volatilitas pasar.<br>
                - <b style="color:{CMC_TEXT};">CCI</b> — Mendeteksi siklus overbought/oversold.<br>
                - <b style="color:{CMC_TEXT};">SMA/EMA</b> — Rata-rata pergerakan harga untuk melihat arah tren.
                </p>
                """,
                unsafe_allow_html=True,
            )
