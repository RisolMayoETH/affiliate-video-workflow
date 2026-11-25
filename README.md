# Affiliate Video Workflow (AVD ↔ HCE)

Alur kerja terintegrasi otonom yang menggabungkan **Affiliate Video Director (AVD)** sebagai pengendali alur kerja utama dengan **Human Copywriting Engine (HCE)** sebagai spesialis intelijen pemasaran dan copywriting Bahasa Indonesia.

## Struktur Proyek

```text
.
├── AGENTS.md                                  # Aturan orkestrasi otonom AVD <-> HCE
├── .agents/
│   └── skills/
│       ├── review/                            # /review: Product & buyer intelligence, strategi, image prompts
│       ├── fast/                              # /fast: Mode Rapid Affiliate Review tepat 10 detik
│       ├── turbo/                             # /turbo: Mode Turbo Affiliate Review tepat 15 detik
│       ├── storyboard/                        # /storyboard: Storyboard adaptif 9:16 & loop review dua arah
│       ├── video/                             # /video: Segmentasi klip <=10s, video prompts & publishing package
│       ├── human-copywriting-engine/          # /human-copywriting-engine: Spesialis copywriting & HCE mandiri
│       └── shared/                            # Modul pengetahuan bersama, template, & skrip validator/bridge
│           ├── hce-collaboration.md           # Kontrak kolaborasi & review dua arah (maks 3 iterasi)
│           └── scripts/
│               ├── campaign_check.py          # Inisialisasi & validasi kesiapan tahap kampanye
│               ├── dialogue_timing.py         # Validator suku kata Bahasa Indonesia & urutan timestamp
│               ├── hce_bridge.py              # Bridge eksekusi kolaborasi otonom HCE <-> AVD
│               └── test_hce_integration.py    # Suite uji integrasi
└── human-copywriting-engine/                  # Mesin pengetahuan, refiner bahasa, & evaluator 7 dimensi HCE
```

## Penggunaan Cepat

### 1. Inisialisasi & Jalankan Kolaborasi Otonom

```powershell
# Inisialisasi kampanye baru
python .agents/skills/shared/scripts/campaign_check.py --init ./campaigns <slug-produk> --product "<Nama Produk>"

# Jalankan kolaborasi dua arah HCE <-> AVD secara otonom (maks. 3 iterasi)
python .agents/skills/shared/scripts/hce_bridge.py collaborate ./campaigns/<slug-produk> --from-campaign --platform tiktok --max-iterations 3 --write-deliverables

# Validasi hasil kampanye
python .agents/skills/shared/scripts/campaign_check.py ./campaigns/<slug-produk> --stage video --validate-timing --check-collaboration
python .agents/skills/shared/scripts/dialogue_timing.py ./campaigns/<slug-produk>/03-storyboard/storyboard.md
```

### 2. Mode Skill Mandiri

- **AVD per tahap:** `/review`, `/storyboard`, `/video`
- **Mode Rapid Affiliate Review (10 detik):** `/fast`
- **Mode Turbo Affiliate Review (15 detik):** `/turbo`
- **HCE mandiri:** `/human-copywriting-engine` atau `PYTHONPATH=human-copywriting-engine python -m hce --root human-copywriting-engine ...` (serta pembelajaran video lokal via `human-copywriting-engine/.agents/skills/belajar/SKILL.md`)

## Verifikasi Integrasi

```powershell
python -m unittest discover -s ".agents/skills/shared/scripts" -p "test_*.py" -v
```
