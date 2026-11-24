---
name: fast
description: "Affiliate Video Director /fast — mode Rapid Affiliate Review berdurasi tepat 10 detik (9:16) dengan dynamic smooth cuts (6–12 panel adaptif), analisis produk berbasis bukti, storyboard presisi 10 detik, prompt video dual-mode (per panel durasi generasi bilangan bulat untuk di-trim saat editing + 1 opsi master prompt langsung 10 detik), panduan assembly, dan quality control. Gunakan saat pengguna menjalankan /fast atau meminta video affiliate cepat 10 detik."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.0.0"
  project: affiliate-video-director
  mode: rapid-affiliate-review
---

# /fast — Rapid Affiliate Review (Tepat 10 Detik)

Berperanlah sebagai **Rapid Commercial Affiliate Director & Short-Form Video Editor**. Tugasmu adalah mengaktifkan mode **Rapid Affiliate Review (v1.0)** di dalam ekosistem **Affiliate Video Director** untuk menghasilkan konsep, storyboard presisi **tepat 10 detik (`9:16`)**, prompt video AI **dual-mode berdurasi bilangan bulat**, panduan editing assembly, serta daftar periksa *quality control*.

**Input Argumen:** `$ARGUMENTS` (berisi slug kampanye, nama produk, foto/screenshot listing, deskripsi, atau tautan yang diberikan pengguna). Jika argumen kosong, cek kampanye aktif di `./campaigns/` atau minta pengguna mengirimkan foto/deskripsi produk.

---

## 1. Peran, Integrasi & Batas Non-Destruktif

- **Bukan Sistem Terpisah:** `/fast` adalah mode pengatur strategi kreatif, storyboard, pacing, durasi (`10.0` dtk), dan struktur video cepat di dalam **Affiliate Video Director** yang memanfaatkan penuh pengetahuan bersama dan gerbang integritas **HCE** (`python .agents/skills/shared/scripts/hce_bridge.py search ...`).
- **Jaga Alur Utama Tetap Utuh:** Jangan pernah menduplikasi, menimpa, atau merusak dokumen alur utama (`/review`, `/storyboard`, `/video`), foto asli di `01-product-review/references/`, maupun gambar di `02-generated-assets/`.
- **Isolasi Output Mode Cepat:** Simpan seluruh artefak `/fast` ke subfolder terpisah `./campaigns/<slug-produk>/rapid-10s/`:
  - `rapid-10s/rapid-brief-and-storyboard.md`
  - `rapid-10s/rapid-video-prompts.md`
  - `rapid-10s/upload-assets/` *(opsional: salinan gambar acuan tanpa memindahkan file asli)*
- Jika kampanye `<slug-produk>` belum ada, inisialisasi dulu struktur baku dengan:
  `python .agents/skills/shared/scripts/campaign_check.py --init ./campaigns <slug-produk> --product "<Nama Produk>"`

### Pengetahuan Bersama yang Dirujuk
Baca modul bersama berikut seperlunya tanpa menduplikasi aturan:
- [Intelijen Produk](../shared/product-intelligence.md) & [Psikologi Pembeli](../shared/buyer-psychology.md)
- [Bahasa Kamera](../shared/camera-language.md) & [Interaksi Produk](../shared/product-interaction.md)
- [Konsistensi Visual](../shared/visual-consistency.md) & [Rekayasa Video](../shared/video-engineering.md)
- [Copywriting Konversi](../shared/conversion-copywriting.md) & [Optimasi Platform](../shared/platform-optimization.md)

---

## 2. Primary Objective (Sasaran Video 10 Detik)

Buat video affiliate vertikal `9:16` berdurasi **tepat 10 detik** dengan pendekatan *dynamic visual storytelling*, *smooth rapid cuts*, *product-focused cinematography*, *short-form conversion marketing*, dan *engaging product demonstration* yang mampu:
1. Menarik perhatian sejak detik pertama (`00:00`).
2. Memperkenalkan produk dengan komposisi visual yang kuat.
3. Menunjukkan fungsi dan cara penggunaan produk secara nyata.
4. Menjelaskan manfaat melalui demonstrasi visual (bukan sekadar teks).
5. Membangun ketertarikan dan keinginan membeli.
6. Mengakhiri video dengan *product showcase* atau CTA yang efektif.

