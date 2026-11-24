#!/usr/bin/env python3
"""Inisialisasi dan validasi kesiapan serta timing adaptif memori kampanye Affiliate Video Director."""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import dialogue_timing  # noqa: E402
except ImportError:  # Paket standalone /review tidak menyertakan dialogue_timing.py
    dialogue_timing = None  # type: ignore[assignment]

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VIDEO_EXTS = {".mp4", ".mov", ".webm"}
IGNORED_FILENAMES = {".gitkeep", ".ds_store", "thumbs.db"}

MAX_FINAL_DURATION = 40.0
DEFAULT_MAX_CLIP_DURATION = 10.0

CTA_KEYWORDS = (
    "cta",
    "keranjang",
    "checkout",
    "link di bio",
    "link produk",
    "tautan produk",
    "komentar",
    "klik link",
    "beli sekarang",
    "order sekarang",
    "check out",
)

CAMPAIGN_SUBDIRS = [
    "01-product-review/references",
    "02-generated-assets/hero",
    "02-generated-assets/detail",
    "02-generated-assets/demonstration",
    "02-generated-assets/lifestyle",
    "02-generated-assets/environment",
    "02-generated-assets/video-references",
    "03-storyboard",
    "04-video",
    "04-video/upload-assets",
    "05-publishing",
    "_collaboration",
    "_archive",
]


def _today_iso() -> str:
    return datetime.date.today().isoformat()


def _load_campaign_template() -> dict:
    tpl_path = Path(__file__).resolve().parent.parent / "templates" / "campaign.json"
    if tpl_path.is_file():
        return json.loads(tpl_path.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0",
        "slug": "",
        "product_name": "",
        "category": "",
        "language": "id",
        "aspect_ratio": "9:16",
        "platforms": ["tiktok", "facebook-reels", "instagram-reels"],
        "created": "",
        "updated": "",
        "key_facts": [],
        "stages": {
            "review": {
                "status": "not-started",
                "files": [],
                "recommended_duration": None,
                "estimated_panels": None,
            },
            "storyboard": {
                "status": "not-started",
                "files": [],
                "scenes": [],
                "total_duration": 0,
                "image": None,
                "images": [],
            },
            "video": {
                "status": "not-started",
                "max_clip_duration": DEFAULT_MAX_CLIP_DURATION,
                "generator_supports_extended_clip": False,
                "generations": [],
            },
            "publishing": {"status": "not-started", "files": []},
        },
        "assets": [],
        "decisions": [],
        "collaboration": {
            "enabled": True,
            "partner_skill": "human-copywriting-engine",
            "status": "not-started",
            "iterations": 0,
            "max_iterations": 3,
            "converged": False,
            "hce_score": None,
            "avd_score": None,
            "retrieved_knowledge_ids": [],
            "artifacts_dir": "_collaboration",
            "version_history": [],
        },
    }


def init_campaign(campaigns_root: Path, slug: str, product_name: str, category: str = "") -> int:
    """Buat struktur direktori kampanye baru dan file campaign.json."""
    target = campaigns_root / slug
    if target.exists():
        print(
            f"[GAGAL] Direktori kampanye sudah ada: {target}\n"
            "Untuk melindungi aset pengguna, inisialisasi dibatalkan.",
            file=sys.stderr,
        )
        return 1

    for rel in CAMPAIGN_SUBDIRS:
        (target / rel).mkdir(parents=True, exist_ok=True)

    today = _today_iso()
    data = _load_campaign_template()
    data["slug"] = slug
    data["product_name"] = product_name
    if category:
        data["category"] = category
    data["created"] = today
    data["updated"] = today

    (target / "campaign.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] Kampanye '{slug}' berhasil diinisialisasi di: {target}")
    print("Langkah berikutnya:")
    print(f"  1. Simpan foto asli produk atau screenshot listing ke: {target / '01-product-review' / 'references'}")
    print(f"  2. Jalankan perintah /review {slug}")
    return 0


def _list_files(folder: Path, extensions: set[str] | None = None) -> list[Path]:
    if not folder.is_dir():
        return []
    items = []
    for p in sorted(folder.rglob("*")):
        if not p.is_file():
            continue
        if p.name.lower() in IGNORED_FILENAMES:
            continue
        if extensions is not None and p.suffix.lower() not in extensions:
            continue
        items.append(p)
    return items


