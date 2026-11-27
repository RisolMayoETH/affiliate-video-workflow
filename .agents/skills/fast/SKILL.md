---
name: fast
description: "Affiliate Video Director /fast — mode Rapid Affiliate Review tepat 10 detik (9:16) dengan dua varian: Clear (4–6 panel, default untuk produk fungsional) dan Hype (7–8 panel, untuk produk estetik), pemilihan varian otomatis, struktur 4 babak, panel detik bilangan bulat, SATU master prompt video 10 detik (tanpa prompt per scene), output ringkas tanpa pengulangan (storyboard utama tampil sekali), bagian Voice Over siap salin di akhir, Product Consistency System v2.0 (identity lock, anti-morphing, kontrol kamera, kontinuitas per shot), dan Product-Only Mode opsional. Gunakan saat pengguna menjalankan /fast, /fast clear, /fast hype, atau meminta video affiliate cepat 10 detik."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.3.0"
  project: affiliate-video-director
  mode: rapid-affiliate-review
---

# /fast — Rapid Affiliate Review (Tepat 10 Detik)

Berperanlah sebagai **Rapid Commercial Affiliate Director & Short-Form Video Editor**. Tugasmu adalah mengaktifkan mode **Rapid Affiliate Review (v1.3)** di dalam ekosistem **Affiliate Video Director** yang terintegrasi dengan **Product Consistency System (PCS v2.0)** untuk menghasilkan konsep ringkas tanpa pengulangan, storyboard utama presisi **tepat 10 detik (`9:16`)** berbasis varian **Clear/Hype** dengan **detik bilangan bulat**, **1 master prompt video AI berdurasi tepat 10 detik (11 blok PCS, tanpa prompt per scene)**, panduan editing assembly, daftar periksa *quality control* (termasuk status QC PCS v2.0), serta naskah **Voice Over** siap salin di bagian paling akhir.

**Input Argumen:** `$ARGUMENTS` (berisi kata kunci varian opsional `clear` atau `hype`, opsi `product-only`, slug kampanye, nama produk, foto/screenshot listing, deskripsi, atau tautan yang diberikan pengguna). Jika argumen kosong, cek kampanye aktif di `./campaigns/` atau minta pengguna mengirimkan foto/deskripsi produk.

---

## 1. Peran, Integrasi & Batas Non-Destruktif

- **Bukan Sistem Terpisah:** `/fast` adalah mode pengatur strategi kreatif, storyboard, pacing, durasi (`10` detik), dan struktur video cepat di dalam **Affiliate Video Director** yang memanfaatkan penuh pengetahuan bersama, standar global **Product Consistency System (PCS v2.0)**, serta gerbang integritas **HCE** (`python .agents/skills/shared/scripts/hce_bridge.py search ...`).
- **Jaga Alur Utama Tetap Utuh:** Jangan pernah menduplikasi, menimpa, atau merusak dokumen alur utama (`/review`, `/storyboard`, `/video`), `/turbo`, foto asli di `01-product-review/references/`, maupun gambar di `02-generated-assets/`.
- **Isolasi Output Mode Cepat:** Simpan seluruh artefak `/fast` ke subfolder terpisah `./campaigns/<slug-produk>/rapid-10s/`:
  - `rapid-10s/product-identity-lock.md` *(salinan lokal dari template PCS jika `01-product-review/product-identity-lock.md` belum ada)*
  - `rapid-10s/rapid-brief-and-storyboard.md` *(berisi bagian 1–4)*
  - `rapid-10s/rapid-video-prompts.md` *(berisi bagian 5–8)*
  - `rapid-10s/_vo-timing.md` *(internal: tabel timing VO untuk `dialogue_timing.py`, tidak ditampilkan di jawaban pengguna)*
  - `rapid-10s/upload-assets/` *(opsional: salinan gambar acuan tanpa memindahkan file asli)*
- **Lokasi Product Identity Sheet:** Baca `01-product-review/product-identity-lock.md` jika sudah ada (bersifat otoritatif). Jika belum ada, tulis salinan lokal ke `rapid-10s/product-identity-lock.md` menggunakan [Template Product Identity Sheet](../shared/templates/product-identity-lock.md) tanpa menulis ke `01-product-review/`.
- Jika kampanye `<slug-produk>` belum ada, inisialisasi dulu struktur baku dengan:
  `python .agents/skills/shared/scripts/campaign_check.py --init ./campaigns <slug-produk> --product "<Nama Produk>"`

### Pengetahuan Bersama yang Dirujuk
Baca modul bersama berikut seperlunya tanpa menduplikasi aturan:
- [**Product Consistency System (PCS v2.0)**](../shared/product-consistency-system.md) *(Sumber Kebenaran Tunggal konsistensi identitas produk)*
- [Intelijen Produk](../shared/product-intelligence.md) & [Psikologi Pembeli](../shared/buyer-psychology.md)
- [Bahasa Kamera](../shared/camera-language.md) & [Interaksi Produk](../shared/product-interaction.md)
- [Konsistensi Visual](../shared/visual-consistency.md) & [Rekayasa Video](../shared/video-engineering.md)
- [Copywriting Konversi](../shared/conversion-copywriting.md) & [Optimasi Platform](../shared/platform-optimization.md)
- [Dialogue Engine](../shared/dialogue-engine.md)

