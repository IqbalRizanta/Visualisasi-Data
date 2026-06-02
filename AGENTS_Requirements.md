# 🤖 PANDUAN UTAMA OPENCODE AGENT (MASTER INSTRUCTION)

**[UNTUK DIBACA OLEH AGENT SEBELUM MEMULAI EKSEKUSI PROYEK]**

## 1. KONTEKS PROYEK (PROJECT CONTEXT)
Kamu adalah AI Developer Assistant (OpenCode Agent) tingkat lanjut. Tugas utama kamu adalah membantu *user* menyelesaikan Proyek Ujian Akhir Semester (UAS). Proyek ini adalah tugas kelompok (3 orang) yang memiliki dua *deliverables* utama:
1. **Website Dashboard Visualisasi Data:** Dibangun menggunakan bahasa **Python** dan framework **Streamlit**.
2. **Artikel Proyek:** Sebuah artikel teknis format Markdown (`.md`) yang menjelaskan proses pembuatan dashboard tersebut (sebagai portofolio/laporan UAS).

## 2. SUMBER DATA (DATA SOURCE)
* **File Target:** `btc_2015_2024.csv` (berada di direktori kerja).
* **Konteks Data:** Data historis harga pasar dan indikator teknikal Bitcoin dari tahun 2015 hingga 2024.
* **Kolom Penting:** `date`, `open`, `high`, `low`, `close`, `volume`, `rsi_7`, `rsi_14`, `macd`, `bollinger`.

## 3. ATURAN PENGKODEAN (CODING CONSTRAINTS & RULES)
* **Wajib gunakan Streamlit Caching:** Gunakan decorator `@st.cache_data` pada fungsi pembacaan dan pemrosesan file CSV agar aplikasi tidak *lagging*.
* **Konversi Tipe Data:** Kolom `date` wajib diubah menjadi tipe `datetime` menggunakan Pandas sebelum divisualisasikan.
* **Library Visualisasi:** Gunakan `plotly.express` atau `plotly.graph_objects` untuk grafik yang interaktif. Jika tidak memungkinkan, gunakan `altair`.
* **Clean Code:** Berikan komentar (komentar dalam bahasa Indonesia) pada bagian kode yang penting agar mudah dipahami oleh dosen.

## 4. TAHAPAN EKSEKUSI (STEP-BY-STEP EXECUTION PLAN)
Agent wajib mengeksekusi proyek ini dengan urutan berikut:

### FASE 1: Eksplorasi Data & Setup Streamlit (`app.py`)
1. Buat file `app.py`.
2. Buat fungsi untuk meload `btc_2015_2024.csv` dengan `@st.cache_data`.
3. Buat navigasi Sidebar (menggunakan `st.sidebar.radio` atau `st.sidebar.selectbox`) dengan 3 menu: "Beranda", "Tren Harga", dan "Indikator Teknikal".

### FASE 2: Pengembangan Fitur Dashboard (Selesaikan per menu)
1. **Menu Beranda:** Tampilkan judul UAS, deskripsi singkat dataset, tampilkan *dataframe* raw data, dan beberapa KPI (*Key Performance Indicators*) seperti Harga Tertinggi sepanjang masa, dll.
2. **Menu Tren Harga:** Buat visualisasi interaktif (*Line Chart*) pergerakan harga `close` berdasarkan waktu. Sediakan *filter* rentang waktu (misal: *slider* tahun).
3. **Menu Indikator Teknikal:** Buat visualisasi yang membandingkan garis harga (`close`) dengan setidaknya 2 indikator teknikal yang ada di dataset (seperti `rsi_14` atau `macd`).

### FASE 3: Pembuatan Artikel UAS (`Artikel_UAS.md`)
Setelah file `app.py` selesai dibuat dan berjalan dengan baik, buat sebuah file baru bernama `Artikel_UAS.md`.
Artikel ini HARUS mengikuti template profesional berikut:
1. **Pendahuluan:** Latar belakang analisis harga Bitcoin.
2. **Tim Pengembang:** Kosongkan placeholder untuk nama 3 anggota kelompok.
3. **Teknologi & Data:** Penjelasan penggunaan Python, Streamlit, Pandas, dan isi dataset.
4. **Fitur Dashboard:** Penjelasan 3 menu yang dibuat di fase 2 (berikan placeholder "[INSERT SCREENSHOT HERE]" untuk diisi gambar oleh *user* nantinya).
5. **Kesimpulan & Insight:** Analisis singkat tentang data.

## 5. PENYELESAIAN
Setelah menyelesaikan Fase 1 hingga Fase 3, laporkan kepada *user* bahwa kode `app.py` dan `Artikel_UAS.md` telah selesai dibuat dan siap untuk di- *review*. Jangan berhalusinasi membuat file CSV baru, gunakan yang sudah ada.
