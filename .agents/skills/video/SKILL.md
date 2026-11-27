---
name: video
description: "Affiliate Video Director /video - rekayasa prompt video AI per segmen generasi (maks. 10 detik per klip kecuali generator mendukung lebih, total video final maks. 40 detik, vertikal 9:16) dari storyboard yang disetujui: arsitektur 11 blok Product Consistency System v2.0, timeline per detik, koreografi kamera terkontrol, kontinuitas per shot, Product-Only Mode opsional, audio VO Bahasa Indonesia tepat waktu, serta paket publikasi TikTok & Reels. Gunakan setelah /storyboard disetujui."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.2.0"
  project: affiliate-video-director
---

# /video — Rekayasa Prompt Video AI, Segmentasi Klip & Paket Publikasi

Berperanlah sebagai **AI Video Prompt Engineer & Commercial Cinematographer**. Tugasmu adalah mengonversi storyboard yang sudah disetujui (`total_duration ≤ 40` detik) menjadi segmen generasi video AI yang logis, konsisten dengan standar global **Product Consistency System (PCS v2.0)**, sinematis, sinkron durasi dialog, serta paket publikasi siap unggah untuk TikTok, Instagram Reels, dan Facebook Reels.

**Input Argumen:** `$ARGUMENTS` (slug kampanye atau path direktori kampanye, opsional disertai opsi `product-only`). Jika kosong, cek kampanye terbaru di `./campaigns/` atau tanyakan ke pengguna.

## Langkah 0: Cek Prasyarat Kampanye

1. Jalankan pengecekan tahap video:
   `python ../shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage video`
   *(Jika dijalankan lewat plugin di folder lain, gunakan `${CLAUDE_SKILL_DIR}/../shared/scripts/campaign_check.py`.)*
2. Baca wajib: `campaign.json`, `01-product-review/product-brief.md`, `01-product-review/marketing-strategy.md`, `03-storyboard/storyboard.md`, serta seluruh daftar aset di `01-product-review/references/`, `02-generated-assets/`, dan `03-storyboard/storyboard*.png`.
3. **Baca / Lengkapi `01-product-review/product-identity-lock.md` (PCS §1):** Jika file ini sudah ada, jadikan acuan otoritatif untuk blok identitas produk. Jika belum ada, buat dari [Template Product Identity Sheet](../shared/templates/product-identity-lock.md) berdasarkan hasil `/review` dan foto asli di `01-product-review/references/`, lalu tandai detail yang belum pasti sebagai `[PERLU DICEK]` (memicu status `WARNING` di QC tanpa mengarang fakta).
4. Jika `storyboard.md` hilang (kode keluar `2`), hentikan proses dan jelaskan agar pengguna menjalankan `/storyboard <slug-produk>` dulu. Jika `storyboard.md` masih berstatus `draft`, lanjutkan hanya jika ada tanda persetujuan kolaborasi otonom HCE ↔ AVD di `campaign.json` atau setelah konfirmasi pengguna.

## Pengetahuan yang Dimuat

Baca modul pengetahuan berikut sesuai tahap `/video`:

- [**Product Consistency System (PCS v2.0)**](../shared/product-consistency-system.md) *(Sumber Kebenaran Tunggal konsistensi identitas produk)*
- [Memori Kampanye](../shared/campaign-memory.md)
- [Rekayasa Video](../shared/video-engineering.md)
- [Bahasa Kamera](../shared/camera-language.md)
- [Mesin Dialog](../shared/dialogue-engine.md)
- [Konsistensi Visual](../shared/visual-consistency.md)
- [Interaksi Produk](../shared/product-interaction.md)
- [Optimasi Platform](../shared/platform-optimization.md)
- [Copywriting Konversi](../shared/conversion-copywriting.md)
- [Protokol Kolaborasi HCE](../shared/hce-collaboration.md)

## Alur Kerja (A – G)

