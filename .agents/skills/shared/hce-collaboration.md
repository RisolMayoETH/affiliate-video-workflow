# Protokol Kolaborasi Otonom: Affiliate Video Director ↔ Human Copywriting Engine (HCE)

Dokumen ini menetapkan kontrak kerja resmi antara **Affiliate Video Director (AVD)** sebagai **pengendali alur kerja utama (*primary workflow controller*)** dan **Human Copywriting Engine (HCE)** sebagai **spesialis intelijen pemasaran & copywriting (*dedicated marketing intelligence and copywriting specialist*)**.

Kedua skill tetap mempertahankan identitas, pengetahuan, perintah, dan kemampuan mandirinya, namun berkolaborasi secara otonom ketika pengguna menyerahkan produk baru ke Affiliate Video Director.

---

## 1. Pembagian Tanggung Jawab

| Domain | Pemilik Utama | Ruang Lingkup Spesifik |
|---|---|---|
| **Marketing & Copy Intelligence** | **HCE** (`human-copywriting-engine`) | Analisis pasar & posisi produk, identifikasi target audiens, analisis *pain points*, psikologi pembeli, strategi affiliate, USP, generasi hook, copywriting, konsep storytelling, dialog Bahasa Indonesia natural, CTA lintas platform, evaluasi & penyempurnaan naskah |
| **Creative Direction & Video Production** | **AVD** (`/review`, `/storyboard`, `/video`) | Audit fakta & visual referensi asli (`references/`), arahan kreatif visual, perencanaan adegan, durasi variabel adaptif (`≤ 40` dtk), storyboard adaptif `9:16`, deskripsi visual, arah kamera, demonstrasi fisik produk, prompt gambar, prompt video AI (`≤ 10` dtk/klip), instruksi editing, paket publikasi final |

---

## 2. Alur Kerja Kolaborasi 11 Langkah (Eksekusi Otonom)

Saat pengguna menyerahkan produk baru (foto, screenshot listing, deskripsi, tautan, atau harga) ke Affiliate Video Director:

1. **AVD Menerima Produk:** AVD mengumpulkan materi asli pengguna (tanpa mengarang spesifikasi).
2. **AVD Menginisialisasi Kampanye:** Struktur baku dibuat di `./campaigns/<slug-produk>/` beserta folder `_collaboration/`.
3. **AVD Memanggil HCE untuk Intelijen & Strategi:** HCE menerima paket terstruktur `hce-product-input.json`, memanggil basis pengetahuan HCE secara selektif, serta memetakan analisis produk, audiens, psikologi pembeli, USP, dan strategi pemasaran.
4. **HCE Menghasilkan Aset Copywriting Awal (`v1`):** HCE menyusun hook pembuka, sudut storytelling/demonstrasi, dialog VO natural, naskah adegan, CTA per platform, dan caption SEO, lalu menyimpannya ke `_collaboration/hce-package-v1.json`.
5. **AVD Menerima Output HCE:** AVD menyerap strategi, USP, hook, dan narasi HCE sambil tetap mengikatkan seluruh detail fisik pada Otoritas #1 (`01-product-review/references/`).
6. **AVD Menyusun Rencana Produksi (`v1`):** AVD membangun storyboard adaptif `9:16` (jumlah panel & durasi variabel `≤ 40` dtk), rencana klip (`≤ 10` dtk/klip), arahan visual/kamera/demo, serta menyimpannya ke `_collaboration/avd-plan-v1.json` dan draf dokumen kampanye.
7. **Review Dua Arah (*Bidirectional Review*):** Kedua skill mengevaluasi artefak masing-masing pada putaran yang sama (`review-round-K.json`).
8. **Permintaan Revisi dari HCE:** Jika HCE menemukan kelemahan pemasaran, hook, CTA, kealamian bahasa, pelanggaran integritas, atau ketidakcocokan visual terhadap strategi, HCE mengirim permintaan revisi terstruktur (`HCE-REQ-*`).
9. **Permintaan Revisi dari AVD:** Jika AVD menemukan masalah keterlaksanaan visual, kontinuitas, timing/suku kata dialog, angka digit di VO, kualitas demo fisik, atau ritme adegan, AVD mengirim permintaan revisi terstruktur (`AVD-REQ-*`).
10. **Kolaborasi Iteratif Terbatas (Maksimal 3 Iterasi):** Agen penanggung jawab menerapkan revisi bertarget, menaikkan nomor versi (`v2`, `v3`), mengarsipkan dokumen Markdown lama ke `_archive/`, dan menguji ulang hingga konvergen atau mencapai batas **3 iterasi**.
11. **Paket Kampanye Final:** Setelah lolos review dua arah (atau mencapai kondisi terbaik pada batas iterasi 3), AVD menulis dan memvalidasi paket kampanye final menggunakan konvensi output baku AVD (`01-product-review/`, `03-storyboard/`, `04-video/`, `05-publishing/`, `campaign.json`).

---

## 3. Antarmuka Pertukaran Data Terstruktur (`_collaboration/`)

Seluruh komunikasi HCE ↔ AVD diisolasi di `./campaigns/<slug-produk>/_collaboration/`:

```text
campaigns/<slug-produk>/_collaboration/
├── hce-product-input.json      # Input produk faktual + konteks visual AVD
├── hce-package-v1.json         # Output intelijen & copywriting HCE versi 1
├── hce-package-vN.json         # Revisi HCE versi N (v2, v3 jika ada revisi)
├── avd-plan-v1.json            # Rencana storyboard, klip & visual AVD versi 1
├── avd-plan-vN.json            # Revisi AVD versi N (v2, v3 jika ada revisi)
├── review-round-1.json         # Evaluasi dua arah putaran 1 (HCE + AVD + requests)
├── review-round-K.json         # Evaluasi dua arah putaran K (maks. K = 3)
└── collaboration-summary.json  # Ringkasan akhir, status konvergensi, skor & riwayat versi
```