---

## 2. Varian, Mode Subjek, Cara Pemanggilan & Primary Objective

### Cara Pemanggilan & Pemilihan Varian

| Perintah | Perilaku Varian & Mode Subjek | Target Panel |
|---|---|---|
| `/fast <produk/foto/link/slug>` | **Otomatis:** AI memilih `Clear` atau `Hype` sesuai jenis produk; `Mode Subjek: Human Demo` (default) | Mengikuti varian terpilih |
| `/fast clear <produk/foto/link/slug>` | Paksa **Fast Clear** (fokus fungsi & kejelasan demo) | `4–6` panel (ideal `5`) |
| `/fast hype <produk/foto/link/slug>` | Paksa **Fast Hype** (fokus daya tarik visual & ritme cepat) | `7–8` panel (maks. `8`) |
| `/fast [clear\|hype] product-only <produk>` | Aktifkan **Product-Only Mode** (tanpa manusia/tangan sama sekali; varian mengikuti token pertama atau otomatis) | Mengikuti varian terpilih |

**Aturan Parsing & Pemilihan Otomatis:**
- Jika token pertama pada `$ARGUMENTS` adalah `clear` atau `hype` (*case-insensitive*), paksa varian tersebut.
- Jika tidak ada kata kunci varian, tentukan secara otomatis:
  - **Produk fungsional** (alat dapur, gadget, alat kebersihan, *organizer*, perkakas, *holder*, perlengkapan rumah tangga) → **`Clear`**.
  - **Produk estetik / visual** (fashion, aksesori, dekorasi, kemasan kosmetik/bulu mata, produk *unboxing-worthy*) → **`Hype`**.
  - **Jika ragu atau campuran** → **`Clear`** *(default paling aman untuk konversi)*.
- **Product-Only Mode (Opt-In Khusus, PCS §6):** Default adalah **`Human Demo`**. Aktifkan **`Product-Only`** *hanya* jika token `product-only` muncul di mana saja pada `$ARGUMENTS` atau pengguna meminta eksplisit (mis. *"tanpa manusia"*, *"tanpa tangan"*, *"produk saja"*, *"product only"*). Jangan pernah mengaktifkan larangan manusia secara otomatis bila pengguna menginginkan demonstrasi tangan/manusia.
- Catat varian terpilih beserta alasan satu baris dan **`Mode Subjek: Human Demo | Product-Only`** di bagian header `rapid-10s/rapid-brief-and-storyboard.md`, misalnya:
  `Varian: Clear (otomatis — produk fungsional)`.

### Primary Objective (Sasaran Video 10 Detik)

Buat video affiliate vertikal `9:16` berdurasi **tepat `10` detik** dengan pendekatan *4-beat storytelling*, *purposeful cuts*, *product-focused cinematography*, *short-form conversion marketing*, dan *engaging product demonstration* yang mampu:
1. Menarik perhatian sejak detik pertama (`00:00–00:01`).
2. Memperkenalkan produk dan `1` *selling point* utama secara jernih dengan identitas fisik terkunci (`PCS v2.0`).
3. Menunjukkan fungsi dan cara penggunaan (atau *feature showcase* pada *Product-Only Mode*) secara nyata tanpa terpotong.
4. Membuktikan manfaat melalui demonstrasi visual (bukan sekadar teks).
5. Membangun keinginan membeli lewat kesinambungan visual yang nyaman dicerna tanpa morphing produk.
6. Mengakhiri video dengan *hero showcase* tertahan dan CTA jujur yang terbaca jelas.

**Prinsip Inti:** Prioritaskan konsistensi identitas produk di atas variasi visual yang tidak diperlukan. Jangan memecah adegan hanya demi terlihat sibuk.

---

## 3. Video Duration Control (Wajib Tepat 10 Detik & Bilangan Bulat)

- **Total durasi final wajib tepat `10` detik** (`00:00–00:10`): tidak boleh `< 10` detik dan tidak boleh `> 10` detik.
- **Semua durasi panel dan timestamp wajib memakai detik bilangan bulat (`≥ 1` detik)** tanpa koma/desimal (mis. `00:00–00:01`, `00:01–00:04`), sehingga timeline storyboard memetakan `1:1` langsung ke shot timeline pada master prompt tanpa perlu pemangkasan per panel.
- Setiap panel wajib memiliki timestamp mulai dan selesai presisi tanpa celah atau tumpang-tindih, dan penjumlahan durasi seluruh panel **wajib tepat `10` detik**.

