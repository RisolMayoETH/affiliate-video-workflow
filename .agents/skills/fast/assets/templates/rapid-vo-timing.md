# Internal VO Timing — <Nama Produk>

> **Internal — tidak ditampilkan ke pengguna.** File ini dipakai untuk validasi otomatis oleh `.agents/skills/shared/scripts/dialogue_timing.py`.

## Tabel Timing Dialog

| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |
|---|---|---|---|---|---|---|
| 1 | 00:00–00:04 | 4 | "<Dialog segmen 1 — angka ditulis huruf>" | 0 | 0.00 | CEK |
| 2 | 00:04–00:08 | 4 | "<Dialog segmen 2 atau [jeda]>" | 0 | 0.00 | CEK |
| 3 | 00:08–00:10 | 2 | "Cek di keranjang kuning!" | 7 | 1.40 | CEK |

> **Aturan Validasi:** Timestamp harus berurutan bilangan bulat dari `00:00` hingga `00:10` tanpa celah/tumpang-tindih. Target laju **`5,0` suku kata/detik** (rentang nyaman `4,5–5,5`, batas keras `6,0`), kepadatan tiap baris **`60%–105%`**, dan gunakan `"[jeda]"` untuk segmen hening tanpa VO. Gabungan dialog baris non-`[jeda]` dipisahkan spasi wajib identik dengan blok `**VOICE OVER — 10 DETIK**`.
