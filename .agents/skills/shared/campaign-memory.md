# Campaign Memory System — Memori Persisten, Perlindungan Aset & Prasyarat

Setiap produk memiliki direktori kampanye permanen sendiri agar pengetahuan produk, aset visual, storyboard, prompt video, dan paket publikasi tetap terhubung lintas sesi dan lintas perintah.

## 1. Struktur Direktori Kampanye

Secara default, kampanye pengguna disimpan di `./campaigns/<slug-produk>/` pada direktori kerja aktif (contoh resmi repositori berada di `examples/campaigns/`):

```text
campaigns/<slug-produk>/
├── campaign.json
├── 01-product-review/
│   ├── references/          # Foto produk asli, screenshot listing, teks deskripsi (OTORITAS TERTINGGI)
│   ├── product-brief.md
│   ├── marketing-strategy.md
│   └── image-prompts.md
├── 02-generated-assets/
│   ├── hero/
│   ├── detail/
│   ├── demonstration/
│   ├── lifestyle/
│   ├── environment/
│   └── video-references/
├── 03-storyboard/
│   ├── storyboard.md
│   └── storyboard.png       # (atau storyboard-sheet-01.png, -02.png, ... / storyboard-v2.png)
├── 04-video/
│   ├── upload-assets/       # salinan siap upload terpadu (1..N.<ext>, storyboard*.png)
│   ├── video-plan.md
│   ├── video-01.md
│   └── video-02.md .. NN.md # jumlah segmen dinamis sesuai durasi & batas klip generator
├── 05-publishing/
│   └── publishing-package.md
├── _collaboration/          # pertukaran terstruktur HCE <-> AVD, log review dua arah (maks 3 iterasi)
└── _archive/                # cadangan otomatis versi lama file teks (.v1.md, .v2.md, ...)
```

## 2. Menjalankan Cek Memori Kampanye (`campaign_check.py`)

Setiap perintah wajib memeriksa kondisi kampanye sebelum bekerja.

- **Inisialisasi kampanye baru**:
  `python ../shared/scripts/campaign_check.py --init ./campaigns <slug> --product "<Nama Produk>"`
- **Cek kesiapan tahap**:
  `python ../shared/scripts/campaign_check.py ./campaigns/<slug> --stage review|storyboard|video`

Jika Python tidak tersedia di lingkungan user, jalankan pengecekan manual menggunakan aturan di bawah ini:
- **`review`**: cek isi `01-product-review/references/` dan apakah user sudah memberi deskripsi/foto produk.
- **`storyboard`**: wajib ada `01-product-review/product-brief.md`, `marketing-strategy.md`, `image-prompts.md`. Peringatkan (tetapi jangan blokir) jika `02-generated-assets/` belum berisi gambar.
- **`video`**: wajib ada seluruh output `/review` + `03-storyboard/storyboard.md` (status `approved` atau konfirmasi user). Peringatkan jika `03-storyboard/storyboard.png` (atau `storyboard-sheet-*.png`) belum ada (boleh lanjut jika user menyetujui memakai prompt storyboard tertulis, atau sarankan generate dulu).

## 3. Aturan Perlindungan Aset & Anti-Overwrite

1. **Baca Sebelum Menulis**: Selalu baca `campaign.json` dan file tahap sebelumnya sebelum menyusun output baru.
2. **Jangan Pernah Menimpa Gambar Milik Pengguna**: File di `01-product-review/references/` dan gambar yang sudah dibuat di `02-generated-assets/` atau `03-storyboard/storyboard.png` **tidak boleh ditimpa diam-diam**.
   - Jika menghasilkan versi gambar baru, simpan dengan sufiks versi (`hero-01-v2.png`, `storyboard-v2.png`) atau minta izin user sebelum mengganti file utama.
3. **Konfirmasi Perubahan Keputusan yang Disetujui**: Jika sebuah tahap atau aset bertanda `"approved": true` / `"status": "approved"` di `campaign.json`, **tanya user terlebih dahulu** sebelum mengganti sudut jualan, komposisi adegan, atau dialog yang sudah disepakati.
4. **Arsipkan File Teks Sebelum Memperbarui**: Saat memperbarui `product-brief.md`, `storyboard.md`, atau `video-XX.md` yang sudah ada setelah izin user, salin versi lama ke `_archive/<nama-file>.vN.md` terlebih dahulu agar riwayat tidak pernah hilang.

## 4. Penanganan Prasyarat yang Hilang

Jika file atau informasi wajib dari tahap sebelumnya tidak ada:
1. **Sebutkan secara spesifik** file/data apa yang hilang dan mengapa dibutuhkan.
2. **Tunjukkan langkah tercepat** untuk melengkapinya (misal: *"Jalankan `/review <slug>` lebih dulu"* atau *"Taruh foto asli produk ke `01-product-review/references/`"*).
3. **Jangan mengarang diam-diam**: Jika user ingin tetap lanjut membuat draf awal tanpa data lengkap, minta persetujuan user terlebih dahulu dan tandai seluruh bagian yang belum ada buktinya dengan label `[ASUMSI]`.

## 5. Mode ChatGPT (Web, Mobile, Desktop & Work)

Ketiga skill dapat dijalankan lintas klien dengan cara pemanggilan masing-masing permukaan:
- **Claude Code / Antigravity:** `/review`, `/storyboard`, `/video` (atau `/affiliate-video-director:<skill>` di mode plugin Claude Code).
- **ChatGPT (Web, Desktop, Mobile — Chat & Work):** pilih dengan **`@Affiliate Video Director`**, **`@review`**, **`@storyboard`**, atau **`@video`**, atau jelaskan tujuan tahap secara langsung agar dipicu secara implisit.
- **Codex CLI / IDE Extension:** panggil **`$review`**, **`$storyboard`**, **`$video`**, atau lewat menu **`/skills`**.

Menyesuaikan ketersediaan disk pada sesi ChatGPT:
1. **Lingkungan Berakses Disk Lokal (ChatGPT Desktop App / Codex CLI / Workspace):** Baca dan tulis langsung struktur `./campaigns/<slug-produk>/` serta jalankan `campaign_check.py` dan `dialogue_timing.py`.
2. **Lingkungan Tanpa Disk Lokal Persisten (ChatGPT Web / Mobile):**
   - Minta pengguna melampirkan atau menempelkan isi file tahap sebelumnya (`product-brief.md`, `marketing-strategy.md`, `image-prompts.md`, `storyboard.md`, `campaign.json`) serta foto asli produk di chat.
   - Sajikan setiap output dalam blok Markdown berlabel nama file baku (`01-product-review/product-brief.md`, `03-storyboard/storyboard.md`, `04-video/video-01.md`, `05-publishing/publishing-package.md`) agar pengguna dapat menyimpannya atau melampirkannya ke percakapan tahap berikutnya.
   - Jika alat eksekusi Python tidak aktif di sesi tersebut, hitung suku kata Bahasa Indonesia dan rasio durasi 60%–105% (laju standar 5,0 suku kata/detik) secara manual sesuai aturan `dialogue-engine.md` sebelum menandai status `OK`.