def _nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def collect_inventory(campaign_dir: Path) -> dict[str, list[str]]:
    """Kelompokkan file aset kampanye berdasarkan 5 kategori hierarki otoritas."""
    def rel_list(paths: list[Path]) -> list[str]:
        return [p.relative_to(campaign_dir).as_posix() for p in paths]

    refs = _list_files(campaign_dir / "01-product-review" / "references")
    lifestyle_dirs = ["hero", "detail", "lifestyle", "environment"]
    lifestyle_files: list[Path] = []
    for sub in lifestyle_dirs:
        lifestyle_files.extend(_list_files(campaign_dir / "02-generated-assets" / sub, IMAGE_EXTS))

    demo_files = _list_files(campaign_dir / "02-generated-assets" / "demonstration", IMAGE_EXTS)
    video_ref_files = _list_files(campaign_dir / "02-generated-assets" / "video-references", IMAGE_EXTS)
    storyboard_imgs = _list_files(campaign_dir / "03-storyboard", IMAGE_EXTS)

    return {
        "product-reference": rel_list(refs),
        "generated-lifestyle": rel_list(lifestyle_files),
        "product-demonstration": rel_list(demo_files),
        "video-reference": rel_list(video_ref_files),
        "storyboard": rel_list(storyboard_imgs),
    }


def _has_cta(campaign_data: dict, sb_text: str, pub_text: str = "") -> bool:
    """Periksa keberadaan CTA di storyboard, metadata scenes, atau publishing package."""
    if campaign_data.get("cta_optional"):
        return True
    combined_parts = [sb_text, pub_text]
    for sc in campaign_data.get("stages", {}).get("storyboard", {}).get("scenes", []):
        for key in ("title", "purpose", "marketing_purpose", "dialog", "on_screen_text"):
            val = sc.get(key)
            if isinstance(val, str):
                combined_parts.append(val)
    combined = "\n".join(combined_parts).lower()
    if re.search(r"\bcta\b", combined):
        return True
    return any(kw != "cta" and kw in combined for kw in CTA_KEYWORDS)


def _validate_scene_timestamps(scenes: list[dict], prefix: str) -> list[str]:
    """Validasi field timestamp opsional pada daftar scenes di campaign.json."""
    if dialogue_timing is None:
        return []
    errors: list[str] = []
    prev_end: float | None = None
    for idx, sc in enumerate(scenes, start=1):
        ts = sc.get("timestamp")
        if not ts:
            continue
        dur = float(sc.get("duration", 0))
        sid = sc.get("id", idx)
        try:
            start_s, end_s = dialogue_timing.parse_timestamp_range(str(ts))
            if abs((end_s - start_s) - dur) > dialogue_timing.TIMESTAMP_TOLERANCE:
                errors.append(
                    f"{prefix}/campaign.json: scene {sid} timestamp '{ts}' ({end_s - start_s:.2f}s) "
                    f"!= duration ({dur:.2f}s)"
                )
            if prev_end is None and abs(start_s) > dialogue_timing.TIMESTAMP_TOLERANCE:
                errors.append(
                    f"{prefix}/campaign.json: scene {sid} timestamp awal harus 00:00 (ditemukan '{ts}')"
                )
            elif prev_end is not None:
                if start_s < prev_end - dialogue_timing.TIMESTAMP_TOLERANCE:
                    errors.append(f"{prefix}/campaign.json: scene {sid} timestamp overlap ('{ts}')")
                elif start_s > prev_end + dialogue_timing.TIMESTAMP_TOLERANCE:
                    errors.append(f"{prefix}/campaign.json: scene {sid} timestamp gap ('{ts}')")
            prev_end = end_s
        except ValueError as exc:
            errors.append(f"{prefix}/campaign.json: scene {sid} {exc}")
    return errors


