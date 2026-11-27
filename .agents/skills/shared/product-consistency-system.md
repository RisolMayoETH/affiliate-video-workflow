# Product Consistency System (PCS v2.0) — Standar Global Konsistensi Identitas Produk

Dokumen ini adalah **sumber kebenaran tunggal (*Single Source of Truth*)** untuk menjaga konsistensi identitas fisik produk selama proses generasi gambar dan video AI di seluruh alur kerja **Affiliate Video Director**.

## 0. Ruang Lingkup & Prioritas

- **Berlaku untuk:** `/fast`, `/turbo`, `/video`, serta suplai data identitas dari `/review` dan `/storyboard`.
- **Hierarki Otoritas:** Foto referensi produk asli (`01-product-review/references/`, **Otoritas #1**) selalu mengalahkan gambar hasil generate maupun deskripsi asumsi.
- **Prinsip Utama:** **Prioritaskan konsistensi identitas produk di atas variasi visual yang tidak diperlukan.** Jangan mengorbankan keakuratan bentuk, warna, material, logo, atau komponen demi sudut kamera ekstrem atau efek transisi berlebihan.

---

## 1. SYSTEM 1 — Product Identity Lock

Tujuan: mengunci identitas fisik produk secara spesifik berdasarkan foto referensi asli sebelum prompt gambar maupun prompt video dibuat.

### 10 Aspek Wajib Identifikasi (dengan Tag Fakta)

Setiap aspek wajib ditandai status faktanya (`[TERVERIFIKASI]`, `[ASUMSI]`, atau `[PERLU DICEK]`):

1. **Product category and exact identity** *(kategori & identitas spesifik produk)*
2. **Main body shape and geometry** *(bentuk bodi utama & geometri)*
3. **Original proportions and dimensions when known** *(proporsi asli & dimensi metrik bila diketahui)*
4. **Primary and secondary colors** *(warna utama, warna sekunder, & warna aksen)*
5. **Material and surface texture** *(material & tekstur permukaan: matte/glossy/plush/metal/transparan)*
6. **Components and their exact quantities** *(daftar komponen & jumlah pastinya)*
7. **Distinctive visual anchors** *(penanda visual khas yang menjadi ciri ikonik produk)*
8. **Logo, label, typography and branding** *(letak, bentuk, dan isi logo/label/tipografi)*
9. **Mechanical structures and moving components** *(struktur mekanis, engsel, pengunci, tombol, bagian bergerak)*
10. **Accessories and their relationship to the main product** *(aksesori tambahan & keterhubungannya dengan unit utama)*

### Aturan Penulisan Deskripsi Spesifik vs Generik

Tulis *English Identity Descriptor* yang presisi secara fisik, bukan deskripsi kategori umum:

- **BURUK (Terlalu Generik):** `"Gray elephant baby chair."`
- **BENAR (Spesifik & Terkunci):** `"Gray plush elephant-shaped seat with a rounded padded body, curved backrest, thick armrests, two pink inner ears, two black eyes, a long downward trunk, four small elephant feet and two cream-colored lower front openings."`

### Aturan Ketat Identitas Produk

- **Jangan mengarang** komponen, motif, atau fitur yang tidak terlihat di referensi.
- **Jangan mengganti warna asli** dengan varian warna lain dari listing yang sama.
- **Jangan mengubah desain produk** menjadi versi generik atau versi lain.
- **Jangan menambahkan aksesori** (wadah, kabel, dudukan, gantungan) yang tidak ada pada referensi.
- **Bedakan fakta visual (`[TERVERIFIKASI]`) dari asumsi (`[ASUMSI]` / `[PERLU DICEK]`)**.
- **Gunakan foto produk asli (`01-product-review/references/`) sebagai otoritas utama.**

### Lokasi Product Identity Sheet (`templates/product-identity-lock.md`)

- **`/review` dan `/video`:** Menulis atau membaca `01-product-review/product-identity-lock.md`. *(Jangan menimpa lembar yang sudah `Approved` tanpa mengarsipkannya lebih dulu ke `_archive/`.)*
- **`/fast` dan `/turbo`:** Membaca `01-product-review/product-identity-lock.md` jika sudah ada (bersifat otoritatif). Jika belum ada, tulis salinan lokal ke `rapid-10s/product-identity-lock.md` atau `turbo-15s/product-identity-lock.md` agar isolasi subfolder mode cepat tetap terjaga.

---

## 2. SYSTEM 2 — Object Permanence Lock

Tujuan: memastikan produk diperlakukan sebagai satu objek fisik yang sama dan permanen di sepanjang video.

**Blok Instruksi Wajib (English Copy-Ready):**
```text
- The product must remain the same physical object throughout the entire video.
- All original components must remain attached in their correct positions.
- No component may disappear, detach, duplicate or spontaneously appear.
- Product geometry must remain consistent between frames and shots.
- Camera movement must not cause the AI to reinterpret the product as a different object.
- All distinctive visual anchors must remain consistent.
- A feature that becomes less visible due to perspective must still physically exist.
```

**Ketentuan Tambahan:**
- Untuk produk multikomponen, cantumkan daftar lengkap komponen beserta jumlahnya yang wajib tetap ada sepanjang video.
- Untuk produk yang dapat dibongkar-pasang atau memiliki mekanisme bergerak (tutup flip, pengunci tiang, mangkuk lepas-pasang), perubahan kondisi fisik **hanya boleh terjadi apabila secara eksplisit diperintahkan pada shot tertentu di storyboard** (sebutkan nomor shot-nya secara eksplisit).

---

## 3. SYSTEM 3 — Anti-Morphing Lock

Tujuan: menekan risiko perubahan bentuk, warna, material, atau penggantian objek selama generasi video.

### A. Larangan Inti (Core Anti-Morphing Constraints — Wajib Ada)

```text
No product morphing, no geometry changes, no product replacement, no disappearing components, no duplicated components, no color shifting, no texture transformation, no material substitution, no logo distortion, no spontaneous redesign, no melting or deformation, no inconsistent product proportions, no unexplained structural changes.
```

### B. Larangan Spesifik Produk (Wajib Disesuaikan per Produk)

Dilarang hanya memakai negative prompt generik. Setiap prompt wajib menambahkan larangan spesifik yang diturunkan langsung dari daftar komponen dan *visual anchors* produk (`no missing, detached, duplicated or altered <component>`):

- **Contoh Kursi/Sofa Plush Karakter (mis. Gajah):** `no disappearing or distorted elephant face, trunk, pink inner ears, black eyes, thick armrests, four feet, or two cream-colored lower front openings.`
- **Contoh Blender / Chopper:** `no missing, warped or duplicated blending jar, handle, motor base, control knob, stainless blades, brand logo, or lid accessories.`
- **Contoh Alat Rumah Tangga Kaku (mis. Sikat/Pel Lengkung):** `no straightening of the S-curved neck, no missing oval hanging hole, no collar ring disappearance, no switching handle color, no changing dual-tone bristle arrangement.`
- **Contoh Botol Kosmetik / Skincare:** `no melting or unreadable front brand label typography, no cap color shift, no pump nozzle alteration, no bottle silhouette narrowing or widening.`

---

## 4. SYSTEM 4 — Camera Movement Control

Tujuan: mengendalikan pergerakan kamera agar tidak memicu rekonstruksi produk yang keliru oleh generator AI.

### 8 Parameter Kamera Wajib (Tetapkan Sebelum Menulis Master Prompt)

1. **Camera position** *(posisi kamera terhadap produk)*
2. **Camera angle** *(sudut vertikal/horizontal)*
3. **Camera movement** *(jenis gerakan fisik kamera)*
4. **Movement direction** *(arah gerak: maju, mundur, geser kiri/kanan, naik/turun)*
5. **Movement intensity** *(intensitas: static, subtle, gentle, smooth, moderate)*
6. **Subject visibility** *(bagian produk yang wajib tetap terlihat jelas)*
7. **Product framing** *(skala dan posisi produk di zona tengah `9:16`)*
8. **Transition method** *(clean cut, match cut, natural action transition)*

### Profil Risiko Kamera Produk

| Profil Risiko Produk | Ciri Produk | Gerakan Kamera Aman | Gerakan yang Dihindari |
|---|---|---|---|
| **Simple / Rigid** | Bentuk kaku simetris, sedikit komponen, tanpa label teks rumit | Push-in, pull-out, lateral tracking, *arc* sudut moderat terkontrol | Orbit `360°` penuh tanpa referensi multi-sudut, whip pan ekstrem |
| **Moderate** | Bentuk lengkung/ergonomis, 2–5 komponen, ada sambungan atau tekstur khusus | Controlled push-in/pull-out, steady tracking, tilt perlahan, macro detail | Rotasi produk tidak perlu, perubahan perspektif mendadak |
| **Complex** *(risiko morphing tinggi)* | Bentuk plush/karakter/lunak, banyak komponen, label teks terbaca, permukaan transparan atau reflektif | **Konservatif:** subtle push-in, gentle pull-out, steady lateral slide, static macro detail | Segala bentuk orbit memutar, sudut ekstrem yang menyembunyikan fitur kunci, pergerakan cepat |

### Aturan Wajib Pergerakan Kamera

- **Prioritaskan pergerakan kamera mengelilingi produk yang diam (*stationary product*).**
- **Hindari rotasi produk yang tidak perlu.**
- **Hindari perubahan perspektif yang ekstrem.**
- **Hindari orbit `360°` penuh** kecuali secara eksplisit dibutuhkan **dan** didukung foto referensi multi-sudut.
- **Hindari kamera menembus (*passing through*) produk.**
- **Jaga produk tetap terpusat (*centered*) dan terlihat jelas.**
- Gunakan *controlled push-in*, *pull-out*, *tracking*, *lateral movement*, dan *macro shots*.
- **Jangan gunakan gerakan kamera yang menyembunyikan fitur kritis produk terlalu lama.**
- **Tidak ada batas sudut seragam untuk semua produk:** pilih sudut kamera sesuai geometri produk dan kebutuhan naratif storyboard.

---

## 5. SYSTEM 5 — Shot-by-Shot Identity Continuity

Tujuan: memastikan kunci identitas produk hadir di **setiap shot** pada timeline, bukan hanya di paragraf pembuka master prompt.

### Data Wajib di Setiap Shot
Setiap baris shot di `[7. SHOT-BY-SHOT TIMELINE]` wajib memuat:
- **Product identity reference** *(penegasan masih objek fisik asli yang sama)*
- **Visible product components** *(komponen yang terlihat pada shot tersebut)*
- **Required visual anchors** *(penanda khas yang wajib tampak/terjaga)*
- **Camera angle & movement** *(sudut, gerakan, arah, intensitas)*
- **Product visibility requirement** *(apa yang wajib terbaca jelas)*
- **Continuity requirements** *(kesinambungan dengan shot sebelumnya)*
- **Negative constraints relevant to that shot** *(larangan spesifik untuk sudut/aksi shot itu)*

### Format Baku Baris Shot (Copy-Ready English)

```text
- Shot <n> (<t0>–<t1>, <beat> — <VIEW>): <action/composition>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; <view-specific instruction>. Continuity: <what must match previous shot>. Avoid: <shot-relevant negatives>.
```

### Contoh Instruksi per Sudut Pandang *(Adaptif Sesuai Produk & Storyboard — Jangan Dipakai Kaku)*

- **FRONT VIEW:** `The complete original product must be visible. Preserve all original components and exact geometry.`
- **THREE-QUARTER VIEW:** `Maintain the same exact physical product. All distinctive components remain attached and unchanged. Do not reconstruct or replace the product.`
- **SIDE VIEW:** `Preserve the original geometry and all attached components, including features that are partially hidden by perspective.`
- **MACRO DETAIL:** `Show the exact original material, texture, logo and distinctive product details without inventing new structures.`
- **FINAL HERO:** `Return to a complete and recognizable product composition. All original components must be present.`

---

## 6. Human Mode vs Product-Only Mode

**Aturan Aktivasi:**
- **Default:** **`Human Mode`** *(demonstrasi tangan/subjek Indonesia yang konsisten tetap berjalan seperti biasa)*. **Dilarang mengaktifkan larangan manusia secara otomatis pada seluruh video.**
- **`Product-Only Mode` (Opt-In Khusus):** Aktif **hanya** apabila pengguna meminta secara eksplisit (mis. *"tanpa manusia"*, *"tanpa tangan"*, *"produk saja"*, *"product only"*) atau menyertakan token `product-only` pada argumen perintah (mis. `/fast clear product-only <produk>`, `/turbo product-only <produk>`), atau sesuai instruksi storyboard `/video`.
- Catat mode aktif pada baris metadata **`Mode Subjek: Human Demo | Product-Only`** di file storyboard dan prompt video.

### Blok `[5. HUMAN MODE]` (Default)
```text
[5. HUMAN MODE]
Consistent Indonesian adult hands only (natural sawo matang skin, clean short nails, consistent neutral sleeve), no face visible unless explicitly requested. Hand-to-product contact must be physically plausible with honest real-world scale. Hands must never permanently obscure distinctive product anchors or key components.
```

### Blok `[5. PRODUCT-ONLY MODE]` (Opt-In)
```text
[5. PRODUCT-ONLY MODE]
Product is the sole subject in every shot. Strictly NO humans, NO babies, NO children, NO hands, NO arms, NO legs, NO body parts, NO human reflections or silhouettes, and NO human interaction.
```

**Penyesuaian Saat `Product-Only Mode` Aktif:**
- Gunakan teknik *commercial product showcase*: **Front hero view**, **Three-quarter view**, **Side profile**, **Macro detail**, dan **Final hero shot**.
- Babak *Demo* pada `/fast` atau `/turbo` beralih menjadi *feature & mechanism showcase* (mekanisme nyata produk bekerja atau *camera reveal* tanpa tangan).
- `Continuity Anchors` menghapus spesifikasi tangan/lengan baju dan fokus penuh pada konsistensi produk, permukaan dudukan/meja, ruangan, dan cahaya.
- Aturan **Voice Over (VO)** dan **CTA** tetap berlaku normal tanpa perubahan.

---

## 7. Master Prompt Architecture (11 Blok Baku)

Seluruh master prompt video di `/fast`, `/turbo` (Mode A dan Klip Mode B1), serta `/video` wajib menggunakan **11 label blok berikut secara persis** dalam Bahasa Inggris:

```text
[1. VIDEO SPECIFICATION]
Duration: <N> seconds. Vertical 9:16 commercial affiliate product video. <mode/style summary>.

[2. PRODUCT IDENTITY LOCK]
<Specific English Identity Descriptor from product-identity-lock.md — never a generic category phrase.>

[3. OBJECT PERMANENCE LOCK]
- The product must remain the same physical object throughout the entire video.
- All original components must remain attached in their correct positions: <explicit component + count list>.
- No component may disappear, detach, duplicate or spontaneously appear.
- Product geometry must remain consistent between frames and shots.
- Camera movement must not cause the AI to reinterpret the product as a different object.
- All distinctive visual anchors must remain consistent: <anchor list>.
- A feature that becomes less visible due to perspective must still physically exist.
- Moving/detachable parts (<list or "none">): only change state when explicitly instructed in the storyboard (<shot ref or "none">).

[4. ANTI-MORPHING LOCK]
Core constraints: No product morphing, no geometry changes, no product replacement, no disappearing components, no duplicated components, no color shifting, no texture transformation, no material substitution, no logo distortion, no spontaneous redesign, no melting or deformation, no inconsistent product proportions, no unexplained structural changes.
Product-specific constraints: <mandatory product-specific lines from component & anchor list>.

[5. HUMAN MODE]   (atau [5. PRODUCT-ONLY MODE] sesuai Mode Subjek)
<Exact block from Section 6.>

[6. ENVIRONMENT & CONTINUITY LOCK]
<Consistent setting, surface, directional natural daylight, color temperature, framing zone (middle safe zone), and First-Frame Anchor (0s) when multi-clip.>

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (<t0>–<t1>, <beat> — <VIEW>): <action/composition>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; <view-specific instruction>. Continuity: <match previous>. Avoid: <shot negatives>.
...
- Final Shot (<t_prev>–<N>s, Hero + CTA — FINAL HERO): ... leaving the bottom 28% completely uncluttered for CTA overlay.
<Last-Frame Anchor (<N>s) when multi-clip.>

[8. CAMERA MOVEMENT CONTROL]
Risk profile: <Simple/Rigid | Moderate | Complex>. Move camera around a stationary product; no needless product rotation; no extreme perspective jumps; no full 360-degree orbit; no camera passing through product; keep product centered and key features visible.

[9. AUDIO DIRECTION]
<BGM + synced SFX cues. For /fast: keep no-speech clause so off-screen VO is added cleanly in editing. For /video or /turbo with inline VO cue: follow skill audio rule.>

[10. NEGATIVE PROMPT]
<Combined product-specific anti-morphing constraints + shot negatives + subject-mode negatives (no face / or no humans/hands at all in Product-Only Mode) + no burned-in text, no watermarks, no marketplace UI.>

[11. FINAL PRODUCT IDENTITY VERIFICATION]
Verify from start to finish that the rendered product remains 100% identical to the original reference photos in shape, proportions, colors, material textures, logo/label, and exact component count (<summary of locked anchors>) with zero morphing or missing parts.
```

**Catatan Penting Penerapan:**
- Untuk klip lanjutan (`Klip 02+` pada `/turbo` Mode B1 dan `video-02.md+` pada `/video`), baris pertama di dalam blok kode prompt **wajib tetap `"Continue the video."`** tepat sebelum `[1. VIDEO SPECIFICATION]`.
- `First-Frame Anchor (0s)` ditempatkan di `[6. ENVIRONMENT & CONTINUITY LOCK]`; `Last-Frame Anchor` ditempatkan di akhir `[7. SHOT-BY-SHOT TIMELINE]`.
- Untuk `/turbo` Mode B2 (prompt per panel), tiap blok boleh diringkas menjadi `1` baris padat, namun **ke-11 label blok wajib tetap hadir**.

---

## 8. Quality Control Konsistensi Produk (PCS v2.0)

Setiap finalisasi master prompt wajib memeriksa **5 kelompok cek PCS** berikut:

```markdown
**PRODUCT IDENTITY:**
- [ ] Product shape matches the original reference.
- [ ] Original colors are preserved.
- [ ] Material and texture remain consistent.
- [ ] All original components are accounted for.
- [ ] Logos and distinctive details remain unchanged.

**OBJECT PERMANENCE:**
- [ ] Product remains the same physical object.
- [ ] No components disappear.
- [ ] No components detach unexpectedly.
- [ ] No spontaneous structural changes.

**ANTI-MORPHING:**
- [ ] No product replacement.
- [ ] No geometry changes.
- [ ] No duplicated components.
- [ ] No unexplained color or texture changes.

**CAMERA CONTROL:**
- [ ] Camera movements are appropriate for the product.
- [ ] Critical features remain recognizable.
- [ ] No unnecessary extreme perspective changes.
- [ ] Camera movement does not conflict with product continuity.

**SHOT CONTINUITY:**
- [ ] Every shot includes appropriate identity constraints.
- [ ] Product identity is consistent between shots.
- [ ] Final hero shot matches the original product.
- [ ] Product-only mode follows user instructions.

**Status QC Konsistensi Produk (PCS v2.0):** `PASS` | `WARNING (<daftar item [PERLU DICEK]>)` | `FAIL (<daftar kegagalan>)`
```

**Aturan Status:**
- **`PASS`:** Seluruh `21` butir terpenuhi dan terverifikasi dari foto referensi asli.
- **`WARNING`:** Ada detail identitas produk yang tidak dapat dipastikan dari foto referensi. Sebutkan detail tersebut di status `WARNING`, tandai `[PERLU DICEK]` di *Product Identity Sheet*, dan tulis `"exactly as shown in the reference"` di prompt **tanpa mengarang detail**.
- **`FAIL`:** Ada pelanggaran konsistensi, komponen hilang, atau konflik kamera/mode subjek. **Wajib diperbaiki sebelum output diserahkan ke pengguna** — jangan pernah menyerahkan hasil berstatus `FAIL`.

---

## 9. Peta Integrasi Antar-Skill

| Skill | Peran terhadap PCS v2.0 | Lokasi *Product Identity Sheet* |
|---|---|---|
| `/review` | Mengisi 10 aspek identitas produk & membuat sheet awal | `01-product-review/product-identity-lock.md` |
| `/storyboard` | Memvalidasi aset gambar terhadap komponen & *anchors* sheet | Membaca `01-product-review/product-identity-lock.md` |
| `/video` | Memakai arsitektur `11` blok + PCS QC pada setiap `video-NN.md` | Membaca (atau melengkapi) `01-product-review/product-identity-lock.md` |
| `/fast` | Memakai arsitektur `11` blok pada 1 master prompt `10s` + PCS QC + `Product-Only Mode` | Membaca `01-product-review/product-identity-lock.md` bila ada; jika tidak ada, menulis `rapid-10s/product-identity-lock.md` |
| `/turbo` | Memakai arsitektur `11` blok pada Mode A `15s` & Mode B + PCS QC + `Product-Only Mode` | Membaca `01-product-review/product-identity-lock.md` bila ada; jika tidak ada, menulis `turbo-15s/product-identity-lock.md` |
