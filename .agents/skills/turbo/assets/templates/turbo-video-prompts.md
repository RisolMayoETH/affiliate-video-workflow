# Turbo Video Prompts & Assembly Guide (15s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Turbo Affiliate Review v1.2` (`/turbo` — Sekali Jalan)
- **Mode Subjek:** `<Human Demo | Product-Only>`
- **Product Identity Sheet (PCS v2.0):** `<01-product-review/product-identity-lock.md | turbo-15s/product-identity-lock.md>`
- **Acuan Storyboard:** `turbo-15s/turbo-brief-and-storyboard.md` & **1 lembar gambar** `turbo-15s/upload-assets/storyboard-9panel.png`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`15` detik**
- **Aturan Generator Video:** Seluruh prompt generasi di bawah wajib menggunakan **detik bilangan bulat tanpa koma/desimal** (`2`, `3`, `4`, `5`, `6`, `7`, `8`, `10`, atau `15` seconds) dan mengikuti **Arsitektur 11 Blok PCS v2.0**.

---

## Opsi 1 (Mode A — Utama Sekali Jalan): `1` Master Video Prompt Langsung `15` Seconds (`1×` Generasi)

> Gunakan opsi ini sebagai alur default untuk menghasilkan seluruh video **`15` detik (`0s–15s`) dalam 1 kali generasi** menggunakan generator video yang mendukung durasi `15` detik langsung (lampirkan referensi produk `Otoritas #1` bersama **1 lembar storyboard tunggal**).

