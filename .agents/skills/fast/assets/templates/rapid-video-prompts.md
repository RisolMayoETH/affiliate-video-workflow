# Rapid Video Prompt, QC & Voice Over (10s) — <Nama Produk>

- **Slug Kampanye:** `<slug-produk>`
- **Mode:** `Rapid Affiliate Review v1.2` (`/fast`)
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
   - CTA akhir (`00:08–00:10`, di atas zona `28%` bawah layar): gunakan kalimat singkat jujur (`"Cek di keranjang kuning!"` untuk TikTok atau `"Cek link di bio!"` untuk Reels) tanpa klaim kelangkaan/diskon palsu.

---

## 7. Quality Control Checklist

**Duration & Prompt**
- [ ] Total durasi storyboard utama tepat `10` detik (`00:00–00:10`, penjumlahan: `<... = 10>` detik) dengan seluruh panel memakai bilangan bulat (`≥ 1` detik).
- [ ] Jumlah panel sesuai varian terpilih (`Clear`: `4–6` panel; `Hype`: `7–8` panel).
- [ ] File `rapid-video-prompts.md` hanya berisi `1` master prompt `10` detik tanpa prompt per scene/panel.

**Storytelling & Pacing**
- [ ] Mengikuti struktur 4 babak (`Hook → Demo → Hasil/Manfaat → Hero + CTA`) dengan fokus `1` selling point utama.
- [ ] Hook menarik di `00:00–00:01` dan produk terlihat jelas.
- [ ] Demo berdurasi `≥ 2` detik dalam satu aksi utuh tanpa terpotong.
- [ ] Penutup Hero + CTA ditahan `≥ 2` detik dengan tujuan yang jelas.
- [ ] Pergantian teks overlay maksimal `2` kali dan tanpa pergantian shot yang membingungkan.

**Visual & Continuity**
- [ ] Produk 100% konsisten dengan referensi asli, tanpa deformasi.
- [ ] Tangan/lengan baju, latar, cahaya konsisten, dan produk selalu di zona tengah layar.
- [ ] Prompt gambar storyboard disusun dalam `1` lembar tunggal.

**Audio**
- [ ] Musik sesuai karakter produk, SFX tersinkronisasi pada pergantian shot, tanpa *audio clipping*.

**Output**
- [ ] Tidak ada tabel ringkasan babak & durasi terpisah; setiap panel hanya tampil satu kali.
- [ ] Urutan output tepat `1–8` dengan `## Voice Over` paling akhir.

**Voice Over**
- [ ] Hanya ada `1` versi VO terbaik (atau dinyatakan tidak digunakan dengan alasan singkat), selaras 4 babak, tanpa mengulang teks layar kata per kata.
- [ ] Bahasa Indonesia lisan natural, seluruh angka ditulis dengan huruf/kata (tanpa digit), dan tanpa klaim yang tidak terverifikasi.
- [ ] File internal `_vo-timing.md` lolos validasi `dialogue_timing.py` *(atau `N/A` bila VO tidak digunakan)*.

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
