# Video Generation Prompt <NN> — <Nama Produk>

- **File:** `04-video/video-<NN>.md`
- **Mode Subjek:** `<Human Demo | Product-Only>`
- **Durasi Klip:** `<durasi>` detik *(maks. `10` detik bilangan bulat, kecuali generator terpilih secara eksplisit mendukung lebih)*
- **Rasio Aspek:** `9:16`
- **Panel Storyboard Dicakup:** `Adegan <X>` *(atau `Adegan <X–Y>` bila menggabungkan beberapa shot)*
- **Rentang Timestamp Storyboard:** `<00:00–00:08>`

## 1. Gambar Referensi Wajib Dilampirkan

> **Folder Siap Upload:** Seluruh foto acuan sudah disatukan ke `04-video/upload-assets/` dengan nama berurutan `1.<ext>..N.<ext>` dan `storyboard.png` *(atau `storyboard-sheet-*.png`)* agar mudah dicari saat mengunggah. (`01-product-review/references/` tetap menjadi **Otoritas #1 (`product-reference`)** untuk kebenaran fisik produk.)

1. `04-video/upload-assets/<X>.<ext>` *(jangkar Adegan `<X>` dari `02-generated-assets/...`)* — **Otoritas #2/#3/#4**: acuan visual awal segmen, tangan/subjek, dan latar.
2. `04-video/upload-assets/<Y>.<ext>` *(jangkar panel berikutnya di klip ini, jika ada)* — **Otoritas #2/#3/#4**: acuan shot lanjutan di dalam klip.
3. `04-video/upload-assets/storyboard.png` *(atau `storyboard-sheet-01.png`)* — **Otoritas #5 (`storyboard`)**: acuan komposisi frame dan urutan gerak panel `<X–Y>`.
4. `01-product-review/references/...` — **Otoritas #1 (`product-reference`)**: acuan mutlak bentuk, warna, material, dan proporsi produk.

## 2. Instruksi Kepatuhan Storyboard & Kunci Konsistensi

- **Strict Storyboard Adherence:** Follow panels `<X–Y>` of the approved storyboard exactly in framing, variable shot durations, action order, camera choreography, and marketing rhythm without inventing off-script scenes.
- **Product Identity Sheet (PCS v2.0):** `01-product-review/product-identity-lock.md` *(English Identity Descriptor, Component Permanence List, Anti-Morphing Constraints, & Camera Risk Profile wajib diterapkan penuh)*
- **Mode Subjek:** `<Human Demo | Product-Only>` *(PCS §6)*
- **First-Frame Anchor (`0.0s`):** `<Exact starting pose of product, hand/no-hand, camera angle, and lighting matching the previous clip's hand-off or opening hook.>`
- **Hand / Character Consistency Lock:** `<Untuk Human Demo: tangan dewasa Indonesia konsisten, kuku bersih, lengan baju konsisten, tanpa wajah | Untuk Product-Only: tanpa manusia/tangan sama sekali.>`
- **Environment & Lighting Lock:** `<Ruangan, permukaan, arah cahaya alami, dan suhu warna konsisten.>`

## 3. Master Video Prompt (Copy-Ready English — Arsitektur 11 Blok PCS v2.0)

```text
Continue the video. *(wajib dicantumkan untuk Klip 2, 3, 4, dst. tepat sebelum [1. VIDEO SPECIFICATION]; hapus baris ini pada Klip 1)*
[1. VIDEO SPECIFICATION]
Duration: <durasi> seconds. Vertical 9:16 commercial affiliate video covering panels <X-Y> of the approved storyboard.

[2. PRODUCT IDENTITY LOCK]
<Paste the exact specific English Identity Descriptor from 01-product-review/product-identity-lock.md — never a generic category phrase.>

[3. OBJECT PERMANENCE LOCK]
- The product must remain the same physical object throughout the entire video.
- All original components must remain attached in their correct positions: <explicit component and quantity list from product-identity-lock.md>.
- No component may disappear, detach, duplicate or spontaneously appear.
- Product geometry must remain consistent between frames and shots.
- Camera movement must not cause the AI to reinterpret the product as a different object.
- All distinctive visual anchors must remain consistent: <anchor list>.
- A feature that becomes less visible due to perspective must still physically exist.
- Moving/detachable parts (<list or "none">): only change state when explicitly instructed in the timeline (<shot ref or "none">).

[4. ANTI-MORPHING LOCK]
Core constraints: No product morphing, no geometry changes, no product replacement, no disappearing components, no duplicated components, no color shifting, no texture transformation, no material substitution, no logo distortion, no spontaneous redesign, no melting or deformation, no inconsistent product proportions, no unexplained structural changes.
Product-specific constraints: <Paste product-specific anti-morphing lines from 01-product-review/product-identity-lock.md.>

[5. HUMAN MODE]
Consistent Indonesian adult hands only (natural sawo matang skin, clean short nails, consistent neutral sleeve), no face visible unless explicitly requested. Hand-to-product contact must be physically plausible with honest real-world scale. Hands must never permanently obscure distinctive product anchors or key components.
*(If Mode Subjek is Product-Only, replace Block 5 above with:
[5. PRODUCT-ONLY MODE]
Product is the sole subject in every shot. Strictly NO humans, NO babies, NO children, NO hands, NO arms, NO legs, NO body parts, NO human reflections or silhouettes, and NO human interaction.)*

[6. ENVIRONMENT & CONTINUITY LOCK]
<Consistent natural directional daylight, household textures, safe framing within center 20%-68% vertical zone.>
First-Frame Anchor (0.0s): <Describe exact opening composition, product position, hand/no-hand placement, and camera placement.>

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (0s-Xs, Adegan <X> — <VIEW>): <Action and physical movement>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; <view-specific instruction>. Continuity: <opening match / previous clip hand-off>. Avoid: <shot-relevant negatives>.
- Shot 2 (Xs-Ys, Adegan <X+1> — <VIEW>): <Action and physical movement>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact physical product; visible components: <list>; anchors: <list>; <view-specific instruction>. Continuity: <match Shot 1>. Avoid: <shot-relevant negatives>.
Last-Frame Anchor (<durasi>s): <Exact ending pose, lighting, and motion bridging cleanly into next clip or clean CTA hold leaving bottom 28% uncluttered.>

[8. CAMERA MOVEMENT CONTROL]
Risk profile: <Simple/Rigid | Moderate | Complex>. Move the camera smoothly around a stationary product; avoid needless product rotation, extreme perspective changes, full 360-degree orbit, or camera passing through the product; keep the product centered and critical features recognizable.

[9. AUDIO DIRECTION]
Off-camera natural Indonesian reviewer voice-over synchronized to the dialogue timing table, realistic product action SFX, balanced BGM with zero clipping.

[10. NEGATIVE PROMPT]
<Product-specific anti-morphing constraints>, <shot-relevant negatives>, <Human Demo: no visible human face, no talking head, no extra fingers | Product-Only Mode: no humans, no babies, no children, no hands, no arms, no legs, no body parts, no human reflections or silhouettes>, no aimless zoom or spinning 360 orbit, no burned-in text, no marketplace UI, no watermarks.

[11. FINAL PRODUCT IDENTITY VERIFICATION]
Verify across the entire clip that the rendered product remains 100% identical to the original reference photos in exact geometry, proportions, colors, surface textures, logo/label, and component count (<summary of locked components and anchors>), with zero morphing or missing parts.
```

## 4. Arahan Audio & Dialog VO Bahasa Indonesia

- **Profil Pembicara:** Pengulas *off-camera*, tidak terlihat di kamera, suara Bahasa Indonesia natural, artikulasi jelas, ekspresif dan persuasif.
- **Segmen Dialog & SFX:**
  - `<00:00–00:02>` *(Adegan X — nada <emosi>)*: `"..."` | SFX: `<suara alami produk>`
  - *(Untuk panel singkat `1–2` dtk tanpa narasi, tulis `[jeda]` dan andalkan SFX produk yang kuat.)*

## 5. Hand-Off Kontinuitas ke Klip Berikutnya

- **Kondisi Frame Terakhir (`Last-Frame Anchor`):** <Posisi pasti produk, tangan/subjek, arah gerak, dan pencahayaan pada detik akhir klip ini.>
- **Arahan Penyambungan ke `video-<NN+1>.md`:** <Instruksi sambungan gerak, posisi kamera, dan kesinambungan cahaya untuk klip berikutnya — atau tandai sebagai akhir video dengan zona aman CTA.>

## 6. Quality Control Konsistensi Produk (PCS v2.0)

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

**Status QC Konsistensi Produk (PCS v2.0):** `<PASS | WARNING (<daftar item [PERLU DICEK]>) | FAIL (<daftar kegagalan>)>`

## Tabel Timing Dialog

| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |
|---|---|---|---|---|---|---|
| <X> | 00:00–00:02 | 2 | "..." | 0 | 0.00 | OK |
