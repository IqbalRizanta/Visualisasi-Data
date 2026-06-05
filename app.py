import streamlit as st
import pandas as pd
from navigation import show_beranda, show_tren_harga, show_indikator_teknikal

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
    .topbar {{ min-height: 48px; }}
    .topbar .logo {{ font-size: 1.3rem; font-weight: 700; color: {CMC_ORANGE}; }}
    .topbar .logo span {{ color: {CMC_TEXT}; }}
    .topbar .subtitle {{ font-size: 0.72rem; color: {CMC_TEXT2}; margin-top: -2px; }}

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
        <div>
            <div class="logo">₿ <span>BitcoinDashboard</span></div>
            <div class="subtitle">Bitcoin Price Trends With Indicators (8 Years)</div>
        </div>
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

# Navigasi Multi-Page (MPA)
if menu == "Beranda":
    show_beranda(df)
elif menu == "Tren Harga":
    show_tren_harga(df)
elif menu == "Indikator Teknikal":
    show_indikator_teknikal(df)
