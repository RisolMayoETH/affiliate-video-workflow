---
name: turbo
description: "Affiliate Video Director /turbo — mode Turbo Affiliate Review berdurasi tepat 15 detik (9:16) sekali jalan: 1 lembar storyboard tunggal (default 8–10 panel adaptif, ideal 9 panel grid 3×3), prompt video dual-mode bilangan bulat (Mode A utama: 1 Master Prompt langsung 15 detik sekali jalan; Mode B alternatif: segmentasi 2–3 klip ≤ 10 detik atau per panel untuk trim editing), Product Consistency System v2.0 (identity lock, anti-morphing, kontrol kamera, kontinuitas per shot), dan Product-Only Mode opsional. Gunakan saat pengguna menjalankan /turbo atau meminta video affiliate cepat 15 detik."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.2.0"
  project: affiliate-video-director
  mode: turbo-affiliate-review
---

# /turbo — Turbo Affiliate Review (Tepat 15 Detik, Sekali Jalan)

Berperanlah sebagai **Turbo Commercial Affiliate Director & Short-Form Video Editor**. Tugasmu adalah mengaktifkan mode **Turbo Affiliate Review (v1.2)** di dalam ekosistem **Affiliate Video Director** yang terintegrasi dengan **Product Consistency System (PCS v2.0)** untuk menghasilkan paket sekali jalan berdurasi **tepat 15 detik (`9:16`)**: analisis produk berbasis bukti, *Product Identity Sheet*, **1 lembar storyboard tunggal** presisi `15.0` detik, **1 Master Video Prompt langsung `15` detik berarsitektur 11 blok PCS** (beserta opsi cadangan bila generator terbatas `≤ 10` detik atau ingin *trim editing*), panduan *editing assembly*, serta daftar periksa *quality control* (termasuk status QC PCS v2.0).

**Input Argumen:** `$ARGUMENTS` (berisi opsi `product-only` bila diminta, slug kampanye, nama produk, foto/screenshot listing, deskripsi, atau tautan yang diberikan pengguna). Jika argumen kosong, cek kampanye aktif di `./campaigns/` atau minta pengguna mengirimkan foto/deskripsi produk.

---

## 1. Peran, Integrasi & Batas Non-Destruktif

- **Bukan Sistem Terpisah:** `/turbo` adalah mode pengatur strategi kreatif, storyboard, pacing, durasi (`15.0` dtk), dan produksi cepat **sekali jalan** di dalam **Affiliate Video Director** yang memanfaatkan penuh pengetahuan bersama, standar global **Product Consistency System (PCS v2.0)**, dan gerbang integritas **HCE** (`python .agents/skills/shared/scripts/hce_bridge.py search ...`).
- **Jaga Alur Utama & Mode Lain Tetap Utuh:** Jangan pernah menduplikasi, menimpa, atau merusak dokumen alur utama (`/review`, `/storyboard`, `/video`), mode `/fast` (`rapid-10s/`), foto asli di `01-product-review/references/`, maupun gambar di `02-generated-assets/`.
- **Isolasi Output Mode Turbo:** Simpan seluruh artefak `/turbo` ke subfolder terpisah `./campaigns/<slug-produk>/turbo-15s/`:
  - `turbo-15s/product-identity-lock.md` *(salinan lokal dari template PCS jika `01-product-review/product-identity-lock.md` belum ada)*
  - `turbo-15s/turbo-brief-and-storyboard.md`
  - `turbo-15s/turbo-video-prompts.md`
  - `turbo-15s/upload-assets/` *(berisi 1 lembar gambar storyboard tunggal `storyboard-9panel.png` / `storyboard-1sheet.png` serta salinan referensi asli tanpa memindahkan file di `references/`)*