def validate_campaign_timing(
    campaign_dir: Path,
    max_total_duration: float = MAX_FINAL_DURATION,
    prefix: str | None = None,
) -> list[str]:
    """Validasi aturan durasi adaptif (<=40s), panel bervariasi, batas klip 10s, timestamp, dialog, dan CTA."""
    errors: list[str] = []
    label = prefix or campaign_dir.name
    if dialogue_timing is None:
        return [f"{label}: modul dialogue_timing.py diperlukan untuk validasi timing penuh"]
    cj_path = campaign_dir / "campaign.json"
    if not cj_path.is_file():
        return [f"{label}: campaign.json tidak ditemukan"]

    try:
        cj = json.loads(cj_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label}/campaign.json: JSON rusak ({exc})"]

    sb_stage = cj.get("stages", {}).get("storyboard", {})
    scenes = sb_stage.get("scenes", [])
    total_dur = float(sb_stage.get("total_duration", 0))

    if total_dur <= 0:
        errors.append(f"{label}/campaign.json: stages.storyboard.total_duration harus > 0")
    elif total_dur > max_total_duration + 1e-6:
        errors.append(
            f"{label}/campaign.json: total_duration ({total_dur:.2f}s) melebihi batas maksimal {max_total_duration:.1f}s"
        )

    if not scenes:
        errors.append(f"{label}/campaign.json: stages.storyboard.scenes kosong")
        return errors

    scene_ids = [s.get("id") for s in scenes]
    for idx, s in enumerate(scenes, start=1):
        sdur = float(s.get("duration", 0))
        if sdur <= 0:
            errors.append(f"{label}/campaign.json: scene {s.get('id', idx)} durasi harus > 0")

    scene_dur_sum = sum(float(s.get("duration", 0)) for s in scenes)
    if abs(scene_dur_sum - total_dur) > 1e-6:
        errors.append(
            f"{label}/campaign.json: jumlah durasi scenes ({scene_dur_sum:.2f}s) != total_duration ({total_dur:.2f}s)"
        )

    errors.extend(_validate_scene_timestamps(scenes, label))

    # Validasi gambar storyboard (single, multi-sheet, atau prompt fallback)
    sb_md_path = campaign_dir / "03-storyboard" / "storyboard.md"
    sb_img = sb_stage.get("image")
    sb_images = sb_stage.get("images") or []
    sb_text = ""

    if sb_img:
        img_file = campaign_dir / sb_img
        if not _nonempty_file(img_file):
            errors.append(f"{label}: storyboard.image '{sb_img}' tidak ada atau kosong")
    if sb_images:
        if not isinstance(sb_images, list):
            errors.append(f"{label}/campaign.json: stages.storyboard.images harus berupa list")
        else:
            for img_rel in sb_images:
                if not _nonempty_file(campaign_dir / str(img_rel)):
                    errors.append(f"{label}: storyboard sheet '{img_rel}' tidak ada atau kosong")

    if sb_md_path.is_file():
        sb_text = sb_md_path.read_text(encoding="utf-8")
        if not sb_img and not sb_images and "## Prompt Gambar Storyboard" not in sb_text:
            errors.append(
                f"{label}/03-storyboard/storyboard.md: harus ada gambar storyboard atau heading '## Prompt Gambar Storyboard'"
            )
        sb_dt = dialogue_timing.check_table(
            sb_md_path, max_total_duration=max_total_duration, require_start_zero=True
        )
        if not sb_dt["ok"]:
            errors.extend(f"{label}/03-storyboard/storyboard.md: {e}" for e in sb_dt["errors"])
        elif abs(sb_dt["total_duration"] - total_dur) > dialogue_timing.TIMESTAMP_TOLERANCE:
            errors.append(
                f"{label}/03-storyboard/storyboard.md: total durasi tabel ({sb_dt['total_duration']:.2f}s) "
                f"!= total_duration campaign.json ({total_dur:.2f}s)"
            )
    else:
        errors.append(f"{label}: file wajib hilang -> 03-storyboard/storyboard.md")

    pub_path = campaign_dir / "05-publishing" / "publishing-package.md"
    pub_text = pub_path.read_text(encoding="utf-8") if pub_path.is_file() else ""
    if sb_text and not _has_cta(cj, sb_text, pub_text):
        errors.append(
            f"{label}: CTA tidak ditemukan di storyboard/publishing (tambahkan CTA atau set 'cta_optional': true)"
        )

    # Validasi segmen generasi video bila sudah ada
    vid_stage = cj.get("stages", {}).get("video", {})
    generations = vid_stage.get("generations", [])
    if generations:
        supports_ext = bool(vid_stage.get("generator_supports_extended_clip", False))
        declared_max = vid_stage.get("max_clip_duration")
        allowed_clip = float(declared_max) if declared_max is not None else DEFAULT_MAX_CLIP_DURATION
        if allowed_clip > DEFAULT_MAX_CLIP_DURATION + 1e-6 and not supports_ext:
            errors.append(
                f"{label}/campaign.json: max_clip_duration ({allowed_clip:.1f}s) melebihi 10.0s "
                "tanpa generator_supports_extended_clip = true"
            )
        effective_clip_limit = allowed_clip if supports_ext else DEFAULT_MAX_CLIP_DURATION

        covered_scenes: list = []
        gen_dur_sum = 0.0
        for gen in generations:
            gfile_rel = gen.get("file", "")
            gscenes = gen.get("scenes", [])
            gdur = float(gen.get("duration", 0))
            if gdur <= 0:
                errors.append(f"{label}: durasi generasi '{gfile_rel}' ({gdur}s) harus > 0")
            elif gdur > effective_clip_limit + 1e-6:
                errors.append(
                    f"{label}: durasi generasi '{gfile_rel}' ({gdur:.2f}s) melebihi batas klip "
                    f"{effective_clip_limit:.1f}s (set generator_supports_extended_clip: true jika generator mendukung)"
                )
            gen_dur_sum += gdur
            covered_scenes.extend(gscenes)

            gpath = campaign_dir / gfile_rel
            if not gpath.is_file():
                errors.append(f"{label}: file generasi video hilang -> {gfile_rel}")
                continue

            gtext = gpath.read_text(encoding="utf-8")
            for sid in gscenes:
                if not re.search(rf"\bAdegan\s+{re.escape(str(sid))}\b", gtext, re.IGNORECASE):
                    errors.append(f"{label}/{gfile_rel}: tidak menyebut 'Adegan {sid}'")

            dt_res = dialogue_timing.check_table(
                gpath, max_total_duration=effective_clip_limit, require_start_zero=False
            )
            if not dt_res["ok"]:
                errors.extend(f"{label}/{gfile_rel}: {e}" for e in dt_res["errors"])
            elif abs(dt_res["total_duration"] - gdur) > dialogue_timing.TIMESTAMP_TOLERANCE:
                errors.append(
                    f"{label}/{gfile_rel}: total durasi tabel ({dt_res['total_duration']:.2f}s) "
                    f"!= durasi generasi ({gdur:.2f}s)"
                )

        if abs(gen_dur_sum - total_dur) > 1e-6:
            errors.append(
                f"{label}/campaign.json: jumlah durasi generations ({gen_dur_sum:.2f}s) "
                f"!= total_duration ({total_dur:.2f}s)"
            )
        if len(covered_scenes) != len(set(covered_scenes)):
            errors.append(f"{label}/campaign.json: ada scene terduplikasi di generations ({covered_scenes})")
        if set(covered_scenes) != set(scene_ids):
            errors.append(
                f"{label}/campaign.json: cakupan scene generations {covered_scenes} != scenes {scene_ids}"
            )

    return errors


