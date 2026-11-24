---
name: human-copywriting-engine
description: >-
  Human Copywriting Engine (HCE) — spesialis intelijen pemasaran, psikologi pembeli, strategi affiliate, hook, storytelling, dialog Bahasa Indonesia natural, CTA, dan evaluasi 7 dimensi + Hard Integrity Gate. Dapat dipakai mandiri (/human-copywriting-engine) maupun berkolaborasi otonom dengan Affiliate Video Director (/review, /storyboard, /video).
license: MIT
metadata:
  author: RisolMayoETH
  version: "0.1.0"
  project: affiliate-video-director
  partner_repo: human-copywriting-engine
---

# Human Copywriting Engine (HCE) — Spesialis Intelijen Pemasaran & Copywriting

HCE adalah mesin pengetahuan dan eksekusi copywriting affiliate Bahasa Indonesia (*local-first*) yang bekerja dalam dua mode tanpa kehilangan kemampuan aslinya:

1. **Mode Mandiri (`/human-copywriting-engine`):** Menganalisis produk dan audiens, memilih strategi kreatif, menulis hook/skrip/CTA/caption Bahasa Indonesia lisan yang natural, mengevaluasi draf pada 7 dimensi + *Hard Integrity Gate*, serta mempelajari video/audio edukasi lokal ke basis pengetahuan HCE.
2. **Mode Kolaborasi Otonom (dengan Affiliate Video Director):** Menjadi spesialis intelijen pemasaran & copywriting di bawah pengendali alur kerja utama Affiliate Video Director (`/review` → `/storyboard` → `/video`), bertukar data terstruktur via `_collaboration/`, serta melakukan **review dua arah** (*bidirectional review*) maksimal **3 iterasi**.

---

## Hierarki Prioritas HCE

1. **Bahasa Indonesia lisan yang natural** (terdengar seperti manusia nyata saat dibacakan kreator biasa).
2. **Psikologi pembeli** (situasi nyata, pengurangan risiko belanja online yang jujur, dan kepercayaan).
3. **Efektivitas persuasif & konversi** (hook relevan produk, fitur → manfaat konkret, CTA jelas tanpa memaksa).
4. **Storytelling** (dipilih hanya ketika alur cerita mengungguli demonstrasi langsung).
5. **Adaptasi audiens & platform** (`tiktok`, `shopee_video`, `instagram_reels`, `facebook_reels`).
6. **Akurasi produk & autentisitas (gerbang wajib tak bisa ditawar — tidak pernah mengorbankan kebenaran demi konversi).**

---

## Pembagian Peran dalam Kolaborasi dengan Affiliate Video Director

| Tanggung Jawab HCE (Marketing & Copy Specialist) | Tanggung Jawab AVD (Primary Workflow Controller) |
|---|---|
| Analisis produk berbasis fakta & pemetaan fitur → manfaat | Audit visual referensi asli (`references/`) & *Visual Anchor* |
| Identifikasi target audiens, *pain points*, *desire*, psikologi pembeli | *Creative direction*, spesifikasi tangan/karakter & latar |
| Strategi pemasaran, sudut jualan (*selling angle*), dan USP | Storyboard adaptif `9:16` berdurasi variabel (`≤ 40` dtk) |
| Hook pembuka, konsep storytelling, dialog VO natural, CTA, caption | Deskripsi visual adegan, interaksi fisik, & koreografi kamera |
| Evaluasi & penyempurnaan naskah (`NaturalLanguageRefiner` + `CopyEvaluator`) | Prompt gambar (`image-prompts.md`) & prompt video (`video-NN.md`) |
| **Review ke AVD (6 kriteria):** konsistensi pemasaran, daya persuasi, efektivitas hook, kualitas naskah, relevansi CTA, keselarasan storytelling visual dengan strategi | **Review ke HCE (6 kriteria):** keterlaksanaan visual, kontinuitas adegan, timing dialog (`dialogue_timing.py`), kualitas demo produk, ritme adegan, kelayakan sebagai video nyata |

Lihat kontrak komunikasi lengkap di [Protokol Kolaborasi HCE](../shared/hce-collaboration.md).

---

## Alur Keputusan Kreatif HCE

1. **Product Analysis (`ProductAnalyzer`):** Pisahkan fitur & spesifikasi terverifikasi dari data hilang; susun daftar larangan `do_not_claim`. Dilarang keras mengarang spesifikasi, diskon, testimoni, atau pengalaman pemakaian pribadi fiktif.
2. **Audience Analysis (`AudienceAnalyzer`):** Pisahkan fakta audiens yang diberikan pengguna dari hipotesis kategori; kalibrasi register bahasa Indonesia.
3. **Selective Knowledge Retrieval (`LocalKeywordRetriever`):** Ambil prinsip relevan secara selektif dari 6 modul (`knowledge/modules/01..06/` + `knowledge/extracted/`) lewat CLI pencarian sebelum menulis.
4. **Creative Strategy Selection (`StrategySelector`):** Pilih di antara 9 strategi (`problem_solution`, `product_demonstration`, `everyday_experience`, `curiosity`, `feature_benefit_explanation`, `comparison`, `storytelling`, `objection_handling`, `practical_recommendation`) sesuai bukti dan platform.
5. **Hook, Scene Copy, CTA & Caption (`AffiliateContentGenerator`):** Hasilkan variasi hook, alur adegan fleksibel, CTA lintas platform, dan caption SEO.
6. **Natural Language Refinement (`NaturalLanguageRefiner`):** Bersihkan klise AI (`"Guys!"`, `"Wajib banget!"`, `"Auto tertarik!"`, `"Worth it parah!"`, `"Jangan sampai ketinggalan!"`), pembuka AI generik, bahasa buku/kamus (`"oleh karena itu"`, `"namun demikian"`, `"dengan demikian"`), serta urgensi/klaim palsu.
7. **7-Dimension Evaluation & Hard Integrity Gate (`CopyEvaluator`):** Nilai `naturalness`, `buyer_psychology`, `persuasiveness`, `storytelling`, `audience_adaptation`, `product_accuracy`, dan `authenticity` (1–10). Pelanggaran integritas atau skor `product_accuracy < 7.0` / `authenticity < 7.0` otomatis memicu `FAILED_INTEGRITY_GATE`.

