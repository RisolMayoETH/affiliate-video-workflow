# Video Generation Plan — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode Subjek:** `<Human Demo | Product-Only>`
- **Acuan Otoritatif:** `03-storyboard/storyboard.md` (+ `storyboard.png` atau `storyboard-sheet-*.png`)
- **Total Durasi Storyboard:** `<total>` detik *(`<jumlah>` panel berdurasi variabel, maks. 40.0 detik)*
- **Rasio Aspek:** `9:16`
- **Batas Maksimal Per Klip Generator:** `<10.0>` detik *(default `10.0` dtk; ubah hanya jika generator terpilih secara eksplisit mendukung lebih lama dan dicatat di `campaign.json`)*
- **Jumlah Segmen Klip Dinamis:** `<M>` klip *(sesuai titik potong alami cerita — bukan jumlah tetap)*
- **Folder Bahan Upload Terpadu:** `04-video/upload-assets/` *(berisi `1.<ext>..N.<ext>` dan `storyboard.png` / `storyboard-sheet-*.png`)*

## Pemetaan Panel Storyboard ke Segmen Klip Video

| File Generasi | Panel Dicakup | Rentang Waktu Asli | Durasi Klip | Frame Awal → Frame Akhir & Transisi | Target File |
|---|---|---|---|---|---|
| Klip 1 | Adegan 1–3 | `00:00–00:08` | `8` dtk | Mulai dari hook (`1.jpg`) → tutup saat transisi ke demo (`3.jpg`) | `04-video/video-01.md` |
| Klip 2 | Adegan 4–6 | `00:08–00:18` | `10` dtk | Sambung gerak dari Klip 1 → tutup di hasil transisi before-after | `04-video/video-02.md` |
| Klip 3..M | Adegan 7–N | `00:18–<total>` | `≤ 10` dtk | Sambung hingga hero penutup & zona aman CTA | `04-video/video-03.md` ... |

*(Sesuaikan jumlah baris dan durasi segmen dengan `total_duration` storyboard serta batas klip generator.)*

## Ringkasan Kunci Kontinuitas Lintas Generasi

- **Product Identity Sheet (PCS v2.0):** `01-product-review/product-identity-lock.md` (`<ringkasan English Identity Descriptor & profil risiko kamera>`)
- **Karakter Tangan & Pakaian (`Mode Subjek`):** `<Human Demo: tangan konsisten tanpa wajah | Product-Only Mode: tanpa manusia/tangan sama sekali>`
- **Ruangan & Pencahayaan:** ...
- **Identitas Audio VO:** Pengulas *off-camera* berbahasa Indonesia, suara hangat-tegas, tanpa wajah tampil.