### A. Adaptive Video Clip Segmentation
- Pecah storyboard yang disetujui ke `04-video/video-plan.md` dalam rasio vertikal **9:16** (total durasi final maks. **40 detik**, sama persis dengan storyboard).
- Batas maksimal per segmen klip adalah **10 detik** (kecuali generator terpilih secara eksplisit mendukung durasi lebih panjang dan dicatat di `campaign.json`).
- **Durasi Wajib Bilangan Bulat (Tanpa Koma/Desimal):** Generator video AI tidak menerima durasi pecahan/koma (seperti `9,5` atau `9.5` detik). Oleh karena itu, durasi setiap klip video (`Duration: <N> seconds.`), penanda waktu di dalam timeline klip (`0s–3s`, `3s–6s`, dst.), serta durasi tiap adegan penyusunnya **wajib berupa bilangan bulat utuh** (misal `10` detik penuh, bukan `9.5` detik).
- **Jumlah klip dinamis** (bisa 1, 2, 3, 4, 5, atau lebih—**jangan pernah memaksa setiap kampanye menjadi tepat 2 video**). Gabungkan beberapa panel storyboard berdurasi bulat ke dalam satu segmen klip bila masuk akal dan tidak melebihi batas klip.

### B. Video Prompt Engineering & Paket Upload Terpadu (Arsitektur 11 Blok PCS)
- Salin (tanpa memindahkan atau menghapus file asli) aset foto jangkar tiap adegan dari `02-generated-assets/` secara berurutan (`1.<ext>`, `2.<ext>`, ..., `N.<ext>`) serta gambar storyboard (`storyboard.png` atau `storyboard-sheet-01.png`, ...) ke satu folder siap upload **`04-video/upload-assets/`** agar pengguna mudah mencari seluruh bahan upload sekaligus.
- Buat file terpisah `04-video/video-01.md`, `video-02.md`, ..., `video-NN.md`. Setiap file wajib mengikuti **Arsitektur Master Prompt 11 Blok PCS v2.0** (`../shared/product-consistency-system.md` §7):
  - `[1. VIDEO SPECIFICATION]` *(durasi bilangan bulat, rasio 9:16)*
  - `[2. PRODUCT IDENTITY LOCK]` *(English Identity Descriptor spesifik dari `01-product-review/product-identity-lock.md`)*
  - `[3. OBJECT PERMANENCE LOCK]` *(7 aturan permanensi + daftar komponen & bagian bergerak)*
  - `[4. ANTI-MORPHING LOCK]` *(larangan inti + larangan spesifik produk)*
  - `[5. HUMAN MODE]` **atau** `[5. PRODUCT-ONLY MODE]` *(sesuai `Mode Subjek` aktif)*
  - `[6. ENVIRONMENT & CONTINUITY LOCK]` *(ruangan, cahaya, zona tengah + `First-Frame Anchor (0.0s)`)*
  - `[7. SHOT-BY-SHOT TIMELINE]` *(setiap shot memakai format baris PCS §5 + `Last-Frame Anchor` di akhir)*
  - `[8. CAMERA MOVEMENT CONTROL]` *(profil risiko produk + aturan gerak kamera PCS §4)*
  - `[9. AUDIO DIRECTION]` *(arahan BGM, SFX, dan VO Bahasa Indonesia verbatim)*
  - `[10. NEGATIVE PROMPT]` *(gabungan anti-morphing spesifik + shot negatives + subject-mode negatives)*
  - `[11. FINAL PRODUCT IDENTITY VERIFICATION]` *(verifikasi akhir identitas fisik)*
- Untuk setiap klip lanjutan (`video-02.md`, `video-03.md`, `video-04.md`, dan seterusnya), wajib diawali kalimat `"Continue the video."` pada baris pertama di dalam blok **Master Video Prompt** tepat sebelum `[1. VIDEO SPECIFICATION]` (jangan dicantumkan pada `video-01.md`).
- Sertakan pula `## 6. Quality Control Konsistensi Produk (PCS v2.0)` beserta status (`PASS` / `WARNING` / `FAIL`) di setiap `video-NN.md` tepat sebelum `## Tabel Timing Dialog`.

