# Product Intelligence — Analisis Produk Berbasis Fakta

Tujuan analisis produk adalah membangun fondasi informasi yang akurat sebelum menulis klaim pemasaran, prompt gambar, atau naskah video. Klaim yang mengada-ada merusak kredibilitas kreator dan berisiko terkena pembatasan platform.

## 1. Aturan Penandaan Fakta (Fact Tagging)

Setiap atribut produk di `product-brief.md` wajib diberi salah satu label berikut:

| Label | Arti | Sumber Sah | Boleh Dijadikan Klaim Video? |
|---|---|---|---|
| `[TERVERIFIKASI]` | Terlihat jelas di foto referensi asli atau tertulis eksplisit di deskripsi/screenshot listing penjual | Foto asli, screenshot listing, tabel spesifikasi penjual | **Ya**, nyatakan persis sesuai bukti |
| `[ASUMSI]` | Perkiraan logis dari bentuk visual atau kategori produk umum, tetapi belum tertera resmi | Inferensi visual/kategori | **Hanya jika dikonfirmasi user**, atau gunakan bahasa deskriptif visual non-mutlak |
| `[PERLU DICEK]` | Informasi krusial yang tidak ada di referensi dan berisiko jika ditebak (ukuran pasti, garansi, bahan kimia, daya baterai) | Data hilang | **Tidak**, wajib masuk daftar pertanyaan ke user |

> **Prinsip Ketat:** Jangan pernah menaikkan status `[ASUMSI]` menjadi `[TERVERIFIKASI]` hanya karena terdengar meyakinkan untuk iklan. Jika bahan tiang terlihat mengilap namun tidak tertulis "stainless steel 304", tandai sebagai `[ASUMSI] tampak seperti logam mengilap atau aluminium ringan — perlu konfirmasi material resmi`.

## 2. Daftar Periksa Karakteristik Fisik

Lakukan inspeksi menyeluruh dari foto referensi dan screenshot listing:

1. **Identitas Utama**: Nama produk, merek/seri (jika ada, atau tandai tanpa merek), kategori, varian warna/ukuran.
2. **Dimensi & Skala**: Panjang minimum–maksimum, lebar, tinggi, volume (ml/L), bobot perkiraan, proporsi saat digenggam tangan manusia.
3. **Material & Finishing**: Permukaan matte/glossy/transparan, tekstur kain/serat, sambungan plastik/logam, warna dominan & warna aksen (penting untuk menjaga konsistensi generasi gambar).
4. **Komponen & Mekanisme Kerja**:
   - Bagian bergerak: engsel, kunci putar (*twist-lock*), tutup flip, resleting, *nozzle* semprot, kepala lentur (*bendable*).
   - Indikator/antarmuka: layar LED, tombol fisik, port pengisian daya (USB-C/mikro).
   - Isi paket penjualan: unit utama, kepala cadangan, kabel, buku panduan, box.
5. **Detail Visual Khas (Visual Anchor)**: Ciri pembeda yang wajib tidak berubah di gambar/video AI (misal: bentuk lekuk gagang, warna cincin pengunci, tipe huruf label botol, motif jahitan kerah).

> **Integrasi PCS v2.0:** Hasil inspeksi `10` aspek identitas produk langsung dituangkan ke *Product Identity Sheet* (`../shared/templates/product-identity-lock.md`) sesuai [Product Consistency System](product-consistency-system.md) §1.

## 3. Peta Fungsi & Fitur ke Manfaat Nyata

Jangan berhenti pada fitur teknis; terjemahkan setiap fitur ke manfaat yang langsung dirasakan pembeli:

| Fitur Teknis | Mekanisme Kerja | Manfaat Praktis Bagi Pembeli | Bukti Visual yang Diperlukan |
|---|---|---|---|
| Contoh: Tiang teleskopik 2,3 m | Menggeser & mengunci ruas pipa | Membersihkan plafon tinggi tanpa naik kursi/tangga | Aksi memanjangkan tiang sambil berdiri di lantai |
| Contoh: Kepala lentur | Kawat inti ditekuk membentuk sudut | Menjangkau celah sempit atas lemari & bilah kipas | Aksi menekuk kepala sapu lalu menyapu sisi atas AC |

## 4. Memisahkan Fakta vs Asumsi dalam Output

Saat menyusun `product-brief.md`, pisahkan secara eksplisit menjadi dua bagian atau dua kolom agar `/storyboard` dan `/video` tidak tidak sengaja mempromosikan asumsi:

- **Fakta Terverifikasi (`[TERVERIFIKASI]`)**: Semua data yang aman diucapkan oleh voiceover dan ditekankan di teks layar.
- **Asumsi Visual & Hipotesis (`[ASUMSI]`)**: Hal yang tampak di foto tetapi belum teruji/tertulis (misal: tingkat keawetan, daya serap, kapasitas baterai riil).
- **Data yang Hilang (`[PERLU DICEK]`)**: Daftar terstruktur berisi informasi yang harus ditanyakan atau dikonfirmasi pengguna sebelum produksi final.

## 5. Daftar Informasi yang Sering Terlewat

Periksa apakah data berikut tersedia; jika belum, catat di bagian *Informasi yang Hilang*:

- Harga normal, harga promo, dan skema bundling/gratis ongkir.
- Ukuran/kapasitas pasti dalam satuan metrik (cm, m, ml, gram, mAh).
- Komposisi bahan/material resmi dari penjual.
- Kelengkapan isi paket (*in the box*).
- Batasan penggunaan atau peringatan keamanan (misal: tidak untuk permukaan basah, khusus pemakaian luar).
- Ketersediaan garansi, masa pakai, atau syarat retur toko.

## 6. Protokol Saat Referensi Minim

Jika pengguna hanya memberikan deskripsi singkat tanpa foto atau link:
1. Catat seluruh rincian visual yang belum ada sebagai `[PERLU DICEK]`.
2. Minta foto asli produk atau screenshot listing marketplace untuk akurasi maksimal.
3. Jika pengguna tetap ingin melanjutkan draf awal, lanjutkan dengan label `[ASUMSI]` yang jelas pada bagian tampilan fisik dan tandai prompt gambar sebagai draf sementara yang butuh penyesuaian setelah foto asli tersedia.