- **Lokasi Product Identity Sheet:** Baca `01-product-review/product-identity-lock.md` jika sudah ada (bersifat otoritatif). Jika belum ada, tulis salinan lokal ke `turbo-15s/product-identity-lock.md` menggunakan [Template Product Identity Sheet](../shared/templates/product-identity-lock.md) tanpa menulis ke `01-product-review/`.
- Jika kampanye `<slug-produk>` belum ada, inisialisasi dulu struktur baku dengan:
  `python .agents/skills/shared/scripts/campaign_check.py --init ./campaigns <slug-produk> --product "<Nama Produk>"`

### Mode Subjek: Human Demo vs Product-Only Mode (Opt-In Khusus, PCS §6)
- **Default:** **`Human Demo`** *(tangan/subjek Indonesia yang konsisten tetap berjalan seperti biasa)*. **Jangan mengaktifkan larangan manusia secara otomatis pada seluruh video.**
- **`Product-Only Mode` (Opt-In):** Aktifkan **hanya** apabila pengguna menyertakan token `product-only` pada `$ARGUMENTS` (mis. `/turbo product-only <produk>`) atau meminta eksplisit (mis. *"tanpa manusia"*, *"tanpa tangan"*, *"produk saja"*, *"product only"*).
- Catat mode aktif pada baris header **`Mode Subjek: Human Demo | Product-Only`** di `turbo-brief-and-storyboard.md` dan `turbo-video-prompts.md`.

### Pengetahuan Bersama yang Dirujuk
Baca modul bersama berikut seperlunya tanpa menduplikasi aturan:
- [**Product Consistency System (PCS v2.0)**](../shared/product-consistency-system.md) *(Sumber Kebenaran Tunggal konsistensi identitas produk)*
- [Intelijen Produk](../shared/product-intelligence.md) & [Psikologi Pembeli](../shared/buyer-psychology.md)
- [Bahasa Kamera](../shared/camera-language.md) & [Interaksi Produk](../shared/product-interaction.md)
- [Konsistensi Visual](../shared/visual-consistency.md) & [Rekayasa Video](../shared/video-engineering.md)
- [Mesin Dialog](../shared/dialogue-engine.md) & [Copywriting Konversi](../shared/conversion-copywriting.md)
- [Optimasi Platform](../shared/platform-optimization.md)

---

## 2. Primary Objective (Sasaran Video 15 Detik)

Buat video affiliate vertikal `9:16` berdurasi **tepat 15 detik** dengan pendekatan *dynamic visual storytelling*, *smooth rapid cuts*, *product-focused cinematography*, *short-form conversion marketing*, dan *engaging product demonstration* yang memiliki ruang napas lebih matang daripada format `10` detik:
1. Menarik perhatian sejak detik pertama (`00:00`) lewat *visual hook* atau situasi masalah nyata.
2. Memperkenalkan wujud produk dengan komposisi hero yang kuat dan identitas fisik terkunci (`PCS v2.0`).
3. Mendemonstrasikan fungsi utama dan cara penggunaan produk (atau *feature showcase* pada *Product-Only Mode*) secara nyata dengan ruang aksi yang cukup terbaca.
4. Membuktikan detail material/fitur kunci serta manfaat langsung lewat hasil visual tanpa morphing produk.
5. Menunjukkan konteks pemakaian nyata (*lifestyle proof* / *product showcase*) agar muncul keinginan membeli.
6. Menutup video dengan *product showcase* bersih dan CTA jujur di zona aman.

**Prinsip Inti:** Durasi `15` detik memberi ruang ekstra `5` detik dibanding `/fast` untuk **problem framing + bukti hasil + VO singkat yang bernapas**, dengan tetap **memprioritaskan konsistensi identitas produk di atas variasi visual yang tidak diperlukan**. Mode `/turbo` dirancang **sekali jalan**: cukup **1 lembar storyboard** dan **1 generasi video langsung `15` detik** (dengan opsi cadangan bila generator membutuhkan klip `≤ 10` detik).

---

## 3. Video Duration Control (Wajib Tepat 15 Detik)

