# Video Generation Prompt <NN> — <Nama Produk>

- **File:** `04-video/video-<NN>.md`
- **Durasi Klip:** `<durasi>` detik *(maks. `10.0` detik, kecuali generator terpilih secara eksplisit mendukung lebih)*
- **Rasio Aspek:** `9:16`
- **Panel Storyboard Dicakup:** `Adegan <X>` *(atau `Adegan <X–Y>` bila menggabungkan beberapa shot)*
- **Rentang Timestamp Storyboard:** `<00:00–00:08.5>`

## 1. Gambar Referensi Wajib Dilampirkan

> **Folder Siap Upload:** Seluruh foto acuan sudah disatukan ke `04-video/upload-assets/` dengan nama berurutan `1.<ext>..N.<ext>` dan `storyboard.png` *(atau `storyboard-sheet-*.png`)* agar mudah dicari saat mengunggah. (`01-product-review/references/` tetap menjadi **Otoritas #1 (`product-reference`)** untuk kebenaran fisik produk.)

1. `04-video/upload-assets/<X>.<ext>` *(jangkar Adegan `<X>` dari `02-generated-assets/...`)* — **Otoritas #2/#3/#4**: acuan visual awal segmen, tangan, dan latar.
2. `04-video/upload-assets/<Y>.<ext>` *(jangkar panel berikutnya di klip ini, jika ada)* — **Otoritas #2/#3/#4**: acuan shot lanjutan di dalam klip.
3. `04-video/upload-assets/storyboard.png` *(atau `storyboard-sheet-01.png`)* — **Otoritas #5 (`storyboard`)**: acuan komposisi frame dan urutan gerak panel `<X–Y>`.
4. `01-product-review/references/...` — **Otoritas #1 (`product-reference`)**: acuan mutlak bentuk, warna, material, dan proporsi produk.

## 2. Instruksi Kepatuhan Storyboard & Kunci Konsistensi

- **Strict Storyboard Adherence:** Follow panels `<X–Y>` of the approved storyboard exactly in framing, variable shot durations, action order, camera choreography, and marketing rhythm without inventing off-script scenes.
- **First-Frame Anchor (`0.0s`):** <Exact starting pose of product, hand/sleeve, camera angle, and lighting matching the previous clip's hand-off or opening hook.>
- **Product Consistency Lock:** ...
- **Hand / Character Consistency Lock:** ...
- **Environment & Lighting Lock:** ...

## 3. Master Video Prompt (Copy-Ready English)

```text
Continue the video. *(wajib dicantumkan untuk Klip 2, 3, 4, dst.; hapus baris ini pada Klip 1)*
Duration: <durasi> seconds. Vertical 9:16 commercial affiliate video.
Strictly match the attached original product reference photo for exact product shape, color, material, and hardware details, and follow panels <X-Y> of the attached storyboard for framing, rhythm, and sequence.

[STARTING FRAME (0.0s)]
<Describe exact opening composition, product position, hand position, and camera placement.>

[SCENE TIMELINE & PHYSICAL ACTIONS]
- 0.0s–X.Xs (Adegan <X> — <durasi panel>): ...
- X.Xs–Y.Ys (Adegan <X+1> — <durasi panel>): ...

[CAMERA CHOREOGRAPHY]
<Specific camera techniques with marketing/narrative purpose — e.g., slow dolly pull-back, macro rack focus, tracking movement, action-based transition; intentional rhythm variation.>

[LIGHTING & ATMOSPHERE]
<Consistent natural directional daylight, realistic household textures, safe framing within center 20%-68% vertical zone.>

[TRANSITIONS & ENDING FRAME]
Opening: <immediate in-action start / match cut from previous clip>. Mid-clip cuts: <purposeful cuts between packed panels>. Closing: <exact ending pose and motion bridging cleanly into next clip or clean CTA hold>.

[NEGATIVE INSTRUCTIONS]
No human face visible, no talking head, no floating or warped product parts, no color shift, no extra fingers, no aimless zooming or spinning 360 camera orbit, no burned-in text, no watermarks.
```

## 4. Arahan Audio & Dialog VO Bahasa Indonesia

- **Profil Pembicara:** Pengulas *off-camera*, tidak terlihat di kamera, suara Bahasa Indonesia natural, artikulasi jelas, ekspresif dan persuasif.
- **Segmen Dialog & SFX:**
  - `<00:00–00:02.5>` *(Adegan X — nada <emosi>)*: `"..."` | SFX: `<suara alami produk>`
  - *(Untuk panel singkat `1–2` dtk tanpa narasi, tulis `[jeda]` dan andalkan SFX produk yang kuat.)*

## 5. Hand-Off Kontinuitas ke Klip Berikutnya

- **Kondisi Frame Terakhir (`Last-Frame Anchor`):** <Posisi pasti produk, tangan, arah gerak, dan pencahayaan pada detik akhir klip ini.>
- **Arahan Penyambungan ke `video-<NN+1>.md`:** <Instruksi sambungan gerak, posisi kamera, dan kesinambungan cahaya untuk klip berikutnya — atau tandai sebagai akhir video dengan zona aman CTA.>

## Tabel Timing Dialog

| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |
|---|---|---|---|---|---|---|
| <X> | 00:00–00:02.5 | 2.5 | "..." | 0 | 0.00 | OK |
