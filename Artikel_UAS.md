# Membangun Dashboard Analisis Tren Bitcoin (2015–2024) Menggunakan Python dan Streamlit

**Gambar Thumbnail/Cover:**
*[INSERT SCREENSHOT HERE — Tampilan utama dashboard]*

---

## 1. Pendahuluan

Bitcoin sebagai aset kripto terbesar di dunia telah menunjukkan volatilitas harga yang ekstrem sejak kemunculannya. Memahami pola pergerakan harga historis dan indikator teknikal menjadi krusial bagi investor dan analis untuk mengambil keputusan yang lebih terukur.

Proyek ini merupakan bagian dari Ujian Akhir Semester (UAS) mata kuliah Visualisasi Data. Tujuan utama proyek ini adalah membangun sebuah dashboard interaktif berbasis web yang mampu menampilkan data historis harga Bitcoin dari tahun 2015 hingga 2024 secara visual dan intuitif.

Dashboard yang dibangun memungkinkan pengguna untuk menjelajahi tren harga, menganalisis indikator teknikal seperti RSI dan MACD, serta memperoleh wawasan cepat melalui metrik-metrik utama yang disajikan secara real-time.

## 2. Tentang Tim Kami

- **[Nama Anggota 1]**: Peran
- **[Nama Anggota 2]**: Peran
- **[Nama Anggota 3]**: Peran

## 3. Dataset yang Digunakan

Dataset yang digunakan dalam proyek ini adalah `btc_2015_2024.xlsx`, yang mencakup data harga harian Bitcoin dari 2 Januari 2015 hingga 29 April 2024.

**Sumber Data:** Data diperoleh dari sumber historis pasar kripto. Informasi lebih lanjut dapat dilihat di bagian Referensi.

**Deskripsi Singkat:** Dataset terdiri dari 3.406 baris dan 20 kolom yang mencakup harga pembukaan (open), harga tertinggi (high), harga terendah (low), harga penutupan (close), volume perdagangan, serta berbagai indikator teknikal seperti RSI, MACD, Bollinger Bands, CCI, SMA, EMA, dan ATR.

**Fitur Utama:**
- Harga *Close* harian Bitcoin
- Volume transaksi
- Indikator RSI 7 dan RSI 14
- MACD (*Moving Average Convergence Divergence*)
- *Bollinger Bands*
- *Moving Average* (SMA 50, EMA 50, SMA 100, EMA 100)
- CCI 7 dan CCI 14
- *True Range* dan ATR 7/14

## 4. Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python
- **Framework Web:** Streamlit
- **Library Manipulasi Data:** Pandas
- **Library Visualisasi:** Plotly
- **Tools Pendukung:** Visual Studio Code, Git

Pemilihan Streamlit didasarkan pada kemudahan pembuatan dashboard data science secara cepat dengan sedikit kode. Plotly dipilih karena kemampuannya menghasilkan grafik interaktif yang responsif dan estetis.

## 5. Fitur Utama Website & Dashboard

Dashboard terdiri dari tiga menu utama yang dapat diakses melalui sidebar navigasi.

### Menu 1: Beranda (Home)

Halaman ini menyajikan gambaran umum dataset dan metrik utama.

*[INSERT SCREENSHOT HERE — Tampilan halaman Beranda dengan KPI cards]*

**Fitur:**
- Empat kartu KPI: Harga Terakhir, Harga Tertinggi (ATH), Harga Terendah, dan Rata-rata Harga.
- Tampilan cuplikan dataset (10 baris pertama) untuk memberikan konteks data.
- Informasi jumlah total baris dan kolom dataset.

### Menu 2: Tren Harga (Price Trends)

Halaman ini menampilkan visualisasi pergerakan harga penutupan Bitcoin dalam bentuk *line chart* interaktif.

*[INSERT SCREENSHOT HERE — Tampilan grafik Tren Harga dengan slider tahun]*