### C. Camera Direction (PCS §4)
- Terapkan **System 4 — Camera Movement Control** (`../shared/product-consistency-system.md` §4): tetapkan 8 parameter kamera sebelum menulis master prompt dan sesuaikan gerak dengan profil risiko produk (*Simple/Rigid*, *Moderate*, *Complex*).
- Gunakan teknik bermakna (*tracking*, *dolly*, *macro*, *rack focus*, *match cut*, *whip pan*, *POV*, *action transition*). Utamakan kamera bergerak mengelilingi produk diam; larang zoom atau rotasi produk tanpa alasan, perubahan perspektif ekstrem, serta orbit `360°` penuh kecuali perlu dan didukung referensi multi-sudut. Tidak ada batas sudut seragam untuk semua produk.

### D & E. Audio & Dialogue Timing
- Default **pengulas off-camera berbahasa Indonesia natural**, ekspresif, tanpa pembicara tampak di layar.
- Pecah dialog persis per timestamp panel dan **tulis angka dengan kata** (gunakan `[jeda]` bila panel singkat sengaja hening/ASMR). Pastikan tiap `video-NN.md` memiliki `## Tabel Timing Dialog` (di bagian paling akhir file) lalu jalankan validator:
  `python ../shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/04-video/video-01.md` *(ulang untuk setiap file `video-NN.md`)*.

### F. Continuity & Mode Subjek (Human Demo vs Product-Only Mode)
- Jaga kesamaan mutlak identitas produk di setiap shot (**PCS §5 Shot-by-Shot Identity Continuity**), ruangan, arah cahaya, perspektif kamera, frame awal/akhir antar klip, dan karakter suara di seluruh generasi video.
- **Mode Subjek (`Human Demo` vs `Product-Only Mode`, PCS §6):** Default adalah **`Human Demo`** (tangan/lengan konsisten tanpa wajah). Aktifkan **`Product-Only Mode`** **hanya** bila pengguna meminta eksplisit (*"tanpa manusia"*, *"tanpa tangan"*, *"produk saja"*, `product-only`) atau sesuai instruksi storyboard yang disetujui; gunakan teknik *commercial product showcase* (*Front hero view*, *Three-quarter view*, *Side profile*, *Macro detail*, *Final hero shot*) dan catat **`Mode Subjek: Human Demo | Product-Only`** di `video-plan.md` dan setiap `video-NN.md`.

### G. Publishing Package & Audit Final HCE ↔ AVD
- Buat `05-publishing/publishing-package.md` berisi 3 variasi caption SEO, kelompok hashtag, 5 variasi CTA lintas platform, 5 alternatif hook pembuka, dan catatan zona aman overlay teks (termasuk penempatan *on-screen text* dari storyboard).
- Pastikan seluruh caption, 5 alternatif hook, dan 5 variasi CTA lolos evaluasi HCE (`NaturalLanguageRefiner` + 7 dimensi + *Hard Integrity Gate* — bebas klise AI, bebas urgensi/diskon fiktif, dan tepat platform) dengan menjalankan:
  `python ../shared/scripts/hce_bridge.py hce-review ./campaigns/<slug-produk>`
- Jalankan pengecekan menyeluruh kampanye:
  `python ../shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage video --validate-timing --check-collaboration`

## File Output, Template & Gerbang Kualitas

1. `04-video/video-plan.md` — [Template Rencana Video](assets/templates/video-plan.md)
2. `04-video/video-01.md`, `video-02.md`, ... — [Template Prompt Video](assets/templates/video-prompt.md)
3. `05-publishing/publishing-package.md` — [Template Paket Publikasi](assets/templates/publishing-package.md)

Perbarui `campaign.json` (`stages.video.max_clip_duration`, `stages.video.generations`, `stages.video.status`, `stages.publishing`, `collaboration`). Arsipkan versi lama ke `_archive/` sebelum menimpa file teks yang sudah disetujui.
**Gerbang Kualitas:** Total durasi storyboard `≤ 40` dtk; total durasi seluruh `video-NN.md` tepat sama dengan storyboard; setiap klip `≤ batas generator` (default `10` dtk); setiap panel tercakup tepat satu kali; fakta produk konsisten; status QC Konsistensi Produk (PCS v2.0) pada setiap `video-NN.md` bernilai `PASS` atau `WARNING` (dilarang `FAIL`); seluruh `dialogue_timing.py` lolos keluar kode `0`; evaluasi HCE `PASSED` dan kolaborasi selesai ≤ 3 iterasi.
