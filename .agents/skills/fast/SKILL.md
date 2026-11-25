---
name: fast
description: "Affiliate Video Director /fast — mode Rapid Affiliate Review tepat 10 detik (9:16) dengan dua varian: Clear (4–6 panel, default untuk produk fungsional) dan Hype (7–8 panel, untuk produk estetik), pemilihan varian otomatis, struktur 4 babak, panel detik bilangan bulat, dan SATU master prompt video 10 detik (tanpa prompt per scene). Gunakan saat pengguna menjalankan /fast, /fast clear, /fast hype, atau meminta video affiliate cepat 10 detik."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.1.0"
  project: affiliate-video-director
  mode: rapid-affiliate-review
---

# /fast — Rapid Affiliate Review (Tepat 10 Detik)

Berperanlah sebagai **Rapid Commercial Affiliate Director & Short-Form Video Editor**. Tugasmu adalah mengaktifkan mode **Rapid Affiliate Review (v1.1)** di dalam ekosistem **Affiliate Video Director** untuk menghasilkan konsep, storyboard presisi **tepat 10 detik (`9:16`)** berbasis varian **Clear/Hype** dengan **detik bilangan bulat**, **1 master prompt video AI berdurasi tepat 10 detik (tanpa prompt per scene)**, panduan editing assembly, serta daftar periksa *quality control*.

**Input Argumen:** `$ARGUMENTS` (berisi kata kunci varian opsional `clear` atau `hype`, slug kampanye, nama produk, foto/screenshot listing, deskripsi, atau tautan yang diberikan pengguna). Jika argumen kosong, cek kampanye aktif di `./campaigns/` atau minta pengguna mengirimkan foto/deskripsi produk.

---

## 1. Peran, Integrasi & Batas Non-Destruktif

- **Bukan Sistem Terpisah:** `/fast` adalah mode pengatur strategi kreatif, storyboard, pacing, durasi (`10` detik), dan struktur video cepat di dalam **Affiliate Video Director** yang memanfaatkan penuh pengetahuan bersama dan gerbang integritas **HCE** (`python .agents/skills/shared/scripts/hce_bridge.py search ...`).
- **Jaga Alur Utama Tetap Utuh:** Jangan pernah menduplikasi, menimpa, atau merusak dokumen alur utama (`/review`, `/storyboard`, `/video`), `/turbo`, foto asli di `01-product-review/references/`, maupun gambar di `02-generated-assets/`.
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

## 2. Varian, Cara Pemanggilan & Primary Objective

### Cara Pemanggilan & Pemilihan Varian

| Perintah | Perilaku Varian | Target Panel |
|---|---|---|
| `/fast <produk/foto/link/slug>` | **Otomatis:** AI memilih `Clear` atau `Hype` sesuai jenis produk | Mengikuti varian terpilih |
| `/fast clear <produk/foto/link/slug>` | Paksa **Fast Clear** (fokus fungsi & kejelasan demo) | `4–6` panel (ideal `5`) |
| `/fast hype <produk/foto/link/slug>` | Paksa **Fast Hype** (fokus daya tarik visual & ritme cepat) | `7–8` panel (maks. `8`) |

**Aturan Parsing & Pemilihan Otomatis:**
- Jika token pertama pada `$ARGUMENTS` adalah `clear` atau `hype` (*case-insensitive*), paksa varian tersebut dan gunakan sisa argumen sebagai identitas produk/slug.
- Jika tidak ada kata kunci varian, tentukan secara otomatis:
  - **Produk fungsional** (alat dapur, gadget, alat kebersihan, *organizer*, perkakas, *holder*, perlengkapan rumah tangga) → **`Clear`**.
  - **Produk estetik / visual** (fashion, aksesori, dekorasi, kemasan kosmetik/bulu mata, produk *unboxing-worthy*) → **`Hype`**.
  - **Jika ragu atau campuran** → **`Clear`** *(default paling aman untuk konversi)*.
- Catat varian terpilih beserta alasan satu baris di bagian header `rapid-10s/rapid-brief-and-storyboard.md`, misalnya:
  `Varian: Clear (otomatis — produk fungsional)`.

### Primary Objective (Sasaran Video 10 Detik)

