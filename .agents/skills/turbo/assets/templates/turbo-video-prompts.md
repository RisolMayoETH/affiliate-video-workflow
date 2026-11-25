# Turbo Video Prompts & Assembly Guide (15s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Turbo Affiliate Review v1.0` (`/turbo`)
- **Acuan Storyboard:** `turbo-15s/turbo-brief-and-storyboard.md`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`15` detik**
- **Aturan Durasi Generator Video:** Seluruh prompt generasi di bawah wajib menggunakan **detik bilangan bulat tanpa koma/desimal** (`≤ 10` seconds per klip).

---

## Opsi 1 (Mode A — Strategi Utama Direkomendasikan): Segmentasi Multi-Shot Adaptif (`2–3` Klip, Total Tepat `15` Seconds)

- **Pola Segmentasi Terpilih:** `<mis. 2 Klip (8s + 7s = 15s) / 2 Klip (10s + 5s = 15s) / 3 Klip (5s + 5s + 5s = 15s) / 3 Klip (4s + 6s + 5s = 15s)>`
- **Alasan Strategi Terbaik:** `<Jelaskan pertimbangan kontinuitas demonstrasi, jumlah perpindahan scene, dan kompatibilitas batas generator>`

### Klip 01 — `<Babak Pembuka / Hook, Reveal & Awal Demo>` (`<X>` Seconds)
- **Durasi Generasi AI:** `<X>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL 01–PANEL <k>` (`00:00.0–00:0<X>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<lembar storyboard / aset jangkar bila tersedia>`
- **Copy-Ready Prompt (English):**
```text
Duration: <X> seconds. Vertical 9:16 commercial affiliate video with dynamic smooth cuts.
[PRODUCT IDENTITY LOCK]: Strictly match exact shape, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo across every shot.
[HAND & ENVIRONMENT LOCK]: Consistent Indonesian adult hand (natural sawo matang skin, clean short nails, neutral sleeve, no face shown), consistent setting and soft natural daylight throughout.
[FIRST-FRAME ANCHOR (0s)]: <Exact visual state of product, hand, camera angle, and desk/setting at 0s>.

[MULTI-SHOT TIMELINE (0s-<X>s)]
- Shot 1 (0s-1s, Hook): ...
- Shot 2 (1s-3s, Reveal / Problem-Solution): ...
- Shot 3 (3s-<X>s, ...): ...

[CAMERA & TRANSITION STYLE]: <Purposeful commercial shots connected by clean match cuts and natural action transitions>.
[LAST-FRAME ANCHOR (<X>s)]: <Exact pose of product, hand position, camera angle, and lighting state at the final frame for seamless hand-off to Clip 02>.
[NEGATIVE / AVOID]: No product morphing, no color shift, no missing or extra parts, no extra fingers, no human face, no arrows, no graphic lines, no burned-in text, no watermarks.
```
- **Audio / SFX / VO Cue:** `<BGM + SFX sinkron + kutipan VO opsional segmen ini>`

---

### Klip 02 — `<Babak Lanjutan / Demo Inti, Detail & Closing atau Jembatan>` (`<Y>` Seconds)
- **Durasi Generasi AI:** `<Y>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL <k+1>–PANEL <m>` (`00:0<X>.0–00:<X+Y>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<frame terakhir Klip 01 bila fitur extend/image-to-video tersedia + storyboard>`
- **Copy-Ready Prompt (English):**
```text
Continue the video.
Duration: <Y> seconds. Vertical 9:16 commercial affiliate video continuing seamlessly from Clip 01.
[PRODUCT IDENTITY LOCK]: Maintain 100% identical product design, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo.
[HAND & ENVIRONMENT LOCK]: Exact same Indonesian adult hand, sleeve, room setting, and natural daylight direction as Clip 01.
[FIRST-FRAME ANCHOR (0s)]: Match the exact ending state of Clip 01 (<state>) before transitioning cleanly into the next action.

[MULTI-SHOT TIMELINE (0s-<Y>s)]
- Shot 1 (0s-2s, ...): ...
- Shot 2 (2s-<Y>s, ...): ...

[CAMERA & TRANSITION STYLE]: ...
[LAST-FRAME ANCHOR (<Y>s)]: <Exact ending hero/hand-off framing; if final clip, keep bottom 28% completely uncluttered for CTA overlay>.
[NEGATIVE / AVOID]: No sudden jump in lighting or product identity, no product morphing, no extra fingers, no human face, no arrows, no graphic lines, no burned-in text, no watermarks.
```
- **Audio / SFX / VO Cue:** `<SFX sinkron + kutipan VO opsional segmen ini>`

*(Tambahkan `### Klip 03` dengan pola yang sama—diawali `"Continue the video."`—apabila memilih strategi `3` klip seperti `5+5+5` atau `4+6+5`. Pastikan total Klip 01 + 02 [+ 03] tepat **`15` seconds**.)*

---

## Opsi 2 (Mode B — Alternatif Kontrol Presisi Maksimal): Prompt Individual per Panel (`Generasi Bilangan Bulat → Trim Editing`)

> Catatan: Gunakan opsi ini bila ingin mengontrol setiap panel satu per satu di editor (*surgical beat-synced rapid cuts*). Generate tiap panel dengan durasi bilangan bulat (`2`, `3`, atau `4` seconds) lalu *trim* tepat pada puncak aksi sesuai durasi target panel hingga total timeline **tepat `15.0` detik**.

### Prompt Panel 01 — `<Judul / Fungsi Panel 01>`
- **Durasi Generasi AI:** `3` seconds *(atau `2` / `4` seconds)*
- **Target Trim Storyboard:** `1.0` detik (`00:00.0–00:01.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*
- **Copy-Ready Prompt (English):**
```text
Duration: 3 seconds. Vertical 9:16 commercial product video.
[PRODUCT IDENTITY LOCK]: Strictly match exact shape, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo.
[COMPOSITION & CAMERA]: <Shot type, camera angle, and camera movement matching PANEL 01>.
[SUBJECT ACTION]: <Exact realistic physical motion of product and consistent Indonesian adult hand within 0s-2s for clean trim>.
[LIGHTING & ENVIRONMENT]: <Consistent natural lighting and clean setting>.
[NEGATIVE / AVOID]: No product deformation, no missing or extra parts, no extra fingers, no human face, no arrows, no graphic lines, no burned-in text, no watermarks.
```
- **Audio / SFX Cue (Editing):** `<SFX / beat sinkron pada 00:00.0–00:01.0>`

*(Ulangi blok `Prompt Panel 02` s.d. `Prompt Panel <N>` dengan durasi generasi bilangan bulat masing-masing.)*

---

## Opsi VO Bahasa Indonesia & Tabel Timing Dialog *(Hapus atau Biarkan Opsional Jika Video Tanpa VO)*

- **Naskah Lengkap VO (`60–68` suku kata, angka dieja kata):**
  `"<Tuliskan naskah VO utuh 15 detik yang natural lisan>"`

## Tabel Timing Dialog

| Segmen | Waktu Mulai | Waktu Selesai | Durasi (dtk) | Dialog Verbatim (Bahasa Indonesia) | Catatan Intonasi |
|---|---|---|---|---|---|
| Klip 01 | `00:00.0` | `00:05.0` | `5.0` | `"..."` | Santai, memancing rasa ingin tahu |
| Klip 02 | `00:05.0` | `00:10.0` | `5.0` | `"..."` | Jelas, informatif saat demo |
| Klip 03 | `00:10.0` | `00:15.0` | `5.0` | `"..."` | Hangat, ajakan natural |

> Jika menggunakan tabel di atas, validasi dengan:
> `python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/turbo-15s/turbo-video-prompts.md --max-duration 15`

---

## Panduan Editing & Final Assembly (`1080 × 1920`, Tepat `15` Detik)

1. **Susunan Timeline (`CapCut` / NLE):**
   - **Jalur Mode A (`2–3` klip):** Impor Klip `01`..`02/03` berurutan, rapikan titik sambung antar-klip (*clean cut* / *match cut* presisi) sehingga total timeline **tepat `15.0` detik** (`00:00.0–00:15.0`).
   - **Jalur Mode B (per panel):** Susun klip Panel `01`..`<N>` dan *trim* pada puncak aksi sesuai timestamp storyboard hingga total timeline **tepat `15.0` detik**.
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`), nol jeda kosong/frame hitam.
3. **Mixing Audio (BGM + SFX + VO Opsional):**
   - BGM di `-18 dB` s.d. `-16 dB` (turunkan ke `-22 dB` saat VO masuk), SFX aksi di `-10 dB`, VO di `-6 dB`, total puncak audio `< -1.0 dB` (bebas *clipping*).
4. **Penempatan Text Overlay & CTA Zona Aman:**
   - Hindari area UI platform: atas `14%`, kanan `16%`, bawah `28%`.
   - Teks ringkas manfaat di zona `20%–32%` atas dan CTA jujur di zona `60%–70%` tengah-bawah pada detik penutup (`00:13.0–00:15.0`), tanpa klaim kelangkaan/diskon palsu.
