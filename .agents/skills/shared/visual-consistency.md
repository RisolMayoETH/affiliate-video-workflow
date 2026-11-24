# Visual Consistency — Hierarki Otoritas Aset & Kunci Identitas Produk

Kesalahan terbesar dalam produksi iklan berbasis AI adalah *product drift*: warna botol berganti, panjang gagang menyusut, logo meleleh, atau tangan mendadak berganti baju antar adegan. Dokumen ini menetapkan hukum otoritas visual yang wajib dipatuhi ketiga perintah.

## 1. Lima Klasifikasi Gambar & Hierarki Otoritas

Setiap gambar dalam kampanye wajib masuk salah satu dari lima kelas berikut. Angka lebih kecil berarti otoritas lebih tinggi:

| Peringkat | Kategori Resmi (`campaign.json`) | Deskripsi & Lokasi Penyimpanan | Peran Otoritatif |
|---|---|---|---|
| **1 (Tertinggi)** | `product-reference` | Foto asli produk, screenshot listing marketplace (`01-product-review/references/`) | **Sumber Kebenaran Tunggal** untuk bentuk fisik, warna, label, proporsi, material, dan kelengkapan produk |
| **2** | `generated-lifestyle` | Foto hero, detail makro, lifestyle, dan referensi ruangan hasil generate (`02-generated-assets/hero/`, `detail/`, `lifestyle/`, `environment/`) | Referensi gaya, suasana ruangan, dan pencahayaan yang sudah divalidasi cocok dengan #1 |
| **3** | `product-demonstration` | Foto hasil generate yang memperlihatkan tangan memegang/memakai produk (`02-generated-assets/demonstration/`) | Referensi posisi jari, pose penggunaan, dan konsistensi tangan/lengan yang cocok dengan #1 |
| **4** | `video-reference` | Frame awal / keyframe terpilih untuk langsung diumpankan ke generator video (`02-generated-assets/video-references/`) | Frame jangkar visual saat generasi video dimulai |
| **5** | `storyboard` | Gambar panel storyboard berurutan (`03-storyboard/storyboard.png`) | Otoritas **urutan adegan, komposisi frame, arah gerak, dan timing** — **bukan** otoritas detail fisik produk |

## 2. Aturan Emas Pencegahan Konflik Aset

1. **Referensi Asli Selalu Menang**: Gambar hasil generate (#2, #3, #4, #5) **tidak pernah** lebih berwenang daripada referensi produk asli (#1).
2. **Penanganan Konflik**: Jika gambar hasil generate memiliki detail produk yang melenceng (misal: kepala sapu berubah warna, jumlah ruas berbeda, teks botol ngaco), **peringkat #1 menang**. Catat konflik tersebut di evaluasi `/storyboard` dan perbaiki atau beri instruksi koreksi eksplisit sebelum dipakai di `/video`.
3. **Jangan Ulangi Kesalahan di Prompt Video**: Saat menulis prompt video, selalu lampirkan `product-reference` (#1) berdampingan dengan `video-reference`/`product-demonstration` dan `storyboard` (#5), lalu jelaskan peran masing-masing referensi secara tegas.

## 3. Aturan Bahasa Prompt Generator vs Dialog

- **Prompt Gambar & Video (Copy-Ready)**: Selalu tulis dalam **Bahasa Inggris** yang presisi secara sinematografi dan anatomi fisik, karena generator gambar/video modern (ImageGen, Veo, Kling, Sora, Google Flow) merespons arahan kamera, tekstur, dan fisika jauh lebih akurat dalam bahasa Inggris.
- **Dialog VO / Ucapan Terdengar**: Selalu tulis dalam **Bahasa Indonesia natural** di dalam tanda kutip verbatim (`"..."`) pada blok audio/dialog agar pengucapan tetap lokal dan sinkron dengan `## Tabel Timing Dialog`.

## 4. Blok Wajib Pengunci Identitas (Identity Locks)

Setiap prompt gambar di `/review` dan prompt video di `/video` wajib memuat kunci konsistensi:

- **PRODUCT IDENTITY LOCK**: Bentuk geometris, rasio dimensi, warna tiap komponen (utama & aksen), tipe permukaan (*matte/glossy/brushed*), ciri mekanis (ulir kunci, engsel, tutup), larangan mengubah label/proporsi.
- **HAND / CHARACTER LOCK**: Warna kulit, bentuk jari, kuku, ketiadaan aksesori berlebih, serta warna/potongan lengan pakaian yang identik di semua generasi.
- **ENVIRONMENT & LIGHTING LOCK**: Jenis ruangan, warna dinding/meja, posisi jendela/sumber cahaya, arah bayangan, dan suhu warna (*color temperature*) agar sambungan antar video tidak loncat.

## 5. Daftar Periksa Evaluasi Aset di `/storyboard`

Sebelum aset dipakai sebagai referensi video, beri penilaian eksplisit untuk 6 aspek:
1. Akurasi bentuk & warna produk terhadap `product-reference`
2. Konsistensi tangan/lengan & anatomi jari
3. Kestabilan arah dan warna pencahayaan
4. Kebersihan & kesesuaian latar lingkungan
5. Ruang aman komposisi vertikal 9:16
6. Kelayakan langsung sebagai gambar awal generator video (`Pakai` / `Perbaiki` / `Buang`)
