# Video Engineering — Rekayasa Prompt Video AI, Segmentasi Klip & Kontinuitas

`/video` menerjemahkan storyboard yang sudah disetujui (`total_duration <= 40` detik) menjadi rangkaian segmen generasi video AI yang logis, konsisten, sinematis, dan sinkron dialog untuk platform seperti Google Flow / Veo, Kling, Sora, Runway, atau Seedance.

## 1. Aturan Segmentasi Klip & Durasi Generasi

- **Batas Maksimal Durasi Video Final:** **40 detik** (`total_duration <= 40.0` s).
- **Batas Maksimal Per Generasi Klip:** **10 detik** (`max_clip_duration = 10.0` s), **kecuali** generator video yang dipilih user secara eksplisit mendukung durasi lebih panjang dan dicatat di `campaign.json` (`stages.video.generator_supports_extended_clip: true`).
- **Jumlah Generasi Bersifat Dinamis:** **Dilarang keras memaksa setiap kampanye menjadi tepat 2 klip video.** Pecah storyboard yang disetujui menjadi segmen generasi logis mengikuti batas generator dan titik potong cerita:
  - Kampanye `10 dtk` → bisa `1` klip (`10` dtk)
  - Kampanye `18–20 dtk` → bisa `2` klip (`9+9` atau `10+10` dtk) atau `3` klip (`6+7+7` dtk) sesuai titik transisi
  - Kampanye `28–35 dtk` (target default) → bisa `3–4` klip (misal `8+9+8+7 = 32` dtk atau `9+10+9 = 28` dtk)
  - Kampanye `36–40 dtk` → bisa `4–5` klip (misal `9+10+10+9 = 38` dtk atau `8+8+8+8+8 = 40` dtk)
- **Penggabungan Multi-Panel dalam Satu Klip:** Satu klip generasi boleh memuat **beberapa panel storyboard berdurasi variabel** sekaligus selama masih dalam batas maksimal klip (misal Panel 1 `2.0s` + Panel 2 `1.5s` + Panel 3 `3.5s` + Panel 4 `2.5s` = klip `9.5` detik) dan aksi fisiknya dapat dieksekusi mulus dalam satu rangkaian gerak.
- **Total Durasi Klip = Durasi Video Final:** Penjumlahan durasi seluruh `video-NN.md` **wajib sama persis** dengan `total_duration` storyboard yang disetujui, tanpa panel terlewat atau terduplikasi.
- **Rasio Default:** Vertikal **9:16** (adaptasi hanya jika user meminta eksplisit).

## 2. Bahasa Prompt Video

- **Semua instruksi visual, fisika, pencahayaan, kamera, dan negative prompt** wajib ditulis dalam **Bahasa Inggris** agar generator video memahami detail sinematografi dengan akurat.
- **Semua ucapan VO / narasi lisan** wajib dikutip dalam **Bahasa Indonesia natural verbatim** sesuai `## Tabel Timing Dialog`, disertai arahan nada suara (*voice tone & pacing*).

## 3. Urutan Blok Wajib di Setiap `video-NN.md`

Setiap file prompt generasi video wajib memuat bagian terstruktur berikut:

