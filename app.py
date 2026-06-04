import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Bitcoin Dashboard - CMC Style", layout="wide")

# Palet CoinMarketCap
CMC_BG = "#0B0E11"
CMC_CARD = "#1E2329"
CMC_GREEN = "#16C784"
CMC_RED = "#EA3943"
CMC_TEXT = "#FFFFFF"
CMC_TEXT2 = "#848E9C"
CMC_BORDER = "#2B3139"
CMC_ORANGE = "#F7931A"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {{ font-family: 'Inter', -apple-system, sans-serif; }}
    .block-container {{ padding-top: 3.5rem; }}
    .main > div {{ padding-top: 0 !important; }}
    #stDecoration {{ display: none; }}
    .stApp {{ background: {CMC_BG}; }}

    /* CMC-style top bar */
    .topbar {{
        background: {CMC_CARD}; border-bottom: 1px solid {CMC_BORDER};
        padding: 0.6rem 1.2rem; border-radius: 12px; margin-bottom: 1.2rem;
        display: flex; align-items: center; gap: 1rem;
    }}
    .topbar .logo {{ font-size: 1.3rem; font-weight: 700; color: {CMC_ORANGE}; }}
    .topbar .logo span {{ color: {CMC_TEXT}; }}
    .topbar .menu-item {{ color: {CMC_TEXT2}; font-size: 0.85rem; font-weight: 500; cursor: pointer; padding: 0.3rem 0.8rem; border-radius: 6px; }}
    .topbar .menu-item.active {{ color: {CMC_TEXT}; background: {CMC_BG}; }}

    /* Hero price ala CMC */
    .cmc-hero {{ padding: 0.5rem 0 0.8rem; }}
    .cmc-hero .rank-badge {{
        display: inline-block; background: {CMC_CARD}; border: 1px solid {CMC_BORDER};
        border-radius: 4px; padding: 0.15rem 0.5rem; font-size: 0.7rem; color: {CMC_TEXT2};
        font-weight: 600; margin-right: 0.5rem;
    }}
    .cmc-hero .coin-name {{ font-size: 1.5rem; font-weight: 700; color: {CMC_TEXT}; }}
    .cmc-hero .coin-symbol {{ font-size: 0.9rem; color: {CMC_TEXT2}; margin-left: 0.4rem; }}
    .cmc-hero .price {{ font-size: 2rem; font-weight: 700; color: {CMC_TEXT}; margin-top: 0.3rem; }}
    .cmc-hero .price-change {{
        display: inline-block; border-radius: 6px; padding: 0.25rem 0.7rem;
        font-size: 1rem; font-weight: 600; margin-left: 0.8rem;
    }}
    .cmc-hero .price-change.up {{ background: "{CMC_GREEN}20"; color: {CMC_GREEN}; }}
    .cmc-hero .price-change.down {{ background: "{CMC_RED}20"; color: {CMC_RED}; }}

    /* CMC stats bar */
    .stats-row {{ display: flex; gap: 2rem; flex-wrap: wrap; background: {CMC_CARD}; border-radius: 10px; padding: 0.8rem 1.2rem; margin: 0.8rem 0; border: 1px solid {CMC_BORDER}; }}
    .stat-item {{ }}
    .stat-item .sl {{ font-size: 0.7rem; color: {CMC_TEXT2}; text-transform: uppercase; letter-spacing: 0.3px; }}
    .stat-item .sv {{ font-size: 0.95rem; font-weight: 600; color: {CMC_TEXT}; margin-top: 0.15rem; }}
    .stat-item .sp {{ font-size: 0.8rem; color: {CMC_TEXT2}; }}

    /* Metric cards */
    .metric-card {{
        background: {CMC_CARD}; border-radius: 10px; padding: 1rem;
        border: 1px solid {CMC_BORDER};
    }}
    .metric-card .ml {{ font-size: 0.7rem; color: {CMC_TEXT2}; text-transform: uppercase; letter-spacing: 0.3px; }}
    .metric-card .mv {{ font-size: 1.1rem; font-weight: 600; color: {CMC_TEXT}; }}

    .sidebar-brand {{ text-align: center; padding: 0.8rem 0; }}
    .sidebar-brand h2 {{ color: {CMC_ORANGE}; margin: 0; font-size: 1.2rem; }}
    .sidebar-brand p {{ color: {CMC_TEXT2}; font-size: 0.7rem; margin: 0.1rem 0 0 0; }}

    /* Table styling */
    .stDataFrame {{ background: transparent; }}
    .stDataFrame table {{ background: {CMC_CARD} !important; }}
    .stDataFrame th {{ background: {CMC_CARD} !important; color: {CMC_TEXT2} !important; font-size: 0.75rem; text-transform: uppercase; border-bottom: 1px solid {CMC_BORDER} !important; }}
    .stDataFrame td {{ background: transparent !important; color: {CMC_TEXT} !important; border-bottom: 1px solid {CMC_BORDER} !important; }}

    @media (max-width: 640px) {{
        .cmc-hero .price {{ font-size: 1.4rem; }}
        .cmc-hero .price-change {{ font-size: 0.85rem; }}
        .stats-row {{ gap: 1rem; }}
    }}
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

