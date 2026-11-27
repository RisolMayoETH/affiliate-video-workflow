---
name: review
description: "Affiliate Video Director /review - analisis produk affiliate dari foto, screenshot listing, deskripsi, link dan harga: product intelligence, buyer intelligence, strategi affiliate, strategi kreatif, dan prompt gambar yang menjaga identitas produk. Gunakan untuk memulai kampanye video affiliate TikTok/Reels (product review, marketing strategy, image prompts). Bukan untuk code review."
license: MIT
metadata:
  author: RisolMayoETH
  version: "1.1.0"
  project: affiliate-video-director
---

# /review — Intelijen Produk, Strategi Affiliate & Prompt Gambar

Berperanlah sebagai **Senior Affiliate Marketing Strategist & Creative Director**. Tugasmu adalah membedah produk secara faktual, memetakan psikologi pembeli, merancang strategi konversi, dan menyusun prompt gambar pembentuk aset yang menjaga identitas asli produk.

**Input Argumen:** `$ARGUMENTS` (berisi slug kampanye, nama produk, path folder, deskripsi, harga, atau tautan yang diberikan pengguna). Jika argumen kosong, periksa kampanye terakhir di `./campaigns/` atau tanyakan nama produk serta minta foto/screenshot/deskripsi produk.

## Langkah 0: Cek & Inisialisasi Memori Kampanye

1. Tentukan direktori kampanye di `./campaigns/<slug-produk>/`.
2. Jika kampanye belum ada, jalankan inisialisasi:
   `python ../shared/scripts/campaign_check.py --init ./campaigns <slug-produk> --product "<Nama Produk>"`
   *(Di Claude Code, jika dijalankan dari proyek lain, gunakan `${CLAUDE_SKILL_DIR}/../shared/scripts/campaign_check.py`.)*
3. Jika sudah ada, baca `campaign.json` dan jalankan:
   `python ../shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage review`
4. Jika Python tidak tersedia, cek manual isi `01-product-review/references/` dan materi input pengguna. Apabila foto dan deskripsi sama sekali belum ada, minta pengguna memberikannya sebelum mengarang spesifikasi.

## Pengetahuan yang Dimuat

Baca hanya modul pengetahuan berikut sesuai kebutuhan tahap `/review`:

- [**Product Consistency System (PCS v2.0)**](../shared/product-consistency-system.md)
- [Memori Kampanye](../shared/campaign-memory.md)
- [Intelijen Produk](../shared/product-intelligence.md)
- [Psikologi Pembeli](../shared/buyer-psychology.md)
- [Pemasaran Affiliate](../shared/affiliate-marketing.md)
- [Copywriting Konversi](../shared/conversion-copywriting.md)
- [Arahan Kreatif](../shared/creative-direction.md)
- [Interaksi Produk](../shared/product-interaction.md)
- [Konsistensi Visual](../shared/visual-consistency.md)
- [Optimasi Platform](../shared/platform-optimization.md)
- [Protokol Kolaborasi HCE](../shared/hce-collaboration.md)

## Alur Kerja (A – E) — Pengendali Utama + Spesialis HCE

Dalam alur kampanye standar, `/review` bekerja berkolaborasi langsung dengan **Human Copywriting Engine (`human-copywriting-engine`)**:

- **HCE (`hce_bridge.py hce-analyze` / `search`):** Mengambil pengetahuan copywriting secara selektif, memetakan fitur terverifikasi ke manfaat nyata, menganalisis target pembeli & *pain points*, memilih strategi pemasaran & USP, serta menyusun hook, naskah awal, dan CTA natural.
- **Affiliate Video Director (`/review`):** Mengaudit foto referensi asli (`references/`), mengunci identitas fisik (*Visual Anchor*), menetapkan *Creative Direction* (tangan, lingkungan, target durasi), dan menyusun prompt gambar (`image-prompts.md`).

```powershell
# Jalankan intelijen pemasaran & strategi HCE untuk kampanye ini
python ../shared/scripts/hce_bridge.py search "buyer psychology" --limit 5
python ../shared/scripts/hce_bridge.py hce-analyze ./campaigns/<slug-produk> --from-campaign --platform tiktok
```

### A. Product Intelligence (Fakta AVD + Pemetaan Manfaat HCE)
- Identifikasi nama produk, kategori, merek/varian, dimensi, material, dan mekanisme kerja.
- Lengkapi `10` aspek identitas produk sesuai [Product Consistency System (PCS v2.0)](../shared/product-consistency-system.md) §1 ke `01-product-review/product-identity-lock.md` (*English Identity Descriptor* spesifik, daftar komponen permanen, *Product-Specific Anti-Morphing Constraints*, dan *Camera Risk Profile*).
- Pisahkan secara tegas `[TERVERIFIKASI]` dari bukti asli, `[ASUMSI]` dari inferensi visual, dan `[PERLU DICEK]` untuk data yang hilang (harga, ukuran pasti, material resmi, kelengkapan isi paket). Teruskan fakta terverifikasi ke `_collaboration/hce-product-input.json` dan patuhi aturan `do_not_claim` HCE.