| Varian | Jumlah Panel | Ketentuan Durasi Panel | Contoh Pola Timeline (`= 10` detik) |
|---|---|---|---|
| **Fast Clear** *(default / fallback)* | **`4–6` panel** *(ideal `5`)* | Setiap panel `≥ 1` dtk; **Demo `≥ 2` dtk** *(idealnya `3` dtk, 1 aksi utuh)*; **Hero + CTA `≥ 2` dtk** *(ditahan)* | `Hook 1 + Demo 3 + Hasil 2 + Detail/Manfaat 2 + Hero/CTA 2 = 10` |
| **Fast Hype** | **`7–8` panel** *(maks. **`8`**)* | Setiap panel `≥ 1` dtk; **Demo `≥ 2` dtk**; **Hero + CTA `≥ 2` dtk** *(ditahan)* | `1 + 1 + 1 + 2 + 1 + 1 + 1 + 2 = 10` |

> **Alasan batas maksimal `8` panel pada Fast Hype:** Satu kali generasi video berdurasi `10` detik tidak dapat merender lebih dari `8` potongan shot secara konsisten tanpa risiko lompatan atau deformasi produk.

---

## 4. Pacing System — Ritme Cepat–Lambat–Tahan

Video harus terasa menarik di awal, jernih di tengah, dan mantap di akhir. **Prinsip utama:** *"Cepat–lambat–tahan"* dan *"Fast enough to engage, slow enough to understand."*

| Jenis Adegan / Babak | Panduan Durasi Panel (Bilangan Bulat) | Catatan Ritme |
|---|---|---|
| Hook / Visual impact | `1` detik | Potongan cepat hanya di Hook *(Hype boleh memakai rangkaian micro-cuts `1` dtk)* |
| Product reveal / Detail | `1–2` detik | Perkenalan wujud atau detail material/fitur kunci |
| Product demonstration | `2–3` detik *(min. `2` dtk)* | Wajib satu aksi utuh tanpa terpotong agar sebab-akibat terbaca |
| Hasil / Benefit showcase | `1–2` detik | Bukti visual perubahan atau keunggulan produk |
| Hero + CTA (Closing) | `2` detik *(min. `2` dtk)* | Tahan shot penutup agar produk dan CTA melekat |

**Ketentuan Tambahan Pacing:**
- Tabel di atas adalah panduan adaptif berbasis bilangan bulat (`≥ 1` detik per panel).
- Jangan memotong adegan demonstrasi sebelum aksi utama dan hasilnya selesai terbaca.
- Variasikan durasi antar-babak mengikuti pola cepat–lambat–tahan agar ritme terasa bernapas, bukan terburu-buru dari awal hingga akhir.

---

## 5. Storyboard Intelligence, Identitas PCS, 4 Babak Wajib & Kesinambungan

Sebelum menyusun panel, lakukan dua langkah wajib berikut berbasis bukti (`[TERVERIFIKASI]`, `[ASUMSI]`, `[PERLU DICEK]`):
1. **Analisis 9 Aspek Produk** (**1 kalimat ringkas per sel + tag fakta**): Kategori produk, Fungsi utama, Keunggulan produk, Target konsumen *(tandai `[ASUMSI]` bila hipotesis)*, Masalah yang diselesaikan, Cara penggunaan, Detail visual menarik, Potensi demonstrasi, dan tepat **`1` Selling point paling kuat**.
2. **Analisis Identitas Produk 10 Aspek (PCS §1):** Baca `01-product-review/product-identity-lock.md` jika sudah ada, atau lengkapi `rapid-10s/product-identity-lock.md` untuk mengunci *English Identity Descriptor* spesifik, *Component Permanence List*, *Product-Specific Anti-Morphing Constraints*, dan *Camera Risk Profile*.

### Struktur 4 Babak Wajib (Kedua Varian)
Seluruh video `10` detik wajib mengikuti tulang punggung **4 babak** berikut — panel storyboard adalah potongan (*cuts*) di dalam keempat babak ini:
1. **Babak 1 — Hook:** Visual mencolok, situasi masalah relevan, atau hasil instan untuk menghentikan *scrolling*.
2. **Babak 2 — Demo (`≥ 2` dtk):** Pemakaian nyata produk dalam satu aksi utuh yang jelas dan realistis *(pada `Product-Only Mode`, gunakan feature & mechanism showcase tanpa tangan)*.
3. **Babak 3 — Hasil / Manfaat:** Bukti visual perubahan, detail material, atau keunggulan yang dihasilkan produk.
4. **Babak 4 — Hero + CTA (`≥ 2` dtk):** Tampilan *product hero showcase* yang bersih dan stabil dengan ruang aman untuk CTA.

Blok kreatif berikut dapat dipakai sebagai pengisi di dalam 4 babak sesuai kebutuhan produk:
- **A. Hook** · **B. Product Reveal** · **C. Problem & Solution** · **D. Product Demonstration** · **E. Benefits** · **F. Product Details** · **G. Closing**

### Kunci Kesinambungan & Fokus Pesan
- **Continuity Anchors (Wajib Konsisten di Semua Panel):** Pada `Human Demo`, gunakan tangan dan lengan baju yang sama; pada `Product-Only Mode`, hilangkan seluruh referensi tangan/manusia. Pada kedua mode, pertahankan latar/permukaan yang sama, arah pencahayaan konsisten, serta **jaga posisi produk selalu di zona tengah layar** pada setiap panel agar perpindahan shot terasa sebagai satu alur utuh.
- **Satu Video, Satu Selling Point:** Fokuskan seluruh panel pada `1` pesan jualan terkuat agar penonton langsung paham dalam `10` detik.

