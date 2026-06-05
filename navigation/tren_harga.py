import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CMC_BG = "#0B0E11"
CMC_CARD = "#1E2329"
CMC_GREEN = "#16C784"
CMC_RED = "#EA3943"
CMC_TEXT = "#FFFFFF"
CMC_TEXT2 = "#848E9C"
CMC_BORDER = "#2B3139"
CMC_ORANGE = "#F7931A"


def show_tren_harga(df):
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
        fig.update_yaxes(type="log", row=1, col=1)

    fig.update_xaxes(showgrid=True, gridcolor=CMC_BORDER, row=1, col=1)
    fig.update_yaxes(showgrid=True, gridcolor=CMC_BORDER, tickprefix="$", tickformat=",", row=1, col=1)

    st.plotly_chart(fig, config={'responsive': True})

    # -- Drawdown Chart --
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
