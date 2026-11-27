# Image Generation Prompts — <Nama Produk>

> **Aturan Otoritas:** Seluruh prompt di bawah harus melampirkan foto referensi produk asli dari `01-product-review/references/` sebagai sumber kebenaran nomor satu, serta menyalin **English Identity Descriptor** spesifik dari `01-product-review/product-identity-lock.md` (jangan memakai deskripsi kategori generik). Simpan hasil generate ke subdirektori target di `02-generated-assets/` (format `.png` atau `.jpg` keduanya diterima).

## Ringkasan Aset yang Dibutuhkan

| ID | Jenis Foto | Kategori Otoritas | Target Simpan | Referensi Wajib Dilampirkan | Rasio |
|---|---|---|---|---|---|
| `IMG-01` | Hero Product Shot | `generated-lifestyle` | `02-generated-assets/hero/hero-01.png` | Foto referensi asli | `9:16` |
| `IMG-02` | Macro Detail Shot | `generated-lifestyle` | `02-generated-assets/detail/detail-01.png` | Foto referensi asli | `9:16` |
| `IMG-03` | Hands-On Demonstration | `product-demonstration` | `02-generated-assets/demonstration/demo-01.png` | Foto referensi asli | `9:16` |
| `IMG-04` | Lifestyle / Environment | `generated-lifestyle` | `02-generated-assets/lifestyle/lifestyle-01.png` | Foto referensi asli | `9:16` |

---

## IMG-01 — Product Hero Shot
- **Kategori:** `generated-lifestyle`
- **Target Simpan:** `02-generated-assets/hero/hero-01.png`
- **Referensi Wajib:** `01-product-review/references/...`
- **Rasio:** `9:16`

**Copy-Ready Prompt (English):**
```text
[PRODUCT IDENTITY LOCK]: <Paste specific English Identity Descriptor and exact component list from 01-product-review/product-identity-lock.md matching the attached original product reference photo.>
Commercial 9:16 vertical hero photography of <product> in <natural Indonesian home/lifestyle setting>. Clean composition centered in the 20%-68% vertical safe zone. Soft directional daylight, crisp realistic textures, shallow depth of field, authentic commercial look, no text overlay, no watermark.
Negative / Avoid: <product-specific anti-morphing constraints from product-identity-lock.md>, altered product shape, wrong color, deformed mechanism, extra parts, floating text, watermark, logo distortion, plastic CGI look, human face.
```

---

## IMG-02 — Product Macro Detail Shot
- **Kategori:** `generated-lifestyle`
- **Target Simpan:** `02-generated-assets/detail/detail-01.png`
- **Referensi Wajib:** `01-product-review/references/...`
- **Rasio:** `9:16`

**Copy-Ready Prompt (English):**
```text
[PRODUCT IDENTITY LOCK]: <Paste specific English Identity Descriptor from 01-product-review/product-identity-lock.md, emphasizing exact close-up material, texture, logo/label, and mechanical details.>
Vertical 9:16 macro commercial photograph focusing on <key mechanical/material detail>. Natural sidelight revealing realistic texture, crisp focus on product craft, softly blurred background.
Negative / Avoid: <product-specific anti-morphing constraints>, blurry texture, melted details, altered hardware, text artifacts, watermark.
```

---

## IMG-03 — Hands-On Demonstration Shot
- **Kategori:** `product-demonstration`
- **Target Simpan:** `02-generated-assets/demonstration/demo-01.png`
- **Referensi Wajib:** `01-product-review/references/...`
- **Rasio:** `9:16`

**Copy-Ready Prompt (English):**
```text
[PRODUCT IDENTITY LOCK]: <Paste specific English Identity Descriptor and exact component list from 01-product-review/product-identity-lock.md.>
[HAND/CHARACTER LOCK]: natural Indonesian adult hand, clean nails, consistent light neutral cotton sleeve, no visible face.
First-person POV 9:16 vertical shot showing hand naturally performing <specific physical interaction with product> inside <environment>. Realistic grip physics, accurate scale, soft daylight, no text.
Negative / Avoid: <product-specific anti-morphing constraints>, extra fingers, deformed hand, floating grip, face visible, wrong product scale, text overlay, watermark.
```

---

## IMG-04 — Lifestyle & Environment Reference
- **Kategori:** `generated-lifestyle`
- **Target Simpan:** `02-generated-assets/lifestyle/lifestyle-01.png` *(atau `environment/env-01.png`)*
- **Referensi Wajib:** `01-product-review/references/...`
- **Rasio:** `9:16`

**Copy-Ready Prompt (English):**
```text
[PRODUCT IDENTITY LOCK]: <Paste specific English Identity Descriptor and exact component list from 01-product-review/product-identity-lock.md.>
Vertical 9:16 realistic Indonesian home environment shot showing <product> ready for use in context. Warm natural daylight, uncluttered background, realistic household textures, 9:16 vertical safe framing.
Negative / Avoid: <product-specific anti-morphing constraints>, cluttered background, surreal lighting, altered product geometry, text, watermark, human face.
```
