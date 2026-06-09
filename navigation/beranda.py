import streamlit as st
import pandas as pd
from navigation.theme import (
    CMC_CARD, CMC_GREEN, CMC_RED,
    CMC_TEXT, CMC_TEXT2, CMC_BORDER, CMC_ORANGE,
    section_heading, card_container,
)


def show_beranda(df):
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

    # === ABOUT DATASET ===
    section_heading("Bitcoin Price Trends With Indicators (8 Years)")

    teks = (
        "This dataset offers a detailed examination of Bitcoin's price behavior over the last eight years, "
        "featuring a range of technical indicators for analyzing its trends. It captures the daily opening, "
        "highest, lowest, and closing prices, along with trading volume. The dataset includes momentum "
        'indicators such as the 7-day and 14-day <b style="color:' + CMC_TEXT + ';">Relative Strength Index (RSI)</b> '
        "to determine if the asset is overbought or oversold. It also contains the 7-day and 14-day "
        '<b style="color:' + CMC_TEXT + ';">Commodity Channel Index (CCI)</b>, which compares the current price '
        "to the historical average to spot short- and medium-term trends. Additionally, it encompasses "
        "moving averages like the 50-day and 100-day "
        '<b style="color:' + CMC_TEXT + ';">Simple Moving Average (SMA)</b> '
        "and <b style=\"color:" + CMC_TEXT + ';">Exponential Moving Average (EMA)</b>, which shed light on the asset\'s '
        "trend direction. Other essential indicators in the dataset are the "
        '<b style="color:' + CMC_TEXT + ';">Moving Average Convergence Divergence (MACD)</b>, '
        '<b style="color:' + CMC_TEXT + ';">Bollinger Bands</b> for assessing price volatility, the '
        '<b style="color:' + CMC_TEXT + ';">True Range</b>, and the 7-day and 14-day '
        '<b style="color:' + CMC_TEXT + ';">Average True Range (ATR)</b> that provide insights into market volatility. '
        "This dataset's primary goal is to forecast the closing price for the next day, making it a crucial "
        "tool for predicting future market movements."
    )
    card_container(
        f'<p style="color:{CMC_TEXT2}; font-size:0.88rem; line-height:1.6; margin:0;">{teks}</p>'
    )

    # === TENTANG DATASET ===
    section_heading("Tentang Dataset")

    sum_na = df.isna().sum().sum()
    dataset_table = f"""
            <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">
                <tr>
                    <td style="color:{CMC_TEXT2}; padding:0.3rem 0.8rem 0.3rem 0; width:140px;">Sumber</td>
                    <td style="color:{CMC_TEXT}; font-weight:500;">Kaggle — {len(df):,} baris · {len(df.columns)} kolom</td>
                </tr>
                <tr>
                    <td style="color:{CMC_TEXT2}; padding:0.3rem 0.8rem 0.3rem 0;">Periode</td>
                    <td style="color:{CMC_TEXT}; font-weight:500;">
                        {df['date'].min().strftime('%d %b %Y')} — {df['date'].max().strftime('%d %b %Y')}
                        ({(df['date'].max() - df['date'].min()).days} hari)
                    </td>
                </tr>
                <tr>
                    <td style="color:{CMC_TEXT2}; padding:0.3rem 0.8rem 0.3rem 0;">Author Dataset</td>
                    <td style="color:{CMC_TEXT}; font-weight:500;">A. Pillai (aspillai)</td>
                </tr>
                <tr>
                    <td style="color:{CMC_TEXT2}; padding:0.3rem 0.8rem 0.3rem 0;">Missing Values</td>
                    <td style="color:{CMC_TEXT}; font-weight:500;">{sum_na}</td>
                </tr>
                <tr>
                    <td style="color:{CMC_TEXT2}; padding:0.3rem 0.8rem 0.3rem 0;">Link</td>
                    <td style="color:{CMC_ORANGE}; font-weight:500;">
                        <a href="https://www.kaggle.com/datasets/aspillai/bitcoin-price-trends-with-indicators-8-years" target="_blank" style="color:{CMC_ORANGE}; text-decoration:none;">
                            kaggle.com/datasets/aspillai/bitcoin-price-trends-with-indicators-8-years
                        </a>
                    </td>
                </tr>
            </table>
    """
    card_container(dataset_table)

    # Struktur kolom
    st.markdown(f'<p style="color:{CMC_TEXT2}; font-size:0.8rem; font-weight:600; margin-bottom:0.3rem;">STRUKTUR KOLOM</p>', unsafe_allow_html=True)

    kolom_info = [
        ["date", "Tanggal perdagangan (YYYY-MM-DD)", "Date"],
        ["open, high, low, close", "Harga pembukaan, tertinggi, terendah, penutupan harian", "Float (USD)"],
        ["volume", "Volume perdagangan harian", "Float (USD)"],
        ["next_day_close", "Harga penutupan hari berikutnya", "Float (USD)"],
        ["sma_50, sma_100", "Simple Moving Average 50 & 100 hari", "Float (USD)"],
        ["ema_50, ema_100", "Exponential Moving Average 50 & 100 hari", "Float (USD)"],
        ["rsi_7, rsi_14", "Relative Strength Index periode 7 & 14", "Float (0–100)"],
        ["cci_7, cci_14", "Commodity Channel Index periode 7 & 14", "Float"],
        ["macd", "Moving Average Convergence Divergence", "Float"],
        ["bollinger", "Bollinger Bands (nilai upper band)", "Float (USD)"],
        ["TrueRange", "True Range (volatilitas harian)", "Float (USD)"],
        ["atr_7, atr_14", "Average True Range periode 7 & 14", "Float (USD)"],
    ]

    tabel_html = (
        f'<table style="width:100%; border-collapse:collapse; font-size:0.78rem;">'
        f'<tr style="border-bottom:1px solid {CMC_BORDER}; color:{CMC_TEXT2};">'
        f'<th style="padding:0.4rem 0.6rem; text-align:left; font-weight:600;">Kolom</th>'
        f'<th style="padding:0.4rem 0.6rem; text-align:left; font-weight:600;">Deskripsi</th>'
        f'<th style="padding:0.4rem 0.6rem; text-align:left; font-weight:600;">Tipe</th></tr>'
    )
    for col, desc, tipe in kolom_info:
        tabel_html += (
            f'<tr style="border-bottom:1px solid {CMC_BORDER};">'
            f'<td style="padding:0.35rem 0.6rem; color:{CMC_GREEN}; font-family:monospace;">{col}</td>'
            f'<td style="padding:0.35rem 0.6rem; color:{CMC_TEXT2};">{desc}</td>'
            f'<td style="padding:0.35rem 0.6rem; color:{CMC_TEXT2};">{tipe}</td></tr>'
        )
    tabel_html += "</table>"

    card_container(tabel_html, padding="0.5rem 1rem", margin="0.3rem 0 1.2rem 0")

    # === DATA TABLE ===
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
    st.caption(f"Menampilkan {len(df_tampil):,} dari {len(df):,} baris · {len(df.columns)} kolom")
