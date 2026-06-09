import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from navigation.theme import (
    CMC_GREEN, CMC_RED,
    CMC_TEXT, CMC_TEXT2, CMC_ORANGE,
    section_heading, base_chart_layout, apply_grid_styling,
)


def show_indikator_teknikal(df):
    section_heading("Analisis Indikator Teknikal", font_size="1.3rem")

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

        fig.update_layout(**base_chart_layout(
            height=180 * n_rows,
            margin=dict(t=20, b=30, l=30, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1, font=dict(color=CMC_TEXT2)),
        ))
        apply_grid_styling(fig, rows=n_rows)

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