### Struktur Permintaan Revisi (`revision_requests`)

Setiap temuan review memakai skema seragam agar dapat diproses otomatis:

```json
{
  "request_id": "AVD-REQ-01",
  "reviewer": "affiliate-video-director",
  "target_agent": "hce",
  "scene_number": 2,
  "category": "dialogue_timing",
  "severity": "blocker",
  "issue": "Dialog adegan 2 terlalu cepat (29 suku kata dalam 4.0 dtk = 7.25 sk/dtk).",
  "constraint": "Rentang aman 12-20 suku kata, tanpa angka digit.",
  "action_required": "Padatkan dialog tanpa menghilangkan fitur terverifikasi."
}
```

Aturan perutean `target_agent`:
- `target_agent = "hce"` untuk: dialog terlalu cepat/singkat, angka digit di VO, klise AI/bahasa buku, klaim tanpa bukti, CTA tidak sesuai platform, hook lemah, atau kurangnya cakupan fitur terverifikasi.
- `target_agent = "affiliate-video-director"` untuk: keterlaksanaan visual, demo produk kurang membuktikan klaim HCE, kontinuitas tangan/produk/latar, ritme/durasi panel monoton atau terlalu lama (`> 6.5` dtk per panel), klip melebihi `10.0` dtk, atau zona aman CTA terganggu.

---

## 4. Rubrik Review Dua Arah (Bidirectional Review)

### A. Enam Kriteria Evaluasi oleh HCE (`hce_review`)
1. `marketing_consistency`: Apakah sudut jualan, pesan inti, fitur terverifikasi, dan larangan klaim terjaga konsisten dari strategi hingga publikasi?
2. `persuasiveness`: Apakah fitur diterjemahkan ke manfaat nyata dan menjawab keraguan pembeli secara jujur?
3. `hook_effectiveness`: Apakah hook 2 detik pertama spesifik ke produk/masalah dan langsung memicu perhatian?
4. `script_quality`: Apakah lolos **7 dimensi + Hard Integrity Gate HCE** (`naturalness`, `buyer_psychology`, `persuasiveness`, `storytelling`, `audience_adaptation`, `product_accuracy`, `authenticity`) serta bersih dari klise AI dan bahasa kaku?
5. `cta_relevance`: Apakah CTA natural, berorientasi tindakan, dan persis sesuai platform (`keranjang kuning` untuk TikTok, `link bio/komentar` untuk IG/FB Reels, `keranjang/tautan` untuk Shopee Video)?
6. `visual_strategy_alignment`: Apakah deskripsi visual dan demonstrasi di storyboard AVD benar-benar mendukung dan membuktikan strategi pemasaran HCE?

### B. Enam Kriteria Evaluasi oleh AVD (`avd_review`)
1. `visual_executability`: Apakah setiap adegan dapat dieksekusi oleh generator gambar/video AI dengan instruksi visual, sudut kamera, dan pencahayaan yang konkret?
2. `scene_continuity`: Apakah *Product Lock*, *Hand/Wardrobe Lock*, *Environment/Lighting Lock*, dan transisi antar adegan/klip terjaga konsisten?
3. `dialogue_timing`: Apakah seluruh dialog VO lolos aturan `dialogue_timing.py` (60%–105% dari durasi panel pada `5,0` sk/dtk, `≤ 6,0` sk/dtk, nol angka digit, timestamp berurutan mulai `00:00`, total `≤ 40,0` dtk)?
4. `product_demonstration_quality`: Apakah demonstrasi fisik dan interaksi tangan menampilkan mekanisme/bukti nyata produk, bukan sekadar memegang produk diam?
5. `scene_pacing`: Apakah durasi panel bervariasi sesuai fungsi adegan (hook cepat, demo lebih panjang, tanpa panel monoton atau melebihi batas klip)?
6. `video_workability`: Apakah segmentasi klip (`≤ 10,0` dtk per klip), total durasi (`= storyboard`), serta alur audio-visual benar-benar bekerja sebagai iklan video nyata?

---

## 5. Aturan Pengendalian Loop, Otonomi & Pelestarian Data

- **Batas Maksimal 3 Iterasi:** `max_iterations` dikunci paling tinggi `3`. Tidak boleh ada loop tanpa batas. Jika setelah 3 putaran belum 100% konvergen, sistem berhenti bersih pada iterasi ke-3, mencatat sisa catatan secara jujur di `collaboration-summary.json`, dan tidak menimpa data asli.
- **Eksekusi Otonom Penuh:** Selama alur kampanye normal, kolaborasi HCE ↔ AVD berjalan otomatis tanpa meminta persetujuan manual di tengah jalan—kecuali pengguna secara eksplisit meminta jeda per tahap atau saat referensi produk benar-benar kosong.
- **Riwayat Versi & Anti-Timpa:** Setiap revisi file teks mengarsipkan versi sebelumnya ke `_archive/<nama-file>.vN.md`. Foto asli di `01-product-review/references/` dan aset gambar di `02-generated-assets/` atau `03-storyboard/*.png` **tidak pernah ditimpa**.
- **Anti-Halusinasi Klaim:** Baik HCE maupun AVD dilarang keras menambahkan spesifikasi angka, harga promo, testimoni, atau pengalaman pemakaian pribadi yang tidak berasal dari bukti produk terverifikasi.
- **Keamanan Kegagalan:** Jika terjadi kesalahan pada salah satu tahap, laporkan akar masalah secara akurat dan pertahankan seluruh berkas kampanye serta `_collaboration/` yang sudah ada.