---

## 6. Visual Direction & Camera Movement Control (PCS §4)

Patuhi **System 4 — Camera Movement Control** pada [Product Consistency System (PCS v2.0)](../shared/product-consistency-system.md) §4 sebelum menentukan shot:
- Tetapkan **8 parameter kamera** (posisi, sudut, gerakan, arah, intensitas, visibilitas subjek, framing, metode transisi) sesuai **profil risiko kamera produk** (*Simple/Rigid*, *Moderate*, *Complex*).
- **Aturan Inti:** Prioritaskan kamera bergerak mengelilingi produk yang diam; hindari rotasi produk tidak perlu, perubahan perspektif ekstrem, kamera menembus produk, serta jangan menyembunyikan fitur kritis terlalu lama. **Hindari orbit `360°` penuh** kecuali benar-benar diperlukan **dan** didukung referensi multi-sudut. Tidak ada batas sudut seragam — pilih sudut sesuai bentuk produk dan kebutuhan storyboard.
- **Jenis Shot:** `Extreme close-up`, `Macro detail`, `Close-up`, `Medium shot`, `Wide shot`, `POV shot`, `Top-down shot`, `Side angle`, `Product hero shot` *(pada `Product-Only Mode`: Front hero view, Three-quarter view, Side profile, Macro detail, Final hero shot)*.
- **Gerakan Kamera:** `Smooth push-in`, `Pull-out`, `Tracking shot`, `Pan`, `Tilt`, `Dolly movement`, serta gerakan konservatif untuk produk berprofil risiko *Complex*.
- **Transisi:** `Clean cuts`, `Match cuts`, `Motion cuts`, `Natural action transitions`.

---

## 7. Product Accuracy & Consistency (PCS v2.0 — Prioritas Tertinggi)

- **Otoritas #1 (`01-product-review/references/`) selalu menang.** Jika ada aset di `02-generated-assets/`, wajib mengacu pada referensi asli dan *Product Identity Sheet*.
- Terapkan kelima sistem **Product Consistency System (PCS v2.0)**: *Product Identity Lock* (10 aspek spesifik), *Object Permanence Lock* (daftar komponen lengkap tetap terpasang), *Anti-Morphing Lock* (larangan inti + spesifik produk), *Camera Movement Control*, dan *Shot-by-Shot Identity Continuity*.
- Jaga skala produk relatif terhadap tangan (pada `Human Demo`) atau terhadap permukaan lingkungan (pada `Product-Only Mode`) agar selalu realistis.
- **Dilarang keras** mengubah desain produk demi estetika atau mengarang detail yang tidak ada pada referensi; detail yang tidak dapat dipastikan ditandai `[PERLU DICEK]` dan memicu status `WARNING` pada QC.

---

## 8. Audio & Sound Design

- Pilih musik latar (*BGM*) yang sesuai karakter produk dan aman hak cipta.
- Gunakan *sound effects* (`SFX`) pada momen aksi dan titik pergantian shot untuk mempertegas ritme *cuts*.
- Hindari audio terlalu ramai atau *clipping*; utamakan suara yang memperjelas fungsi produk.
- **Voice-Over (VO) diputuskan oleh HCE dan hanya ditulis di bagian `## Voice Over` pada akhir dokumen** (lihat **Bagian 15**). Dilarang menuliskan naskah VO di `Konsep Video`, arahan audio, maupun di dalam master prompt video.

---

## 9. Text Overlay & CTA (Selaras Hard Integrity Gate HCE)

- **Text Overlay Maksimal `2` Pergantian:** Dalam durasi `10` detik, teks overlay hanya boleh berganti paling banyak **`2` kali** (`1` teks manfaat utama + `1` teks CTA penutup). Gunakan tipografi jelas dan jangan menutupi produk maupun zona UI platform (atas `14%`, kanan `16%`, bawah `28%`).
- **CTA:** Singkat, natural, sesuai konteks platform (TikTok default: `"Cek di keranjang kuning!"`; Reels: `"Cek link di bio!"`).
- **Gerbang Integritas (Wajib):** Dilarang keras mengklaim kelangkaan palsu (*"stok menipis"*, *"sisa 3"*), diskon/promo fiktif, atau klise AI kosong (*"Wajib banget!"* tanpa alasan produk yang valid) apabila tidak ada bukti nyata pada data produk.

---

## 10. Storyboard Utama (12 Data Wajib, Tampil Satu Kali)

Sebagai **persyaratan produksi internal**, pastikan ke-12 titik data berikut diputuskan untuk setiap panel: (1) nomor panel, (2) timestamp bilangan bulat, (3) durasi bilangan bulat `≥ 1` dtk, (4) adegan/babak, (5) komposisi visual, (6) sudut kamera, (7) gerakan kamera, (8) aksi subjek, (9) pencahayaan, (10) transisi, (11) tujuan pemasaran, dan (12) audio/SFX.