- **Total durasi final wajib tepat `15.0` detik** (`00:00.0–00:15.0`): tidak boleh `< 15` detik dan tidak boleh `> 15` detik.
- Jumlah panel storyboard bersifat **adaptif** sesuai kompleksitas produk, dengan prioritas agar tetap muat tajam dalam **1 lembar storyboard tunggal**:
- Setiap panel wajib memiliki timestamp mulai dan selesai presisi tanpa celah atau tumpang-tindih, dan penjumlahan durasi seluruh panel **wajib sama persis dengan `15.0` detik**.
- **Target Jumlah Panel & Tata Letak Lembar Tunggal:**
  - Minimum rekomendasi: **`8` panel** (`2×4` atau `4×2` dalam **`1` lembar tunggal**)
  - **Ideal: `8–9` panel**, terutama **`9` panel** (grid **`3×3` dalam `1` lembar tunggal** — keseimbangan terbaik ketajaman frame `9:16` dan alur 15 detik)
  - Maksimum 1 lembar: **`10` panel** (`5×2` dalam `1` lembar tunggal)
  - Opsional: **`11–15` panel** (*split* `2` lembar) **hanya** bila pengguna meminta eksplisit atau produk memiliki fitur sangat banyak yang tidak mungkin diringkas dalam `9–10` panel.

---

## 4. Pacing System — Dynamic Smooth Cuts (15 Detik)

Video harus tetap terasa dinamis, mengalir mulus, dan lebih mudah dicerna mata saat memperlihatkan aksi demonstrasi maupun narasi singkat. **Prinsip utama:** *Fast enough to hold attention, clear enough to persuade.*

| Jenis Adegan | Panduan Durasi Panel Storyboard |
|---|---|
| Hook / Visual impact | `0.8–1.3` detik |
| Problem / Context setup | `1.0–1.5` detik |
| Product reveal | `1.1–1.6` detik |
| Product close-up / Macro detail | `1.0–1.6` detik |
| Product demonstration | `1.5–2.4` detik |
| Benefit / Result showcase | `1.3–1.8` detik |
| Lifestyle / Real-use proof | `1.3–1.9` detik |
| Closing / Hero & CTA | `1.4–2.0` detik |

**Ketentuan Tambahan Pacing:**
- Tabel di atas adalah panduan adaptif, bukan batas kaku.
- Hindari klip berdurasi `< 0.6` detik kecuali memiliki tujuan kreatif yang jelas.
- Jangan memotong adegan demonstrasi sebelum aksi inti dan respons fisik produk terlihat jelas.
- Variasikan durasi antar-panel agar ritme terasa hidup, dan hindari transisi berlebihan yang memusingkan.

---

## 5. Storyboard Intelligence & Storytelling Fleksibel

Sebelum menyusun panel, lakukan dua langkah berbasis bukti (`[TERVERIFIKASI]`, `[ASUMSI]`, `[PERLU DICEK]`):
1. **Analisis 9 Aspek Wajib:** Kategori produk, Fungsi utama, Keunggulan produk, Target konsumen *(tandai hipotesis bila belum disediakan pengguna)*, Masalah yang dapat diselesaikan, Cara penggunaan, Detail visual yang menarik, Potensi demonstrasi, dan Selling point paling kuat.
2. **Analisis Identitas Produk 10 Aspek (PCS §1):** Baca `01-product-review/product-identity-lock.md` jika sudah ada, atau lengkapi `turbo-15s/product-identity-lock.md` untuk mengunci *English Identity Descriptor* spesifik, *Component Permanence List*, *Product-Specific Anti-Morphing Constraints*, dan *Camera Risk Profile*.

Susun urutan alur fleksibel dari blok berikut (pilih kombinasi terkuat sesuai produk):
- **A. Hook:** Visual unik produk, demonstrasi hasil instan, situasi masalah relevan, atau *close-up* detail memikat.
- **B. Problem & Context:** Tunjukkan singkat masalah harian yang membuat produk dibutuhkan.
- **C. Product Reveal:** Perlihatkan wujud produk utuh dengan komposisi visual tajam.
- **D. Product Demonstration:** Perlihatkan pemakaian nyata langkah demi langkah secara realistis *(atau feature & mechanism showcase pada `Product-Only Mode`)*.
- **E. Product Details:** Sorot material, tekstur, mekanisme, atau detail fitur pembeda.
- **F. Benefits & Lifestyle Proof:** Tonjolkan manfaat melalui hasil nyata di konteks pengguna.
- **G. Closing & CTA:** Tutup dengan *product showcase* bersih dan ruang aman CTA sesuai platform.