# Top bar navigasi ala CMC
st.markdown(
    f"""
    <div class="topbar">
        <div class="logo">₿ <span>CryptoDashboard</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <h2>₿ Bitcoin Dashboard</h2>
            <p>Analisis Harga 2015–2024</p>
            <hr style="border-color: {CMC_BORDER}; margin: 0.8rem 0;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    menu = st.radio("Menu", ["Beranda", "Tren Harga", "Indikator Teknikal"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("**Tim Pengembang**")
    st.caption("Muhammad Iqbal Rizanta")
    st.caption("Muhammad Zaldy Zufar Ramadhan")
    st.caption("Verrel Shafry Hermawan")

# MENU BERANDA — ala CMC coin page
if menu == "Beranda":
    harga_now = df["close"].iloc[-1]
    harga_sebelum = df["close"].iloc[-2]
    selisih = harga_now - harga_sebelum
    pct = (selisih / harga_sebelum) * 100
    delta_class = "up" if selisih >= 0 else "down"
    arrow = "▲" if selisih >= 0 else "▼"
    ath = df["close"].max()
    ath_date = df.loc[df["close"].idxmax(), "date"].strftime("%d %b %Y")

    st.markdown(
        f"""
        <div class="cmc-hero">
            <div>
                <span class="rank-badge">#1</span>
                <span class="coin-name">Bitcoin</span>
                <span class="coin-symbol">BTC</span>
            </div>
            <div class="price">
                ${harga_now:,.0f}
                <span class="price-change {delta_class}">{arrow} {abs(pct):.2f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stats bar ala CMC
    market_cap = harga_now * 19_000_000
    volume = df["volume"].iloc[-1]
    st.markdown(
        f"""
        <div class="stats-row">
            <div class="stat-item">
                <div class="sl">Market Cap</div>
                <div class="sv">${market_cap:,.0f}</div>
                <div class="sp">+{'%.2f' % ((harga_now - df['close'].iloc[0])/df['close'].iloc[0]*100)}%</div>
            </div>
            <div class="stat-item">
                <div class="sl">Volume (24j)</div>
                <div class="sv">${volume:,.0f}</div>
            </div>
            <div class="stat-item">
                <div class="sl">Tertinggi (ATH)</div>
                <div class="sv">${ath:,.0f}</div>
                <div class="sp">{ath_date}</div>
            </div>
            <div class="stat-item">
                <div class="sl">Terendah</div>
                <div class="sv">${df['close'].min():,.0f}</div>
            </div>
            <div class="stat-item">
                <div class="sl">Rata-rata</div>
                <div class="sv">${df['close'].mean():,.0f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(f'<p style="color:{CMC_TEXT2}; font-size:0.85rem; font-weight:600;">CUPLIKAN DATASET</p>', unsafe_allow_html=True)

    cari = st.text_input("Cari", placeholder="Cari di semua kolom...", label_visibility="collapsed")

    with st.expander("Filter per Kolom"):
        kol1, kol2, kol3 = st.columns(3)
        with kol1:
            tahun_pilih = st.multiselect(
                "Tahun", sorted(df["date"].dt.year.unique()),
                default=sorted(df["date"].dt.year.unique()),
            )
        with kol2:
            harga_min, harga_max = st.slider(
                "Rentang Harga Close",
                min_value=float(df["close"].min()),
                max_value=float(df["close"].max()),
                value=(float(df["close"].min()), float(df["close"].max())),
                format="$%.0f",
            )
        with kol3:
            vol_min, vol_max = st.slider(
                "Rentang Volume",
                min_value=float(df["volume"].min()),
                max_value=float(df["volume"].max()),
                value=(float(df["volume"].min()), float(df["volume"].max())),
            )

    df_tampil = df.copy()
    df_tampil = df_tampil[df_tampil["date"].dt.year.isin(tahun_pilih)]
    df_tampil = df_tampil[(df_tampil["close"] >= harga_min) & (df_tampil["close"] <= harga_max)]
    df_tampil = df_tampil[(df_tampil["volume"] >= vol_min) & (df_tampil["volume"] <= vol_max)]

    if cari:
        mask = df_tampil.astype(str).apply(
            lambda x: x.str.contains(cari, case=False, na=False)
        ).any(axis=1)
        df_tampil = df_tampil[mask]

    st.dataframe(df_tampil, width='stretch', height=350)
    st.caption(f"Menampilkan {len(df_tampil):,} dari {len(df):,} baris · 20 kolom")

# MENU TREN HARGA — Standar Internasional (TradingView / Bloomberg)
elif menu == "Tren Harga":
    st.markdown(f'<p style="color:{CMC_TEXT}; font-size:1.3rem; font-weight:700;">Bitcoin to USD Chart</p>', unsafe_allow_html=True)

    tahun_min = int(df["date"].dt.year.min())
    tahun_max = int(df["date"].dt.year.max())
    tahun_terpilih = st.slider(
        "Pilih rentang tahun",
        min_value=tahun_min, max_value=tahun_max,
        value=(tahun_min, tahun_max),
    )

    batas_awal = pd.Timestamp(f"{tahun_terpilih[0]}-01-01")
    batas_akhir = pd.Timestamp(f"{tahun_terpilih[1]}-12-31")
    df_f = df[(df["date"] >= batas_awal) & (df["date"] <= batas_akhir)]

    log_scale = st.checkbox("Log Scale (untuk melihat pertumbuhan eksponensial)", value=False)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.72, 0.28],
    )

    # -- Candlestick --
    fig.add_trace(
        go.Candlestick(
            x=df_f["date"],
            open=df_f["open"], high=df_f["high"],
            low=df_f["low"], close=df_f["close"],
            name="BTC/USD",
            increasing_line_color=CMC_GREEN, decreasing_line_color=CMC_RED,
        ),
        row=1, col=1,
    )

    # -- SMA 50 --
    fig.add_trace(
        go.Scatter(
            x=df_f["date"], y=df_f["sma_50"],
            mode="lines", name="SMA 50",
            line=dict(color="#F59E0B", width=1.5),
        ),
        row=1, col=1,
    )

    # -- SMA 100 --
    fig.add_trace(
        go.Scatter(
            x=df_f["date"], y=df_f["sma_100"],
            mode="lines", name="SMA 100",
            line=dict(color="#EF4444", width=1.5),
        ),
        row=1, col=1,
    )

    # -- Volume --
    warna_volume = [CMC_GREEN if df_f["close"].iloc[i] >= df_f["open"].iloc[i] else CMC_RED for i in range(len(df_f))]
    fig.add_trace(
        go.Bar(
            x=df_f["date"], y=df_f["volume"],
            name="Volume",
            marker_color=warna_volume,
            opacity=0.6,
        ),
        row=2, col=1,
    )

    fig.update_layout(
        title=dict(
            text=f"BTC/USD ({tahun_terpilih[0]}–{tahun_terpilih[1]})",
            font=dict(size=16, color=CMC_TEXT),
            x=0.5, xanchor="center",
        ),
        hovermode="x unified",
        margin=dict(t=50, b=30, l=30, r=30),
        plot_bgcolor=CMC_CARD,
        paper_bgcolor=CMC_BG,
        font=dict(family="Inter, sans-serif", color=CMC_TEXT2),
        hoverlabel=dict(bgcolor=CMC_CARD, font_size=12, font_color=CMC_TEXT, font_family="Inter"),
        xaxis2=dict(showgrid=True, gridcolor=CMC_BORDER, dtick="M12", tickformat="%Y"),
        yaxis2=dict(showgrid=True, gridcolor=CMC_BORDER, title=dict(text="Volume")),
        legend=dict(orientation="h", yanchor="bottom", y=1.005, xanchor="right", x=1, font=dict(color=CMC_TEXT2)),
    )

    if log_scale:
        fig.update_yaxis(type="log", row=1, col=1)

    fig.update_xaxes(showgrid=True, gridcolor=CMC_BORDER, row=1, col=1)
    fig.update_yaxes(showgrid=True, gridcolor=CMC_BORDER, tickprefix="$", tickformat=",", row=1, col=1)

    st.plotly_chart(fig, config={'responsive': True})

    # -- Drawdown Chart (di bawah, sebagai bonus) --
    ath = df_f["close"].max()
    df_f = df_f.copy()
    df_f["drawdown"] = (df_f["close"] - ath) / ath * 100

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df_f["date"], y=df_f["drawdown"],
            mode="lines",
            name="Drawdown",
            line=dict(color=CMC_RED, width=1.5),
            fill="tozeroy",
            fillcolor="rgba(234, 57, 67, 0.10)",
        )
    )
    fig2.update_layout(
        title=dict(text="Drawdown dari All-Time High (%)", font=dict(size=13, color=CMC_TEXT), x=0.5, xanchor="center"),
        hovermode="x unified",
        height=160,
        margin=dict(t=30, b=20, l=30, r=30),
        plot_bgcolor=CMC_CARD,
        paper_bgcolor=CMC_BG,
        font=dict(family="Inter, sans-serif", color=CMC_TEXT2),
        xaxis=dict(showgrid=True, gridcolor=CMC_BORDER, dtick="M12", tickformat="%Y"),
        yaxis=dict(showgrid=True, gridcolor=CMC_BORDER, ticksuffix="%"),
    )
    st.plotly_chart(fig2, config={'responsive': True})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Open", f"${df_f['open'].iloc[0]:,.0f}")
    col2.metric("Close", f"${df_f['close'].iloc[-1]:,.0f}")
    perf = ((df_f["close"].iloc[-1] - df_f["close"].iloc[0]) / df_f["close"].iloc[0]) * 100
    col3.metric("Change", f"{perf:+.2f}%")
    col4.metric("Drawdown Maks", f"{df_f['drawdown'].min():.1f}%")

# MENU INDIKATOR TEKNIKAL
elif menu == "Indikator Teknikal":
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
