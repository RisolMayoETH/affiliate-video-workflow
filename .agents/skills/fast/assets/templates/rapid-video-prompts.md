# Rapid Video Prompt & Assembly Guide (10s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Rapid Affiliate Review v1.1` (`/fast`)
- **Varian:** `<Clear | Hype>` (`<N>` panel)
- **Acuan Storyboard:** `rapid-10s/rapid-brief-and-storyboard.md`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`10` detik**
- **Aturan Generator Video:** Hanya **1 Master Prompt berdurasi bilangan bulat tepat `10 seconds`** tanpa prompt terpisah per scene/panel.

---

## Master Video Prompt (`10 Seconds`) — Satu-satunya Prompt Video

> **Catatan:** Mode `/fast` hanya menyediakan **1 Master Prompt** agar seluruh timeline `10` detik digenerasi dalam satu alur yang konsisten. Jika generator video pilihanmu belum mendukung durasi `10` detik sekaligus, gunakan generator yang mendukung `10` detik dalam satu kali proses.

- **Durasi Generasi AI:** `10` seconds *(bilangan bulat tepat)*
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<lembar storyboard tunggal / aset jangkar bila tersedia>`
- **Copy-Ready Master Prompt (English):**
```text
Duration: 10 seconds. Vertical 9:16 commercial affiliate product video following a clear 4-beat structure (Hook -> Demo -> Result/Benefit -> Hero + CTA).

[PRODUCT IDENTITY LOCK]:
Strictly preserve the exact physical design, shape, proportions, colors, materials, textures, logo, and component count of the product from the attached original product reference photos across every shot.

[HAND & ENVIRONMENT LOCK]:
Maintain continuity across all shots: the exact same Indonesian adult hand (sawo matang skin, clean natural nails, consistent neutral sleeve), the exact same clean everyday Indonesian room background, consistent soft natural daylight, and keep the product centered in the middle zone of the 9:16 frame in every shot.

[SHOT TIMELINE (0s–10s)]
- Shot 1 (0s–1s, Hook): ...
- Shot 2 (1s–4s, Demo): ...
- Shot 3 (4s–6s, Result/Benefit): ...
- Shot 4 (6s–8s, Detail/Benefit): ...
- Final Shot (8s–10s, Hero + CTA): Clean, steady product hero showcase held for 2 seconds, leaving the bottom 28% of the frame completely clean and unobstructed for CTA overlay.

[CAMERA & TRANSITION STYLE]
Purposeful commercial cinematography combining tight close-ups, steady POV demonstration, and smooth push-in/tracking movements connected by clean cuts and natural action transitions. Fast attention-grabbing opening, unhurried uninterrupted demo, and steady closing hold.

[AUDIO]
Upbeat yet clean background music matched to the product mood, crisp realistic SFX synced to each cut and product action, no audio clipping. (Optional VO: natural Indonesian spoken delivery with numbers spelled out in words, max 5 syllables per second.)

[NEGATIVE / AVOID]
No product morphing or color shift, no missing or invented parts, no logo distortion, no extra fingers, no human face (unless specified), no erratic camera spin, no burned-in text, no watermarks.
```

*(Sesuaikan jumlah baris `Shot 1` s.d. `Final Shot` pada `[SHOT TIMELINE (0s–10s)]` agar memetakan `1:1` terhadap timestamp bilangan bulat di `rapid-brief-and-storyboard.md` — `Clear`: `4–6` shot; `Hype`: `7–8` shot.)*

---

## Panduan Editing & Final Assembly (`1080 × 1920`, Tepat `10` Detik)

1. **Impor 1 Klip & Verifikasi Durasi:** Masukkan klip hasil generasi `10` detik ke editor (`CapCut` / NLE). Pastikan durasi timeline tepat **`10` detik** (`00:00–00:10`). Jika klip hasil generate sedikit lebih panjang dari `10` detik, lakukan *trim* **hanya di bagian akhir** (tanpa pemotongan per panel).
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`), tanpa jeda kosong atau frame hitam.
3. **Sinkronisasi Audio & SFX:** Tambahkan *BGM* sesuai karakter produk (level aman di bawah SFX/VO, bebas *clipping*), dan selaraskan *SFX* aksi tepat pada titik pergantian shot di timeline.
4. **Penempatan Text Overlay & CTA (Maks. `2` Pergantian):**
   - Teks singkat manfaat utama (`1` kali tampil): zona aman `20%–32%` atau `60%–70%` tinggi layar tanpa menutupi produk.
   - CTA akhir (`00:08–00:10`, zona aman di atas `28%` bawah layar): gunakan kalimat singkat jujur (`"Cek produknya sekarang!"`, `"Lihat detailnya!"`, atau `"Cek di keranjang kuning!"`) tanpa klaim kelangkaan/diskon palsu.