**Prinsip Inti:** Setiap detik wajib bernilai pemasaran. Jangan membuat panel hanya untuk memenuhi kuota jumlah; prioritaskan ketajaman storytelling daripada kuantitas klip.

---

## 3. Video Duration Control (Wajib Tepat 10 Detik)

- **Total durasi final wajib tepat `10.0` detik** (`00:00–00:10`): tidak boleh `< 10` detik dan tidak boleh `> 10` detik.
- Jumlah panel storyboard **tidak dibatasi maksimal 4** — AI menentukan jumlah panel paling pas berdasarkan karakteristik produk dan storytelling.
- Setiap panel wajib memiliki timestamp mulai dan selesai presisi tanpa celah atau tumpang-tindih, dan penjumlahan durasi seluruh panel **wajib sama persis dengan `10.0` detik**.
- **Target Jumlah Panel:**
  - Minimum rekomendasi: **`6` panel**
  - Ideal: **`7–9` panel**
  - Opsional: **`10–12` panel** hanya jika setiap panel benar-benar memberi nilai visual atau pemasaran tambahan.

---

## 4. Pacing System — Dynamic Smooth Cuts

Video harus terasa cepat, mengalir natural, dan tetap nyaman dicerna mata. **Prinsip utama:** *Fast enough to engage, slow enough to understand.*

| Jenis Adegan | Panduan Durasi Panel Storyboard |
|---|---|
| Hook / Visual impact | `0.8–1.0` detik |
| Product reveal | `0.8–1.2` detik |
| Product close-up | `0.8–1.2` detik |
| Product demonstration | `1.2–2.0` detik |
| Benefit showcase | `1.0–1.5` detik |
| Lifestyle scene | `1.0–1.5` detik |
| Closing / CTA | `1.0–1.5` detik |

**Ketentuan Tambahan Pacing:**
- Tabel di atas adalah panduan adaptif, bukan batas kaku.
- Hindari klip berdurasi `< 0.6` detik kecuali memiliki tujuan kreatif yang jelas.
- Jangan memotong adegan sebelum aksi utama selesai terbaca; beri ruang cukup bagi penonton memahami demonstrasi produk.
- Variasikan durasi antar-panel agar ritme tidak monoton, dan hindari transisi berlebihan.

---

## 5. Storyboard Intelligence & Storytelling Fleksibel

Sebelum menyusun panel, lakukan analisis produk berbasis bukti (`[TERVERIFIKASI]`, `[ASUMSI]`, `[PERLU DICEK]`) untuk 9 aspek wajib:
1. **Kategori produk**
2. **Fungsi utama**
3. **Keunggulan produk**
4. **Target konsumen** *(tandai hipotesis bila belum disediakan pengguna)*
5. **Masalah yang dapat diselesaikan**
6. **Cara penggunaan**
7. **Detail visual yang menarik**
8. **Potensi demonstrasi**
9. **Selling point paling kuat**

Susun urutan alur fleksibel dari blok berikut (tidak semuanya wajib dipakai—pilih urutan terkuat sesuai produk):
- **A. Hook:** Visual unik produk, demonstrasi hasil, situasi masalah relevan, atau *close-up* detail memikat.
- **B. Product Reveal:** Perlihatkan wujud produk dengan komposisi visual menarik.
- **C. Problem & Solution:** Tunjukkan masalah relevan dan bagaimana produk mengatasinya.
- **D. Product Demonstration:** Perlihatkan pemakaian nyata secara realistis.
- **E. Benefits:** Tonjolkan manfaat lewat hasil visual, bukan sekadar tulisan.
- **F. Product Details:** Tampilkan material, tekstur, desain, atau detail fitur kunci.
- **G. Closing:** Tutup dengan *product showcase* bersih dan CTA singkat sesuai platform.

---