1. **Metadata Generasi:** Nomor file, durasi klip (≤ 10 dtk atau sesuai batas generator terpilih), rasio aspek (`9:16`), panel/adegan storyboard yang dicakup (`Adegan X–Y`), dan rentang timestamp storyboard.
2. **Gambar Referensi Wajib Dilampirkan:** Daftar file dari folder upload terpadu `04-video/upload-assets/` (`1..<ext>`, `2..<ext>`, ..., `storyboard.png` atau `storyboard-sheet-NN.png`) beserta rujukan ke `01-product-review/references/` (**Otoritas #1 `product-reference`**).
3. **Instruksi Kepatuhan Storyboard:** Penegasan mengikuti urutan panel, durasi variabel, teks layar, dan tujuan pemasaran di storyboard tanpa improvisasi visual yang bertentangan.
4. **Kunci Konsistensi (`Consistency Locks`):**
   - `Product Identity Sheet + PCS Locks`: Merujuk langsung pada `01-product-review/product-identity-lock.md` serta menerapkan *Product Identity Lock*, *Object Permanence Lock*, dan *Anti-Morphing Lock* sesuai [Product Consistency System (PCS v2.0)](product-consistency-system.md) §1–3.
   - `Hand / Character Lock` *(atau `Product-Only Mode`)*: Kulit, jari, baju lengan yang konsisten (default *hands-only* tanpa wajah), atau tanpa manusia sama sekali bila `Product-Only Mode` diaktifkan pengguna/storyboard (PCS §6).
   - `Environment & Lighting Lock`: Ruangan, properti latar, arah & suhu cahaya.
5. **Master Video Prompt (Copy-Ready English):** Wajib mengikuti **Arsitektur Master Prompt 11 Blok** (`[1. VIDEO SPECIFICATION]` s.d. `[11. FINAL PRODUCT IDENTITY VERIFICATION]`) di `../shared/product-consistency-system.md` §7:
   - **Kalimat Pembuka Klip Lanjutan (Klip 2+):** Untuk `video-02.md`, `video-03.md`, `video-04.md`, dan seterusnya, wajib diawali baris pertama `"Continue the video."` di dalam blok prompt tepat sebelum `[1. VIDEO SPECIFICATION]` (tidak untuk `video-01.md`).
   - **Kondisi Frame Awal (`First-Frame Anchor`):** Ditempatkan pada `[6. ENVIRONMENT & CONTINUITY LOCK]` (posisi produk, tangan/tanpa tangan, sudut kamera, dan kondisi latar di detik `0.0s`).
   - **Timeline Shot-by-Shot & Kontinuitas Identitas:** Ditempatkan pada `[7. SHOT-BY-SHOT TIMELINE]` memakai format baris shot PCS §5 untuk `0.0s–X.Xs`, dan ditutup dengan `Last-Frame Anchor` di akhir blok 7.
   - **Koreografi Kamera & Kontrol Risiko:** Ditempatkan pada `[8. CAMERA MOVEMENT CONTROL]` sesuai profil risiko kamera produk (PCS §4).
   - **Negative Instructions:** Ditempatkan pada `[10. NEGATIVE PROMPT]` dengan larangan anti-morphing spesifik produk sesuai PCS §3 (ditambah larangan wajah atau larangan manusia penuh bila `Product-Only Mode`).
6. **Arahan Audio & Dialog VO Bahasa Indonesia:** Off-camera Indonesian reviewer, intonasi per segmen timestamp, kutipan verbatim, dan SFX alami.
7. **Kondisi Frame Akhir & Hand-Off Kontinuitas:** Deskripsi eksplisit frame penutup (`Last-Frame Anchor`: posisi produk, tangan, arah gerak, cahaya) dan instruksi penyambungan ke `video-(NN+1).md` (atau catatan penutup video).
8. **`## Tabel Timing Dialog`:** Untuk verifikasi otomatis suku kata, rentang timestamp berkesinambungan, dan kesesuaian durasi.

## 4. Catatan Model-Agnostik (Veo / Kling / Sora / Flow)

- Gunakan **Image-to-Video / Reference-to-Video** alih-alih *Text-to-Video* polos kapan pun referensi asli dan aset gambar tersedia.
- Jangan menaruh instruksi teks grafis promo ("DISKON 50%") ke dalam prompt video generator karena sering merusak ejaan; tambahkan teks layar (*on-screen text*) dari storyboard saat *finishing* di CapCut/editor sesuai zona aman platform.
- Jika model tujuan memiliki batas 5 detik atau 8 detik, pecah panel storyboard ke segmen ≤ 5 atau ≤ 8 detik tanpa memotong tengah suku kata dialog atau mengubah total durasi final.