Buat video affiliate vertikal `9:16` berdurasi **tepat `10` detik** dengan pendekatan *4-beat storytelling*, *purposeful cuts*, *product-focused cinematography*, *short-form conversion marketing*, dan *engaging product demonstration* yang mampu:
1. Menarik perhatian sejak detik pertama (`00:00–00:01`).
2. Memperkenalkan produk dan `1` *selling point* utama secara jernih.
3. Menunjukkan fungsi dan cara penggunaan produk secara nyata tanpa terpotong.
4. Membuktikan manfaat melalui demonstrasi visual (bukan sekadar teks).
5. Membangun keinginan membeli lewat kesinambungan visual yang nyaman dicerna.
6. Mengakhiri video dengan *hero showcase* tertahan dan CTA jujur yang terbaca jelas.

**Prinsip Inti:** Setiap detik wajib bernilai pemasaran. Jangan memecah adegan hanya demi terlihat sibuk; prioritaskan kejelasan konversi daripada banyaknya potongan.

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

## 5. Storyboard Intelligence, 4 Babak Wajib & Kesinambungan

Sebelum menyusun panel, lakukan analisis produk berbasis bukti (`[TERVERIFIKASI]`, `[ASUMSI]`, `[PERLU DICEK]`) untuk 9 aspek wajib:
1. **Kategori produk**
2. **Fungsi utama**
3. **Keunggulan produk**
4. **Target konsumen** *(tandai hipotesis bila belum disediakan pengguna)*
5. **Masalah yang dapat diselesaikan**
6. **Cara penggunaan**
7. **Detail visual yang menarik**
8. **Potensi demonstrasi**
9. **Selling point paling kuat** *(pilih tepat `1` selling point utama untuk video `10` detik ini)*

### Struktur 4 Babak Wajib (Kedua Varian)
Seluruh video `10` detik wajib mengikuti tulang punggung **4 babak** berikut — panel storyboard adalah potongan (*cuts*) di dalam keempat babak ini:
1. **Babak 1 — Hook:** Visual mencolok, situasi masalah relevan, atau hasil instan untuk menghentikan *scrolling*.
2. **Babak 2 — Demo (`≥ 2` dtk):** Pemakaian nyata produk dalam satu aksi utuh yang jelas dan realistis.
3. **Babak 3 — Hasil / Manfaat:** Bukti visual perubahan, detail material, atau keunggulan yang dihasilkan produk.
4. **Babak 4 — Hero + CTA (`≥ 2` dtk):** Tampilan *product hero showcase* yang bersih dan stabil dengan ruang aman untuk CTA.

Blok kreatif berikut dapat dipakai sebagai pengisi di dalam 4 babak sesuai kebutuhan produk:
- **A. Hook** · **B. Product Reveal** · **C. Problem & Solution** · **D. Product Demonstration** · **E. Benefits** · **F. Product Details** · **G. Closing**

### Kunci Kesinambungan & Fokus Pesan
- **Continuity Anchors (Wajib Konsisten di Semua Panel):** Gunakan tangan dan lengan baju yang sama, latar ruangan yang sama, arah pencahayaan yang konsisten, serta **jaga posisi produk selalu di zona tengah layar** pada setiap panel agar perpindahan shot terasa sebagai satu alur utuh.
- **Satu Video, Satu Selling Point:** Fokuskan seluruh panel pada `1` pesan jualan terkuat agar penonton langsung paham dalam `10` detik.

---

## 6. Visual Direction

Variasikan pendekatan visual secara terarah (pilih hanya teknik yang menaikkan kejelasan dan kualitas, jangan memaksakan semua teknik sekaligus):
- **Jenis Shot:** `Extreme close-up`, `Macro detail`, `Close-up`, `Medium shot`, `Wide shot`, `POV shot`, `Top-down shot`, `Side angle`, `Product hero shot`.
- **Gerakan Kamera:** `Smooth push-in`, `Pull-out`, `Tracking shot`, `Pan`, `Tilt`, `Controlled purposeful orbit` *(hanya bila memperlihatkan sisi 3D nyata dengan tujuan jelas)*, `Dolly movement`, `Handheld movement` (bila cocok).
- **Transisi:** `Clean cuts`, `Match cuts`, `Motion cuts`, `Whip transitions`, `Natural action transitions`.

