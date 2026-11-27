# Rapid Video Prompt, QC & Voice Over (10s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Rapid Affiliate Review v1.3` (`/fast`)
- **Varian:** `<Clear | Hype>` (`<N>` panel)
- **Mode Subjek:** `<Human Demo | Product-Only>`
- **Product Identity Sheet (PCS v2.0):** `<01-product-review/product-identity-lock.md | rapid-10s/product-identity-lock.md>`
- **Acuan Storyboard:** `rapid-10s/rapid-brief-and-storyboard.md`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`10` detik**
- **Aturan Generator Video:** Hanya **1 Master Prompt berdurasi bilangan bulat tepat `10 seconds`** mengikuti **11 Blok PCS v2.0**, tanpa prompt terpisah per scene/panel.

---

## 5. Master Prompt Video (10 Detik)

> **Catatan:** Mode `/fast` hanya menyediakan **1 Master Prompt** agar seluruh timeline `10` detik digenerasi dalam satu alur yang konsisten. Jika generator video belum mendukung durasi `10` detik sekaligus, gunakan generator yang mendukung generasi `10` detik dalam satu kali proses (jangan memecah prompt per scene).

- **Durasi Generasi AI:** `10` seconds *(bilangan bulat tepat)*
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<lembar storyboard tunggal / aset jangkar bila tersedia>`
- **Copy-Ready Master Prompt (English):**
```text
[1. VIDEO SPECIFICATION]
Duration: 10 seconds. Vertical 9:16 commercial affiliate product video following a clear 4-beat structure (Hook -> Demo -> Result/Benefit -> Hero + CTA).

[2. PRODUCT IDENTITY LOCK]
<Paste the exact specific English Identity Descriptor from product-identity-lock.md — never a generic category description.>

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
Product-specific constraints: <Paste product-specific anti-morphing lines from product-identity-lock.md.>

[5. HUMAN MODE]
Consistent Indonesian adult hands only (natural sawo matang skin, clean short nails, consistent neutral sleeve), no face visible unless explicitly requested. Hand-to-product contact must be physically plausible with honest real-world scale. Hands must never permanently obscure distinctive product anchors or key components.
*(If Mode Subjek is Product-Only, replace the heading and body of Block 5 above with:
[5. PRODUCT-ONLY MODE]
Product is the sole subject in every shot. Strictly NO humans, NO babies, NO children, NO hands, NO arms, NO legs, NO body parts, NO human reflections or silhouettes, and NO human interaction.)*

[6. ENVIRONMENT & CONTINUITY LOCK]
Maintain continuity across all shots: ONE consistent clean everyday Indonesian room setting and surface, consistent soft natural directional daylight and color temperature, and keep the product centered in the middle safe zone of the 9:16 frame in every shot.

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (0s–1s, Hook — FRONT VIEW / OPENING): <Action and composition>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; complete original product visible with exact geometry. Continuity: establish baseline lighting, surface, and product scale. Avoid: <shot-relevant negatives>.
- Shot 2 (1s–4s, Demo — THREE-QUARTER VIEW): <Uninterrupted demo or feature showcase>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact physical product; visible components: <list>; anchors: <list>; all distinctive components remain attached and unchanged without reconstruction. Continuity: match Shot 1 lighting, setting, and scale. Avoid: <shot-relevant negatives>.
- Shot 3 (4s–6s, Result/Benefit — SIDE / MACRO VIEW): <Detail or result payoff>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; preserve original geometry, material texture, and features partially hidden by perspective. Continuity: match Shot 2 lighting and product position. Avoid: <shot-relevant negatives>.
- Shot 4 (6s–8s, Detail/Benefit — MACRO DETAIL): <Texture/benefit highlight>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; exact original material, texture, and logo without inventing new structures. Continuity: match previous shots seamlessly. Avoid: <shot-relevant negatives>.
- Final Shot (8s–10s, Hero + CTA — FINAL HERO): Clean, steady product hero showcase held for 2 seconds leaving the bottom 28% completely uncluttered for CTA overlay. Camera: <position/angle>, <conservative push-in/static>, <direction>, <subtle intensity>. Identity: same exact product; visible components: <complete component list>; anchors: <all anchors>; complete recognizable product composition with all original components present. Continuity: return cleanly to unified lighting and center framing. Avoid: <shot-relevant negatives>.

[8. CAMERA MOVEMENT CONTROL]
Risk profile: <Simple/Rigid | Moderate | Complex>. Move the camera smoothly around a stationary product; avoid needless product rotation, extreme perspective changes, full 360-degree orbit, or camera passing through the product; keep the product centered and critical features recognizable across all shots.

[9. AUDIO DIRECTION]
Upbeat yet clean background music matched to the product mood, crisp realistic SFX synced to each cut and product action, no audio clipping. No on-camera speaking, no lip-sync, no generated speech; leave clean audio space for an off-screen Indonesian voice-over added in editing. *(Remove the last sentence if VO is not used.)*

[10. NEGATIVE PROMPT]
<Product-specific anti-morphing constraints>, <shot-relevant negatives>, <Human Demo: no visible human face, no extra fingers | Product-Only Mode: no humans, no babies, no children, no hands, no arms, no legs, no body parts, no human reflections or silhouettes>, no erratic camera spin, no burned-in text, no marketplace UI, no watermarks.