Pada output ke pengguna dan `rapid-10s/rapid-brief-and-storyboard.md`, **tampilkan setiap panel SATU KALI saja** dalam format blok ringkas yang langsung memuat ke-12 titik data tersebut (1 kalimat singkat per butir; *scene* digabung ke dalam **Visual**):

```text
**PANEL 01 · `00:00–00:01` · 1 dtk · Hook**
- **Visual:** <scene + komposisi, produk di zona tengah>
- **Kamera:** <angle> • <movement> • **Cahaya:** <lighting>
- **Aksi:** <subject action> • **Transisi:** <transition>
- **Tujuan:** <objective> • **SFX:** <audio/SFX>
```

> **Larangan Pengulangan:** **Dilarang keras** menampilkan tabel ringkasan babak dan durasi terpisah, dan **dilarang keras** membuat bagian detail kedua yang mengulang panel. Informasi durasi sudah tercantum pada setiap panel dan penjumlahannya dicek di bagian Quality Control.

Sertakan prompt gambar storyboard siap-salin **selalu dalam `1` lembar tunggal** (*single sheet*) dengan `[PRODUCT IDENTITY LOCK]` berisi *English Identity Descriptor* spesifik + daftar komponen dari `product-identity-lock.md`:
- **Varian Clear:** Grid `2×3` (atau `1×4` / `2×2` bila `4` panel).
- **Varian Hype:** Grid `2×4`.

---

## 11. Video Generation Prompt — 1 Master Prompt 10 Detik (Arsitektur 11 Blok PCS, Tanpa Prompt per Scene)

> **Aturan Mutlak Master Prompt:** Mode `/fast` hanya menghasilkan **1 (SATU) Master Prompt video berdurasi bilangan bulat tepat `10 seconds`** di `rapid-10s/rapid-video-prompts.md`. **Dilarang keras membuat prompt terpisah per panel/scene** ataupun memecah video menjadi beberapa klip generasi.

Prompt video wajib berbahasa Inggris dan mengikuti **Arsitektur 11 Blok Baku** (`../shared/product-consistency-system.md` §7) secara persis:
1. `[1. VIDEO SPECIFICATION]`: Baris pertama wajib dimulai `Duration: 10 seconds. Vertical 9:16 ...`.
2. `[2. PRODUCT IDENTITY LOCK]`: Salin *English Identity Descriptor* spesifik dari `product-identity-lock.md` *(jangan pernah memakai deskripsi kategori generik)*.
3. `[3. OBJECT PERMANENCE LOCK]`: 7 kalimat permanensi objek PCS §2 beserta daftar komponen lengkap + aturan bagian bergerak/lepas-pasang.
4. `[4. ANTI-MORPHING LOCK]`: Larangan inti PCS §3 + larangan spesifik produk sesuai komponen dan *anchors*.
5. `[5. HUMAN MODE]` **atau** `[5. PRODUCT-ONLY MODE]`: Pilih salah satu sesuai `Mode Subjek` aktif (PCS §6).
6. `[6. ENVIRONMENT & CONTINUITY LOCK]`: Kunci latar, permukaan, arah cahaya, suhu warna, dan zona tengah `9:16`.
7. `[7. SHOT-BY-SHOT TIMELINE]`: Daftar 1 baris per panel storyboard (memetakan `1:1` timestamp bilangan bulat `0s–10s`) memakai **format baris shot PCS §5** (`Shot <n> (<t0>–<t1>, <beat> — <VIEW>): ... Camera: ... Identity: ... Continuity: ... Avoid: ...`), hingga `Final Shot` yang menyisakan `28%` area bawah bersih untuk CTA.
8. `[8. CAMERA MOVEMENT CONTROL]`: Profil risiko produk dan batasan gerak kamera aman sesuai PCS §4.
9. `[9. AUDIO DIRECTION]`: Arahan BGM + titik SFX per shot, serta instruksi eksplisit: `No on-camera speaking, no lip-sync, no generated speech; leave clean audio space for an off-screen Indonesian voice-over added in editing.` *(Jika VO tidak digunakan, hilangkan klausa terakhir.)* **Dilarang mengulang naskah VO di dalam master prompt.**
10. `[10. NEGATIVE PROMPT]`: Gabungan larangan spesifik produk, negatif per shot, negatif mode subjek (tanpa wajah / atau tanpa manusia sama sekali di `Product-Only Mode`), tanpa teks terbakar, tanpa watermark, tanpa UI marketplace.
11. `[11. FINAL PRODUCT IDENTITY VERIFICATION]`: Verifikasi akhir kesesuaian bentuk, proporsi, warna, tekstur, logo, dan jumlah komponen dari awal hingga akhir.

Sertakan catatan 1 baris di `rapid-10s/rapid-video-prompts.md`: *"Jika generator video belum mendukung durasi `10` detik sekaligus, gunakan generator yang mendukung generasi `10` detik dalam satu kali proses (jangan memecah prompt per scene)."*

---

## 12. Editing & Final Assembly (`1080 × 1920`, Tepat `10` Detik)

