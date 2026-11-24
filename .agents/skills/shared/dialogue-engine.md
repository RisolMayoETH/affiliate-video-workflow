# Dialogue Engine — Mesin Dialog Bahasa Indonesia & Timing VO

Dialog *off-camera* adalah penggerak emosi dan konversi. Dialog harus terdengar seperti manusia Indonesia sungguhan yang sedang merekomendasikan barang berguna ke temannya—ekspresif, ringkas, tidak berbelit, dan pas dengan durasi variabel tiap panel.

## 1. Standar Kecepatan Bicara (Speaking Rate)

- **Laju Standar VO Ekspresif Indonesia:** **5,0 suku kata per detik** (*syllables per second*).
- **Rentang Nyaman:** **4,5 – 5,5 suku kata/detik**.
- **Batas Keras Maksimal:** **6,0 suku kata/detik** (di atas ini terdengar terburu-buru atau terpotong oleh mesin video/TTS).
- **Target Kepadatan Adegan:** Ucapan harus mengisi **60% – 105%** durasi adegan.
  - Di bawah 60% → terlalu banyak ruang hening canggung (*dead air*), kecuali memang ditandai hening sengaja.
  - Di atas 105% → kalimat menabrak transisi adegan berikutnya.
- **Adegan Hening Disengaja (`[jeda]`):** Sangat dianjurkan untuk *detail insert* cepat (`1–2` detik) atau momen transisi ASMR murni agar suara VO tidak terdengar terburu-buru. Tulis `[jeda]` di kolom dialog.

## 2. Aturan Menghitung Suku Kata (Konsisten dengan Validator)

Skrip `skills/shared/scripts/dialogue_timing.py` menggunakan aturan berikut:

1. **Kelompok Vokal:** Setiap gugus vokal (`a`, `i`, `u`, `e`, `o`) dalam satu kata dihitung 1 suku kata, **kecuali** diftong Indonesia (`ai`, `au`, `oi`, `ei`) yang dihitung sebagai 1 kesatuan bunyi.
   - Contoh: `sa-pu` = 2, `pa-kai` = 2 (`ai` = 1), `sa-rang` = 2, `la-ba-la-ba` = 4, `ti-dak` = 2.
2. **Dilarang Menulis Angka Digit di Dialog:**
   - **SALAH:** `"Panjangnya 2,3 m dan beratnya 500 gr"` → sulit dibaca konsisten & memicu peringatan validator!
   - **BENAR:** `"Panjangnya dua koma tiga meter"` atau `"Cuma seratus ribuan"`.
   - Validator menghitung tiap digit (`0-9`) sebagai 2 suku kata dan mengeluarkan **peringatan** agar angka ditulis dengan huruf kata.
3. **Nama Merek / Istilah Asing:** Tulis sealami mungkin sesuai pelafalan lisan atau pilih padanan Indonesia agar ritme napas terjaga.

## 3. Rumus Cepat & Panduan Durasi Variabel

$$\text{Target Suku Kata} \approx \text{Durasi Adegan (detik)} \times 5{,}0$$

Panduan kapasitas kata untuk berbagai durasi panel variabel:

| Durasi Panel | Target Suku Kata (60%–100%) | Maksimal Aman (105% @ 5.0 sk/dtk) | Perkiraan Panjang Kalimat / Penggunaan |
|---|---|---|---|
| **1,0 – 1,5 detik** | 3 – 7 suku kata *(atau `[jeda]`)* | 8 suku kata | 1–3 kata hentakan atau *detail insert* tanpa VO (`[jeda]`) |
| **2,0 detik** | 6 – 10 suku kata | 10 suku kata | 3–4 kata singkat (Hook cepat / transisi / CTA singkat) |
| **2,5 detik** | 8 – 12 suku kata | 13 suku kata | 3–5 kata pendek |
| **3,0 detik** | 9 – 15 suku kata | 16 suku kata | 5–6 kata (Reveal / CTA jelas) |
| **4,0 detik** | 12 – 20 suku kata | 21 suku kata | 6–9 kata (Before-after / validasi) |
| **5,0 detik** | 15 – 25 suku kata | 26 suku kata | 8–11 kata (Demonstrasi) |
| **6,0 detik** | 18 – 30 suku kata | 31 suku kata | 10–14 kata (Demonstrasi langkah lengkap) |

> **Tips Ritme Multi-Panel:** Pada panel cepat `1–2` detik, Anda boleh memakai `[jeda]` (membiarkan suara SFX produk bekerja) atau menyambungkan kalimat alami melintasi batas visual di dalam editor audio tanpa memaksakan kalimat panjang ke dalam 1,5 detik.

## 4. Gaya Bicara Natural & Ekspresif

- **Gunakan Bahasa Lisan:** Pakai *nggak*, *banget*, *nih*, *tuh*, *serius*, *jujur*, *kebetulan*, *langsung*, sesuai target audiens (hindari "produk ini sangat direkomendasikan untuk Anda miliki").
- **Tandai Penekanan Emosi:** Di arahan audio `/video`, jelaskan intonasi (misal: *nada gemas/relatable di hook → nada takjub/mantap saat pembuktian → nada antusias mengajak di CTA*).
- **Jangan Korbankan Kejelasan:** Jika satu adegan terasa terlalu padat, ringkas kata atau perpanjang durasi panel di storyboard alih-alih memaksa bicara cepat.

## 5. Format Baku `## Tabel Timing Dialog` & Urutan Timestamp

Baik `03-storyboard/storyboard.md` maupun setiap `04-video/video-XX.md` **wajib** memuat heading persis `## Tabel Timing Dialog` diikuti tabel Markdown berikut agar dapat diverifikasi otomatis oleh `dialogue_timing.py`:

```markdown
## Tabel Timing Dialog

| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |
|---|---|---|---|---|---|---|
| 1 | 00:00–00:02 | 2.0 | "Masih naik kursi buat sapu plafon?" | 11 | 2.20 | TERLALU_CEPAT |
```

*(Contoh di atas mengingatkan: `11 sk` dalam `2.0` dtk = `110%` akan ditolak; ringkas jadi `10 sk` atau gunakan durasi `2.5` dtk agar `OK`.)*

Aturan validasi timestamp yang wajib dipenuhi:
1. Rentang timestamp tiap baris (`MM:SS–MM:SS` atau `MM:SS.S–MM:SS.S`) harus berurutan tanpa celah (*gap*) maupun tumpang-tindih (*overlap*).
2. Selisih `selesai - mulai` pada timestamp harus cocok dengan kolom `Durasi (dtk)`.
3. Pada `storyboard.md`, timestamp harus dimulai dari `00:00` dan total durasi maksimal **40,0 detik**.
4. Seluruh dialog di kolom `Dialog (VO)` harus ditulis persis sama dengan kutipan dialog pada rincian adegan/generasi terkait.
