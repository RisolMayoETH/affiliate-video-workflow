# Rapid Video Prompts & Assembly Guide (10s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Rapid Affiliate Review v1.0` (`/fast`)
- **Acuan Storyboard:** `rapid-10s/rapid-brief-and-storyboard.md`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`10` detik**
- **Aturan Durasi Generator Video:** Seluruh prompt generasi di bawah wajib menggunakan **detik bilangan bulat tanpa koma/desimal**.

---

## Opsi 1 (Mode A — Direkomendasikan): Prompt Individual per Panel (`Generasi Bilangan Bulat → Trim Editing`)

> Catatan: Jangan memaksakan durasi generasi sama dengan durasi pendek panel (`0.8–2.0` dtk) bila model membutuhkan ruang gerak tambahan. Generate tiap panel dengan durasi bilangan bulat (`2`, `3`, `4`, atau `5` seconds), lalu potong (*trim*) tepat pada puncak aksi sesuai durasi target panel di editor.

### Prompt Panel 01 — `<Judul / Fungsi Panel 01>`
- **Durasi Generasi AI:** `2` seconds *(atau `3` seconds)*
- **Target Trim Storyboard:** `1.0` detik (`00:00–00:01.0`)
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<aset jangkar di 02-generated-assets/ bila ada>`
- **Copy-Ready Prompt (English):**
```text
Duration: 2 seconds. Vertical 9:16 commercial product video.
[PRODUCT IDENTITY LOCK]: Strictly match exact shape, proportions, colors, materials, textures, logos, and component count from the attached original product reference photo.
[COMPOSITION & CAMERA]: <Shot type, camera angle, and camera movement matching PANEL 01>.
[SUBJECT ACTION]: <Exact realistic physical motion of product and consistent Indonesian adult hand, keeping the core hero motion clear between 0s–2s for clean 1s trim>.
[LIGHTING & ENVIRONMENT]: <Consistent natural lighting and clean setting>.
[NEGATIVE / AVOID]: No product deformation, no missing or extra parts, no logo distortion, no extra fingers, no human face (unless specified), no burned-in text, no watermarks.
```
- **Audio / SFX Cue (Editing):** `<SFX / beat sinkron pada 00:00–00:01.0>`

*(Ulangi blok `Prompt Panel 02` s.d. `Prompt Panel <N>` dengan durasi generasi bilangan bulat masing-masing.)*

---

## Opsi 2 (Mode B — Alternatif Satu Kali Generasi): 1 Master Video Prompt (`10 Seconds`)

> Catatan: Gunakan opsi ini jika model generator video pilihanmu mendukung rangkaian *multi-shot rapid cuts* berdurasi **tepat `10` detik** dalam satu generasi sekaligus.

- **Durasi Generasi AI:** `10` seconds *(bilangan bulat tepat)*
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<aset jangkar utama + lembar storyboard bila tersedia>`
- **Copy-Ready Master Prompt (English):**
```text
Duration: 10 seconds. Vertical 9:16 fast-paced commercial affiliate video with dynamic smooth cuts.
Strictly preserve the exact physical design, proportions, colors, materials, textures, logo, and components of the product from the attached original product reference photos across every shot. Maintain consistent Indonesian adult hand (sawo matang skin, clean nails, consistent neutral sleeve) and natural home lighting throughout.

[MULTI-SHOT RAPID TIMELINE (0s–10s)]
- Shot 1 (0s–1s, Hook): ...
- Shot 2 (1s–2s, Reveal): ...
- ...
- Final Shot (9s–10s, Hero Showcase / CTA Safe Space): Clean upright/held hero framing leaving the bottom 28% completely uncluttered for CTA overlay.

[CAMERA & TRANSITION STYLE]
Purposeful commercial cinematography combining tight close-ups, medium POV demos, and smooth push-in/tracking shots connected by clean match cuts and natural motion transitions.

[NEGATIVE / AVOID]
No product morphing or color shift, no invented parts, no unreadable distorted text, no extra fingers, no aimless 360 camera spin, no burned-in text, no watermarks.
```

---

## Panduan Editing & Final Assembly (`1080 × 1920`, Tepat `10` Detik)

1. **Urutan & Trim Timeline:** Susun klip Mode A berurutan dari Panel `01` hingga Panel `<N>` (atau impor klip Mode B), lalu *trim* presisi sesuai timestamp storyboard hingga durasi total **tepat `10.0` detik** (`00:00–00:10`).
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`), tanpa jeda kosong/frame hitam.
3. **Sinkronisasi Audio & SFX:** Letakkan *BGM* sesuai karakter produk (level aman di bawah SFX/VO, bebas *clipping*), dan selaraskan setiap *SFX* aksi tepat pada titik potong (*cut*) pergantian klip.
4. **Penempatan Text Overlay & CTA:**
   - Teks singkat manfaat utama: zona aman `20%–32%` atau `60%–70%` tinggi layar (jangan menutupi produk).
   - CTA akhir (`00:08.5–00:10.0` atau sesuai panel penutup): gunakan kalimat singkat jujur (`"Cek produknya sekarang!"`, `"Lihat detailnya!"`, atau `"Cek di keranjang kuning!"`) tanpa klaim kelangkaan/diskon palsu.