**Fitur:**
- *Slider* interaktif untuk memfilter rentang tahun (2015–2024).
- Grafik garis besar dengan area *fill* berwarna oranye (*Bitcoin orange*).
- Informasi statistik tambahan: harga awal, harga akhir, dan persentase perubahan selama periode terpilih.
- *Tooltip* interaktif saat *hover* untuk melihat detail harga pada tanggal tertentu.

### Menu 3: Indikator Teknikal (Technical Analysis)

Halaman ini memungkinkan pengguna membandingkan harga penutupan Bitcoin dengan berbagai indikator teknikal.

*[INSERT SCREENSHOT HERE — Tampilan halaman Indikator Teknikal dengan subplot]*

**Fitur:**
- *Multiselect* untuk memilih minimal 2 indikator yang ingin ditampilkan.
- Tata letak *subplot* vertikal dengan harga *close* di bagian atas dan indikator di bawahnya.
- Enam pilihan indikator: RSI 14, RSI 7, MACD, Bollinger Bands, CCI 14, SMA 50, EMA 50.
- Panel *expander* berisi penjelasan singkat setiap indikator.
- Palet warna monokromatik dengan aksen oranye Bitcoin untuk tampilan profesional.

## 6. Tantangan dan Proses Pembuatan

**Tantangan 1 — Konversi Format Tanggal:** Dataset awal menyimpan tanggal dalam format *serial number* Excel (integer). Solusinya adalah menggunakan konversi `pd.to_datetime('1899-12-30') + pd.to_timedelta()` untuk menghasilkan format datetime yang benar.

**Tantangan 2 — Performa Aplikasi:** Dataset yang cukup besar dapat menyebabkan aplikasi Streamlit lambat saat *reload*. Solusinya adalah menggunakan dekorator `@st.cache_data` agar data cukup dimuat sekali selama sesi berlangsung.

**Tantangan 3 — Tata Letak Profesional:** Menghindari tampilan yang terlihat seperti tugas kuliah biasa. Solusinya adalah menerapkan prinsip UI/UX: palet warna minimalis (hitam, abu-abu, oranye), *white space* yang cukup, serta kartu metrik dengan bayangan halus.

## 7. Kesimpulan dan Insight

Berdasarkan visualisasi data historis Bitcoin 2015–2024, beberapa insight yang dapat diperoleh:

1. **Volatilitas Tinggi:** Bitcoin menunjukkan volatilitas harga yang sangat tinggi. Pergerakan harga dari sekitar $200 pada awal 2015 hingga mencapai hampir $68.000 pada puncaknya (*all-time high*) menunjukkan potensi keuntungan sekaligus risiko yang besar.

2. **Siklus Pasar:** Terdapat pola siklus *bull run* dan *bear market* yang jelas. Puncak harga terjadi sekitar tahun 2017–2018 dan 2021, diikuti koreksi signifikan.

3. **Indikator Teknikal:** Penggunaan indikator seperti RSI dan MACD membantu mengidentifikasi kondisi *overbought* (jenuh beli) dan *oversold* (jenuh jual) yang sering kali mendahului pembalikan arah harga.

4. **Tren Jangka Panjang:** Meskipun volatil, tren jangka panjang Bitcoin menunjukkan pertumbuhan yang positif dari tahun ke tahun, meskipun dengan fluktuasi yang tajam di sepanjang perjalanannya.

## 8. Referensi & Link Proyek

- **Link Website / Dashboard:** [Link Streamlit Community Cloud — akan diisi setelah *deploy*]
- **Link GitHub Repository:** [Link GitHub Repository — akan diisi]
- **Link Dataset Asli:** [Link sumber dataset — akan diisi]

---

### Tips Pengembangan

1. Dashboard ini dapat di-*deploy* ke Streamlit Community Cloud agar dapat diakses secara publik oleh dosen dan teman-teman.
2. Gunakan *multi-page* atau *tabs* jika ingin memisahkan halaman penjelasan, dashboard, dan tentang tim secara lebih terstruktur.
3. Screenshot setiap grafik dapat diganti dengan gambar asli setelah aplikasi berjalan.
