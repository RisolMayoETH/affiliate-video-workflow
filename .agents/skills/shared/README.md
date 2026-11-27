# Shared Knowledge Engine — Affiliate Video Director

Direktori `skills/shared/` menyimpan seluruh pengetahuan bersama, template state kampanye, dan skrip validasi/cek yang digunakan oleh ketiga perintah (`/review`, `/storyboard`, `/video`).

## Mengapa Tidak Ada `SKILL.md` di Sini?

Sesuai spesifikasi Agent Skills, folder yang tidak memiliki `SKILL.md` tidak didaftarkan sebagai perintah atau skill mandiri oleh klien AI. Menempatkan pengetahuan bersama di `skills/shared/` memastikan:

1. **Tidak muncul sebagai perintah keempat** di menu `/` pengguna.
2. **Path relatif `../shared/<file>.md` tetap konsisten** baik saat diakses dari repositori ini, sebagai plugin Claude Code, maupun setelah disalin ke `~/.claude/skills/`, `.agents/skills/`, atau `~/.gemini/config/skills/`.
3. **Pemuatan selektif (Progressive Disclosure)**: tiap perintah hanya membaca modul pengetahuan yang relevan dengan tahapnya.

## Peta Pemuatan Pengetahuan (Load Map)

| Modul Pengetahuan | `/review` | `/storyboard` | `/video` |
|---|:---:|:---:|:---:|
| `product-intelligence.md` | Ya | - | - |
| `buyer-psychology.md` | Ya | - | - |
| `affiliate-marketing.md` | Ya | - | - |
| `conversion-copywriting.md` | Ya | Ya | Ya |
| `product-interaction.md` | Ya | Ya | Ya |
| `creative-direction.md` | Ya | Ya | - |
| `camera-language.md` | - | Ya | Ya |
| `dialogue-engine.md` | - | Ya | Ya |
| `visual-consistency.md` | Ya | Ya | Ya |
| `product-consistency-system.md` | Ya | Ya | Ya |
| `storyboard-principles.md` | - | Ya | - |
| `video-engineering.md` | - | - | Ya |
| `platform-optimization.md` | Ya | - | Ya |
| `campaign-memory.md` | Ya | Ya | Ya |
| `hce-collaboration.md` | Ya | Ya | Ya |

> **Catatan Mode Cepat (`/fast` & `/turbo`):** Kedua mode cepat juga wajib memuat `product-consistency-system.md` bersama `visual-consistency.md`, `camera-language.md`, dan `video-engineering.md`.

## Skrip & Template Bersama

- [templates/campaign.json](./templates/campaign.json) — Skema baku memori kampanye (termasuk blok `collaboration` opsional).
- [templates/product-identity-lock.md](./templates/product-identity-lock.md) — Template baku *Product Identity Sheet* (PCS v2.0).
- [scripts/campaign_check.py](./scripts/campaign_check.py) — Inisialisasi direktori kampanye & cek prasyarat per tahap (`--validate-timing`, `--check-collaboration`).
- [scripts/dialogue_timing.py](./scripts/dialogue_timing.py) — Penghitung suku kata Bahasa Indonesia & validator durasi dialog.
- [scripts/hce_bridge.py](./scripts/hce_bridge.py) — Jembatan eksekusi kolaborasi dua arah antara Affiliate Video Director dan Human Copywriting Engine (`search`, `hce-analyze`, `avd-review`, `hce-review`, `collaborate`).
