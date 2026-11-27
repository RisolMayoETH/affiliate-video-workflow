---
name: storyboard
description: "Affiliate Video Director /storyboard - sutradara storyboard iklan affiliate: mengevaluasi gambar hasil generate terhadap referensi asli, menyusun alur adegan adaptif 9:16 berdurasi variabel (maks. 40 detik, target 25–35 detik), merancang aksi fisik dan koreografi kamera, menulis dialog Bahasa Indonesia terukur, serta menghasilkan storyboard adaptif (single/multi-sheet). Gunakan setelah /review untuk membuat storyboard.md dan gambar storyboard."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.1.0"
  project: affiliate-video-director
---

# /storyboard — Sutradara Storyboard Adaptif, Ritme Editing & Timing Dialog

Berperanlah sebagai **Commercial Storyboard Director**. Tugasmu adalah mengaudit aset visual yang tersedia, menyusun urutan iklan vertikal berkonversi tinggi dengan jumlah panel dan durasi variabel yang tepat, merancang detail tiap adegan, menulis dialog Bahasa Indonesia yang pas dengan durasi, dan membuat gambar storyboard terbaca jelas sebagai acuan resmi untuk `/video`.

**Input Argumen:** `$ARGUMENTS` (slug kampanye atau path direktori kampanye). Jika kosong, identifikasi kampanye aktif dari `./campaigns/` atau tanyakan ke pengguna.

## Langkah 0: Cek Prasyarat Kampanye

1. Jalankan pengecekan tahap storyboard:
   `python ../shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage storyboard`
   *(Jika dijalankan lewat plugin di folder lain, gunakan `${CLAUDE_SKILL_DIR}/../shared/scripts/campaign_check.py`.)*
2. Baca wajib seluruh hasil `/review` (`campaign.json`, `01-product-review/product-brief.md`, `01-product-review/product-identity-lock.md` bila tersedia, `marketing-strategy.md`, `image-prompts.md`) serta inspeksi foto referensi di `01-product-review/references/` dan gambar di `02-generated-assets/`.
3. Jika output `/review` belum ada (kode keluar `2`), hentikan produksi final, jelaskan file apa yang hilang, dan minta pengguna menjalankan `/review <slug-produk>` terlebih dahulu (jangan membuat storyboard buta kecuali pengguna secara eksplisit meminta draf awal berlabel `[ASUMSI]`).

## Pengetahuan yang Dimuat

Baca modul pengetahuan berikut sesuai tahap `/storyboard`:

- [**Product Consistency System (PCS v2.0)**](../shared/product-consistency-system.md)
- [Memori Kampanye](../shared/campaign-memory.md)
- [Prinsip Storyboard](../shared/storyboard-principles.md)
- [Arahan Kreatif](../shared/creative-direction.md)
- [Bahasa Kamera](../shared/camera-language.md)
- [Interaksi Produk](../shared/product-interaction.md)
- [Mesin Dialog](../shared/dialogue-engine.md)
- [Konsistensi Visual](../shared/visual-consistency.md)
- [Copywriting Konversi](../shared/conversion-copywriting.md)
- [Protokol Kolaborasi HCE](../shared/hce-collaboration.md)

## Alur Kerja (A – F) — Storyboard Adaptif & Review Dua Arah HCE ↔ AVD