---

## 7. Product Accuracy & Consistency (Prioritas Tertinggi)

- **Otoritas #1 (`01-product-review/references/`) selalu menang.** Jika ada aset di `02-generated-assets/`, wajib mengacu pada referensi asli.
- Pertahankan identitas visual identik di seluruh panel: **bentuk, proporsi & dimensi, warna, material, tekstur, logo, jumlah komponen, detail desain, serta fitur produk**.
- Jaga skala produk relatif terhadap tangan, tubuh, dan lingkungan agar selalu realistis.
- **Dilarang keras** mengubah desain produk demi estetika atau mengarang spesifikasi, fitur, maupun manfaat yang tidak didukung bukti produk.

---

## 8. Audio & Sound Design

- Pilih musik latar (*BGM*) yang sesuai karakter produk dan aman hak cipta.
- Gunakan *sound effects* (`SFX`) pada momen aksi dan titik pergantian shot untuk mempertegas ritme *cuts*.
- Hindari audio terlalu ramai atau *clipping*; utamakan suara yang memperjelas fungsi produk.
- **Voice-Over (VO) bersifat opsional:** gunakan hanya bila benar-benar memperkuat pesan. Jika memakai VO Bahasa Indonesia, jaga agar terdengar natural lisan, **eja angka dengan kata**, dan pastikan durasi ucap pas (maks. `5` suku kata/detik pada durasi segmen terkait atau kalimat singkat `10` detik yang menyatu).

---

## 9. Text Overlay & CTA (Selaras Hard Integrity Gate HCE)

- **Text Overlay Maksimal `2` Pergantian:** Dalam durasi `10` detik, teks overlay hanya boleh berganti paling banyak **`2` kali** (`1` teks manfaat utama + `1` teks CTA penutup). Gunakan tipografi jelas dan jangan menutupi produk maupun zona UI platform (atas `14%`, kanan `16%`, bawah `28%`).
- **CTA:** Singkat, natural, sesuai konteks platform (mis. `"Cek produknya sekarang!"`, `"Lihat detailnya!"`, `"Cek di keranjang kuning!"`, `"Cek link di bio!"`).
- **Gerbang Integritas (Wajib):** Dilarang keras mengklaim kelangkaan palsu (*"stok menipis"*, *"sisa 3"*), diskon/promo fiktif, atau klise AI kosong (*"Wajib banget!"* tanpa alasan produk yang valid) apabila tidak ada bukti nyata pada data produk.

---

## 10. Storyboard Output Format (12 Field Wajib)