[11. FINAL PRODUCT IDENTITY VERIFICATION]
Verify from 0s to 10s that the rendered product remains 100% identical to the original reference photos in exact geometry, proportions, colors, surface textures, logo/label, and component count (<summary of locked components and anchors>), with zero morphing, zero missing parts, and zero invented features.
```

*(Sesuaikan jumlah baris `Shot 1` s.d. `Final Shot` pada `[7. SHOT-BY-SHOT TIMELINE]` agar memetakan `1:1` terhadap timestamp bilangan bulat di `rapid-brief-and-storyboard.md` — `Clear`: `4–6` shot; `Hype`: `7–8` shot.)*

---

## 6. Editing & Final Assembly

1. **Impor 1 Klip & Verifikasi Durasi:** Masukkan klip hasil generasi `10` detik ke editor (`CapCut` / NLE). Pastikan durasi timeline tepat **`10` detik** (`00:00–00:10`). Jika klip sedikit lebih panjang dari `10` detik, lakukan *trim* **hanya di bagian akhir** (tanpa pemotongan per panel).
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`), tanpa jeda kosong atau frame hitam.
3. **Sinkronisasi Audio & SFX:** Tambahkan *BGM* sesuai karakter produk, dan selaraskan *SFX* aksi tepat pada titik pergantian shot di storyboard utama.
4. **Penempatan Voice Over (`## Voice Over`):** Tempatkan rekaman/TTS VO tepat pada rentang waktu segmen yang tervalidasi di `_vo-timing.md` (mis. `00:00–00:04`, `00:04–00:08`, `00:08–00:10`) agar tidak menabrak pergantian visual; atur VO sekitar **`-6 dBFS`** dan turunkan BGM ke sekitar **`-22 dBFS`**. *(Lewati jika VO tidak digunakan.)*
5. **Penempatan Text Overlay & CTA (Maks. `2` Pergantian):**
   - Teks singkat manfaat utama (`1` kali tampil): zona aman `20%–32%` atau `60%–70%` tinggi layar tanpa menutupi produk.
   - CTA akhir (`00:08–00:10`, di atas zona `28%` bawah layar): gunakan kalimat singkat jujur (`"Cek di keranjang kuning!"` untuk TikTok atau `"Cek link di bio!"` untuk Reels) tanpa klaim kelangkaan/diskon palsu.

---

## 7. Quality Control Checklist

**Duration & Prompt**
- [ ] Total durasi storyboard utama tepat `10` detik (`00:00–00:10`, penjumlahan: `<... = 10>` detik) dengan seluruh panel memakai bilangan bulat (`≥ 1` detik).
- [ ] Jumlah panel sesuai varian terpilih (`Clear`: `4–6` panel; `Hype`: `7–8` panel).
- [ ] File `rapid-video-prompts.md` hanya berisi `1` master prompt `10` detik berarsitektur `11` blok PCS tanpa prompt per scene/panel.

**Storytelling & Pacing**
- [ ] Mengikuti struktur 4 babak (`Hook → Demo → Hasil/Manfaat → Hero + CTA`) dengan fokus `1` selling point utama.
- [ ] Hook menarik di `00:00–00:01` dan produk terlihat jelas.
- [ ] Demo berdurasi `≥ 2` detik dalam satu aksi utuh tanpa terpotong *(atau feature showcase pada Product-Only Mode)*.
- [ ] Penutup Hero + CTA ditahan `≥ 2` detik dengan tujuan yang jelas.
- [ ] Pergantian teks overlay maksimal `2` kali dan tanpa pergantian shot yang membingungkan.

**Storyboard & Audio**
- [ ] Prompt gambar storyboard disusun dalam `1` lembar tunggal.
- [ ] Musik sesuai karakter produk, SFX tersinkronisasi pada pergantian shot, tanpa *audio clipping*.

**Output**
- [ ] Tidak ada tabel ringkasan babak & durasi terpisah; setiap panel hanya tampil satu kali.
- [ ] Urutan output tepat `1–8` dengan `## Voice Over` paling akhir.

**Voice Over**
- [ ] Hanya ada `1` versi VO terbaik (atau dinyatakan tidak digunakan dengan alasan singkat), selaras 4 babak, tanpa mengulang teks layar kata per kata.
- [ ] Bahasa Indonesia lisan natural, seluruh angka ditulis dengan huruf/kata (tanpa digit), dan tanpa klaim yang tidak terverifikasi.
- [ ] File internal `_vo-timing.md` lolos validasi `dialogue_timing.py` *(atau `N/A` bila VO tidak digunakan)*.

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

**Status QC Konsistensi Produk (PCS v2.0):** `<PASS | WARNING (<daftar item [PERLU DICEK]>) | FAIL (<daftar kegagalan>)>`

---

## 8. Voice Over

**VOICE OVER — 10 DETIK**

```text
<Tulis satu naskah VO terbaik lengkap dari awal sampai akhir — bahasa lisan natural, angka ditulis huruf, jeda dengan tanda baca>
```

- **Voice character:** <karakter suara yang direkomendasikan>
- **Gender:** <pilihan gender suara bila relevan>
- **Delivery:** <gaya penyampaian per babak>
- **Tone:** <emosi dan intonasi>
- **Speaking rate:** ± 5 suku kata/detik (`<N>` suku kata dalam 10 detik; `dialogue_timing.py`: LOLOS)

*(Jika HCE menilai VO tidak diperlukan, ganti blok di atas dengan `**VOICE OVER — TIDAK DIGUNAKAN**` dan 1–2 kalimat alasan singkat.)*