---

## 6. Visual Direction & Camera Movement Control (PCS §4)

Patuhi **System 4 — Camera Movement Control** pada [Product Consistency System (PCS v2.0)](../shared/product-consistency-system.md) §4 sebelum menyusun shot dan master prompt:
- Tetapkan **8 parameter kamera** (posisi, sudut, gerakan, arah, intensitas, visibilitas subjek, framing, metode transisi) sesuai **profil risiko kamera produk** (*Simple/Rigid*, *Moderate*, *Complex*).
- **Aturan Inti:** Prioritaskan pergerakan kamera mengelilingi produk yang diam; hindari rotasi produk tidak perlu, perubahan perspektif ekstrem, kamera menembus produk, serta jangan menyembunyikan fitur kritis terlalu lama. **Hindari orbit `360°` penuh** kecuali secara eksplisit dibutuhkan **dan** didukung foto referensi multi-sudut. Tidak ada batas sudut kamera seragam — sesuaikan dengan bentuk produk dan kebutuhan storyboard.
- **Jenis Shot:** `Extreme close-up`, `Macro detail`, `Close-up`, `Medium shot`, `Wide shot`, `POV shot`, `Top-down shot`, `Side angle`, `Product hero shot` *(pada `Product-Only Mode`: Front hero view, Three-quarter view, Side profile, Macro detail, Final hero shot)*.
- **Gerakan Kamera:** `Smooth push-in`, `Pull-out`, `Tracking shot`, `Pan`, `Tilt`, `Dolly movement`, serta gerak konservatif untuk produk *Complex*.
- **Transisi:** `Clean cuts`, `Match cuts`, `Motion cuts`, `Whip transitions`, `Speed ramps` secara terbatas, `Natural action transitions`.

---

## 7. Product Accuracy & Consistency (PCS v2.0 — Prioritas Tertinggi)

- **Otoritas #1 (`01-product-review/references/`) selalu menang.** Jika ada aset di `02-generated-assets/` atau `turbo-15s/upload-assets/`, seluruhnya wajib mengacu pada referensi asli dan *Product Identity Sheet*.
- Terapkan kelima sistem **Product Consistency System (PCS v2.0)**: *Product Identity Lock* (10 aspek spesifik), *Object Permanence Lock* (seluruh komponen terpasang permanen), *Anti-Morphing Lock* (larangan inti + spesifik produk), *Camera Movement Control*, dan *Shot-by-Shot Identity Continuity*.
- Jaga skala produk relatif terhadap tangan/tubuh (pada `Human Demo`) atau terhadap permukaan ruangan (pada `Product-Only Mode`) agar selalu realistis.
- **Dilarang keras** mengubah desain produk demi estetika atau mengarang detail yang tidak didukung bukti produk; detail yang belum pasti wajib ditandai `[PERLU DICEK]` dan memicu status `WARNING` di QC.

---

## 8. Strategi Prompt Video Sekali Jalan & Arsitektur 11 Blok PCS (`1× 15s` Utama + Cadangan `≤ 10s`)

> **Aturan Teknis Generator Video:** Generator video AI **tidak mendukung durasi desimal/koma** (seperti `1.2`, `2.5`, atau `7.5` seconds). Seluruh prompt generasi video **wajib memakai durasi bilangan bulat** (`2`, `3`, `4`, `5`, `6`, `7`, `8`, `10`, atau **`15` seconds** untuk generator yang mendukung output langsung `15` detik).

Agar pengguna bisa langsung membuat video dan storyboard **dalam satu kali jalan**, sediakan struktur berikut di `turbo-15s/turbo-video-prompts.md`, di mana **seluruh prompt video mengikuti Arsitektur 11 Blok PCS v2.0** (`../shared/product-consistency-system.md` §7):

