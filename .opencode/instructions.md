# VisualisasiData — UAS Dashboard Project

## Deliverables
- `app.py` — Streamlit app (file tunggal)
- `Artikel_UAS.md` — Laporan artikel (template struktur di `.opencode/artikel_template.md`)

## Dataset
- File: `btc_2015_2024.csv` — harus sudah ada, jangan membuat CSV palsu
- Kolom: `date`, `open`, `high`, `low`, `close`, `volume`, `rsi_7`, `rsi_14`, `macd`, `bollinger`

## Coding Rules
- `@st.cache_data` pada fungsi load CSV
- `pd.to_datetime()` pada kolom `date`
- Plotly untuk grafik interaktif
- Komentar kode dalam Bahasa Indonesia
- Sidebar (`st.sidebar.radio`): "Beranda", "Tren Harga", "Indikator Teknikal"

## 3 Menu Dashboard
1. **Beranda** — Judul UAS, deskripsi dataset, dataframe mentah, KPI (harga tertinggi, dll)
2. **Tren Harga** — Line chart interaktif `close` vs `date`, slider/filter tahun
3. **Indikator Teknikal** — Overlay `close` + minimal 2 indikator (`rsi_14`, `macd`, dll)

## Artikel (`Artikel_UAS.md`)
- Ikuti struktur template di `.opencode/artikel_template.md`
- Tim: 3 placeholder nama anggota
- Sertakan `[INSERT SCREENSHOT HERE]` untuk placeholder gambar