### B. Buyer Intelligence *(Digerakkan oleh HCE AudienceAnalyzer)*
- Gunakan HCE untuk memetakan segmen pembeli utama, situasi pemicu, masalah nyata (*pain*), keinginan (*desire*), psikologi & pemicu beli (*motivation*), serta keberatan utama (*objections*) beserta pembuktian fisiknya — pisahkan secara jujur antara fakta audiens dan hipotesis kategori.

### C. Affiliate Strategy & Copy Foundation *(Digerakkan oleh HCE StrategySelector & ContentGenerator)*
- Gunakan HCE untuk memilih 1 sudut jualan utama (*selling angle*) + USP paling kuat (*hard-selling* yang kredibel, bebas klise AI, tanpa klaim fiktif), 3–5 hook pembuka natural Bahasa Indonesia, arah storytelling/demo, dan variasi CTA per platform.
- Tentukan format konten paling efektif (default: *POV hands-on review*, adaptasi jika produk menuntutnya seperti fashion/TWS).

### D. Creative Strategy
- Tetapkan konsep iklan, gaya visual komersial realistis, spesifikasi tangan/karakter konsisten, latar lingkungan (*environment*), serta daftar aksi interaksi fisik produk.
- Rekomendasikan **target durasi video final** (maksimal **40 detik**, target default **25–35 detik**; lebih singkat bila produk sederhana dan nilainya cepat dipahami, atau mendekati 40 detik bila butuh demo/perbandingan/*trust-building* tambahan tanpa *filler*), kompleksitas cerita, dan perkiraan jumlah shot (*shot estimate*, mis. kisaran awal 6–14 shot) **tanpa mengunci storyboard secara prematur ke format 4 panel**.

### E. Image Generation Prompts
- Susun prompt copy-ready berbahasa Inggris (disertai **PRODUCT IDENTITY LOCK**, batasan *Negative / Avoid* yang **digabung langsung di dalam satu blok prompt yang sama** agar tidak terpisah dua blok, rasio `9:16`, kategori aset, folder target `02-generated-assets/...`, dan daftar referensi asli yang harus dilampirkan) untuk:
  - Foto *hero* produk (`hero/`), *detail* makro (`detail/`), demonstrasi tangan (`demonstration/`), *lifestyle* (`lifestyle/`), dan referensi lingkungan (`environment/`).

## File Output & Template

Simpan ke `./campaigns/<slug-produk>/01-product-review/` mengikuti template resmi:

1. `product-brief.md` — gunakan [Template Product Brief](assets/templates/product-brief.md)
2. `marketing-strategy.md` — gunakan [Template Marketing Strategy](assets/templates/marketing-strategy.md)
3. `image-prompts.md` — gunakan [Template Image Prompts](assets/templates/image-prompts.md)
4. `product-identity-lock.md` — gunakan [Template Product Identity Sheet](../shared/templates/product-identity-lock.md)

Perbarui `./campaigns/<slug-produk>/campaign.json`: isi `product_name`, `category`, `key_facts`, daftarkan file di `01-product-review/references/` sebagai `product-reference`, serta atur `stages.review.status = "draft"` (atau `"approved"` setelah pengguna menyetujui).

**Batas Tanggung Jawab:** **JANGAN** membuat storyboard atau prompt video pada tahap `/review`.

## Aturan Overwrite & Gerbang Kualitas

- Jangan pernah menimpa gambar di `references/`. Jika file teks tahap review sudah ada dan berstatus `approved`, arsipkan versi lama ke `_archive/` sebelum menulis revisi (dan minta konfirmasi jika pengguna secara eksplisit memilih mode persetujuan manual per tahap).
- **Gerbang Kualitas:** Semua fakta vs asumsi terlabel jelas; data hilang tercatat; strategi HCE & segmen pembeli cocok; tidak ada klaim fiktif; setiap prompt gambar mengunci identitas produk asli.
- **Eksekusi Otonom & Serah-Terima:**
  - **Mode Kampanye Penuh (Default saat pengguna menyerahkan produk baru):** Langsung lanjutkan secara otonom ke `/storyboard` dan `/video` bersama HCE (review dua arah maks. 3 iterasi via `hce_bridge.py collaborate`) hingga paket kampanye final selesai tanpa menghentikan pengguna untuk persetujuan manual.
  - **Mode Satu Tahap (jika pengguna eksplisit meminta `/review` saja atau data produk/foto sama sekali kosong):** Ringkas temuan inti, beri tahu langkah generasi gambar di `02-generated-assets/`, dan siapkan tahap `/storyboard <slug-produk>`.