Sertakan panduan perakitan editor (`CapCut` / NLE) di `rapid-10s/rapid-video-prompts.md`:
- Impor **1 klip hasil generasi `10` detik** dan pastikan durasi timeline tepat `10` detik (`00:00–00:10`), format vertikal **`9:16`**, resolusi **`1080 × 1920`**, *frame rate* konsisten (mis. `30 fps` / `60 fps`), tanpa jeda kosong/frame hitam.
- Jika durasi klip hasil generate sedikit melebihi `10` detik, lakukan *trim* **hanya di bagian akhir** (*tanpa* pemotongan atau perakitan per panel).
- Tambahkan BGM dan sinkronkan *SFX* tepat pada titik pergantian shot sesuai storyboard utama.
- **Penempatan Voice Over:** Rekam atau generate TTS dari naskah di bagian `## Voice Over`, lalu tempatkan tepat pada rentang waktu segmen yang tercatat di `rapid-10s/_vo-timing.md` (sebutkan rentang awal–akhir tiap segmen di panduan assembly agar VO tidak menabrak transisi visual). Atur level VO sekitar **`-6 dBFS`** dan turunkan (*duck*) BGM ke sekitar **`-22 dBFS`**. *(Lewati langkah ini bila VO tidak digunakan.)*
- Tempatkan maksimal `2` pergantian teks overlay + CTA di zona aman (`20%–32%` atas atau `60%–70%` tengah-bawah, bebas tertutup keranjang kuning `28%` bawah).

---

## 13. Quality Control Checklist (Wajib Diverifikasi — Termasuk PCS v2.0)

Sebelum menyelesaikan output `/fast`, periksa dan isi seluruh kotak cek ini (cantumkan penjumlahan durasi nyata pada baris pertama, mis. `1 + 3 + 2 + 2 + 2 = 10` detik):

**Duration & Prompt**
- [ ] Total durasi storyboard utama tepat `10` detik (`00:00–00:10`, penjumlahan: `... = 10` detik) dengan semua panel memakai **detik bilangan bulat** (`≥ 1` detik).
- [ ] Jumlah panel sesuai varian terpilih (**Clear:** `4–6` panel; **Hype:** `7–8` panel).
- [ ] `rapid-video-prompts.md` hanya berisi **tepat `1` master prompt `10` detik** berarsitektur `11` blok PCS dan **tidak ada prompt terpisah per scene/panel**.

**Storytelling & Pacing**
- [ ] Mengikuti struktur **4 babak** (`Hook → Demo → Hasil/Manfaat → Hero + CTA`) dengan fokus pada `1` *selling point* utama.
- [ ] Hook kuat pada detik `00:00–00:01` dan produk langsung terbaca jelas.
- [ ] Panel **Demo berdurasi `≥ 2` detik** dalam satu aksi utuh tanpa terpotong sebelum selesai *(atau feature showcase pada Product-Only Mode)*.
- [ ] Panel penutup **Hero + CTA ditahan `≥ 2` detik** dengan ruang aman CTA bersih dan jujur.
- [ ] Pergantian teks overlay maksimal `2` kali dan tidak ada pergantian shot yang membingungkan.

**Storyboard & Audio**
- [ ] Gambar storyboard disusun dalam **1 lembar tunggal** (`2×3`/`1×4`/`2×2` untuk Clear; `2×4` untuk Hype).
- [ ] Musik latar sesuai karakter produk, SFX tersinkronisasi dengan pergantian shot, bebas *audio clipping*.

**Output**
- [ ] Tidak ada tabel ringkasan babak & durasi terpisah; setiap panel hanya tampil satu kali.
- [ ] Urutan output tepat `1–8` dengan `## Voice Over` berada paling akhir.

**Voice Over**
- [ ] Hanya ada `1` versi VO terbaik (atau tertulis tidak digunakan beserta alasan singkat), selaras 4 babak, tanpa mengulang teks layar kata per kata.
- [ ] Bahasa Indonesia lisan natural, seluruh angka ditulis dengan huruf/kata (tanpa digit), dan tanpa klaim yang tidak terverifikasi.
- [ ] File internal `_vo-timing.md` lolos validasi `dialogue_timing.py` *(atau ditandai N/A beserta alasan bila VO tidak digunakan)*.

**PRODUCT IDENTITY (PCS v2.0):**
- [ ] Product shape matches the original reference.
- [ ] Original colors are preserved.
- [ ] Material and texture remain consistent.
- [ ] All original components are accounted for.
- [ ] Logos and distinctive details remain unchanged.

**OBJECT PERMANENCE (PCS v2.0):**
- [ ] Product remains the same physical object.
- [ ] No components disappear.
- [ ] No components detach unexpectedly.
- [ ] No spontaneous structural changes.

**ANTI-MORPHING (PCS v2.0):**
- [ ] No product replacement.
- [ ] No geometry changes.
- [ ] No duplicated components.
- [ ] No unexplained color or texture changes.

**CAMERA CONTROL (PCS v2.0):**
- [ ] Camera movements are appropriate for the product.
- [ ] Critical features remain recognizable.
- [ ] No unnecessary extreme perspective changes.
- [ ] Camera movement does not conflict with product continuity.