def validate_collaboration(
    campaign_dir: Path,
    prefix: str | None = None,
) -> list[str]:
    """Validasi artefak kolaborasi dua arah HCE <-> AVD dan batas maksimal 3 iterasi."""
    errors: list[str] = []
    label = prefix or campaign_dir.name
    collab_dir = campaign_dir / "_collaboration"
    summary_path = collab_dir / "collaboration-summary.json"

    if not collab_dir.is_dir():
        return [f"{label}: direktori _collaboration/ tidak ditemukan"]
    if not summary_path.is_file():
        return [f"{label}: _collaboration/collaboration-summary.json tidak ditemukan"]

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label}/_collaboration/collaboration-summary.json: JSON rusak ({exc})"]

    iterations = summary.get("iterations")
    max_iters = summary.get("max_iterations")
    if not isinstance(iterations, int) or iterations < 1 or iterations > 3:
        errors.append(
            f"{label}/_collaboration/collaboration-summary.json: iterations ({iterations}) harus integer 1..3"
        )
    if not isinstance(max_iters, int) or max_iters < 1 or max_iters > 3:
        errors.append(
            f"{label}/_collaboration/collaboration-summary.json: max_iterations ({max_iters}) harus integer 1..3"
        )

    if isinstance(iterations, int) and iterations >= 1:
        for k in range(1, min(iterations, 3) + 1):
            round_path = collab_dir / f"review-round-{k}.json"
            if not round_path.is_file():
                errors.append(f"{label}: file review putaran hilang -> _collaboration/review-round-{k}.json")
            else:
                try:
                    json.loads(round_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    errors.append(f"{label}/_collaboration/review-round-{k}.json: JSON rusak ({exc})")

    if not (collab_dir / "hce-product-input.json").is_file():
        errors.append(f"{label}: _collaboration/hce-product-input.json tidak ditemukan")
    if not (collab_dir / "hce-package-v1.json").is_file():
        errors.append(f"{label}: _collaboration/hce-package-v1.json tidak ditemukan")
    if not (collab_dir / "avd-plan-v1.json").is_file():
        errors.append(f"{label}: _collaboration/avd-plan-v1.json tidak ditemukan")

    version_history = summary.get("version_history", [])
    if isinstance(iterations, int) and iterations > 1 and not version_history:
        errors.append(
            f"{label}/_collaboration/collaboration-summary.json: ada {iterations} iterasi tetapi version_history kosong"
        )

    cj_path = campaign_dir / "campaign.json"
    if cj_path.is_file():
        try:
            cj = json.loads(cj_path.read_text(encoding="utf-8"))
            cblock = cj.get("collaboration", {})
            if cblock:
                cj_iters = cblock.get("iterations", 0)
                cj_max = cblock.get("max_iterations", 3)
                if not isinstance(cj_max, int) or cj_max > 3:
                    errors.append(f"{label}/campaign.json: collaboration.max_iterations ({cj_max}) melebihi 3")
                if not isinstance(cj_iters, int) or cj_iters > 3:
                    errors.append(f"{label}/campaign.json: collaboration.iterations ({cj_iters}) melebihi 3")
        except json.JSONDecodeError as exc:
            errors.append(f"{label}/campaign.json: JSON rusak ({exc})")

    return errors


def check_stage(
    campaign_dir: Path,
    stage: str,
    confirmed: bool = False,
    validate_timing: bool = False,
    check_collaboration: bool = False,
) -> int:
    """Periksa prasyarat tahap review, storyboard, atau video."""
    missing: list[str] = []
    warnings: list[str] = []
    present: list[str] = []

    if not campaign_dir.is_dir():
        print(f"[TIDAK SIAP] Direktori kampanye tidak ditemukan: {campaign_dir}")
        return 2

    campaign_json_path = campaign_dir / "campaign.json"
    campaign_data: dict = {}
    if campaign_json_path.is_file():
        try:
            campaign_data = json.loads(campaign_json_path.read_text(encoding="utf-8"))
            present.append("campaign.json")
        except json.JSONDecodeError as exc:
            missing.append(f"campaign.json (JSON rusak: {exc})")
    else:
        warnings.append("campaign.json belum ada (gunakan --init untuk membuat struktur baku)")

    inventory = collect_inventory(campaign_dir)

    if stage == "review":
        if inventory["product-reference"]:
            present.append(f"01-product-review/references/ ({len(inventory['product-reference'])} file)")
        else:
            missing.append(
                "01-product-review/references/ kosong — minta foto asli, screenshot listing, atau deskripsi produk dari pengguna"
            )

    elif stage in ("storyboard", "video"):
        review_req = [
            "01-product-review/product-brief.md",
            "01-product-review/marketing-strategy.md",
            "01-product-review/image-prompts.md",
        ]
        for rel in review_req:
            if _nonempty_file(campaign_dir / rel):
                present.append(rel)
            else:
                missing.append(f"{rel} (jalankan /review terlebih dahulu)")

        gen_count = (
            len(inventory["generated-lifestyle"])
            + len(inventory["product-demonstration"])
            + len(inventory["video-reference"])
        )
        if gen_count == 0:
            warnings.append(
                "02-generated-assets/ belum memiliki gambar hasil generate — "
                "disarankan generate gambar hero/demo dulu atau lanjut dengan referensi asli saja"
            )
        else:
            present.append(f"02-generated-assets/ ({gen_count} gambar)")

        if stage == "video":
            sb_md = campaign_dir / "03-storyboard" / "storyboard.md"
            if _nonempty_file(sb_md):
                present.append("03-storyboard/storyboard.md")
            else:
                missing.append("03-storyboard/storyboard.md (jalankan /storyboard terlebih dahulu)")

            sb_stage = campaign_data.get("stages", {}).get("storyboard", {}) if campaign_data else {}
            sb_status = sb_stage.get("status", "not-started")
            if _nonempty_file(sb_md) and sb_status != "approved" and not confirmed:
                missing.append(
                    f"Persetujuan storyboard (status saat ini: '{sb_status}') — "
                    "minta konfirmasi pengguna atau tambahkan --confirmed"
                )

            total_dur = float(sb_stage.get("total_duration", 0) or 0)
            if total_dur > MAX_FINAL_DURATION + 1e-6:
                missing.append(
                    f"Total durasi storyboard ({total_dur:.2f}s) melebihi batas maksimal {MAX_FINAL_DURATION:.1f} detik"
                )

            if not inventory["storyboard"]:
                warnings.append(
                    "03-storyboard/storyboard*.png belum ditemukan — boleh lanjut memakai prompt tertulis "
                    "di storyboard.md jika pengguna menyetujui"
                )

    timing_errors: list[str] = []
    if validate_timing and campaign_json_path.is_file():
        timing_errors = validate_campaign_timing(campaign_dir)

    collab_errors: list[str] = []
    if check_collaboration:
        collab_errors = validate_collaboration(campaign_dir)

    print(f"=== Cek Kesiapan Tahap: /{stage} ({campaign_dir.name}) ===")
    print("\nFile & Prasyarat Terpenuhi:")
    if present:
        for item in present:
            print(f"  [ADA] {item}")
    else:
        print("  (belum ada)")

    print("\nInventaris Aset Berdasarkan Hierarki Otoritas:")
    for rank, cat in enumerate(
        [
            "product-reference",
            "generated-lifestyle",
            "product-demonstration",
            "video-reference",
            "storyboard",
        ],
        start=1,
    ):
        files = inventory[cat]
        label = ", ".join(files) if files else "(kosong)"
        print(f"  #{rank} {cat}: {label}")

    if warnings:
        print("\nPeringatan:")
        for w in warnings:
            print(f"  [PERINGATAN] {w}")

    if missing or timing_errors or collab_errors:
        print("\nPrasyarat yang Hilang / Kesalahan Timing / Kolaborasi:")
        for m in missing:
            print(f"  [HILANG] {m}")
        for te in timing_errors:
            print(f"  [GAGAL] {te}")
        for ce in collab_errors:
            print(f"  [KOLABORASI] {ce}")
        print("\nStatus: BELUM SIAP")
        return 2

    print("\nStatus: SIAP")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inisialisasi dan cek kesiapan direktori kampanye Affiliate Video Director."
    )
    parser.add_argument(
        "target",
        help="Direktori kampanye (saat --stage/--validate-timing) atau direktori induk campaigns (saat --init).",
    )
    parser.add_argument(
        "slug",
        nargs="?",
        help="Slug kampanye (wajib saat --init, mis. sapu-sawang-teleskopik-2-3m).",
    )
    parser.add_argument("--init", action="store_true", help="Inisialisasi struktur kampanye baru.")
    parser.add_argument("--product", default="", help="Nama produk untuk campaign.json saat --init.")
    parser.add_argument("--category", default="", help="Kategori produk opsional saat --init.")
    parser.add_argument(
        "--stage",
        choices=["review", "storyboard", "video"],
        help="Tahap yang akan diperiksa kesiapannya.",
    )
    parser.add_argument(
        "--confirmed",
        action="store_true",
        help="Tandai bahwa pengguna sudah mengonfirmasi storyboard secara lisan.",
    )
    parser.add_argument(
        "--validate-timing",
        action="store_true",
        help="Jalankan validasi penuh durasi adaptif (<=40s), urutan timestamp, batas klip 10s, dialog, dan CTA.",
    )
    parser.add_argument(
        "--check-collaboration",
        action="store_true",
        help="Validasi artefak kolaborasi dua arah HCE <-> AVD di _collaboration/ dan batas maks. 3 iterasi.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.init:
        if not args.slug:
            parser.error("--init memerlukan argumen slug (contoh: --init ./campaigns nama-produk)")
        product_name = args.product or args.slug.replace("-", " ").title()
        return init_campaign(Path(args.target), args.slug, product_name, args.category)

    if (args.validate_timing or args.check_collaboration) and not args.stage:
        cdir = Path(args.target)
        errs: list[str] = []
        if args.validate_timing:
            errs.extend(validate_campaign_timing(cdir))
        if args.check_collaboration:
            errs.extend(validate_collaboration(cdir))
        print(f"=== Validasi Kampanye: {cdir} ===")
        if errs:
            for e in errs:
                print(f"  [GAGAL] {e}")
            return 2
        print("  [OK] Seluruh cek yang diminta lolos.")
        return 0

    if not args.stage:
        parser.error("Tentukan --init, --stage {review,storyboard,video}, --validate-timing, atau --check-collaboration")

    return check_stage(
        Path(args.target),
        args.stage,
        confirmed=args.confirmed,
        validate_timing=args.validate_timing,
        check_collaboration=args.check_collaboration,
    )


if __name__ == "__main__":
    sys.exit(main())