### Mode A (Strategi Utama Direkomendasikan — Sekali Jalan `1×` Generasi Langsung `15` Seconds)
- Sediakan **`1` Master Video Prompt utuh berdurasi bilangan bulat tepat `15` seconds** menggunakan **11 Blok PCS v2.0** (`[1. VIDEO SPECIFICATION]` s.d. `[11. FINAL PRODUCT IDENTITY VERIFICATION]`).
- Lampirkan **`1` lembar storyboard tunggal** (`turbo-15s/upload-assets/storyboard-9panel.png` / `.jpg` atau `storyboard-1sheet.png`) bersama foto `Otoritas #1` sebagai peta visual seluruh alur `0s–15s` dalam satu kali generasi.
- **Wajib *Self-Contained* di dalam Teks Prompt Inggris:** Seluruh *English Identity Descriptor* spesifik (`Otoritas #1`), daftar komponen permanen, koreksi cacat minor gambar storyboard, serta keseragaman latar **wajib dijelaskan lengkap langsung di dalam prompt bahasa Inggris** tanpa menyebut nama file foto lain yang tidak ikut diunggah (`ref-01...jpg`).
- Penempatan jangkar dalam 11 blok PCS:
  - `[1. VIDEO SPECIFICATION]`: `Duration: 15 seconds. Vertical 9:16 commercial affiliate video...`
  - `[2. PRODUCT IDENTITY LOCK]` s.d. `[5. HUMAN MODE]` / `[5. PRODUCT-ONLY MODE]` sesuai `product-identity-lock.md` & `Mode Subjek`.
  - `[6. ENVIRONMENT & CONTINUITY LOCK]`: Memuat kunci latar/cahaya serta **`First-Frame Anchor (0s)`**.
  - `[7. SHOT-BY-SHOT TIMELINE]`: Memuat seluruh shot `0s–15s` dalam **format baris shot PCS §5** (`Shot <n> (<t0>–<t1>, <beat> — <VIEW>): ... Identity: ... Continuity: ... Avoid: ...`) dan ditutup **`Last-Frame Anchor (15s)`** (ruang bawah `28%` bersih untuk CTA).
  - `[8. CAMERA MOVEMENT CONTROL]`, `[9. AUDIO DIRECTION]` (BGM + SFX + VO cue bila dipakai), `[10. NEGATIVE PROMPT]` (anti-morphing spesifik produk + shot negatives + subject-mode negatives), dan `[11. FINAL PRODUCT IDENTITY VERIFICATION]`.
- Jangan mencantumkan kalimat `"Continue the video."` pada Mode A karena merupakan klip tunggal awal-sampai-akhir.

### Mode B (Alternatif Cadangan — Bila Generator Berbatas `≤ 10` Detik atau Ingin Kontrol Trim NLE)
Sediakan kedua sub-opsi cadangan di bawah Mode A agar kampanye tetap dapat dijalankan di generator jenis apa pun:

1. **Mode B1 — Segmentasi Multi-Shot Adaptif `2` atau `3` Klip (`≤ 10` Detik/Klip, Total `15` Seconds):**
   | Pola Strategi | Pembagian Klip (Bilangan Bulat) | Kapan Dipakai |
   |---|---|---|
   | **Pola 2 Klip Seimbang** | **`8s + 7s = 15s`** | Generator maks. `10s`: Klip 1 (`8s`) mengikat *Hook → Reveal → Demo inti*; Klip 2 (`7s`) melanjutkan *Detail → Hasil → Hero Closing*. |
   | **Pola 2 Klip Fokus Demo Panjang** | **`10s + 5s = 15s`** | Jika 1 aksi demonstrasi membutuhkan rentang panjang (`10s`) lalu ditutup *Lifestyle + CTA* (`5s`). |
   | **Pola 3 Babak Simetris** | **`5s + 5s + 5s = 15s`** | Aman di hampir semua generator termasuk model berbatas `5s`, membagi alur menjadi 3 babak seimbang. |
   | **Pola 3 Babak Klimaks Demo** | **`4s + 6s + 5s = 15s`** | Jika *Hook* super-cepat (`4s`), demo utama butuh ruang ekstra (`6s`), lalu *Closing* (`5s`). |
   - **Aturan Kontinuitas & Arsitektur Mode B1:** Setiap klip **wajib memakai 11 Blok PCS lengkap** (`First-Frame Anchor` di Blok 6, `Last-Frame Anchor` di akhir Blok 7), dan baris pertama **Klip 02** / **Klip 03** **wajib diawali tepat dengan `"Continue the video."`** sebelum `[1. VIDEO SPECIFICATION]` (jangan pada Klip 01).
