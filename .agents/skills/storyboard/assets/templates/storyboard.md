# Storyboard — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Sudut Jualan Utama:** <dari marketing-strategy.md>
- **Alasan Pemilihan Durasi & Jumlah Panel:** <kompleksitas produk, poin jualan, kebutuhan demo/validasi, dan target durasi tanpa filler>
- **Jumlah Adegan:** `<N>` panel *(adaptif sesuai cerita; kisaran awal 6–14 panel, tanpa batas kaku)*
- **Total Durasi:** `<total>` detik *(maks. 40.0 detik; target default 25–35 detik)*
- **Rasio:** `9:16`
- **Status Storyboard:** Draft / Approved *(Setelah disetujui, menjadi acuan otoritatif bagi `/video`)*
- **File Gambar Storyboard:** `03-storyboard/storyboard.png` *(atau daftar lembar berurutan `03-storyboard/storyboard-sheet-01.png`, `storyboard-sheet-02.png` bila > 6–8 panel)*

## 1. Evaluasi Aset Visual (Audit Pra-Storyboard)

| Aset Diperiksa | Kategori | Akurasi Produk vs Ref #1 | Konsistensi Tangan & Cahaya | Komposisi 9:16 | Layak Video? | Vonis |
|---|---|---|---|---|---|---|
| `...` | `...` | ... | ... | ... | Ya/Tidak | `Pakai` / `Perbaiki` / `Buang` |

> **Catatan Hierarki Otoritas:** Apabila terdapat perbedaan detail fisik pada gambar hasil generate, foto referensi asli di `01-product-review/references/` selalu menang.

## 2. Alur Cerita, Struktur Pemasaran & Ritme Editing

- **Struktur Pemasaran Adaptif:** `HOOK` (`00:00–...`) → `PROBLEM / DESIRE` → `PRODUCT REVEAL` → `PRODUCT VALIDATION` → `DEMONSTRATION` → `BENEFIT / RESULT` → `CTA` *(gabungkan tahap bila lebih tajam; langsung mulai dengan hook tanpa intro lambat)*.
- **Strategi Ritme Editing:** <jelaskan variasi durasi cepat–sedang–panjang antar panel dan tujuan tiap pergantian shot>.
- **Kunci Kontinuitas:** <Product Lock, Hand/Sleeve Lock, Environment & Lighting Lock>.

## 3. Rincian Desain Adegan

### Adegan 1 — <Judul Adegan> (`<00:00–00:02>`, `<2.0>` dtk)
- **Deskripsi & Komposisi Visual:** ...
- **Aksi Fisik Produk:** ...
- **Interaksi Produk:** ...
- **Sudut & Posisi Kamera:** ...
- **Gerakan Kamera & Tujuan Naratif:** `<Teknik Kamera> — Tujuan: <alasan menjual/cerita>`
- **Pencahayaan & Ruang Aman 9:16:** ...
- **Dialog (VO):** `"..."` *(atau `[jeda]`)*
- **Teks Layar (*On-Screen Text*):** `<teks singkat opsional atau "Tidak ada">`
- **Tujuan Pemasaran (*Marketing Purpose*):** `<Tangkap perhatian / Ungkap informasi / Demo fungsi / Tunjukkan manfaat / Bangun kepercayaan / Emosi / Dorong checkout>`
- **Transisi ke Panel Berikutnya:** ...

*(Ulangi blok di atas untuk Adegan 2, 3, ..., N dengan durasi variabel yang sesuai aksi; pastikan penjumlahan durasi seluruh adegan = Total Durasi video final `≤ 40.0` detik.)*

## Tabel Timing Dialog

| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |
|---|---|---|---|---|---|---|
| 1 | 00:00–00:02 | 2.0 | "..." | 0 | 0.00 | OK |
| 2 | 00:02–00:05 | 3.0 | "..." | 0 | 0.00 | OK |

## Prompt Gambar Storyboard

*(Sesuaikan jumlah lembar dengan total panel: 1 gambar grid `2×2` untuk 4 panel, `2×3` untuk 6 panel, atau pecah ke beberapa lembar berurutan `storyboard-sheet-01.png`, `storyboard-sheet-02.png` untuk 8–14+ panel agar tetap terbaca tajam.)*

```text
Create a clean <K>-panel commercial storyboard sheet (<grid layout, e.g. 2x3 or 2x4, or Sheet 1 of M for Panels 1-K>, each panel in 9:16 portrait proportion) for <product>.
Attach and strictly obey the exact physical shape, colors, and materials of the product from the original product reference photo.
Panel 1 (top-left): ...
Panel 2: ...
...
Keep consistent Indonesian adult hand, neutral sleeve, natural daylight home setting, subtle panel numbers 1-<K> in corner, minimal directional camera arrows, no long captions or speech bubbles.
```