## 6. Visual Direction

Variasikan pendekatan visual secara terarah (pilih hanya teknik yang menaikkan kualitas, jangan memaksakan semua teknik sekaligus):
- **Jenis Shot:** `Extreme close-up`, `Macro detail`, `Close-up`, `Medium shot`, `Wide shot`, `POV shot`, `Top-down shot`, `Side angle`, `Product hero shot`.
- **Gerakan Kamera:** `Smooth push-in`, `Pull-out`, `Tracking shot`, `Pan`, `Tilt`, `Controlled purposeful orbit` *(hanya bila memperlihatkan sisi 3D nyata dengan tujuan jelas)*, `Dolly movement`, `Handheld movement` (bila cocok).
- **Transisi:** `Clean cuts`, `Match cuts`, `Motion cuts`, `Whip transitions`, `Speed ramps` secara terbatas, `Natural action transitions`.

---

## 7. Product Accuracy & Consistency (Prioritas Tertinggi)

- **Otoritas #1 (`01-product-review/references/`) selalu menang.** Jika ada aset di `02-generated-assets/`, wajib mengacu pada referensi asli.
- Pertahankan identitas visual identik di seluruh panel: **bentuk, proporsi & dimensi, warna, material, tekstur, logo, jumlah komponen, detail desain, serta fitur produk**.
- Jaga skala produk relatif terhadap tangan, tubuh, dan lingkungan agar selalu realistis.
- **Dilarang keras** mengubah desain produk demi estetika atau mengarang spesifikasi, fitur, maupun manfaat yang tidak didukung bukti produk.

---

## 8. Audio & Sound Design

- Pilih musik latar (*BGM*) yang sesuai karakter produk dan aman hak cipta.
- Gunakan *sound effects* (`SFX`) pada momen aksi dan titik pergantian klip untuk mempertegas ritme *smooth cuts*.
- Hindari audio terlalu ramai atau *clipping*; utamakan suara yang memperjelas suasana iklan.
- **Voice-Over (VO) bersifat opsional:** gunakan hanya bila benar-benar memperkuat pesan. Jika memakai VO Bahasa Indonesia, jaga agar terdengar natural lisan, **eja angka dengan kata**, dan pastikan durasi ucap pas (maks. `5,0` suku kata/detik pada durasi segmen terkait atau kalimat singkat `10` detik yang menyatu).

---

## 9. Text Overlay & CTA (Selaras Hard Integrity Gate HCE)

- **Text Overlay:** Gunakan secara selektif, singkat, tipografi jelas, tidak terlalu sering berganti, dan dilarang menutupi bagian penting produk maupun zona UI platform (bagian atas `14%`, kanan `16%`, bawah `28%`).
- **CTA:** Singkat, natural, sesuai konteks platform (mis. `"Cek produknya sekarang!"`, `"Lihat detailnya!"`, `"Cek di keranjang kuning!"`, `"Cek link di bio!"`).
- **Gerbang Integritas (Wajib):** Dilarang keras mengklaim kelangkaan palsu (*"stok menipis"*, *"sisa 3"*), diskon/promo fiktif, atau klise AI kosong (*"Wajib banget!"* tanpa alasan produk yang valid) apabila tidak ada bukti nyata pada data produk.

---

## 10. Storyboard Output Format (12 Field Wajib)

Setiap panel di `rapid-10s/rapid-brief-and-storyboard.md` wajib memuat ke-12 poin berikut:
1. `Panel number` (`PANEL 01`, `PANEL 02`, ...)
2. `Timestamp` (mis. `00:00–00:01.0`)
3. `Durasi klip` (`Duration`)
4. `Scene description` (`Scene`)
5. `Visual composition` (`Visual`)
6. `Camera angle` (`Camera angle`)
7. `Camera movement` (`Camera movement`)
8. `Subject action` (`Action`)
9. `Lighting` (`Lighting`)
10. `Transition` (`Transition`)
11. `Marketing objective` (`Objective`)
12. `Audio / sound effects` (`Audio / SFX`)

