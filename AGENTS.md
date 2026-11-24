# Orchestration Workspace: Affiliate Video Director ↔ Human Copywriting Engine (HCE)

Proyek ini menggabungkan dua skill AI spesialis dalam satu alur kerja kolaboratif yang otonom:

1. **Affiliate Video Director (AVD — Primary Workflow Controller):**
   - Skill: `.agents/skills/review/SKILL.md`, `.agents/skills/storyboard/SKILL.md`, `.agents/skills/video/SKILL.md`, `.agents/skills/fast/SKILL.md`
   - Mengendalikan struktur kampanye (`./campaigns/<slug>/`), audit visual referensi asli, *creative direction*, storyboard adaptif `9:16` (`≤ 40` dtk), koreografi kamera, demonstrasi fisik, prompt gambar & video AI (`≤ 10` dtk/klip, **wajib detik bilangan bulat tanpa koma/desimal**), mode cepat `10` detik (`/fast`), serta paket publikasi akhir.

2. **Human Copywriting Engine (HCE — Marketing Intelligence & Copywriting Specialist):**
   - Skill: `.agents/skills/human-copywriting-engine/SKILL.md` (didukung repositori lokal `./human-copywriting-engine/`)
   - Menangani intelijen produk & pasar, identifikasi audiens & *pain points*, psikologi pembeli, strategi affiliate, USP, generasi hook, storytelling, dialog Bahasa Indonesia natural, CTA lintas platform, serta evaluasi 7 dimensi + *Hard Integrity Gate*.

---

## Aturan Eksekusi Kolaborasi Otonom

1. **Alur Otomatis Saat Pengguna Mengirim Produk:**
   - Cukup terima foto/screenshot/deskripsi/link produk seperti biasa — **jangan meminta persetujuan manual di tengah proses normal**.
   - Inisialisasi kampanye dengan `.agents/skills/shared/scripts/campaign_check.py --init ./campaigns <slug> --product "<Nama Produk>"`.
   - Jalankan kolaborasi otonom HCE ↔ AVD melalui `.agents/skills/shared/scripts/hce_bridge.py collaborate ./campaigns/<slug> ... --max-iterations 3 --write-deliverables`.
   - Periksa seluruh hasil dengan `campaign_check.py` (`--validate-timing --check-collaboration`) dan `dialogue_timing.py`, serta laporkan hasil akhir ke pengguna sesuai bahasa pengguna.

2. **Review Dua Arah (*Bidirectional Review*) & Batas Iterasi:**
   - **HCE mengevaluasi:** konsistensi pemasaran, persuasi, efektivitas hook, kualitas naskah & integritas fakta, relevansi CTA, dan keselarasan visual terhadap strategi.
   - **AVD mengevaluasi:** keterlaksanaan visual, kontinuitas adegan, timing dialog (`dialogue_timing.py`), kualitas demo produk, ritme adegan, dan kelayakan sebagai video nyata.
   - Revisi bertarget dikunci maksimal **3 iterasi** (`max_iterations = 3`), tanpa loop tak terbatas, dengan riwayat versi tersimpan di `_collaboration/` dan `_archive/`.

3. **Kemandirian Kedua Skill & Mode Cepat Tetap Utuh:**
   - Perintah AVD (`/review`, `/storyboard`, `/video`) tetap berjalan sebagaimana mestinya bila dipanggil per tahap.
   - Mode **Rapid Affiliate Review (`/fast`)** berjalan opsional untuk menghasilkan paket video cepat berdurasi tepat `10` detik di `./campaigns/<slug>/rapid-10s/` tanpa mengubah atau merusak alur utama maupun berkas kampanye standar.
   - Skill HCE (`/human-copywriting-engine` dan `/belajar` di `human-copywriting-engine/.agents/skills/belajar/SKILL.md`) tetap dapat dipanggil mandiri tanpa tergantung AVD.

4. **Integritas Data & Penanganan Kesalahan:**
   - Dilarang keras mengarang spesifikasi, diskon, kelangkaan palsu, atau testimoni di luar bukti produk.
   - Jangan pernah menimpa gambar di `01-product-review/references/` atau `02-generated-assets/`. Jika terjadi galat teknis, pertahankan seluruh file kampanye yang sudah ada dan laporkan error secara jujur.
