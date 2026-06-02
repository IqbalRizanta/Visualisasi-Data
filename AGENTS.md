# VisualisasiData — UAS Project

Streamlit dashboard (Python) + artikel laporan untuk analisis harga Bitcoin 2015-2024. Proyek kelompok 3 orang.

## Deliverables

1. `app.py` — Streamlit dashboard (file tunggal). Detail spec di `.opencode/instructions.md`.
2. `Artikel_UAS.md` — Laporan artikel. Template di `.opencode/artikel_template.md`.

## Dataset

`btc_2015_2024.csv` — **belum ada di repo**. Jangan generate CSV palsu; minta user jika tidak ada.
Kolom: `date`, `open`, `high`, `low`, `close`, `volume`, `rsi_7`, `rsi_14`, `macd`, `bollinger`.

## Hard constraints

- `@st.cache_data` pada load CSV
- `pd.to_datetime()` pada kolom `date`
- Plotly untuk grafik interaktif
- Komentar kode dalam **Bahasa Indonesia**
- Sidebar `st.sidebar.radio`: **Beranda**, **Tren Harga**, **Indikator Teknikal**

## Menu specs (ringkas)

| Menu | Isi |
|---|---|
| **Beranda** | Judul, deskripsi dataset, dataframe mentah, KPI (harga tertinggi, dll) |
| **Tren Harga** | Line chart `close` vs `date`, slider filter tahun |
| **Indikator Teknikal** | Overlay `close` + minimal 2 indikator (`rsi_14`, `macd`, dll) |

## Artikel

- Ikuti template `.opencode/artikel_template.md` (8 section)
- 3 placeholder nama anggota tim
- Sertakan `[INSERT SCREENSHOT HERE]` untuk setiap gambar

## Source files

| File | Peran |
|---|---|
| `.opencode/instructions.md` | Detail coding rules & menu specs |
| `.opencode/artikel_template.md` | Template artikel UAS |
| `AGENTS_Requirements.md` | Master instruksi awal proyek |
