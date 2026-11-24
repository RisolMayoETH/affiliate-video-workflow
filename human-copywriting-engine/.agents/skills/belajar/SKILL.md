---
name: belajar
description: >-
  Workflow belajar otomatis dari video atau audio lokal untuk Human Copywriting Engine (HCE).
  Gunakan skill ini setiap kali pengguna mengetik /belajar atau /belejar, melampirkan video/audio,
  atau meminta mempelajari materi dari folder data/incoming/ maupun workspace.
---

# Skill Belajar Video Copywriting HCE (`/belajar`)

Skill ini menjalankan pipeline pembelajaran lokal HCE secara penuh: memindai media, memotong dan mentranskrip audio secara lokal lewat FFmpeg + `faster-whisper`, mengekstrak konsep copywriting terstruktur lewat `file_exchange`, memvalidasi serta menyintesis dengan pengetahuan yang sudah ada, dan menyimpan hasilnya ke knowledge base HCE.

## Langkah Eksekusi Wajib

1. **Kumpulkan Media Baru (Tanpa Menghapus File Asli)**
   - Jika pengguna menyebut atau melampirkan file video/audio baru (`.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.mp3`, `.wav`, `.m4a`), atau ada file media baru di folder kerja yang belum masuk ke `data/incoming/`, **salin** (`Copy-Item`) ke `data/incoming/` tanpa mengubah atau menghapus file aslinya.
   - Jangan khawatir soal duplikat: HCE otomatis mendeteksi duplikat berdasarkan hash SHA-256 saat `scan`.

2. **Pindai & Transkrip Lokal**
   Jalankan perintah berikut di terminal Windows:
   ```powershell
   .\.venv\Scripts\python.exe -m hce scan
   .\.venv\Scripts\python.exe -m hce learn
   ```
   *(Jika komputer memakai CPU dan video sangat panjang, gunakan model `base` atau `tiny` sesuai `config/hce.toml`, dan jika sempat terhenti lanjutkan dengan `.\.venv\Scripts\python.exe -m hce retry`.)*

3. **Periksa Tugas Belajar yang Antre**
   Jalankan `.\.venv\Scripts\python.exe -m hce status` lalu baca semua file JSON yang berstatus `queued` di `data/processed/tasks/<task_id>.json`.

4. **Ekstrak Konsep Copywriting Secara Terstruktur**
   Untuk setiap `LearningTask` yang antre:
   - Baca `transcript_excerpt`, `source_id`, `source_timestamp`, dan `related_existing_concepts`.
   - Ekstrak hanya konsep yang benar-benar diajarkan atau dicontohkan dalam transkrip.
   - Patuhi skema di [extraction_result.schema.json](../../knowledge/schemas/extraction_result.schema.json) dan [concept.schema.json](../../knowledge/schemas/concept.schema.json):
     - Pilih `category` dari: `human_language`, `buyer_psychology`, `persuasive_writing`, `storytelling`, `audience_adaptation`, `creative_evaluation`.
     - Pilih `statement_type` secara jujur: `direct_instructor_statement`, `inferred_explanation`, `verified_fact`, `subjective_opinion`, atau `practical_demonstration`.
     - Jangan mengubah opini subjektif menjadi `verified_fact`.
     - Sertakan `source_id`, `source_timestamp`, `examples`, `counterexamples`, `limitations`, dan `related_concepts`.
   - Tulis file hasil ke `data/processed/results/<task_id>.json`.

5. **Validasi, Sintesis Lintas Sumber & Indeks**
   Jalankan kembali:
   ```powershell
   .\.venv\Scripts\python.exe -m hce learn
   ```
   Pastikan `config/hce.toml` memakai `[reasoning] adapter = "file_exchange"` agar HCE memvalidasi, mencegah duplikat, menjaga sudut pandang pembanding, menyimpan ke `knowledge/extracted/`, mencatat `knowledge/history/learning_history.jsonl`, dan memperbarui `knowledge/index.json`.

6. **Laporkan Hasil ke Pengguna**
   Jalankan:
   ```powershell
   .\.venv\Scripts\python.exe -m hce status
   .\.venv\Scripts\python.exe -m hce report --output data\processed\learning_report.md
   ```
   Sampaikan kepada pengguna dalam bahasa Indonesia: video apa yang dipelajari, daftar konsep yang berhasil diekstrak beserta timestamp sumbernya, apakah ada penggabungan/perbedaan pandangan dengan ilmu sebelumnya, dan apakah masih ada tugas yang tertunda.
