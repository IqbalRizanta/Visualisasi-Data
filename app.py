import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dashboard Bitcoin 2015-2024", layout="wide")

# --- Palet dark mode khas dashboard kripto ---
BITCOIN_ORANGE = "#F7931A"
CHART_BG = "#131722"
GRID = "#2A2E39"
TEXT_LIGHT = "#D1D5DB"
TEXT_WHITE = "#F9FAFB"
GREEN = "#10B981"
RED = "#EF4444"
BLUE = "#3B82F6"
PURPLE = "#8B5CF6"
AMBER = "#F59E0B"
GRAY_MUTED = "#6B7280"

st.markdown(
    f"""
    <style>
    .block-container {{ padding-top: 1rem; }}
    .price-hero {{
        background: linear-gradient(135deg, #1a1d2e, #1e2235);
        border-radius: 16px; padding: 1.8rem 2rem;
        border: 1px solid #2a2e39; margin-bottom: 1rem;
    }}
    .price-hero .label {{ font-size: 0.85rem; color: {GRAY_MUTED}; text-transform: uppercase; letter-spacing: 0.5px; }}
    .price-hero .value {{ font-size: 2.5rem; font-weight: 700; color: {TEXT_WHITE}; }}
    .price-hero .delta {{ font-size: 1.1rem; font-weight: 600; margin-left: 0.8rem; }}
    .price-hero .delta.up {{ color: {GREEN}; }}
    .price-hero .delta.down {{ color: {RED}; }}
    .metric-card {{
        background: #1a1d2e; border-radius: 12px; padding: 1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2); border-left: 3px solid {BITCOIN_ORANGE};
    }}
    .metric-card .ml {{ font-size: 0.75rem; color: {GRAY_MUTED}; text-transform: uppercase; letter-spacing: 0.5px; }}
    .metric-card .mv {{ font-size: 1.3rem; font-weight: 700; color: {TEXT_WHITE}; }}
    .sidebar-brand {{ text-align: center; padding: 1.2rem 0 0.5rem; }}
    .sidebar-brand h2 {{ color: {BITCOIN_ORANGE}; margin: 0; font-size: 1.3rem; }}
    .sidebar-brand p {{ color: {GRAY_MUTED}; font-size: 0.75rem; margin: 0.1rem 0 0 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    df = pd.read_csv("btc_2015_2024.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <h2>₿ Bitcoin Dashboard</h2>
            <p>Analisis Harga 2015–2024</p>
            <hr style="margin: 1rem 0;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    menu = st.radio("Menu", ["Beranda", "Tren Harga", "Indikator Teknikal"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("**Tim Pengembang**")
    st.caption(" Muhammad iqbal Rizanta")
    st.caption(" Muhammad Zaldy Zufar Ramadhan")
    st.caption(" Verrel Shafry Hermawan")

# MENU BERANDA
if menu == "Beranda":
    st.title("Dashboard Analisis Harga Bitcoin")
    st.markdown(
        f'<p style="color:{GRAY_MUTED}; margin-top: -0.5rem; margin-bottom: 1.2rem;">'
        "Data historis harga Bitcoin dan indikator teknikal periode 2015–2024.</p>",
        unsafe_allow_html=True,
    )

    harga_now = df["close"].iloc[-1]
    harga_sebelum = df["close"].iloc[-2]
    selisih = harga_now - harga_sebelum
    pct = (selisih / harga_sebelum) * 100
    delta_class = "up" if selisih >= 0 else "down"
    arrow = "▲" if selisih >= 0 else "▼"

    st.markdown(
        f"""
        <div class="price-hero">
            <div class="label">Harga Bitcoin Terakhir</div>
            <div>
                <span class="value">${harga_now:,.0f}</span>
                <span class="delta {delta_class}">{arrow} ${abs(selisih):,.0f} ({pct:+.2f}%)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(3)
    kpi_list = [
        ("Tertinggi (ATH)", f"${df['close'].max():,.0f}"),
        ("Terendah", f"${df['close'].min():,.0f}"),
        ("Rata-rata", f"${df['close'].mean():,.0f}"),
    ]
    for col, (label, value) in zip(kpi_cols, kpi_list):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="ml">{label}</div><div class="mv">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.divider()
    st.subheader("Cuplikan Dataset")
    st.dataframe(df, use_container_width=True, height=400)
    st.caption(f"Total {len(df):,} baris data · 20 kolom")

# MENU TREN HARGA
elif menu == "Tren Harga":
    st.title("Tren Pergerakan Harga Penutupan Bitcoin")

    mode_filter = st.radio(
        "Filter waktu",
        ["1B", "3B", "6B", "1T", "5T", "All"],
        index=5,
        horizontal=True,
    )

    tanggal_akhir = df["date"].max()
    mapping = {
        "1B": tanggal_akhir - pd.DateOffset(months=1),
        "3B": tanggal_akhir - pd.DateOffset(months=3),
        "6B": tanggal_akhir - pd.DateOffset(months=6),
        "1T": tanggal_akhir - pd.DateOffset(years=1),
        "5T": tanggal_akhir - pd.DateOffset(years=5),
        "All": df["date"].min(),
    }
    batas_awal = mapping[mode_filter]
    df_f = df[df["date"] >= batas_awal]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_f["date"], y=df_f["close"],
            mode="lines",
            name="Harga Close",
            line=dict(color=BITCOIN_ORANGE, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(247, 147, 26, 0.15)",
        )
    )

    fig.update_layout(
        title=dict(
            text="Pergerakan Harga Close Bitcoin",
            font=dict(size=18, color=TEXT_WHITE),
        ),
        xaxis_title="Tanggal",
        yaxis_title="Harga (USD)",
        hovermode="x unified",
        margin=dict(t=50, b=30, l=20, r=20),
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_BG,
        font=dict(color=TEXT_LIGHT),
        xaxis=dict(
            showgrid=True, gridcolor=GRID,
            title=dict(font=dict(color=TEXT_LIGHT)),
            dtick="M12", tickformat="%Y",
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID,
            tickprefix="$", tickformat=",",
            title=dict(font=dict(color=TEXT_LIGHT)),
        ),
    )

    st.plotly_chart(fig, width='stretch')

    col1, col2, col3 = st.columns(3)
    col1.metric("Harga Awal", f"${df_f['close'].iloc[0]:,.0f}")
    col2.metric("Harga Akhir", f"${df_f['close'].iloc[-1]:,.0f}")
    perf = ((df_f["close"].iloc[-1] - df_f["close"].iloc[0]) / df_f["close"].iloc[0]) * 100
    col3.metric("Perubahan", f"{perf:+.2f}%")