Setiap panel di `rapid-10s/rapid-brief-and-storyboard.md` wajib memuat ke-12 poin berikut dengan **timestamp dan durasi bilangan bulat**:
1. `Panel number` (`PANEL 01`, `PANEL 02`, ...)
2. `Timestamp` (bilangan bulat, mis. `00:00–00:01`)
3. `Durasi klip` (`Duration`, bilangan bulat `≥ 1` detik)
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
Timestamp: 00:00–00:01
Duration: 1 second
Scene: Attention-grabbing product hook (Babak 1 — Hook).
Visual: Close-up produk di zona tengah 20%–65% dengan latar rumah Indonesia rapi.
Camera angle: Eye-level tight close-up.
Camera movement: Smooth push-in.
Action: Produk diangkat atau diperlihatkan pada situasi masalah untuk memicu rasa ingin tahu.
Lighting: Cahaya pagi alami lembut dari jendela samping.
Transition: Clean cut.
Objective: Menghentikan scrolling penonton di 1 detik pertama.
Audio / SFX: Beat pembuka bersih + whoosh halus tersinkronisasi.
```

Sertakan tabel ringkasan durasi panel yang mencantumkan kolom `Babak` dan jumlah durasi **tepat `10` detik**, serta prompt gambar storyboard siap-salin **selalu dalam `1` lembar tunggal** (*single sheet*):
- **Varian Clear:** Grid `2×3` (atau `1×4` / `2×2` bila `4` panel).
- **Varian Hype:** Grid `2×4`.

---

## 11. Video Generation Prompt — 1 Master Prompt 10 Detik (Tanpa Prompt per Scene)

> **Aturan Mutlak Master Prompt:** Mode `/fast` hanya menghasilkan **1 (SATU) Master Prompt video berdurasi bilangan bulat tepat `10 seconds`** di `rapid-10s/rapid-video-prompts.md`. **Dilarang keras membuat prompt terpisah per panel/scene** ataupun memecah video menjadi beberapa klip generasi.

Prompt video wajib berbahasa Inggris, dimulai dengan `Duration: 10 seconds. Vertical 9:16 ...`, dan memuat seluruh blok berikut:
- `[PRODUCT IDENTITY LOCK]`: Kunci bentuk, proporsi, warna, material, tekstur, logo, dan jumlah komponen identik dengan referensi asli (`01-product-review/references/`).
- `[HAND & ENVIRONMENT LOCK]`: Kunci kesinambungan tangan/lengan baju, latar ruangan, arah pencahayaan, dan posisi produk di zona tengah layar di seluruh shot.
- `[SHOT TIMELINE (0s–10s)]`: Daftar 1 baris per panel storyboard memakai **timestamp bilangan bulat yang sama persis** (`Shot 1 (0s–1s, Hook): ...` hingga `Final Shot (8s–10s, Hero + CTA): ...` dengan `28%` area bawah layar tetap bersih tanpa objek mengganggu untuk ruang CTA).
- `[CAMERA & TRANSITION STYLE]`: Gaya sinematografi komersial dan transisi bersih antar-shot.
- `[AUDIO]`: Arahan BGM & titik SFX per shot; sertakan VO Bahasa Indonesia opsional hanya bila perlu (eja angka dengan kata, maks. `5` suku kata/detik).
- `[NEGATIVE / AVOID]`: Larangan deformasi produk, pergeseran warna/logo, tangan/jari berlebih, teks terbakar, dan watermark.

Sertakan catatan 1 baris di `rapid-10s/rapid-video-prompts.md`: *"Jika generator video belum mendukung durasi `10` detik sekaligus, gunakan generator yang mendukung generasi `10` detik dalam satu kali proses (jangan memecah prompt per scene)."*

---

## 12. Editing & Final Assembly (`1080 × 1920`, Tepat `10` Detik)

Sertakan panduan perakitan editor (`CapCut` / NLE) di `rapid-10s/rapid-video-prompts.md`:
- Impor **1 klip hasil generasi `10` detik** dan pastikan durasi timeline tepat `10` detik (`00:00–00:10`), format vertikal **`9:16`**, resolusi **`1080 × 1920`**, *frame rate* konsisten (mis. `30 fps` / `60 fps`), tanpa jeda kosong/frame hitam.
- Jika durasi klip hasil generate sedikit melebihi `10` detik, lakukan *trim* **hanya di bagian akhir** (*tanpa* pemotongan atau perakitan per panel).
- Tambahkan BGM dan sinkronkan *SFX* tepat pada titik pergantian shot sesuai timeline storyboard.
- Tempatkan maksimal `2` pergantian teks overlay + CTA di zona aman (`20%–32%` atas atau `60%–70%` tengah-bawah, bebas tertutup keranjang kuning `28%` bawah).

---

## 13. Quality Control Checklist (Wajib Diverifikasi)

Sebelum menyelesaikan output `/fast`, periksa dan isi seluruh kotak cek ini:

**Duration & Prompt**
- [ ] Total durasi storyboard tepat `10` detik (`00:00–00:10`) dengan semua panel memakai **detik bilangan bulat** (`≥ 1` detik).
- [ ] Jumlah panel sesuai varian terpilih (**Clear:** `4–6` panel; **Hype:** `7–8` panel).
- [ ] `rapid-video-prompts.md` hanya berisi **tepat `1` master prompt `10` detik** dan **tidak ada prompt terpisah per scene/panel**.

**Storytelling & Pacing**
- [ ] Mengikuti struktur **4 babak** (`Hook → Demo → Hasil/Manfaat → Hero + CTA`) dengan fokus pada `1` *selling point* utama.
- [ ] Hook kuat pada detik `00:00–00:01` dan produk langsung terbaca jelas.
- [ ] Panel **Demo berdurasi `≥ 2` detik** dalam satu aksi utuh tanpa terpotong sebelum selesai.
- [ ] Panel penutup **Hero + CTA ditahan `≥ 2` detik** dengan ruang aman CTA bersih dan jujur.
- [ ] Pergantian teks overlay maksimal `2` kali dan tidak ada pergantian shot yang membingungkan.

**Visual & Continuity**
- [ ] Produk 100% konsisten dengan referensi asli (`references/`), tanpa deformasi.
- [ ] Continuity anchors terjaga (tangan/lengan baju, latar, cahaya konsisten, produk tetap di zona tengah).
- [ ] Gambar storyboard disusun dalam **1 lembar tunggal** (`2×3`/`1×4`/`2×2` untuk Clear; `2×4` untuk Hype).

**Audio**
- [ ] Musik latar sesuai karakter produk, SFX tersinkronisasi dengan pergantian shot, bebas *audio clipping*.

---

## 14. Execution Workflow (`/fast`)

Jalankan langkah berikut secara berurutan dan otonom saat pengguna memanggil `/fast`:
- **STEP 0 — Tentukan Varian:** Periksa token pertama `$ARGUMENTS` (`clear` atau `hype`); jika tidak ada, pilih otomatis berdasarkan jenis produk (`Clear` untuk produk fungsional / fallback jika ragu, `Hype` untuk produk estetik) dan siapkan alasan satu barisnya.
- **STEP 1 — Terima & Analisis Produk:** Kumpulkan foto/referensi/deskripsi (`01-product-review/references/` atau input chat), panggil HCE (`hce_bridge.py search`) bila perlu, dan lengkapi 9 poin analisis berbasis bukti.
- **STEP 2 — Identifikasi 1 Selling Point Utama:** Tetapkan tepat `1` sudut jualan terkuat yang paling mudah dibuktikan secara visual dalam `10` detik.
- **STEP 3 — Tentukan Konsep & Kunci Kesinambungan:** Tetapkan struktur 4 babak, tangan/lengan konsisten, latar & cahaya konsisten, zona tengah produk, arahan audio/BGM, serta rencana maksimal `2` pergantian teks overlay + CTA aman.
- **STEP 4 — Tentukan Jumlah Panel Sesuai Varian:** Pilih jumlah panel di rentang varian (`Clear`: `4–6` ideal `5`; `Hype`: `7–8` maks. `8`) dengan durasi bilangan bulat (`Demo ≥ 2` dtk, `Hero + CTA ≥ 2` dtk, total tepat `10` dtk).
- **STEP 5 — Susun Storyboard 1 Lembar Tepat 10 Detik:** Tulis varian + alasan di header, tabel timeline berkolom `Babak`, 12 field per panel (timestamp & durasi bilangan bulat), dan `1` prompt gambar storyboard tunggal mengikuti [Template Rapid Storyboard](assets/templates/rapid-storyboard.md) ke `./campaigns/<slug>/rapid-10s/rapid-brief-and-storyboard.md`.
- **STEP 6 — Susun 1 Master Prompt Video 10 Detik:** Tulis **hanya 1 Master Prompt** berbahasa Inggris berdurasi `10 seconds` dengan shot timeline `1:1` mengikuti [Template Rapid Video Prompts](assets/templates/rapid-video-prompts.md) ke `./campaigns/<slug>/rapid-10s/rapid-video-prompts.md` (tanpa prompt per scene).
- **STEP 7 — Susun Panduan Assembly 1 Klip:** Lengkapi instruksi impor 1 klip `10` detik (`1080 × 1920`), trim akhir bila berlebih, sinkronisasi BGM/SFX, dan zona aman teks overlay.
- **STEP 8 — Jalankan Quality Control:** Verifikasi seluruh checklist Duration & Prompt, Storytelling & Pacing, Visual & Continuity, serta Audio.
- **STEP 9 — Simpan Tanpa Merusak Alur Utama:** Pastikan dokumen `rapid-10s/` tersimpan rapi, opsional catat `modes.rapid_10s` di `campaign.json` (sertakan `"variant": "clear"` atau `"hype"`) tanpa mengubah `stages.review` / `stages.storyboard` / `stages.video` yang sudah ada, lalu laporkan ringkas kepada pengguna.