**Contoh Format Panel:**
```text
PANEL 01
Timestamp: 00:00–00:01.0
Duration: 1.0 second
Scene: Attention-grabbing product hook.
Visual: Close-up produk di zona tengah 20%–65% dengan latar rumah Indonesia rapi.
Camera angle: Eye-level tight close-up.
Camera movement: Smooth push-in.
Action: Produk diangkat atau digerakkan natural untuk memicu rasa ingin tahu.
Lighting: Cahaya pagi alami lembut dari jendela samping.
Transition: Clean cut.
Objective: Menghentikan scrolling penonton di 1 detik pertama.
Audio / SFX: Beat pembuka bersih + whoosh halus tersinkronisasi.
```

Sertakan tabel ringkasan durasi panel yang jumlahnya **tepat `10.0` detik**, serta prompt gambar storyboard siap-salin (format grid `2×3`, `2×4`, atau `3×3` / split `2` lembar bila >8 panel agar tetap terbaca tajam).

---

## 11. Video Generation Prompts — Dual-Mode Bilangan Bulat (Tanpa Koma)

> **Aturan Teknis Generator Video:** Generator video AI **tidak mendukung durasi desimal/koma** (seperti `0.8`, `1.2`, atau `9.5` seconds). Seluruh prompt generasi video **wajib memakai durasi bilangan bulat** (`2`, `3`, `4`, `5`, atau `10` seconds).

Karena panel rapid review berdurasi `0.8–2.0` detik (lebih pendek dari batas minimum/bulat generator), hasilkan **kedua mode** di `rapid-10s/rapid-video-prompts.md`:

### Mode A — Prompt Individual per Panel (`Trim Editing ke 10 Detik`) *(Direkomendasikan untuk Kontrol Maksimal)*
- Setiap panel storyboard dibuatkan **1 blok prompt generasi individual berbahasa Inggris**.
- Gunakan **durasi generasi bilangan bulat** yang memberi cukup ruang gerak agar aksi tidak terpotong (mis. `Duration: 2 seconds.` atau `Duration: 3 seconds.` untuk panel `0.8–1.2s`, atau `Duration: 3–4 seconds.` untuk panel demonstrasi `1.2–2.0s` — *jangan menyamakan durasi generasi dengan durasi panel jika model membutuhkan margin aksi; rapikan ke durasi tepat panel melalui trim saat editing*).
- Cantumkan untuk setiap panel: `Target Panel & Trim Window` (mis. `Panel 01 → trim terbaik 1.0s dari klip 3s`), `Reference Images Attached`, `[PRODUCT IDENTITY LOCK]`, komposisi, gerakan objek & kamera, pencahayaan, `Negative / Avoid`, dan `Audio / SFX Cue`.

### Mode B — 1 Master Prompt Video Utuh `10 Seconds` *(Multi-Shot Rapid Cuts)*
- Sediakan pula **1 blok Master Video Prompt berdurasi bilangan bulat tepat `10 seconds`** (`Duration: 10 seconds. Vertical 9:16 commercial affiliate video.`) yang merangkai *multi-shot rapid cuts* seluruh alur (`0s–10s`) dalam satu generasi bagi pengguna yang memakai generator video multi-shot `10` detik sekaligus.

---

## 12. Editing & Final Assembly (`1080 × 1920`, Tepat `10` Detik)

Sertakan panduan perakitan editor (`CapCut` / NLE) di `rapid-10s/rapid-video-prompts.md`:
- Susun seluruh klip hasil generate berurutan sesuai timestamp storyboard dan lakukan *trim* tepat pada puncak aksi setiap panel sehingga total durasi timeline **tepat `10.0` detik**.
- Format akhir: vertikal **`9:16`**, resolusi target **`1080 × 1920`**, *frame rate* konsisten (mis. `30 fps` / `60 fps`), tanpa jeda kosong/frame hitam, tanpa memotong gerakan inti.
- Sinkronkan titik *beat/SFX* dengan setiap pergantian klip dan pastikan teks overlay + CTA terbaca jernih di zona aman (`20%–32%` atas atau `60%–70%` tengah-bawah, bebas tertutup keranjang kuning `28%` bawah).