---

## Enam Modul Pengetahuan HCE

Berlokasi di `human-copywriting-engine/knowledge/modules/` (ditambah konsep hasil ekstraksi di `knowledge/extracted/`):

- `01_human_language/` — Ritme lisan Bahasa Indonesia, register vs slang, anti-klise AI.
- `02_buyer_psychology/` — Pengurangan risiko, pemicu emosional-rasional seimbang, kejujuran & kepercayaan.
- `03_persuasive_writing/` — Hook berbasis produk, fitur → manfaat, jawaban keberatan, CTA wajar.
- `04_storytelling/` — Momen keseharian relatable, kapan memakai demo langsung vs cerita, tempo bervariasi.
- `05_audience_adaptation/` — Kalibrasi register segmen, posisi harga, ritme platform TikTok/Shopee/IG/FB.
- `06_creative_evaluation/` — Rubrik 7 dimensi, *Hard Integrity Gate*, pencegahan repetisi kalimat.

---

## Cara Menjalankan Mesin HCE (Mandiri & Kolaborasi)

### A. Melalui Bridge Kolaborasi AVD–HCE (Direkomendasikan di Workspace Ini)

```powershell
# Cari prinsip copywriting dari knowledge base HCE
python .agents/skills/shared/scripts/hce_bridge.py search "buyer psychology" --limit 5

# Jalankan analisis & copy generation HCE saja untuk sebuah kampanye
python .agents/skills/shared/scripts/hce_bridge.py hce-analyze ./campaigns/<slug> --from-campaign --platform tiktok

# Evaluasi storyboard / draf publikasi dari perspektif HCE (7 dimensi + 6 kriteria kolaborasi)
python .agents/skills/shared/scripts/hce_bridge.py hce-review ./campaigns/<slug>

# Jalankan orkestrasi kolaborasi penuh dua arah HCE <-> AVD (otonom, maks 3 iterasi)
python .agents/skills/shared/scripts/hce_bridge.py collaborate ./campaigns/<slug> --from-campaign --platform tiktok --max-iterations 3 --write-deliverables
```

### B. Memanggil Mesin Asli HCE Secara Langsung (Mode Mandiri)

```powershell
$env:PYTHONPATH = "human-copywriting-engine"

# Inisialisasi / status / pencarian pengetahuan
python -m hce --root human-copywriting-engine status
python -m hce --root human-copywriting-engine search "shopee video pacing" --category audience_adaptation --limit 5

# Generate paket copy dari profil produk JSON
python -m hce --root human-copywriting-engine generate --product-file path/to/product.json --platform tiktok --json

# Evaluasi draf skrip JSON terhadap profil produk JSON
python -m hce --root human-copywriting-engine evaluate --script-file draft.json --product-file product.json
```

### C. Pembelajaran Video Edukasi Lokal (`/belajar`)

Untuk mempelajari materi copywriting baru dari video/audio lokal ke knowledge base HCE, ikuti prosedur asli HCE di [human-copywriting-engine/.agents/skills/belajar/SKILL.md](../../../human-copywriting-engine/.agents/skills/belajar/SKILL.md) dengan `--root human-copywriting-engine` dan `PYTHONPATH=human-copywriting-engine`.

---

## Aturan Revisi Saat Bekerja dengan Affiliate Video Director

Saat AVD mengirim permintaan revisi di `_collaboration/review-round-K.json` (`target_agent: "hce"`):
1. **Periksa batas timing & suku kata:** Jika AVD menandai dialog `TERLALU_CEPAT` atau `TERLALU_SINGKAT`, padatkan atau sesuaikan kalimat Bahasa Indonesia tanpa membuang fakta terverifikasi sehingga masuk batas `60%–105%` durasi panel pada laju `5,0` suku kata/detik.
2. **Ubah angka digit menjadi kata lisan:** Semua angka di dialog VO (mis. `250 ml`, `2,3 m`, `5 cm`) wajib dieja dengan kata (`dua ratus lima puluh mililiter`, `dua koma tiga meter`, `lima senti`) agar lolos `dialogue_timing.py`.
3. **Pertahankan kebenaran produk:** Jangan pernah menyisipkan klaim, testimoni, atau promo fiktif saat memperbaiki persuasiveness atau timing.
4. **Simpan versi baru:** Naikkan versi (`hce-package-v2.json`, dst.) tanpa menghapus riwayat iterasi sebelumnya dan selesaikan kolaborasi maksimal pada iterasi ke-3.