- **Durasi Generasi AI:** `15` seconds *(bilangan bulat tepat `15` detik sekali jalan)*
- **Cakupan Storyboard:** Seluruh `PANEL 01–PANEL <N>` (`00:00.0–00:15.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `turbo-15s/upload-assets/storyboard-9panel.png` *(acuan urutan & komposisi 1 lembar tunggal)*
- **Copy-Ready Master Prompt (English):**
```text
[1. VIDEO SPECIFICATION]
Duration: 15 seconds. Vertical 9:16 commercial affiliate video with dynamic smooth cuts.

[2. PRODUCT IDENTITY LOCK]
<Paste the exact specific English Identity Descriptor from product-identity-lock.md — never a generic category phrase.>

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
*(If Mode Subjek is Product-Only, replace Block 5 above with:
[5. PRODUCT-ONLY MODE]
Product is the sole subject in every shot. Strictly NO humans, NO babies, NO children, NO hands, NO arms, NO legs, NO body parts, NO human reflections or silhouettes, and NO human interaction.)*

[6. ENVIRONMENT & CONTINUITY LOCK]
Consistent setting, surface, soft natural directional daylight, and color temperature throughout; keep product centered in the middle safe zone.
First-Frame Anchor (0s): <Exact visual state of product, hand/no-hand, camera angle, and setting at 0s>.

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (0s-1s, Hook — FRONT / OPENING): <Action and composition>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; complete original product visible with exact geometry. Continuity: establish baseline lighting and scale. Avoid: <shot negatives>.
- Shot 2 (1s-3s, Context & Reveal — THREE-QUARTER VIEW): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact physical product; visible components: <list>; anchors: <list>; all distinctive components remain attached without reconstruction. Continuity: match Shot 1 setting and lighting. Avoid: <shot negatives>.
- Shot 3 (3s-5s, Key Feature Proof — THREE-QUARTER VIEW): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; do not replace or alter components. Continuity: match Shot 2 lighting and position. Avoid: <shot negatives>.
- Shot 4 (5s-7s, Material / Mechanism Demo — SIDE / THREE-QUARTER): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; preserve original geometry and features hidden by perspective. Continuity: match Shot 3 physics and daylight. Avoid: <shot negatives>.
- Shot 5 (7s-9s, Secondary Feature & Macro Detail — MACRO DETAIL): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; exact original material, texture, and logo without inventing new structures. Continuity: match Shot 4 textures and colors. Avoid: <shot negatives>.
- Shot 6 (9s-11s, Benefit / Result Payoff — THREE-QUARTER VIEW): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; preserve complete product geometry. Continuity: match Shot 5 setting. Avoid: <shot negatives>.
- Shot 7 (11s-13s, Lifestyle / Real-Use Proof — FRONT / THREE-QUARTER): <Action>. Camera: <position/angle>, <movement>, <direction>, <intensity>. Identity: same exact product; visible components: <list>; anchors: <list>; preserve all anchors. Continuity: match Shot 6 environment. Avoid: <shot negatives>.
- Shot 8 (13s-15s, Hero Closing & CTA Safe Space — FINAL HERO): Clean centered hero framing in the 18%-68% upper-middle zone, keeping the bottom 28% completely uncluttered for CTA overlay. Camera: <position/angle>, <conservative push-in/static>, <direction>, <subtle intensity>. Identity: same exact product; visible components: <complete component list>; anchors: <all anchors>; complete recognizable product composition with all original components present. Continuity: unified lighting and center framing. Avoid: <shot negatives>.
Last-Frame Anchor (15s): <Exact steady final hero state with clean 28% bottom zone>.

[8. CAMERA MOVEMENT CONTROL]
Risk profile: <Simple/Rigid | Moderate | Complex>. Move the camera smoothly around a stationary product; avoid needless product rotation, extreme perspective changes, full 360-degree orbit, or camera passing through the product; keep the product centered and critical features recognizable.

[9. AUDIO DIRECTION]
<BGM mood + synced SFX across 0s-15s + optional Indonesian VO cue if used.>

[10. NEGATIVE PROMPT]
<Product-specific anti-morphing constraints>, <shot-relevant negatives>, <Human Demo: no visible human face, no extra fingers | Product-Only Mode: no humans, no babies, no children, no hands, no arms, no legs, no body parts, no human reflections or silhouettes>, no arrows, no graphic lines, no burned-in text, no marketplace UI, no watermarks.

[11. FINAL PRODUCT IDENTITY VERIFICATION]
Verify across 0s-15s that the rendered product remains 100% identical to the original reference photos in exact geometry, proportions, colors, surface textures, logo/label, and component count (<summary of locked components and anchors>), with zero morphing or missing parts.
```
- **Audio / SFX / VO Cue:** `<Karakter BGM + titik SFX sinkron 0s–15s + kutipan lengkap VO Bahasa Indonesia bila dipakai>`

---

## Opsi 2 (Mode B — Alternatif Cadangan): Jika Generator Berbatas `≤ 10` Detik atau Ingin Trim NLE

### Mode B1 — Segmentasi Multi-Shot Adaptif (`2–3` Klip Bilangan Bulat `≤ 10s`, Total `15` Seconds)
- **Pola Segmentasi Cadangan:** `<mis. 3 Klip Simetris (5s + 5s + 5s = 15s) / 2 Klip (8s + 7s = 15s) / 2 Klip (10s + 5s = 15s)>`
- **Alasan:** Dipakai jika generator target memiliki batas klip maksimal `5`–`10` detik. Baris pertama di dalam blok prompt **Klip 02** dan **Klip 03** **wajib diawali tepat dengan `"Continue the video."`** sebelum `[1. VIDEO SPECIFICATION]` (jangan pada Klip 01).

#### Klip 01 — `<Babak Pembuka>` (`<X>` Seconds)
- **Durasi Generasi AI:** `<X>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL 01–PANEL <k>` (`00:00.0–00:0<X>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `turbo-15s/upload-assets/storyboard-9panel.png`
- **Copy-Ready Prompt (English):**
```text
[1. VIDEO SPECIFICATION]
Duration: <X> seconds. Vertical 9:16 commercial affiliate video with dynamic smooth cuts.

[2. PRODUCT IDENTITY LOCK]
<Specific English Identity Descriptor from product-identity-lock.md.>

[3. OBJECT PERMANENCE LOCK]
<All 7 permanence rules + component list + moving-part rule.>

[4. ANTI-MORPHING LOCK]
<Core constraints + product-specific anti-morphing constraints.>

[5. HUMAN MODE]   (or [5. PRODUCT-ONLY MODE] matching Mode Subjek)
<Exact Subject Mode block from PCS §6.>

[6. ENVIRONMENT & CONTINUITY LOCK]
<Consistent setting, surface, lighting, and First-Frame Anchor (0s).>

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (0s-1s, <beat> — <VIEW>): ... Camera: ... Identity: ... Continuity: ... Avoid: ...
- Shot 2 (1s-<X>s, <beat> — <VIEW>): ... Camera: ... Identity: ... Continuity: ... Avoid: ...
Last-Frame Anchor (<X>s): <Exact ending pose for seamless hand-off to Clip 02>.

[8. CAMERA MOVEMENT CONTROL]
<Risk profile + camera control rules.>

[9. AUDIO DIRECTION]
<BGM + SFX + optional VO segment cue.>

[10. NEGATIVE PROMPT]
<Product-specific + shot + subject-mode negatives + no arrows, no burned-in text, no watermarks.>

[11. FINAL PRODUCT IDENTITY VERIFICATION]
<Verify exact geometry, colors, textures, logo, and component count throughout Clip 01.>
```
- **Audio / SFX / VO Cue:** `<BGM + SFX + kutipan VO segmen Klip 01>`

#### Klip 02 — `<Babak Lanjutan>` (`<Y>` Seconds)
- **Durasi Generasi AI:** `<Y>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL <k+1>–PANEL <m>` (`00:0<X>.0–00:<X+Y>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, frame terakhir Klip 01, `turbo-15s/upload-assets/storyboard-9panel.png`
- **Copy-Ready Prompt (English):**
```text
Continue the video.
[1. VIDEO SPECIFICATION]
Duration: <Y> seconds. Vertical 9:16 commercial affiliate video continuing seamlessly from Clip 01.

[2. PRODUCT IDENTITY LOCK]
<Same exact specific English Identity Descriptor from product-identity-lock.md.>

[3. OBJECT PERMANENCE LOCK]
<Same exact 7 permanence rules + component list + moving-part rule.>

[4. ANTI-MORPHING LOCK]
<Core constraints + same product-specific anti-morphing constraints.>

[5. HUMAN MODE]   (or [5. PRODUCT-ONLY MODE] matching Mode Subjek)
<Exact Subject Mode block matching Clip 01.>

[6. ENVIRONMENT & CONTINUITY LOCK]
Exact same setting, surface, lighting, and subject continuity as Clip 01.
First-Frame Anchor (0s): Match the exact ending state of Clip 01 before transitioning cleanly into the next action.

[7. SHOT-BY-SHOT TIMELINE]
- Shot 1 (0s-2s, <beat> — <VIEW>): ... Camera: ... Identity: ... Continuity: ... Avoid: ...
- Shot 2 (2s-<Y>s, <beat> — <VIEW>): ... Camera: ... Identity: ... Continuity: ... Avoid: ...
Last-Frame Anchor (<Y>s): <Exact ending hero or hand-off pose>.

[8. CAMERA MOVEMENT CONTROL]
<Risk profile + camera control rules.>

[9. AUDIO DIRECTION]
<SFX + optional VO segment cue.>

[10. NEGATIVE PROMPT]
No sudden lighting jump, <product-specific + shot + subject-mode negatives>, no arrows, no burned-in text, no watermarks.

[11. FINAL PRODUCT IDENTITY VERIFICATION]
<Verify exact geometry, colors, textures, logo, and component count match Clip 01 and original references.>
```
- **Audio / SFX / VO Cue:** `<SFX + kutipan VO segmen Klip 02>`

*(Tambahkan `#### Klip 03` dengan awalan `"Continue the video."` sebelum `[1. VIDEO SPECIFICATION]` bila memakai pola `3` klip seperti `5+5+5` atau `4+6+5`. Total Klip 01 + 02 [+ 03] wajib tepat **`15` seconds**.)*

---

### Mode B2 — Prompt Individual per Panel (`Generasi Bilangan Bulat 2–4s → Trim Editing ke 15.0 Detik`)
> Dipakai jika ingin kontrol ritme super-presisi per beat di editor (*surgical NLE editing*). Generate tiap panel dengan durasi bilangan bulat (`2`, `3`, atau `4` seconds) menggunakan format ringkas **11 label PCS**, lalu *trim* pada puncak aksi sesuai timestamp storyboard.

#### Prompt Panel 01 — `<Judul / Fungsi Panel 01>`
- **Durasi Generasi AI:** `2` seconds *(atau `3` / `4` seconds)*
- **Target Trim Storyboard:** `1.2` detik (`00:00.0–00:01.2`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*
- **Copy-Ready Prompt (English):**
```text
[1. VIDEO SPECIFICATION] Duration: 2 seconds. Vertical 9:16 commercial product video.
[2. PRODUCT IDENTITY LOCK] <Specific English Identity Descriptor from product-identity-lock.md.>
[3. OBJECT PERMANENCE LOCK] Same physical object; all components (<list>) remain attached and consistent without disappearing or duplicating.
[4. ANTI-MORPHING LOCK] No morphing, geometry changes, color shift, or <product-specific missing/altered components>.
[5. HUMAN MODE] <Consistent Indonesian adult hand, no face | or [5. PRODUCT-ONLY MODE] strictly no humans or hands>.
[6. ENVIRONMENT & CONTINUITY LOCK] <Consistent setting, natural daylight, centered 9:16 framing.>
[7. SHOT-BY-SHOT TIMELINE] Shot 1 (0s-2s, <beat> — <VIEW>): <Exact realistic motion for clean trim>. Identity: preserve all components and anchors. Avoid: <shot negatives>.
[8. CAMERA MOVEMENT CONTROL] <Shot type, camera angle, movement, direction, subtle/smooth intensity per PCS risk profile.>
[9. AUDIO DIRECTION] <Crisp realistic product action SFX synced to motion.>
[10. NEGATIVE PROMPT] <Product-specific + subject-mode negatives>, no extra fingers, no arrows, no burned-in text, no watermarks.
[11. FINAL PRODUCT IDENTITY VERIFICATION] Product matches original reference photos 100% in shape, color, texture, logo, and component count.
```
- **Audio / SFX Cue (Editing):** `<SFX / beat sinkron pada 00:00.0–00:01.2>`

*(Ulangi blok `Prompt Panel 02` s.d. `Prompt Panel <N>` dengan durasi generasi bilangan bulat masing-masing.)*

---

## Opsi VO Bahasa Indonesia & Tabel Timing Dialog *(Hapus Jika Video Tanpa VO)*

- **Naskah Lengkap VO (`60–68` suku kata, angka dieja kata):**
  `"<Tuliskan naskah VO utuh 15 detik yang natural lisan>"`

## Tabel Timing Dialog

| Segmen | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status | Catatan Intonasi |
|---|---|---|---|---|---|---|---|
| Fase 1 (0–5s) | 00:00.0–00:05.0 | 5.0 | "..." | 0 | 0.00 | OK | Santai, memancing rasa ingin tahu |
| Fase 2 (5–10s) | 00:05.0–00:10.0 | 5.0 | "..." | 0 | 0.00 | OK | Jelas, informatif saat demo |
| Fase 3 (10–15s) | 00:10.0–00:15.0 | 5.0 | "..." | 0 | 0.00 | OK | Hangat, ajakan natural |

> Validasi otomatis tabel di atas dengan:
> `python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/turbo-15s/turbo-video-prompts.md --max-duration 15`

---

## Panduan Editing & Final Assembly (`1080 × 1920`, Tepat `15` Detik)

1. **Susunan Timeline (`CapCut` / NLE):**
   - **Jalur Mode A (`1` klip `15s` — Sekali Jalan):** Impor 1 klip video `15` detik hasil generasi, verifikasi durasi pas **`15.0` detik** (`00:00.0–00:15.0`) tanpa frame hitam/jeda, lalu lanjutkan ke audio & teks overlay.
   - **Jalur Mode B1 (`2–3` klip `≤ 10s`):** Impor Klip `01`..`02/03` berurutan, rapikan sambungan tepat di *frame anchor* hingga total tepat `15.0` detik.
   - **Jalur Mode B2 (per panel):** Susun klip `Panel 01`..`<N>` dan *trim* pada puncak aksi sesuai timestamp storyboard hingga total tepat `15.0` detik.
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`).
3. **Mixing Audio (BGM + SFX + VO Opsional):**
   - BGM di `-18 dB` s.d. `-16 dB` (turunkan ke `-22 dB` saat VO masuk), SFX aksi di `-10 dB`, VO di `-6 dB`, total puncak audio `< -1.0 dB` (bebas *clipping*).
4. **Penempatan Text Overlay & CTA Zona Aman:**
   - Hindari area UI platform: atas `14%`, kanan `16%`, bawah `28%`.
   - Teks ringkas manfaat di zona `20%–32%` atas dan CTA jujur di zona `60%–70%` tengah-bawah pada detik penutup (`00:13.1–00:15.0`), tanpa klaim kelangkaan/diskon palsu.
