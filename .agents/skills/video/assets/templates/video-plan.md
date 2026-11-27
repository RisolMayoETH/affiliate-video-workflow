# Video Generation Plan — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Acuan Otoritatif:** `03-storyboard/storyboard.md` (+ `storyboard.png` atau `storyboard-sheet-*.png`)
- **Total Durasi Storyboard:** `<total>` detik *(`<jumlah>` panel berdurasi variabel, maks. 40.0 detik)*
- **Rasio Aspek:** `9:16`
- **Batas Maksimal Per Klip Generator:** `<10.0>` detik *(default `10.0` dtk; ubah hanya jika generator terpilih secara eksplisit mendukung lebih lama dan dicatat di `campaign.json`)*
- **Jumlah Segmen Klip Dinamis:** `<M>` klip *(sesuai titik potong alami cerita — bukan jumlah tetap)*
- **Folder Bahan Upload Terpadu:** `04-video/upload-assets/` *(berisi `1.<ext>..N.<ext>` dan `storyboard.png` / `storyboard-sheet-*.png`)*

## Pemetaan Panel Storyboard ke Segmen Klip Video

| File Generasi | Panel Dicakup | Rentang Waktu Asli | Durasi Klip | Frame Awal → Frame Akhir & Transisi | Target File |
|---|---|---|---|---|---|
| Klip 1 | Adegan 1–3 | `00:00–00:08.5` | `8.5` dtk | Mulai dari hook (`1.jpg`) → tutup saat transisi ke demo (`3.jpg`) | `04-video/video-01.md` |
| Klip 2 | Adegan 4–6 | `00:08.5–00:18.0` | `9.5` dtk | Sambung gerak dari Klip 1 → tutup di hasil transisi before-after | `04-video/video-02.md` |
| Klip 3..M | Adegan 7–N | `00:18.0–<total>` | `≤ 10.0` dtk | Sambung hingga hero penutup & zona aman CTA | `04-video/video-03.md` ... |

*(Sesuaikan jumlah baris dan durasi segmen dengan `total_duration` storyboard serta batas klip generator.)*

## Ringkasan Kunci Kontinuitas Lintas Generasi

- **Identitas Produk (Otoritas #1):** ...
- **Karakter Tangan & Pakaian:** ...
- **Ruangan & Pencahayaan:** ...
- **Identitas Audio VO:** Pengulas *off-camera* berbahasa Indonesia, suara hangat-tegas, tanpa wajah tampil.