2. **Mode B2 — Prompt Individual per Panel (`2–4` Seconds Bilangan Bulat → Trim Editing ke `15.0` Detik):**
   - Setiap panel (`PANEL 01`–`PANEL <N>`) dibuatkan `1` blok prompt individual berdurasi bilangan bulat (`2`, `3`, atau `4` seconds) dalam **format ringkas 11 label PCS** (1 baris per label `[1. VIDEO SPECIFICATION]` s.d. `[11. FINAL PRODUCT IDENTITY VERIFICATION]`) beserta `Target Panel & Trim Window` untuk *surgical NLE editing*.

---

## 9. Audio, Sound Design & Voice-Over Terukur

- **BGM & SFX:** Pilih musik latar (*BGM*) sesuai karakter produk (`-18 dB` s.d. `-16 dB`), sertai *sound effects* (`SFX`) pada setiap aksi mekanis dan titik potong klip tanpa *audio clipping* (`peak < -1.0 dB`).
- **Voice-Over (VO) Opsional — Ideal untuk Format `15` Detik:**
  - Format `15` detik sangat efektif memakai VO Bahasa Indonesia off-camera bergaya alami lisan (tidak wajib jika produk murni mengandalkan ASMR/visual, namun sangat direkomendasikan bila ada pesan masalah–solusi–manfaat).
  - **Aturan Wajib VO:** **Eja seluruh angka dengan kata** (mis. `"lima warna"`, `"lima belas detik"`), hindari klise AI, dan jaga kepadatan ucap maksimal **`5,0` suku kata/detik** (target ideal untuk `15` detik adalah **`60–68` suku kata** agar terdengar santai di kisaran `4,2–4,5` suku kata/detik).
  - Jika menggunakan VO terstruktur per segmen waktu, sertakan `## Tabel Timing Dialog` pada `turbo-15s/turbo-video-prompts.md` dan verifikasi menggunakan `python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug>/turbo-15s/turbo-video-prompts.md --max-duration 15`.

---

## 10. Text Overlay & CTA (Selaras Hard Integrity Gate HCE)

- **Text Overlay:** Gunakan secara selektif, singkat, tipografi bersih, dan dilarang menutupi bagian penting produk maupun zona UI platform (bagian atas `14%`, kanan `16%`, bawah `28%`).
- **CTA:** Singkat, jujur, natural sesuai platform (`"Cek produknya di keranjang kuning!"`, `"Lihat detail variannya sekarang!"`, `"Cek link di bio!"`).
- **Gerbang Integritas (Wajib):** Dilarang keras mengklaim kelangkaan palsu (*"stok menipis"*, *"sisa 3"*), diskon/promo fiktif, spesifikasi karangan, atau klise AI kosong apabila tidak ada bukti nyata pada data produk.

---

## 11. Storyboard Output Format (12 Field Wajib)

Setiap panel di `turbo-15s/turbo-brief-and-storyboard.md` wajib memuat ke-12 poin berikut:
1. `Panel number` (`PANEL 01`, `PANEL 02`, ...)
2. `Timestamp` (mis. `00:00.0–00:01.2`)
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