# MENU INDIKATOR TEKNIKAL
elif menu == "Indikator Teknikal":
    st.title("Analisis Indikator Teknikal")

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
        st.warning("Pilih minimal 2 indikator untuk ditampilkan.")
    else:
        n_rows = 1 + len(pilihan)
        fig = make_subplots(
            rows=n_rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            row_heights=[0.35] + [0.65 / len(pilihan)] * len(pilihan),
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"], y=df["close"],
                mode="lines", name="Harga Close",
                line=dict(color=BITCOIN_ORANGE, width=2),
            ),
            row=1, col=1,
        )

        warna_indikator = [BLUE, GREEN, PURPLE, AMBER, RED]
        for i, nama in enumerate(pilihan):
            kolom = indikator_tersedia[nama]
            fig.add_trace(
                go.Scatter(
                    x=df["date"], y=df[kolom],
                    mode="lines", name=nama,
                    line=dict(color=warna_indikator[i % len(warna_indikator)], width=2),
                ),
                row=i + 2, col=1,
            )
            if "RSI" in nama:
                fig.add_hline(y=70, line=dict(color="#DC2626", width=1, dash="dash"), row=i + 2, col=1)
                fig.add_hline(y=30, line=dict(color="#16A34A", width=1, dash="dash"), row=i + 2, col=1)

        fig.update_layout(
            title=dict(text="Perbandingan Harga Close dengan Indikator Teknikal", font=dict(size=16, color=TEXT_WHITE)),
            hovermode="x unified",
            height=220 * n_rows,
            margin=dict(t=50, b=20, l=20, r=20),
            plot_bgcolor=CHART_BG,
            paper_bgcolor=CHART_BG,
            font=dict(color=TEXT_LIGHT),
            legend=dict(orientation="h", yanchor="bottom", y=1.005, xanchor="right", x=1, font=dict(color=TEXT_LIGHT)),
        )
        fig.update_xaxes(showgrid=True, gridcolor=GRID, title=dict(font=dict(color=TEXT_LIGHT)), dtick="M12", tickformat="%Y")
        fig.update_yaxes(showgrid=True, gridcolor=GRID, title=dict(font=dict(color=TEXT_LIGHT)))

        st.plotly_chart(fig, width='stretch')

        with st.expander("Penjelasan Indikator"):
            st.markdown(
                """
                - **RSI (Relative Strength Index):** Mengukur kecepatan & perubahan harga.
                  Nilai > 70 = *overbought* (garis merah), < 30 = *oversold* (garis hijau).
                - **MACD (Moving Average Convergence Divergence):** Menunjukkan hubungan
                  dua EMA. *Golden cross* = tren naik, *death cross* = tren turun.
                - **Bollinger Bands:** Mengukur volatilitas pasar berdasarkan deviasi standar.
                - **CCI (Commodity Channel Index):** Mendeteksi kondisi *overbought*/ *oversold*.
                - **SMA/EMA (Simple/Exponential Moving Average):** Menghaluskan data harga
                  untuk mengidentifikasi arah tren.
                """
            )
