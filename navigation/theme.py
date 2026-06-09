"""Shared CoinMarketCap-style theme constants and reusable UI helpers."""

import streamlit as st

# ── Color palette (CoinMarketCap) ──────────────────────────────────────────
CMC_BG = "#0B0E11"
CMC_CARD = "#1E2329"
CMC_GREEN = "#16C784"
CMC_RED = "#EA3943"
CMC_TEXT = "#FFFFFF"
CMC_TEXT2 = "#848E9C"
CMC_BORDER = "#2B3139"
CMC_ORANGE = "#F7931A"


# ── HTML helpers ───────────────────────────────────────────────────────────
def section_heading(text: str, font_size: str = "1.1rem") -> None:
    """Render a styled section heading."""
    st.markdown(
        f'<p style="color:{CMC_TEXT}; font-size:{font_size}; font-weight:700;">'
        f"{text}</p>",
        unsafe_allow_html=True,
    )


def card_container(inner_html: str, padding: str = "1rem 1.2rem",
                   margin: str = "0.5rem 0 1rem 0") -> None:
    """Wrap *inner_html* in a themed card div and render it."""
    st.markdown(
        f'<div style="background:{CMC_CARD}; border:1px solid {CMC_BORDER}; '
        f'border-radius:10px; padding:{padding}; margin:{margin};">'
        f"{inner_html}</div>",
        unsafe_allow_html=True,
    )


# ── Plotly helpers ─────────────────────────────────────────────────────────
def base_chart_layout(**overrides) -> dict:
    """Return a dict of common Plotly layout settings.

    Any key in *overrides* replaces the default value, so callers can
    customise individual settings while inheriting the rest.
    """
    layout = dict(
        hovermode="x unified",
        plot_bgcolor=CMC_CARD,
        paper_bgcolor=CMC_BG,
        font=dict(family="Inter, sans-serif", color=CMC_TEXT2),
        hoverlabel=dict(
            bgcolor=CMC_CARD,
            font_size=12,
            font_color=CMC_TEXT,
            font_family="Inter",
        ),
    )
    layout.update(overrides)
    return layout


def apply_grid_styling(fig, rows: int = 1, cols: int = 1) -> None:
    """Apply the standard grid color to every subplot axis."""
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            fig.update_xaxes(showgrid=True, gridcolor=CMC_BORDER, row=r, col=c)
            fig.update_yaxes(showgrid=True, gridcolor=CMC_BORDER, row=r, col=c)
