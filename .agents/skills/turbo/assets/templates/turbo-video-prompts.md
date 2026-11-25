# Turbo Video Prompts & Assembly Guide (15s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Turbo Affiliate Review v1.1` (`/turbo` — Sekali Jalan)
- **Acuan Storyboard:** `turbo-15s/turbo-brief-and-storyboard.md` & **1 lembar gambar** `turbo-15s/upload-assets/storyboard-9panel.png`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`15` detik**
- **Aturan Durasi Generator Video:** Seluruh prompt generasi di bawah wajib menggunakan **detik bilangan bulat tanpa koma/desimal** (`2`, `3`, `4`, `5`, `6`, `7`, `8`, `10`, atau `15` seconds).

---

## Opsi 1 (Mode A — Utama Sekali Jalan): `1` Master Video Prompt Langsung `15` Seconds (`1×` Generasi)

> Gunakan opsi ini sebagai alur default untuk menghasilkan seluruh video **`15` detik (`0s–15s`) dalam 1 kali generasi** menggunakan generator video yang mendukung durasi `15` detik langsung (lampirkan referensi produk `Otoritas #1` bersama **1 lembar storyboard tunggal**).

- **Durasi Generasi AI:** `15` seconds *(bilangan bulat tepat `15` detik sekali jalan)*
- **Cakupan Storyboard:** Seluruh `PANEL 01–PANEL <N>` (`00:00.0–00:15.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `turbo-15s/upload-assets/storyboard-9panel.png` *(acuan urutan & komposisi 1 lembar tunggal)*
- **Copy-Ready Master Prompt (English):**
```text
Duration: 15 seconds. Vertical 9:16 commercial affiliate video with dynamic smooth cuts.
[PRODUCT IDENTITY LOCK]: Strictly match exact shape, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo across every shot.
[SUBJECT & ENVIRONMENT LOCK]: Consistent Indonesian adult hands/subject (natural sawo matang skin, clean short nails, neutral/consistent attire, no face shown), consistent setting and soft natural daylight throughout.
[FIRST-FRAME ANCHOR (0s)]: <Exact visual state of product, hand/subject, camera angle, and setting at 0s>.

[MULTI-SHOT TIMELINE (0s-15s)]
- Shot 1 (0s-1s, Hook / Visual Impact): ...
- Shot 2 (1s-3s, Context & Reveal): ...
- Shot 3 (3s-5s, Key Feature Proof): ...
- Shot 4 (5s-7s, Material / Mechanism Demo): ...
- Shot 5 (7s-9s, Secondary Feature & Macro Detail): ...
- Shot 6 (9s-11s, Benefit / Result Payoff): ...
- Shot 7 (11s-13s, Lifestyle / Real-Use Proof): ...
- Shot 8 (13s-15s, Hero Closing & CTA Safe Space): ...

[CAMERA & TRANSITION STYLE]: Crisp purposeful commercial shots connected by clean match cuts and natural action transitions; smooth realistic hand/product physics with zero product morphing.
[LAST-FRAME ANCHOR (15s)]: Clean centered hero framing in the 18%-68% upper-middle zone, keeping the bottom 28% completely uncluttered for CTA overlay.
[NEGATIVE / AVOID]: No product morphing, no color shift, no missing or extra parts, no extra fingers, no human face, no arrows, no graphic lines, no burned-in text, no marketplace UI, no watermarks.
```
- **Audio / SFX / VO Cue:** `<Karakter BGM + titik SFX sinkron 0s–15s + kutipan lengkap VO Bahasa Indonesia bila dipakai>`

---

## Opsi 2 (Mode B — Alternatif Cadangan): Jika Generator Berbatas `≤ 10` Detik atau Ingin Trim NLE

### Mode B1 — Segmentasi Multi-Shot Adaptif (`2–3` Klip Bilangan Bulat `≤ 10s`, Total `15` Seconds)
- **Pola Segmentasi Cadangan:** `<mis. 3 Klip Simetris (5s + 5s + 5s = 15s) / 2 Klip (8s + 7s = 15s) / 2 Klip (10s + 5s = 15s)>`
- **Alasan:** Dipakai jika generator target memiliki batas klip maksimal `5`–`10` detik. Baris pertama di dalam blok prompt **Klip 02** dan **Klip 03** **wajib diawali tepat dengan `"Continue the video."`** (jangan pada Klip 01).

#### Klip 01 — `<Babak Pembuka>` (`<X>` Seconds)
- **Durasi Generasi AI:** `<X>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL 01–PANEL <k>` (`00:00.0–00:0<X>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `turbo-15s/upload-assets/storyboard-9panel.png`
- **Copy-Ready Prompt (English):**
```text
Duration: <X> seconds. Vertical 9:16 commercial affiliate video with dynamic smooth cuts.
[PRODUCT IDENTITY LOCK]: ...
[SUBJECT & ENVIRONMENT LOCK]: ...
[FIRST-FRAME ANCHOR (0s)]: ...

[MULTI-SHOT TIMELINE (0s-<X>s)]
- Shot 1 (0s-1s): ...
- Shot 2 (1s-<X>s): ...

[CAMERA & TRANSITION STYLE]: ...
[LAST-FRAME ANCHOR (<X>s)]: <Exact ending pose for seamless hand-off to Clip 02>.
[NEGATIVE / AVOID]: No product morphing, no extra fingers, no human face, no arrows, no burned-in text, no watermarks.
```
- **Audio / SFX / VO Cue:** `<BGM + SFX + kutipan VO segmen Klip 01>`

#### Klip 02 — `<Babak Lanjutan>` (`<Y>` Seconds)
- **Durasi Generasi AI:** `<Y>` seconds *(bilangan bulat `≤ 10`)*
- **Cakupan Storyboard:** `PANEL <k+1>–PANEL <m>` (`00:0<X>.0–00:<X+Y>.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, frame terakhir Klip 01, `turbo-15s/upload-assets/storyboard-9panel.png`
- **Copy-Ready Prompt (English):**
```text
Continue the video.
Duration: <Y> seconds. Vertical 9:16 commercial affiliate video continuing seamlessly from Clip 01.
[PRODUCT IDENTITY LOCK]: ...
[SUBJECT & ENVIRONMENT LOCK]: Exact same hand/subject, attire, setting, and lighting as Clip 01.
[FIRST-FRAME ANCHOR (0s)]: Match the exact ending state of Clip 01 before transitioning cleanly into the next action.

[MULTI-SHOT TIMELINE (0s-<Y>s)]
- Shot 1 (0s-2s): ...
- Shot 2 (2s-<Y>s): ...

[CAMERA & TRANSITION STYLE]: ...
[LAST-FRAME ANCHOR (<Y>s)]: <Exact ending hero or hand-off pose>.
[NEGATIVE / AVOID]: No sudden lighting jump, no product morphing, no extra fingers, no human face, no arrows, no burned-in text, no watermarks.
```
- **Audio / SFX / VO Cue:** `<SFX + kutipan VO segmen Klip 02>`

*(Tambahkan `#### Klip 03` dengan awalan `"Continue the video."` bila memakai pola `3` klip seperti `5+5+5` atau `4+6+5`. Total Klip 01 + 02 [+ 03] wajib tepat **`15` seconds**.)*

---

### Mode B2 — Prompt Individual per Panel (`Generasi Bilangan Bulat 2–4s → Trim Editing ke 15.0 Detik`)
> Dipakai jika ingin kontrol ritme super-presisi per beat di editor (*surgical NLE editing*). Generate tiap panel dengan durasi bilangan bulat (`2`, `3`, atau `4` seconds) lalu *trim* pada puncak aksi sesuai timestamp storyboard.

#### Prompt Panel 01 — `<Judul / Fungsi Panel 01>`
- **Durasi Generasi AI:** `2` seconds *(atau `3` / `4` seconds)*
- **Target Trim Storyboard:** `1.2` detik (`00:00.0–00:01.2`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*
- **Copy-Ready Prompt (English):**
```text
Duration: 2 seconds. Vertical 9:16 commercial product video.
[PRODUCT IDENTITY LOCK]: Strictly match exact shape, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo.
[COMPOSITION & CAMERA]: <Shot type, camera angle, and camera movement matching PANEL 01>.
[SUBJECT ACTION]: <Exact realistic physical motion within 0s-2s for clean trim>.
[LIGHTING & ENVIRONMENT]: <Consistent natural lighting and clean setting>.
[NEGATIVE / AVOID]: No product deformation, no extra fingers, no human face, no arrows, no burned-in text, no watermarks.
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