Sertakan tabel ringkasan durasi panel yang jumlahnya **tepat `15.0` detik**, pemetaan fase alur (`Babak 1 (0–5s)`, `Babak 2 (5–10s)`, `Babak 3 (10–15s)`), serta **1 prompt gambar storyboard tunggal siap-salin** (`3×3` untuk 9 panel ideal, `2×4`/`4×2` untuk 8 panel, atau `5×2` untuk 10 panel) dengan `[PRODUCT IDENTITY LOCK]` berisi *English Identity Descriptor* spesifik + daftar komponen dari `product-identity-lock.md` agar storyboard dapat langsung dibuat dalam **1 lembar sekali jalan** *(hanya split 2 lembar bila pengguna meminta > 10 panel)*.

---

## 12. Editing & Final Assembly (`1080 × 1920`, Tepat `15` Detik)

Sertakan panduan perakitan editor (`CapCut` / NLE) di `turbo-15s/turbo-video-prompts.md`:
- **Jalur Mode A (`1` klip langsung `15` detik — Sekali Jalan):** Impor 1 klip hasil generasi `15s` ke timeline, pastikan durasi tepat `15.0` detik (`00:00.0–00:15.0`) tanpa frame hitam/jeda, lalu tambahkan sinkronisasi BGM/SFX/VO serta teks overlay + CTA di zona aman dan ekspor.
- **Jalur Mode B1 (`2–3` klip `≤ 10s`):** Susun Klip `01`..`02/03` berurutan, rapikan sambungan antar-klip tepat di *frame anchor* hingga total timeline **tepat `15.0` detik**.
- **Jalur Mode B2 (per panel):** Impor seluruh klip individual lalu *trim* tepat pada puncak aksi setiap panel sesuai timestamp storyboard hingga total timeline **tepat `15.0` detik**.
- Format ekspor akhir: vertikal **`9:16`**, resolusi target **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` / `60 fps`), dan pastikan teks overlay + CTA berada di zona aman (`20%–32%` atas atau `60%–70%` tengah-bawah, bebas tertutup keranjang kuning `28%` bawah).

---

## 13. Quality Control Checklist (Wajib Diverifikasi — Termasuk PCS v2.0)

Sebelum menyelesaikan output `/turbo`, periksa dan isi seluruh kotak cek ini:

**Single-Pass Efficiency, Duration & Clip Strategy**
- [ ] Total durasi storyboard tepat `15.0` detik (`00:00.0–00:15.0`).
- [ ] Storyboard dirancang **1 lembar tunggal** (default `8–10` panel, ideal `9` panel grid `3×3`), tanpa panel `< 0.6` detik tanpa tujuan kreatif jelas.
- [ ] Mode A menyediakan **1 Master Prompt langsung `15` seconds** berarsitektur `11` blok PCS untuk sekali jalan, dan Mode B (B1 `2–3` klip `≤ 10s` + B2 per panel) memakai **bilangan bulat tanpa koma/desimal** serta Klip `02+` B1 diawali `"Continue the video."`.

**Storytelling & Pacing**
- [ ] Hook menarik di detik `00:00–00:01.2`.
- [ ] Masalah/konteks, reveal produk, demonstrasi nyata, detail kunci, dan bukti manfaat tersusun mengalir tanpa filler.
- [ ] Ritme hidup, tidak lambat dan tidak terburu-buru; tidak ada adegan demonstrasi penting yang terpotong sebelum selesai.
- [ ] Ending memiliki showcase/CTA jujur yang jelas dan bebas klaim palsu.

**Audio**
- [ ] Musik sesuai karakter produk, SFX tersinkronisasi dengan cut/gerakan, bebas *clipping*, dan VO opsional (bila dipakai) terukur `≤ 5,0` suku kata/detik dengan angka dieja kata.

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

## 14. Execution Workflow (`/turbo`)

Jalankan langkah berikut secara berurutan dan otonom saat pengguna memanggil `/turbo`:
- **STEP 1 — Terima, Analisis Produk & Deteksi Mode Subjek:** Kumpulkan foto/referensi/deskripsi (`01-product-review/references/` atau input chat), deteksi `Product-Only Mode` bila diminta pengguna (`product-only` / *"tanpa manusia"*; default `Human Demo`), panggil HCE (`hce_bridge.py search`) bila perlu, dan lengkapi 9 poin analisis berbasis bukti.
- **STEP 1B — Susun / Baca Product Identity Sheet (PCS §1):** Jika `01-product-review/product-identity-lock.md` sudah ada, baca sebagai acuan otoritatif; jika belum ada, lengkapi seluruh `10` aspek, daftar komponen, *English Identity Descriptor*, *Product-Specific Anti-Morphing Constraints*, dan *Camera Risk Profile* ke `turbo-15s/product-identity-lock.md` (tandai `[PERLU DICEK]` bila ada detail tak terlihat — jangan dikarang).
- **STEP 2 — Identifikasi Selling Point & Angle `15` Detik:** Tentukan sudut cerita terkuat (Hook + Konteks/Masalah + Reveal + Demo Inti + Bukti Detail/Hasil + CTA) yang memanfaatkan penuh rentang `15` detik.
- **STEP 3 — Tentukan Konsep Kreatif, VO Opsional & Parameter Kamera:** Tetapkan kunci identitas dari sheet, *Continuity Anchors* sesuai `Mode Subjek`, 8 parameter kamera sesuai *Camera Risk Profile* (PCS §4), arahan audio/BGM (+ draf VO `60–68` suku kata bila dipakai), teks overlay zona aman, serta siapkan rancangan `1` video langsung `15` seconds (+ opsi cadangan Mode B `≤ 10s`).
- **STEP 4 — Tentukan Jumlah Panel untuk `1` Lembar Tunggal:** Pilih `8–10` panel adaptif (ideal **`9` panel grid `3×3`**) agar seluruh visual termuat tajam dalam **1 lembar storyboard tunggal** *(kecuali jika pengguna meminta > 10 panel)*.
- **STEP 5 — Susun Storyboard & Buat `1` Lembar Gambar Storyboard:** Tulis lengkap 12 field per panel + tabel verifikasi total tepat `15.0` detik + **1 prompt gambar storyboard tunggal** (memuat *English Identity Descriptor* + daftar komponen) mengikuti [Template Turbo Storyboard](assets/templates/turbo-storyboard.md) ke `./campaigns/<slug>/turbo-15s/turbo-brief-and-storyboard.md`, lalu generate & audit visual `1` lembar storyboard ke `turbo-15s/upload-assets/`.
- **STEP 6 — Susun Video Generation Prompts (11 Blok PCS: Mode A `15s` + Mode B Cadangan):** Tulis Mode A (`1` Master Prompt langsung `15` seconds berarsitektur 11 blok PCS) dan Mode B (`B1` segmentasi `2–3` klip `≤ 10s` dengan `"Continue the video."` di Klip `02+` + 11 blok PCS, serta `B2` prompt per panel bilangan bulat format ringkas 11 label PCS) mengikuti [Template Turbo Video Prompts](assets/templates/turbo-video-prompts.md) ke `./campaigns/<slug>/turbo-15s/turbo-video-prompts.md`.
- **STEP 7 — Susun Panduan Editing Assembly, Audio/SFX/VO & Teks CTA:** Lengkapi instruksi perakitan `1080 × 1920` tepat `15.0` detik (utamakan jalur Mode A `1×` klip), verifikasi `dialogue_timing.py --max-duration 15` (bila ada tabel timing dialog VO), dan zona aman teks overlay.
- **STEP 8 — Jalankan Quality Control (Termasuk PCS v2.0):** Verifikasi seluruh checklist dan pastikan status QC PCS bukan `FAIL`.
- **STEP 9 — Simpan Tanpa Merusak Alur Utama:** Pastikan dokumen `turbo-15s/` tersimpan rapi, catat `modes.turbo_15s` di `campaign.json` (termasuk `"subject_mode": "human-demo" | "product-only"`) tanpa mengubah `stages.*` maupun `modes.rapid_10s` yang sudah ada, lalu laporkan ringkas kepada pengguna.