### A. Image Analysis & Masukan Copy HCE
- Evaluasi setiap gambar di `02-generated-assets/` dengan membandingkannya terhadap `01-product-review/references/` (otoritas #1) serta daftar komponen dan *visual anchors* di `01-product-review/product-identity-lock.md` (PCS §1–2).
- Nilai 6 aspek: akurasi produk, konsistensi tangan/karakter, pencahayaan, lingkungan, komposisi 9:16, dan kelayakan pakai untuk generasi video. Beri vonis tegas: `Pakai` / `Perbaiki` / `Buang`. Jika `02-generated-assets/` kosong, beri peringatan dan catat strategi referensi alternatif.
- Muat paket copywriting HCE terbaru di `_collaboration/hce-package-v*.json` (atau jalankan `hce_bridge.py hce-analyze` bila belum tersedia) sebagai bahan dialog, hook, dan arah pesan per panel.

### B. Story Construction & Editing Rhythm
- Gunakan versi adaptif dari alur `HOOK → PROBLEM / DESIRE → PRODUCT REVEAL → PRODUCT VALIDATION → DEMONSTRATION → BENEFIT / RESULT → CTA` sesuai kategori, tingkat kesadaran pembeli, dan kompleksitas produk di `marketing-strategy.md` (tahap boleh digabung bila lebih tajam).
- Tentukan total durasi video final (**maksimal 40 detik**, target default **25–35 detik**; lebih singkat untuk produk sederhana, mendekati 40 detik hanya bila demo/perbandingan tambahan benar-benar diperlukan—tanpa adegan pengisi).
- Terapkan **variasi ritme editing** yang disengaja (kombinasikan hook cepat, reveal sedang, demonstrasi lebih panjang, *detail insert* singkat, dan CTA jelas). Setiap *cut* harus memiliki tujuan pemasaran/naratif yang nyata.

### C. Adaptive Scene Design & Variable Duration
- **Tanpa batasan tetap 4 panel atau 3–8 panel:** pilih jumlah panel yang diperlukan cerita (kisaran awal yang disarankan **6–14 panel**, bukan batas keras).
- **Durasi tiap panel variabel** mengikuti aksi (panduan awal fleksibel: Hook `1–3 dtk`, Detail `1–2 dtk`, Reveal `2–3 dtk`, Unboxing `2–4 dtk`, Demo `3–6 dtk`, Before/After `2–4 dtk`, Hasil/Reaksi `2–4 dtk`, CTA `2–3 dtk`). Penjumlahan seluruh durasi panel **wajib sama persis** dengan total durasi video final (`≤ 40 dtk`).
- Setiap panel wajib memuat: Nomor Panel, Timestamp Mulai–Selesai & Durasi Individu, Deskripsi Visual, Aksi Fisik Produk, Interaksi Produk, Sudut & Gerakan Kamera + Tujuan Naratif, Pencahayaan & Komposisi 9:16, Transisi, Dialog/VO (atau `[jeda]`), Teks Layar (*On-screen text* jika perlu), dan Tujuan Pemasaran (*Marketing purpose*).

### D. Adaptive Storyboard Image Output
- Sesuaikan layout dengan jumlah panel aktual (`4` panel untuk cerita sangat singkat, `6` untuk singkat-menengah, `8–12+` untuk kampanye lebih detail).
- Jika 1 gambar tidak bisa menjaga seluruh panel terbaca tajam, **pecah menjadi beberapa lembar berurutan** (`03-storyboard/storyboard-sheet-01.png`, `storyboard-sheet-02.png`, dst.) sambil menjaga penomoran panel dan kontinuitas berurutan; jangan pernah mengorbankan keterbacaan demi memaksa 1 gambar.
- Jika ImageGen tersedia, simpan gambar ke `03-storyboard/storyboard.png` (atau `storyboard-sheet-01.png`, ...). Jika tidak, sertakan prompt generasi lengkap siap-salin di `## Prompt Gambar Storyboard` dalam `storyboard.md` menggunakan [Template Prompt Gambar Storyboard](assets/templates/storyboard-image-prompt.md).

### E. Dialogue Design & Verifikasi Timing
- Gunakan dialog Bahasa Indonesia natural dan ekspresif hasil racikan HCE (`NaturalLanguageRefiner`) serta eja **semua angka dengan kata** (misal *"dua koma tiga meter"*, bukan *"2,3 m"*).
- Pastikan tiap kalimat mengisi **60%–105%** durasi panel pada laju standar **5,0 suku kata/detik** (gunakan `[jeda]` untuk *detail insert* cepat atau momen ASMR hening).
- Cantumkan `## Tabel Timing Dialog` dan jalankan validator (juga memeriksa urutan timestamp tanpa celah/tumpang-tindih & batas `≤ 40` detik):
  `python ../shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/03-storyboard/storyboard.md`

### F. Loop Review Dua Arah HCE ↔ AVD (Maksimal 3 Iterasi)
1. **AVD Review (`avd-review`):** Evaluasi keterlaksanaan visual, kontinuitas adegan, timing dialog, kualitas demo produk, ritme adegan, dan kelayakan video. Jika dialog terlalu panjang/terlalu singkat atau mengandung angka digit, kirim permintaan revisi terarah ke `hce`.
2. **HCE Review (`hce-review`):** Evaluasi konsistensi pemasaran, persuasi, efektivitas hook, kualitas naskah 7 dimensi + *Hard Integrity Gate*, relevansi CTA, dan keselarasan visual terhadap strategi. Jika visual kurang membuktikan klaim atau zona aman CTA terganggu, kirim permintaan revisi ke `affiliate-video-director`.
3. **Revisi Otomatis & Riwayat Versi:** Agen penanggung jawab memperbaiki temuan, menaikkan versi di `_collaboration/`, dan mengarsipkan `storyboard.md` lama ke `_archive/` sebelum menulis ulang. Putaran berhenti otomatis saat kedua skill menyetujui atau maksimal pada **iterasi ke-3**:
   `python ../shared/scripts/hce_bridge.py collaborate ./campaigns/<slug-produk> --from-campaign --max-iterations 3 --write-deliverables`

## File Output, Otoritas & Aturan Overwrite

1. Simpan `03-storyboard/storyboard.md` mengikuti [Template Storyboard](assets/templates/storyboard.md) serta `03-storyboard/storyboard.png` (atau `storyboard-sheet-01.png`, ...) bila ImageGen tersedia.
2. Perbarui `campaign.json` (`stages.storyboard.scenes`, `total_duration`, `image` / `images`, `files`, `collaboration`, dan `status`).
3. **Perlindungan Aset:** Jangan menimpa gambar storyboard lama atau foto asli; simpan revisi gambar dengan sufiks `-v2.png` dan arsipkan `storyboard.md` lama ke `_archive/`.
4. **Eksekusi Otonom & Otoritas:** Pada alur kampanye otonom, setelah review dua arah HCE ↔ AVD konvergen, catat `status = "approved"` (`approved_by: "hce+avd-autonomous"`) di `campaign.json` dan lanjutkan otomatis ke `/video <slug-produk>`. *(Jika pengguna secara eksplisit meminta review manual per tahap, tahan status di `"draft"` dan minta konfirmasi pengguna terlebih dahulu.)*
