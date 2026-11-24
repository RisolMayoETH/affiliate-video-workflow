# Aturan Workspace Human Copywriting Engine (HCE)

1. **Pemicu `/belajar` dan `/belejar`**:
   - Setiap kali pengguna mengetik `/belajar` atau `/belejar` (baik sambil melampirkan video, menyebut path file/folder, maupun merujuk ke video di `data/incoming/` atau folder kerja), **segera baca dan jalankan prosedur lengkap pada skill** `.agents/skills/belajar/SKILL.md`.
   - Jangan pernah memodifikasi atau menghapus video sumber asli pengguna; cukup salin file baru ke `data/incoming/` bila belum ada di sana, lalu jalankan `scan`, `learn`, ekstraksi konsep ke `data/processed/results/`, dan `learn` lagi hingga pengetahuan tersimpan di `knowledge/extracted/`.

2. **Pemicu Penulisan, Perbaikan & Evaluasi Copy Affiliate**:
   - Ketika pengguna meminta membuat, memperbaiki, atau mengevaluasi skrip video pendek, hook, CTA, atau caption affiliate Indonesia (TikTok, Shopee Video, Instagram Reels, Facebook Reels), aktifkan skill `.agents/skills/human-copywriting-engine/SKILL.md` dan ambil referensi pengetahuan secara selektif dengan `.\.venv\Scripts\python.exe -m hce search "<topik>"`.
   - Dilarang keras mengarang spesifikasi, diskon fiktif, kelangkaan buatan, testimoni, atau pengalaman pemakaian pribadi yang tidak ada di data produk.

3. **Bahasa Komunikasi**:
   - Jika pengguna menulis dalam bahasa Indonesia, selalu jawab dengan bahasa Indonesia yang jelas, natural, dan terstruktur.