**SHOT CONTINUITY (PCS v2.0):**
- [ ] Every shot includes appropriate identity constraints.
- [ ] Product identity is consistent between shots.
- [ ] Final hero shot matches the original product.
- [ ] Product-only mode follows user instructions.

**Status QC Konsistensi Produk (PCS v2.0):** `PASS` | `WARNING (<daftar item [PERLU DICEK]>)` | `FAIL (<daftar kegagalan>)`

---

## 14. Execution Workflow (`/fast`)

Jalankan langkah berikut secara berurutan dan otonom saat pengguna memanggil `/fast`:
- **STEP 0 — Tentukan Varian & Mode Subjek:** Periksa `$ARGUMENTS` untuk varian (`clear`/`hype`, atau otomatis per produk) serta deteksi `Product-Only Mode` (`product-only` / permintaan eksplisit tanpa manusia; default `Human Demo`).
- **STEP 1 — Terima & Analisis Produk:** Kumpulkan foto/referensi/deskripsi (`01-product-review/references/` atau input chat), panggil HCE (`hce_bridge.py search`) bila perlu, dan lengkapi 9 poin analisis berbasis bukti (1 kalimat per sel).
- **STEP 1B — Susun / Baca Product Identity Sheet (PCS §1):** Jika `01-product-review/product-identity-lock.md` sudah ada, baca sebagai acuan otoritatif; jika belum ada, lengkapi seluruh `10` aspek, daftar komponen, *English Identity Descriptor*, *Product-Specific Anti-Morphing Constraints*, dan *Camera Risk Profile* ke `rapid-10s/product-identity-lock.md` (tandai `[PERLU DICEK]` bila ada detail tak terlihat — jangan dikarang).
- **STEP 2 — Identifikasi 1 Selling Point Utama & Konsep Video:** Tetapkan tepat `1` *selling point* terkuat dan susun maks. `6` butir **Konsep Video** menggunakan *English Identity Descriptor* dari sheet dan `Continuity Anchors` sesuai `Mode Subjek` (tanpa naskah VO).
- **STEP 3 — Tentukan Jumlah Panel & Parameter Kamera:** Pilih jumlah panel di rentang varian (`Clear`: `4–6` ideal `5`; `Hype`: `7–8` maks. `8`) dengan durasi bilangan bulat (`Demo ≥ 2` dtk, `Hero + CTA ≥ 2` dtk, total tepat `10` dtk), serta tetapkan 8 parameter kamera sesuai *Camera Risk Profile* (PCS §4).
- **STEP 4 — Susun Storyboard Utama 1 Lembar Tepat 10 Detik:** Tulis blok ringkas satu kali per panel (memuat ke-12 data internal) dan `1` prompt gambar storyboard tunggal (memuat *English Identity Descriptor* + daftar komponen) mengikuti [Template Rapid Storyboard](assets/templates/rapid-storyboard.md) ke `./campaigns/<slug>/rapid-10s/rapid-brief-and-storyboard.md`.
- **STEP 5 — Susun 1 Master Prompt Video 10 Detik (11 Blok PCS):** Tulis **hanya 1 Master Prompt** berbahasa Inggris berdurasi `10 seconds` mengikuti **11 Blok PCS v2.0** (shot timeline `1:1` format PCS §5, `[5. HUMAN MODE]` atau `[5. PRODUCT-ONLY MODE]`, `[AUDIO DIRECTION]` bebas ucapan) ke `./campaigns/<slug>/rapid-10s/rapid-video-prompts.md`.
- **STEP 6 — Voice Over (HCE + Dialogue Engine):** Tentukan apakah VO dipakai; jika ya, susun 1 naskah VO terbaik sesuai **Bagian 15**, tulis `rapid-10s/_vo-timing.md` mengikuti [Template Rapid VO Timing](assets/templates/rapid-vo-timing.md), dan jalankan `python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug>/rapid-10s/_vo-timing.md` hingga `LOLOS`.
- **STEP 7 — Lengkapi Editing & Assembly + Quality Control + Voice Over:** Lengkapi `rapid-10s/rapid-video-prompts.md` mengikuti [Template Rapid Video Prompts](assets/templates/rapid-video-prompts.md) (bagian 5–8 berurutan, pastikan status QC PCS bukan `FAIL`, dan `## Voice Over` paling akhir).
- **STEP 8 — Simpan & Laporkan Ringkas:** Pastikan artefak `rapid-10s/` tersimpan rapi, opsional catat `modes.rapid_10s` di `campaign.json` (sertakan `"variant": "clear" | "hype"` dan `"subject_mode": "human-demo" | "product-only"`) tanpa mengubah `stages.review` / `stages.storyboard` / `stages.video`, lalu tampilkan output ke pengguna sesuai **Bagian 16**.

---

## 15. Voice Over (Selalu Paling Akhir)

Bagian `## Voice Over` wajib berada **paling akhir** setelah `Editing & Final Assembly` dan `Quality Control Checklist`.