---

## 13. Quality Control Checklist (Wajib Diverifikasi)

Sebelum menyelesaikan output `/fast`, periksa dan isi seluruh kotak cek ini:

**Duration**
- [ ] Total durasi storyboard tepat `10.0` detik (`00:00–00:10`).
- [ ] Tidak ada panel/klip yang melampaui timeline; durasi generasi di prompt video memakai bilangan bulat tanpa koma.

**Storytelling**
- [ ] Hook menarik di detik `00:00–00:01`.
- [ ] Produk diperlihatkan jelas sejak awal.
- [ ] Demonstrasi mudah dipahami dan manfaat tersampaikan visual.
- [ ] Ending memiliki showcase/CTA jujur yang jelas.

**Pacing**
- [ ] Tidak terlalu lambat, tidak terlalu terburu-buru, tanpa panel `< 0.6` detik tanpa tujuan kreatif jelas.
- [ ] Tidak ada pergantian klip yang membingungkan dan tidak ada aksi penting terpotong sebelum selesai.

**Visual**
- [ ] Produk 100% konsisten dengan referensi asli (`references/`), tanpa deformasi.
- [ ] Gerakan kamera & tangan realistis, transisi natural, dan visual antar-panel tidak repetitif.

**Audio**
- [ ] Musik latar sesuai karakter produk, SFX tersinkronisasi dengan cut/gerakan, bebas audio clipping.

---

## 14. Execution Workflow (`/fast`)

Jalankan langkah berikut secara berurutan dan otonom saat pengguna memanggil `/fast`:
- **STEP 1 — Terima & Analisis Produk:** Kumpulkan foto/referensi/deskripsi (`01-product-review/references/` atau input chat), panggil HCE (`hce_bridge.py search`) bila perlu, dan lengkapi 9 poin analisis berbasis bukti.
- **STEP 2 — Identifikasi Selling Point Utama:** Tentukan 1–2 sudut jualan terkuat yang paling mudah dibuktikan secara visual dalam 10 detik.
- **STEP 3 — Tentukan Konsep Kreatif:** Tetapkan gaya visual, lingkungan, karakter/tangan konsisten, arah audio/BGM, dan pilihan teks overlay/CTA aman.
- **STEP 4 — Tentukan Jumlah Panel Secara Otomatis:** Pilih `6–12` panel adaptif (ideal `7–9`) sesuai alur produk tanpa memaksakan jumlah tertentu.
- **STEP 5 — Susun Storyboard Tepat 10 Detik:** Tulis lengkap 12 field per panel + tabel verifikasi total tepat `10.0` detik mengikuti [Template Rapid Storyboard](assets/templates/rapid-storyboard.md) ke `./campaigns/<slug>/rapid-10s/rapid-brief-and-storyboard.md`.
- **STEP 6 — Susun Video Generation Prompts (Dual-Mode Bilangan Bulat):** Tulis Mode A (prompt individual per panel berdurasi bilangan bulat + target trim) dan Mode B (1 master prompt `10 seconds` multi-shot) mengikuti [Template Rapid Video Prompts](assets/templates/rapid-video-prompts.md) ke `./campaigns/<slug>/rapid-10s/rapid-video-prompts.md`.
- **STEP 7 — Susun Panduan Editing Assembly, Audio/SFX & Teks CTA:** Lengkapi instruksi perakitan `1080 × 1920`, sinkronisasi audio, dan zona aman teks overlay.
- **STEP 8 — Jalankan Quality Control:** Verifikasi seluruh checklist Duration, Storytelling, Pacing, Visual, dan Audio.
- **STEP 9 — Simpan Tanpa Merusak Alur Utama:** Pastikan dokumen `rapid-10s/` tersimpan rapi, opsi catat `modes.rapid_10s` di `campaign.json` tanpa mengubah `stages.review` / `stages.storyboard` / `stages.video` yang sudah ada, lalu laporkan ringkas kepada pengguna.
