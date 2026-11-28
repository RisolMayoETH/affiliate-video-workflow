# Rapid Video Prompt, QC & Voice Over (10s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Rapid Affiliate Review v1.3` (`/fast`)
- **Varian:** `<Clear | Hype>` (`<N>` panel)
- **Acuan Storyboard:** `rapid-10s/rapid-brief-and-storyboard.md`
- **Target Output Final:** `9:16` (`1080 × 1920 px`), tepat **`10` detik**
- **Aturan Generator Video:** Hanya **1 Master Prompt berdurasi bilangan bulat tepat `10 seconds`** tanpa prompt terpisah per scene/panel.

---

## 5. Master Prompt Video (10 Detik)

> **Catatan:** Mode `/fast` hanya menyediakan **1 Master Prompt** agar seluruh timeline `10` detik digenerasi dalam satu alur yang konsisten. Jika generator video belum mendukung durasi `10` detik sekaligus, gunakan generator yang mendukung generasi `10` detik dalam satu kali proses (jangan memecah prompt per scene).

- **Durasi Generasi AI:** `10` seconds *(bilangan bulat tepat)*
- **Gambar Referensi Wajib:** `01-product-review/references/...` *(Otoritas #1)*, `<lembar storyboard tunggal / aset jangkar bila tersedia>`
- **Copy-Ready Master Prompt (English):**
```text
Duration: 10 seconds. Vertical 9:16 commercial affiliate product video following the approved conversion-led storyboard and its selected creative route. Keep the hook, complete proof action, benefit, and CTA clear; do not force a fixed shot order when the storyboard uses another valid route.

[PRODUCT IDENTITY LOCK]:
Strictly preserve the exact physical design, shape, proportions, colors, materials, textures, logo, and component count of the product from the attached original product reference photos across every shot.

[HAND & ENVIRONMENT LOCK]:
Maintain continuity across all shots: the exact same Indonesian adult hand (sawo matang skin, clean natural nails, consistent neutral sleeve), the exact same clean everyday Indonesian room background, consistent soft natural daylight, and place the product, hands, and proof action in the clearest unobstructed composition for each shot; do not force identical centered framing when the story requires problem context, scale, mechanism, or result.

[SHOT TIMELINE (0s–10s)]
- Shot 1 (<start–end>, <hook / context>): ...
- Shot 2 (<start–end>, <product reveal / setup if needed>): ...
- Shot 3 (<start–end>, <complete demonstration + proof>): ...
- Shot 4 (<start–end>, <benefit / objection answer>): ...
- Final Shot (<start–10s>, <CTA / product hold>): ... Keep platform CTA safe zone unobstructed; duration must follow the approved storyboard.

[CAMERA & TRANSITION STYLE]
Purposeful commercial cinematography combining tight close-ups, steady POV demonstration, and smooth push-in/tracking movements connected by clean cuts and natural action transitions. Attention-grabbing opening, uninterrupted proof action long enough to understand, and a CTA hold only as long as needed for legibility.

[AUDIO]
Upbeat yet clean background music matched to the product mood, crisp realistic SFX synced to each cut and product action, no audio clipping. No on-camera speaking, no lip-sync, no generated speech; leave clean audio space for an off-screen Indonesian voice-over added in editing.

[NEGATIVE / AVOID]
No product morphing or color shift, no missing or invented parts, no logo distortion, no extra fingers, no human face (unless specified), no erratic camera spin, no burned-in text, no watermarks.
```

*(Sesuaikan jumlah baris `Shot 1` s.d. `Final Shot` pada `[SHOT TIMELINE (0s–10s)]` agar memetakan `1:1` terhadap timestamp bilangan bulat di `rapid-brief-and-storyboard.md` — `Clear`: `4–6` shot; `Hype`: `7–8` shot. Jika VO tidak digunakan, hapus kalimat tentang off-screen voice-over di `[AUDIO]`.)*

---

## 6. Editing & Final Assembly

1. **Impor 1 Klip & Verifikasi Durasi:** Masukkan klip hasil generasi `10` detik ke editor (`CapCut` / NLE). Pastikan durasi timeline tepat **`10` detik** (`00:00–00:10`). Jika klip sedikit lebih panjang dari `10` detik, lakukan *trim* **hanya di bagian akhir** (tanpa pemotongan per panel).
2. **Pengaturan Ekspor:** Rasio **`9:16`**, resolusi **`1080 × 1920 px`**, *frame rate* konsisten (`30 fps` atau `60 fps`), tanpa jeda kosong atau frame hitam.
3. **Sinkronisasi Audio & SFX:** Tambahkan *BGM* sesuai karakter produk, dan selaraskan *SFX* aksi tepat pada titik pergantian shot di storyboard utama.
4. **Penempatan Voice Over (`## Voice Over`):** Tempatkan rekaman/TTS VO tepat pada rentang waktu segmen yang tervalidasi di `_vo-timing.md` (mis. `00:00–00:04`, `00:04–00:08`, `00:08–00:10`) agar tidak menabrak pergantian visual; atur VO sekitar **`-6 dBFS`** dan turunkan BGM ke sekitar **`-22 dBFS`**. *(Lewati jika VO tidak digunakan.)*
5. **Penempatan Text Overlay & CTA (Maks. `2` Pergantian):**
   - Teks singkat manfaat utama (`1` kali tampil): zona aman `20%–32%` atau `60%–70%` tinggi layar tanpa menutupi produk.
   - CTA akhir (mengikuti timestamp storyboard, di atas zona `28%` bawah layar): gunakan kalimat singkat jujur (`"Cek di keranjang kuning!"` untuk TikTok atau `"Cek link di bio!"` untuk Reels) tanpa klaim kelangkaan/diskon palsu.

---

## 7. Quality Control Checklist

**Duration & Prompt**
- [ ] Total durasi storyboard utama tepat `10` detik (`00:00–00:10`, penjumlahan: `<... = 10>` detik) dengan seluruh panel memakai bilangan bulat (`≥ 1` detik).
- [ ] Jumlah panel sesuai varian terpilih (`Clear`: `4–6` panel; `Hype`: `7–8` panel).
- [ ] File `rapid-video-prompts.md` hanya berisi `1` master prompt `10` detik tanpa prompt per scene/panel.

**Storytelling & Pacing**
- [ ] Mengikuti creative route yang dipilih berdasarkan target pembeli, masalah/desire, objection, dan bukti yang tersedia.
- [ ] Hook relevan dengan target pembeli dan langsung terbaca secara visual/verbal.
- [ ] Demo menunjukkan mekanisme dan hasil penting tanpa dipotong sebelum dapat dipahami.
- [ ] CTA mudah dibaca, sesuai platform, dan didukung alasan yang telah dibuktikan.
- [ ] Pergantian teks overlay maksimal `2` kali dan tanpa pergantian shot yang membingungkan.

**Visual & Continuity**
- [ ] Produk 100% konsisten dengan referensi asli, tanpa deformasi.
- [ ] Continuity terjaga saat dibutuhkan; komposisi menempatkan bukti utama di area paling terbaca dan aman dari UI.
- [ ] Prompt gambar storyboard disusun dalam `1` lembar tunggal.

**Audio**
- [ ] Musik sesuai karakter produk, SFX tersinkronisasi pada pergantian shot, tanpa *audio clipping*.

**Output**
- [ ] Tidak ada tabel ringkasan babak & durasi terpisah; setiap panel hanya tampil satu kali.
- [ ] Urutan output tepat `1–9` dengan `## Voice Over` paling akhir.

**Voice Over**
- [ ] Hanya ada `1` versi VO terbaik (atau dinyatakan tidak digunakan dengan alasan singkat), selaras creative route, tanpa mengulang teks layar kata per kata.
- [ ] Bahasa Indonesia lisan natural, seluruh angka ditulis dengan huruf/kata (tanpa digit), dan tanpa klaim yang tidak terverifikasi.
- [ ] File internal `_vo-timing.md` lolos validasi `dialogue_timing.py` *(atau `N/A` bila VO tidak digunakan)*.

---

## Conversion Review Gate

- **Buyer Clarity:** <skor 1–5 dan alasan; minimal 4>
- **Proof Strength:** <skor 1–5 dan alasan; minimal 4>
- **AI Producibility:** <skor 1–5 dan alasan; minimal 4>
- **Status:** <LULUS / REVISI>

Jangan menyatakan hasil conversion rate dari penilaian editorial. Jika ada analytics pascapublikasi, analisis metrik funnel secara terpisah dan usulkan A/B test satu variabel utama.

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