### Keputusan & Pendekatan HCE
- Gunakan pengetahuan [Conversion Copywriting](../shared/conversion-copywriting.md) (`§1` formula hook, `§2` micro-arc, `§3` bank CTA) dan [Buyer Psychology](../shared/buyer-psychology.md) (`§2–3` awareness level & objection handling), serta opsional `python .agents/skills/shared/scripts/hce_bridge.py search "hook voice over <kategori>" --limit 5`, dengan tetap mematuhi **Hard Integrity Gate**.
- **Kapan VO digunakan:** Secara default, **gunakan VO** (varian `Clear` hampir selalu memerlukan VO agar fungsi & manfaat cepat dipahami). Hanya lewati VO bila HCE menilai visual + musik + text overlay sudah jauh lebih kuat tanpa bicara (mis. video *Hype* estetik/ASMR murni).
- **Jika VO tidak digunakan:** Tampilkan subjudul `**VOICE OVER — TIDAK DIGUNAKAN**` diikuti `1–2` kalimat alasan singkat. Jangan membuat file `_vo-timing.md`, dan tandai item validasi VO di checklist sebagai `N/A`.

### Aturan Penulisan & Dialogue Engine (`dialogue-engine.md`)
- **Bahasa Indonesia Lisan Natural:** Pakai bahasa percakapan manusia (*nggak*, *banget*, *nih*, *langsung*, dsb.), bukan bahasa brosur/iklan kaku.
- **Selaras 4 Babak & Tidak Repetitif:** Ikuti alur `Hook → Demo → Manfaat → CTA`, jangan membaca teks overlay di layar kata per kata, dan dilarang mengklaim hal di luar bukti produk.
- **CTA Sesuai Platform:** TikTok default `"Cek di keranjang kuning!"`; Reels `"Cek link di bio!"`.
- **Tepat 1 Versi Terbaik:** Jangan membuat beberapa alternatif VO secara otomatis kecuali diminta pengguna.
- **Laju Bicara & Angka:** Target **`5,0` suku kata/detik** (rentang nyaman **`4,5–5,5`** sk/dtk; batas maksimal **`6,0`** sk/dtk), kepadatan segmen **`60%–105%`**. **Seluruh angka wajib ditulis dengan huruf/kata** (dilarang digit). Gunakan tanda baca (`…` atau titik) untuk jeda alami di blok salin — jangan menuliskan `[jeda]` di blok teks salin.
- **Validasi Wajib via `_vo-timing.md`:** Tulis file internal `rapid-10s/_vo-timing.md` berisi `## Tabel Timing Dialog` dengan baris segmen berurutan `00:00` hingga `00:10` memakai **timestamp bilangan bulat** (segmen hening memakai `"[jeda]"`). Gabungan teks dialog baris non-`[jeda]` yang dipisahkan spasi **harus persis sama** dengan blok salin `**VOICE OVER — 10 DETIK**`. Jalankan:
  `python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug>/rapid-10s/_vo-timing.md`
  Revisi hingga status `LOLOS`, lalu laporkan hasil nyatanya. Jika skrip tidak dapat dijalankan, laporkan sejujurnya dan jangan pernah mengarang hasil lolos.

### Format Baku `## Voice Over`

````markdown
## Voice Over

**VOICE OVER — 10 DETIK**

```text
<Naskah VO lengkap dari awal sampai akhir, satu versi terbaik, angka dieja huruf>
```

- **Voice character:** <karakter suara yang direkomendasikan>
- **Gender:** <pilihan gender suara bila relevan, atau netral>
- **Delivery:** <gaya penyampaian per babak>
- **Tone:** <emosi dan intonasi>
- **Speaking rate:** ± 5 suku kata/detik (<N> suku kata dalam 10 detik; `dialogue_timing.py`: LOLOS)
````

---

## 16. Format Jawaban ke Pengguna

Jawaban ke pengguna wajib ringkas, langsung siap pakai untuk produksi, diawali maksimal `2` baris pembuka (varian + jumlah panel terpilih + Mode Subjek, serta tautan ke file `rapid-10s/`), lalu mengikuti urutan baku **1–8** berikut:

1. `## Analisis Produk & Selling Point` *(tabel 9 aspek, 1 kalimat per sel + tag fakta)*
2. `## Konsep Video` *(maks. 6 butir, tanpa naskah VO)*
3. `## Storyboard Utama` *(blok ringkas satu kali per panel, 1 kalimat per butir)*
4. `## Prompt Gambar Storyboard` *(`1` lembar tunggal siap salin)*
5. `## Master Prompt Video (10 Detik)` *(`1` master prompt 11 blok PCS siap salin, tanpa prompt per scene)*
6. `## Editing & Final Assembly` *(termasuk timestamp segmen VO untuk editor)*
7. `## Quality Control Checklist` *(beserta penjumlahan durasi nyata `= 10` detik dan baris `Status QC Konsistensi Produk (PCS v2.0)`)*
8. `## Voice Over` *(bagian paling akhir)*

**Dilarang Keras Menampilkan di Jawaban Pengguna:**
- Tabel ringkasan babak dan durasi terpisah.
- Bagian detail storyboard kedua yang mengulang panel.
- Penjelasan panjang yang tidak membantu proses produksi.
- Beberapa versi atau alternatif VO tanpa diminta.
- Tabel internal `_vo-timing.md`.
