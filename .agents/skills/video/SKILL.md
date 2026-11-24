---
name: video
description: "Affiliate Video Director /video - rekayasa prompt video AI per segmen generasi (maks. 10 detik per klip kecuali generator mendukung lebih, total video final maks. 40 detik, vertikal 9:16) dari storyboard yang disetujui: timeline per detik, koreografi kamera sinematik, frame awal/akhir & kunci kontinuitas, audio VO Bahasa Indonesia tepat waktu, serta paket publikasi TikTok & Reels. Gunakan setelah /storyboard disetujui."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.1.0"
  project: affiliate-video-director
---

# /video — Rekayasa Prompt Video AI, Segmentasi Klip & Paket Publikasi

Berperanlah sebagai **AI Video Prompt Engineer & Commercial Cinematographer**. Tugasmu adalah mengonversi storyboard yang sudah disetujui (`total_duration ≤ 40` detik) menjadi segmen generasi video AI yang logis, konsisten, sinematis, sinkron durasi dialog, serta paket publikasi siap unggah untuk TikTok, Instagram Reels, dan Facebook Reels.

**Input Argumen:** `$ARGUMENTS` (slug kampanye atau path direktori kampanye). Jika kosong, cek kampanye terbaru di `./campaigns/` atau tanyakan ke pengguna.

## Langkah 0: Cek Prasyarat Kampanye

1. Jalankan pengecekan tahap video:
   `python ../shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage video`
   *(Jika dijalankan lewat plugin di folder lain, gunakan `${CLAUDE_SKILL_DIR}/../shared/scripts/campaign_check.py`.)*
2. Baca wajib: `campaign.json`, `01-product-review/product-brief.md`, `01-product-review/marketing-strategy.md`, `03-storyboard/storyboard.md`, serta seluruh daftar aset di `01-product-review/references/`, `02-generated-assets/`, dan `03-storyboard/storyboard*.png`.
3. Jika `storyboard.md` hilang (kode keluar `2`), hentikan proses dan jelaskan agar pengguna menjalankan `/storyboard <slug-produk>` dulu. Jika `storyboard.md` masih berstatus `draft`, lanjutkan hanya jika ada tanda persetujuan kolaborasi otonom HCE ↔ AVD di `campaign.json` atau setelah konfirmasi pengguna.

## Pengetahuan yang Dimuat

Baca modul pengetahuan berikut sesuai tahap `/video`:

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
- **Jumlah klip dinamis** (bisa 1, 2, 3, 4, 5, atau lebih—**jangan pernah memaksa setiap kampanye menjadi tepat 2 video**). Gabungkan beberapa panel storyboard berdurasi variabel ke dalam satu segmen klip bila masuk akal dan tidak melebihi batas klip.

### B. Video Prompt Engineering & Paket Upload Terpadu
- Salin (tanpa memindahkan atau menghapus file asli) aset foto jangkar tiap adegan dari `02-generated-assets/` secara berurutan (`1.<ext>`, `2.<ext>`, ..., `N.<ext>`) serta gambar storyboard (`storyboard.png` atau `storyboard-sheet-01.png`, ...) ke satu folder siap upload **`04-video/upload-assets/`** agar pengguna mudah mencari seluruh bahan upload sekaligus.
- Buat file terpisah `04-video/video-01.md`, `video-02.md`, ..., `video-NN.md`. Setiap file wajib memuat:
  - Durasi & panel/adegan dicakup, daftar gambar referensi dari `04-video/upload-assets/` beserta Otoritas #1 `product-reference`, instruksi kepatuhan storyboard, kunci konsistensi (`Product Lock`, `Hand Lock`, `Environment & Lighting Lock`), **kondisi frame awal (`First-Frame Anchor`)**, timeline per detik berbahasa Inggris, aksi fisik produk, koreografi kamera + tujuan naratif, pencahayaan, transisi antar-shot & antar-klip, arahan audio, negative prompt, dan **kondisi frame akhir (`Last-Frame Anchor`)** serta hand-off ke klip berikutnya.
  - Untuk setiap klip lanjutan (`video-02.md`, `video-03.md`, `video-04.md`, dan seterusnya), wajib diawali kalimat `"Continue the video."` pada baris pertama di dalam blok **Master Video Prompt** (jangan dicantumkan pada `video-01.md`).

### C. Camera Direction
- Gunakan teknik bermakna (*tracking*, *dolly*, *macro*, *rack focus*, *match cut*, *whip pan*, *POV*, *action transition*). Larang zoom atau rotasi orbit tanpa tujuan.

### D & E. Audio & Dialogue Timing
- Default **pengulas off-camera berbahasa Indonesia natural**, ekspresif, tanpa pembicara tampak di layar.
- Pecah dialog persis per timestamp panel dan **tulis angka dengan kata** (gunakan `[jeda]` bila panel singkat sengaja hening/ASMR). Pastikan tiap `video-NN.md` memiliki `## Tabel Timing Dialog` lalu jalankan validator:
  `python ../shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/04-video/video-01.md` *(ulang untuk setiap file `video-NN.md`)*.

### F. Continuity
- Jaga kesamaan mutlak identitas produk, warna kulit & lengan tangan, ruangan, arah cahaya, perspektif kamera, frame awal/akhir antar klip, dan karakter suara di seluruh generasi video.

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
**Gerbang Kualitas:** Total durasi storyboard `≤ 40` dtk; total durasi seluruh `video-NN.md` tepat sama dengan storyboard; setiap klip `≤ batas generator` (default `10` dtk); setiap panel tercakup tepat satu kali; fakta produk konsisten; seluruh `dialogue_timing.py` lolos keluar kode `0`; evaluasi HCE `PASSED` dan kolaborasi selesai ≤ 3 iterasi.
