# Camera Language — Koreografi Kamera Komersial & Tujuan Naratif

Setiap gerakan kamera harus memiliki **alasan cerita dan penjualan**. Gerakan kamera tanpa tujuan membuat video AI terasa seperti *screensaver* atau render murah.

## 1. Kamus Teknik Kamera yang Bermakna

| Teknik | Mekanisme Visual | Tujuan Naratif / Affiliate | Contoh Penggunaan |
|---|---|---|---|
| **Tracking Shot** | Kamera ikut bergerak sejajar mengikuti pergerakan tangan atau produk | Menjaga fokus penonton pada aksi nyata produk dari titik A ke B | Mengikuti kepala sapu saat meluncur menyapu sudut plafon dari kiri ke kanan |
| **Dolly Push-In / Pull-Back** | Kamera bergerak maju (*push-in*) atau mundur (*pull-back*) di ruang fisik (bukan zoom digital) | *Push-in* membangun intensitas/fokus fitur; *pull-back* membuka konteks ruang atau panjang penuh | *Pull-back* perlahan dari pegangan tangan hingga memperlihatkan panjang tiang dua koma tiga meter penuh |
| **Macro Detail** | Lensa jarak sangat dekat dengan *depth of field* tipis | Membuktikan kualitas material, tekstur serat, jahitan, ukiran label, atau mekanisme pengunci | Makro jari memutar cincin pengunci tiang atau menyentuh kerapatan bulu microfiber |
| **Rack Focus** | Pergeseran fokus tajam dari objek depan ke belakang (atau sebaliknya) dalam satu shot | Mengalihkan perhatian dari masalah ke solusi tanpa potongan kasar | Fokus awal di sarang laba-laba plafon (buram di bawah), lalu fokus berpindah ke kepala sapu naik menghampirinya |
| **Match Cut** | Potongan antar adegan yang menyambung kesamaan bentuk, garis, atau arah gerak | Mempercepat tempo cerita dan menghubungkan dua tempat berbeda secara mulus | Tangan menepuk kepala sapu terlipat → match cut menjadi kepala sapu tertekuk tepat menyentuh sudut AC |
| **Whip Pan** | Geseran kamera cepat bermuatan *motion blur* terarah | Mengalihkan energi adegan, cocok untuk pergantian lokasi atau perbandingan sebelum–sesudah | Whip pan ke kanan dari sudut kotor menuju sudut bersih yang sudah disapu |
| **POV Movement** | Kamera bergerak mengikuti ayunan/sudut pandang pemakai langsung | Menciptakan rasa imersi ("gue sendiri yang lagi nyobain barangnya") | Kamera mendongak bersama tangan yang mengangkat gagang ke langit-langit |
| **Action-Based Transition** | Transisi dipicu oleh gerakan fisik objek (tangan melintas, pintu terbuka, barang diayun menutupi lensa) | Menyembunyikan sambungan antar generasi video AI agar terasa seperti satu alur mulus | Kepala microfiber menyapu mendekati lensa sebentar, lalu tersibak menampilkan ruangan rapi |

## 2. Daftar Gerakan yang Dilarang (Anti-Patterns)

Hindari menulis instruksi berikut di storyboard maupun prompt video:

- **Zoom-in / zoom-out generik berulang**: Membuat video terasa statis seperti *slideshow* foto yang diperbesar. Gunakan *dolly movement* fisik atau aksi tangan nyata.
- **Rotasi orbit 360 derajat tanpa alasan**: Kecuali pada *hero turntable reveal* singkat yang disengaja, orbit berputar terus-menerus sering merusak geometri produk (tulisan terbalik, bentuk pegangan berubah).
- **Handheld goyang berlebihan**: Menurunkan persepsi kualitas produk dan mengaburkan detail fitur. Gunakan *natural micro-handheld stability* saja saat POV.
- **Potongan adegan acak tanpa garis arah**: Melompat dari sudut kiri ke sudut kanan tanpa kesinambungan arah gerak tangan.

## 3. Memilih Posisi Kamera di Frame 9:16

- **Low-Angle Upward**: Untuk menunjukkan jangkauan tinggi (alat plafon, gorden, lemari atas).
- **High-Angle 45° Tabletop**: Untuk unboxing, tes tekstur skincare, kelengkapan paket gadget.
- **Eye-Level Mirror / Chest-Level**: Untuk try-on pakaian tanpa wajah atau semprotan parfum ke leher baju.
- **Over-the-Shoulder / First-Person POV**: Untuk memberi kedekatan emosional saat tangan langsung bekerja.

## 4. Aturan Penulisan di Storyboard & Prompt Video

Di setiap adegan, tuliskan pasangan wajib:
`Gerakan Kamera: [Nama Teknik] — Tujuan: [Alasan Naratif / Pembuktian]`.
Contoh: `Gerakan Kamera: Slow Dolly Pull-Back mendongak — Tujuan: membuktikan tiang tetap lurus dan tidak melengkung saat dipanjangkan penuh ke sudut plafon`.
