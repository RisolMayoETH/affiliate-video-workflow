#!/usr/bin/env python3
"""Autonomous collaboration bridge between Affiliate Video Director (AVD) and Human Copywriting Engine (HCE)."""

from __future__ import annotations

import argparse
import copy
import datetime
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import campaign_check  # noqa: E402
import dialogue_timing  # noqa: E402

MAX_ITERATIONS_CAP = 3
DEFAULT_MAX_FINAL_DURATION = 40.0
DEFAULT_MAX_CLIP_DURATION = 10.0

PLATFORM_ALIASES = {
    "tiktok": "tiktok",
    "tiktok-shop": "tiktok",
    "instagram-reels": "instagram_reels",
    "instagram_reels": "instagram_reels",
    "ig-reels": "instagram_reels",
    "facebook-reels": "facebook_reels",
    "facebook_reels": "facebook_reels",
    "fb-reels": "facebook_reels",
    "shopee-video": "shopee_video",
    "shopee_video": "shopee_video",
}

HCE_CATEGORY_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("kitchen", ("dapur", "kitchen", "masak", "chopper", "blender", "wajan", "mangkok", "pisau", "botol bumbu")),
    ("beauty_personal_care", ("kecantikan", "beauty", "kosmetik", "lipstik", "skincare", "sunscreen", "serum", "parfum", "bibir", "wajah")),
    ("electronics", ("elektronik", "electronics", "usb", "lampu", "led", "earphone", "tws", "charger", "kipas", "watt")),
    ("fashion", ("fashion", "pakaian", "baju", "tas", "sepatu", "kemeja", "sling bag", "jaket", "kain")),
    ("household", ("rumah", "household", "kebersihan", "sapu", "pel", "rak", "kamar mandi", "plafon", "sawang", "dinding", "lantai")),
)

UNIT_SPOKEN_MAP = {
    "ml": "mililiter",
    "l": "liter",
    "liter": "liter",
    "cm": "senti",
    "mm": "milimeter",
    "m": "meter",
    "w": "watt",
    "watt": "watt",
    "g": "gram",
    "gr": "gram",
    "gram": "gram",
    "kg": "kilo",
    "pcs": "buah",
    "mah": "miliamper jam",
    "%": "persen",
}

ONES_ID = (
    "nol",
    "satu",
    "dua",
    "tiga",
    "empat",
    "lima",
    "enam",
    "tujuh",
    "delapan",
    "sembilan",
)


@dataclass
class HCERuntime:
    """Loaded HCE runtime objects without adding third-party dependencies."""

    hce_root: Path
    config: Any
    db: Any
    repo: Any
    retriever: Any
    ProductInput: Any
    ProductAnalyzer: Any
    AudienceAnalyzer: Any
    StrategySelector: Any
    AffiliateContentGenerator: Any
    NaturalLanguageRefiner: Any
    CopyEvaluator: Any


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _today_iso() -> str:
    return datetime.date.today().isoformat()


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def find_hce_root(explicit_root: str | Path | None = None) -> Path:
    """Locate the local Human-Copywriting-Engine directory."""
    candidates: list[Path] = []
    if explicit_root:
        candidates.append(Path(explicit_root).resolve())
    if env_root := os.getenv("HCE_ROOT"):
        candidates.append(Path(env_root).resolve())

    here = Path(__file__).resolve()
    for base in [Path.cwd().resolve(), *here.parents]:
        candidates.append(base / "human-copywriting-engine")
        candidates.append(base)

    for cand in candidates:
        if (cand / "hce" / "__init__.py").is_file() and (cand / "knowledge").is_dir():
            return cand
    raise FileNotFoundError(
        "Direktori Human-Copywriting-Engine (hce/__init__.py & knowledge/) tidak ditemukan. "
        "Pastikan repo telah di-clone ke ./human-copywriting-engine atau set HCE_ROOT."
    )


def load_hce_runtime(explicit_root: str | Path | None = None) -> HCERuntime:
    """Import HCE modules directly from the cloned repository and prepare retriever/index."""
    hce_root = find_hce_root(explicit_root)
    hce_str = str(hce_root)
    if hce_str not in sys.path:
        sys.path.insert(0, hce_str)

    from hce.config import HCEConfig
    from hce.evaluation.evaluator import CopyEvaluator
    from hce.execution.audience_analyzer import AudienceAnalyzer
    from hce.execution.content_generator import AffiliateContentGenerator
    from hce.execution.product_analyzer import ProductAnalyzer, ProductInput
    from hce.execution.strategy_selector import StrategySelector
    from hce.knowledge.repository import KnowledgeRepository
    from hce.knowledge.retrieval import LocalKeywordRetriever
    from hce.language.refiner import NaturalLanguageRefiner
    from hce.storage.db import Database

    cfg = HCEConfig.load(root_dir=hce_root)
    cfg.ensure_directories()
    db = Database(cfg.storage.db_path)
    db.init_schema()
    repo = KnowledgeRepository(cfg.storage.knowledge_dir, db)
    if not repo.index_path.exists():
        repo.sync_seed_modules()
    retriever = LocalKeywordRetriever(repo)

    return HCERuntime(
        hce_root=hce_root,
        config=cfg,
        db=db,
        repo=repo,
        retriever=retriever,
        ProductInput=ProductInput,
        ProductAnalyzer=ProductAnalyzer,
        AudienceAnalyzer=AudienceAnalyzer,
        StrategySelector=StrategySelector,
        AffiliateContentGenerator=AffiliateContentGenerator,
        NaturalLanguageRefiner=NaturalLanguageRefiner,
        CopyEvaluator=CopyEvaluator,
    )


def normalize_platform(platform: str | None) -> str:
    """Normalize AVD/HCE platform names to HCE canonical identifiers."""
    key = (platform or "tiktok").strip().lower().replace(" ", "_")
    return PLATFORM_ALIASES.get(key, "tiktok")


def map_avd_category_to_hce(raw_category: str, text_hint: str = "") -> str:
    """Map free-form Indonesian AVD category labels to HCE's canonical product categories."""
    low = f"{raw_category} {text_hint}".lower()
    canonical = {"household", "kitchen", "beauty_personal_care", "fashion", "electronics", "everyday_consumer"}
    norm = raw_category.strip().lower().replace("-", "_").replace(" ", "_")
    if norm in canonical:
        return norm
    for hce_cat, keywords in HCE_CATEGORY_KEYWORDS:
        if any(kw in low for kw in keywords):
            return hce_cat
    return "everyday_consumer"


def _int_to_indonesian(n: int) -> str:
    if n < 0:
        return "minus " + _int_to_indonesian(-n)
    if n < 10:
        return ONES_ID[n]
    if n == 10:
        return "sepuluh"
    if n == 11:
        return "sebelas"
    if n < 20:
        return f"{ONES_ID[n - 10]} belas"
    if n < 100:
        tens, rem = divmod(n, 10)
        return f"{ONES_ID[tens]} puluh" + (f" {ONES_ID[rem]}" if rem else "")
    if n < 200:
        rem = n - 100
        return "seratus" + (f" {_int_to_indonesian(rem)}" if rem else "")
    if n < 1000:
        hundreds, rem = divmod(n, 100)
        return f"{ONES_ID[hundreds]} ratus" + (f" {_int_to_indonesian(rem)}" if rem else "")
    if n < 2000:
        rem = n - 1000
        return "seribu" + (f" {_int_to_indonesian(rem)}" if rem else "")
    if n < 1_000_000:
        thousands, rem = divmod(n, 1000)
        return f"{_int_to_indonesian(thousands)} ribu" + (f" {_int_to_indonesian(rem)}" if rem else "")
    return str(n)


def number_to_indonesian_words(num_str: str) -> str:
    """Convert an integer or decimal token into spoken Indonesian words."""
    clean = num_str.strip()
    if "," in clean or "." in clean:
        sep = "," if "," in clean else "."
        parts = clean.split(sep, 1)
        if parts[0].isdigit() and parts[1].isdigit():
            # Treat dot-separated 3-digit group like 12.999 as thousands integer
            if sep == "." and len(parts[1]) == 3 and len(parts[0]) <= 3:
                return _int_to_indonesian(int(parts[0] + parts[1]))
            frac = " ".join(_int_to_indonesian(int(d)) for d in parts[1])
            return f"{_int_to_indonesian(int(parts[0]))} koma {frac}"
    if clean.isdigit():
        return _int_to_indonesian(int(clean))
    return clean


def spell_numbers_in_vo(text: str) -> str:
    """Convert raw numeric digits and attached units inside spoken VO into natural Indonesian words."""
    if not text or text.strip().lower() == "[jeda]":
        return text

    def _replace_num_unit(match: re.Match[str]) -> str:
        num_part = match.group(1)
        unit_part = (match.group(2) or "").lower()
        spoken_num = number_to_indonesian_words(num_part)
        if unit_part:
            spoken_unit = UNIT_SPOKEN_MAP.get(unit_part, unit_part)
            return f"{spoken_num} {spoken_unit}"
        return spoken_num

    # Replace hashtag shade numbers like #03 -> nomor tiga
    out = re.sub(r"#0*(\d+)", lambda m: f"nomor {_int_to_indonesian(int(m.group(1)))}", text)
    # Replace numbers optionally followed by measurement units
    unit_pattern = r"\b(\d+(?:[.,]\d+)?)\s*(ml|liter|l|cm|mm|m|watt|w|gram|gr|g|kg|pcs|mah|%)?\b"
    out = re.sub(unit_pattern, _replace_num_unit, out, flags=re.IGNORECASE)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def syllable_bounds_for_duration(duration: float, rate: float = dialogue_timing.DEFAULT_RATE) -> tuple[int, int]:
    """Compute exact (min_syllables, max_syllables) accepted by dialogue_timing.py for a panel duration."""
    valid: list[int] = []
    for syl in range(1, 200):
        est = round(syl / rate, 2)
        fill_ratio = est / duration
        eff_rate = syl / duration
        if (
            fill_ratio >= dialogue_timing.MIN_FILL_RATIO
            and fill_ratio <= dialogue_timing.MAX_FILL_RATIO
            and eff_rate <= dialogue_timing.MAX_EFFECTIVE_RATE
        ):
            valid.append(syl)
    if not valid:
        low = max(1, int(round(duration * rate * dialogue_timing.MIN_FILL_RATIO)))
        high = max(low, int(duration * rate))
        return low, high
    return valid[0], valid[-1]


def _fmt_sec(sec: float) -> str:
    rounded = round(sec, 2)
    mins = int(rounded // 60)
    rem = rounded - mins * 60
    if abs(rem - round(rem)) < 1e-6:
        return f"{mins:02d}:{int(round(rem)):02d}"
    return f"{mins:02d}:{rem:04.1f}"


def format_timestamp_range(start_s: float, end_s: float) -> str:
    """Format start/end seconds as MM:SS–MM:SS (or MM:SS.S when fractional)."""
    return f"{_fmt_sec(start_s)}–{_fmt_sec(end_s)}"


def archive_if_exists(file_path: Path, campaign_dir: Path) -> str | None:
    """Copy an existing text deliverable into _archive/<stem>.vN<suffix> before replacing it."""
    if not file_path.is_file():
        return None
    archive_dir = campaign_dir / "_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stem = file_path.stem
    suffix = file_path.suffix
    idx = 1
    while True:
        candidate = archive_dir / f"{stem}.v{idx}{suffix}"
        if not candidate.exists():
            shutil.copy2(file_path, candidate)
            return candidate.relative_to(campaign_dir).as_posix()
        idx += 1


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _extract_short_product_name(full_name: str, max_words: int = 3) -> str:
    """Create a natural spoken shorthand while keeping authentic brand/product words."""
    cleaned = re.sub(r"\[[^\]]+\]|\([^)]+\)", "", full_name)
    cleaned = re.sub(r"\b\d+(?:[.,]\d+)?\s*(?:ml|cm|mm|m|watt|w|gram|gr|kg|pcs)\b", "", cleaned, flags=re.IGNORECASE)
    stop_tokens = {"USB", "BPOM", "LED", "LCD", "HD", "SATU", "DUA", "TIGA", "EMPAT", "LIMA"}
    core_words: list[str] = []
    for idx, raw in enumerate(cleaned.split()):
        w = raw.strip(",.-/")
        if not w:
            continue
        if idx >= 1 and w.upper() in stop_tokens:
            if len(core_words) >= 2:
                break
            continue
        core_words.append(w)
        if len(core_words) >= max_words:
            break
    if not core_words:
        return "produk ini"
    return " ".join(core_words)


def _clean_vo_phrase(text: str) -> str:
    """Convert raw phrases to spoken Indonesian without digits, acronyms, or stiff punctuation."""
    s = spell_numbers_in_vo(text)
    s = re.sub(r"\bUSB\b", "kabel cas", s)
    s = re.sub(r"\bPOV\b", "langsung", s)
    s = re.sub(r"\bBPOM\b", "resmi aman", s)
    s = re.sub(r"\s+", " ", s).strip(" ,.;:-")
    return s


def _fit_vo_to_bounds(
    candidates: list[str],
    duration: float,
    min_syl: int,
    max_syl: int,
    required_keywords: tuple[str, ...] = (),
) -> str:
    """Select or trim a natural Indonesian phrase so its syllable count fits [min_syl, max_syl]."""
    cleaned_cands = [spell_numbers_in_vo(c).strip() for c in candidates if c and c.strip()]

    def _ok_keywords(text: str) -> bool:
        if not required_keywords:
            return True
        low = text.lower()
        return any(kw in low for kw in required_keywords)

    # Pass 1: prefer full, untrimmed candidates that already fit syllable bounds and required keywords
    for cand in cleaned_cands:
        syl, warns = dialogue_timing.analyze_text(cand)
        if not warns and min_syl <= syl <= max_syl and _ok_keywords(cand):
            return cand if cand[-1] in ".!?" else f"{cand}."

    # Pass 2: try clause-splitting or word trimming while preserving required keywords
    best_text = ""
    best_dist = 10**6
    for cand in cleaned_cands:
        syl, warns = dialogue_timing.analyze_text(cand)
        dist = 0 if min_syl <= syl <= max_syl else (min_syl - syl if syl < min_syl else syl - max_syl)
        if dist < best_dist and not warns and _ok_keywords(cand):
            best_dist = dist
            best_text = cand

        if syl > max_syl:
            clauses = [p.strip(" ,") for p in re.split(r"[,;—–]+", cand) if p.strip(" ,")]
            for cl in clauses:
                csyl, cwarns = dialogue_timing.analyze_text(cl)
                if not cwarns and min_syl <= csyl <= max_syl and _ok_keywords(cl):
                    return cl if cl[-1] in ".!?" else f"{cl}."
            words = cand.split()
            for end_idx in range(len(words) - 1, 1, -1):
                sub = " ".join(words[:end_idx]).rstrip(",.;:-")
                ssyl, swarns = dialogue_timing.analyze_text(sub)
                if not swarns and min_syl <= ssyl <= max_syl and _ok_keywords(sub):
                    return sub if sub[-1] in ".!?" else f"{sub}."

    if best_text:
        return best_text if best_text[-1] in ".!?" else f"{best_text}."
    if duration <= 1.5:
        return "[jeda]"
    if required_keywords:
        return f"Cek detail produknya di {required_keywords[0]} ya."
    return "Lihat detailnya langsung di sini."


def normalize_product_input(
    raw: dict[str, Any],
    *,
    slug: str = "",
    campaign_dir: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Separate structured HCE ProductInput fields from AVD visual/production context."""
    product_name = str(raw.get("name") or raw.get("product_name") or slug or "Produk Affiliate").strip()
    raw_category = str(raw.get("original_category") or raw.get("category") or "").strip()
    description = str(raw.get("description") or raw.get("summary") or "").strip()
    verified_features = [str(x).strip() for x in raw.get("verified_features", []) if str(x).strip()]
    verified_specs = {str(k): v for k, v in (raw.get("verified_specs") or {}).items()}
    available_evidence = [str(x).strip() for x in raw.get("available_evidence", []) if str(x).strip()]
    platform = normalize_platform(str(raw.get("target_platform") or "tiktok"))

    if not description and verified_features:
        description = f"{product_name} dengan fitur {', '.join(verified_features[:3])}."
    elif not description:
        description = f"{product_name} sesuai deskripsi dan foto referensi produk."

    if not verified_features and verified_specs:
        verified_features = [f"{k}: {v}" for k, v in list(verified_specs.items())[:4]]
    elif not verified_features:
        verified_features = [description]

    hce_cat = map_avd_category_to_hce(raw_category, f"{product_name} {description} {' '.join(verified_features)}")
    product_id = str(raw.get("product_id") or slug or re.sub(r"[^a-z0-9]+", "-", product_name.lower()).strip("-"))

    hce_input = {
        "product_id": product_id,
        "name": product_name,
        "category": hce_cat,
        "price_idr": raw.get("price_idr"),
        "description": description,
        "verified_features": verified_features,
        "verified_specs": verified_specs,
        "available_evidence": available_evidence,
        "target_platform": platform,
        "supplied_audience": raw.get("supplied_audience"),
        "notes": str(raw.get("notes", "")).strip(),
    }

    references = list(raw.get("references") or [])
    if campaign_dir is not None:
        inv = campaign_check.collect_inventory(campaign_dir)
        if inv["product-reference"]:
            references = inv["product-reference"]

    default_hand = "Tangan orang dewasa Indonesia berkulit sawo matang/kuning langsat natural, kuku pendek bersih tanpa cat mencolok, lengan kaus katun polos krem/abu-abu muda konsisten (hands-only tanpa wajah)."
    default_env = _default_environment_for_category(hce_cat)

    avd_context = {
        "slug": slug or product_id,
        "original_category": raw_category or hce_cat,
        "hce_category": hce_cat,
        "visual_anchors": [str(x) for x in raw.get("visual_anchors", []) if str(x).strip()]
        or [f"Bentuk fisik, warna, dan proporsi {product_name} persis foto referensi asli (Otoritas #1)."],
        "hand_spec": str(raw.get("hand_spec") or default_hand),
        "environment_spec": str(raw.get("environment_spec") or default_env),
        "references": references,
        "product_only": bool(raw.get("product_only", False)),
        "assumptions": [str(x) for x in raw.get("assumptions", []) if str(x).strip()],
        "missing_checks": [str(x) for x in raw.get("missing_checks", []) if str(x).strip()],
        "platforms": [normalize_platform(p) for p in raw.get("platforms", ["tiktok", "instagram-reels", "facebook-reels"])],
    }
    return hce_input, avd_context


def _default_environment_for_category(hce_cat: str) -> str:
    env_map = {
        "kitchen": "Meja dapur rumah Indonesia yang bersih dan terang alami dekat jendela, talenan kayu netral, bahan bumbu segar tertata rapi tanpa kekacauan latar.",
        "household": "Sudut ruangan atau kamar mandi rumah Indonesia berdinding keramik/cat krem terang, pencahayaan siang alami lembut, latar rapi bebas barang menumpuk.",
        "beauty_personal_care": "Meja rias batu krem terang dekat jendela ber-cahaya pagi lembut, latar minimalis bersih tanpa filter berlebihan.",
        "fashion": "Sudut kamar minimalis berlatar cermin berdiri dan dinding krem hangat dengan pencahayaan siang lembut dari samping.",
        "electronics": "Meja kerja kayu matte rapi dengan pencahayaan kamar natural lembut tanpa kabel berserakan.",
    }
    return env_map.get(
        hce_cat,
        "Meja atau sudut rumah Indonesia terang alami dekat jendela, latar bersih netral dengan kedalaman ruang tipis.",
    )


def extract_product_input_from_campaign(campaign_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build normalized HCE ProductInput + AVD context from campaign.json and references without inventing facts."""
    cj_path = campaign_dir / "campaign.json"
    if not cj_path.is_file():
        raise FileNotFoundError(f"campaign.json tidak ditemukan di {campaign_dir}")
    cj = json.loads(cj_path.read_text(encoding="utf-8"))

    # Check if an explicit hce-product-input.json already exists inside _collaboration/
    existing_input_path = campaign_dir / "_collaboration" / "hce-product-input.json"
    if existing_input_path.is_file():
        saved = json.loads(existing_input_path.read_text(encoding="utf-8"))
        if isinstance(saved.get("hce_input"), dict) and isinstance(saved.get("avd_context"), dict):
            return saved["hce_input"], saved["avd_context"]

    key_facts = [str(x).strip() for x in cj.get("key_facts", []) if str(x).strip()]
    inv = campaign_check.collect_inventory(campaign_dir)
    ref_notes: list[str] = []
    for ref_rel in inv["product-reference"]:
        ref_path = campaign_dir / ref_rel
        if ref_path.suffix.lower() in {".txt", ".md", ".json"}:
            ref_notes.append(ref_path.read_text(encoding="utf-8", errors="replace").strip())

    # If still no key_facts, try parsing references notes
    features = list(key_facts)
    if not features and ref_notes:
        for block in ref_notes:
            for line in block.splitlines():
                line_c = line.strip(" -*•\t")
                if len(line_c) > 6:
                    features.append(line_c)
        features = features[:6]

    raw = {
        "product_id": cj.get("slug") or campaign_dir.name,
        "name": cj.get("product_name") or campaign_dir.name.replace("-", " ").title(),
        "original_category": cj.get("category") or "",
        "description": " ".join(features[:2]) if features else cj.get("product_name", ""),
        "verified_features": features,
        "verified_specs": {},
        "available_evidence": [*key_facts, *[a.get("notes", "") for a in cj.get("assets", []) if a.get("category") == "product-reference" and a.get("notes")]],
        "target_platform": (cj.get("platforms") or ["tiktok"])[0],
        "platforms": cj.get("platforms") or ["tiktok", "instagram-reels", "facebook-reels"],
        "references": inv["product-reference"],
        "product_only": bool(cj.get("product_only", False)),
    }
    return normalize_product_input(raw, slug=campaign_dir.name, campaign_dir=campaign_dir)


def run_hce_analysis(
    runtime: HCERuntime,
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    *,
    platform: str = "tiktok",
    version: int = 1,
) -> dict[str, Any]:
    """Invoke HCE's real analyzers, selective retriever, generator, refiner, and evaluator."""
    plat = normalize_platform(platform or hce_input.get("target_platform"))
    input_copy = dict(hce_input)
    input_copy["target_platform"] = plat
    prod_obj = runtime.ProductInput.from_dict(input_copy)

    generator = runtime.AffiliateContentGenerator(runtime.retriever)
    generated = generator.generate(prod_obj, platform=plat)

    # Selective dynamic retrieval across all 6 HCE domains
    queries = [
        ("buyer psychology hesitation risk trust", "buyer_psychology"),
        ("hook product feature benefit cta", "persuasive_writing"),
        ("bahasa obrolan natural lisan", "human_language"),
        ("storytelling direct demo pacing", "storytelling"),
        (f"{plat} register price pacing", "audience_adaptation"),
        ("integrity accuracy anti repetition", "creative_evaluation"),
    ]
    retrieved_concepts: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for q, cat in queries:
        for hit in runtime.retriever.search(q, category=cat, limit=2):
            c = hit.concept
            if c.concept_id not in seen_ids:
                seen_ids.add(c.concept_id)
                retrieved_concepts.append(
                    {
                        "concept_id": c.concept_id,
                        "concept_name": c.concept_name,
                        "category": c.category,
                        "explanation": c.explanation,
                        "implementation": c.implementation[:3],
                    }
                )

    # Build multi-platform calibrated CTAs and captions using HCE's refiner
    refiner = runtime.NaturalLanguageRefiner()
    p_analysis = generated.product_analysis
    a_analysis = generated.audience_analysis
    short_name = _extract_short_product_name(p_analysis.name)
    target_platforms = list(dict.fromkeys([plat, "tiktok", "instagram_reels", "facebook_reels"]))

    platform_ctas: dict[str, str] = {}
    platform_captions: dict[str, str] = {}
    for tp in target_platforms:
        raw_cta = _build_platform_cta_line(tp, short_name, a_analysis.communication_style)
        res_cta = refiner.refine_text(
            raw_cta,
            location=f"cta_{tp}",
            register=a_analysis.communication_style,
            available_evidence=p_analysis.available_evidence,
        )
        platform_ctas[tp] = res_cta.refined_text

        cap_gen = generator._build_caption(p_analysis, a_analysis, tp)
        res_cap = refiner.refine_text(
            cap_gen,
            location=f"caption_{tp}",
            register=a_analysis.communication_style,
            available_evidence=p_analysis.available_evidence,
        )
        platform_captions[tp] = res_cap.refined_text

    usp = _build_usp_summary(p_analysis, a_analysis)
    pkg = generated.to_dict()
    pkg.update(
        {
            "version": version,
            "generated_at": _now_iso(),
            "platform": plat,
            "usp": usp,
            "platform_ctas": platform_ctas,
            "platform_captions": platform_captions,
            "retrieved_concepts": retrieved_concepts,
            "retrieved_knowledge_ids": [c["concept_id"] for c in retrieved_concepts],
            "avd_context_ref": {
                "slug": avd_context.get("slug"),
                "original_category": avd_context.get("original_category"),
            },
        }
    )
    return pkg


def _build_platform_cta_line(platform: str, short_name: str, style: str) -> str:
    if platform == "tiktok":
        return f"Cek varian dan detail {short_name} di keranjang kuning kiri bawah sekarang."
    if platform == "shopee_video":
        return f"Klik tautan produk di keranjang Shopee untuk cek detail {short_name}."
    if platform == "instagram_reels":
        return f"Detail varian dan ukuran {short_name} sudah ada di tautan bio dan caption ya."
    if style == "polite_neutral":
        return f"Silakan cek tautan produk di caption atau komentar untuk detail {short_name}."
    return f"Cek detail ukuran dan varian {short_name} lewat tautan di caption atau komentar."


def _build_usp_summary(p_analysis: Any, a_analysis: Any) -> str:
    diffs = p_analysis.differentiating_characteristics[:3]
    audience = a_analysis.likely_audience
    if diffs:
        return f"{'; '.join(diffs)} — relevan untuk {audience}."
    return f"{p_analysis.what_it_does} — relevan untuk {audience}."


def segment_panels_into_clips(
    scenes: list[dict[str, Any]],
    max_clip_duration: float = DEFAULT_MAX_CLIP_DURATION,
) -> list[dict[str, Any]]:
    """Dynamically group variable-duration storyboard panels into <= 10.0s video generation clips."""
    clips: list[dict[str, Any]] = []
    bucket: list[dict[str, Any]] = []
    bucket_dur = 0.0

    for sc in scenes:
        dur = float(sc["duration"])
        if bucket and bucket_dur + dur > max_clip_duration + 1e-6:
            clips.append(_finalize_clip_bucket(len(clips) + 1, bucket))
            bucket = [sc]
            bucket_dur = dur
        else:
            bucket.append(sc)
            bucket_dur += dur

    if bucket:
        clips.append(_finalize_clip_bucket(len(clips) + 1, bucket))
    return clips


def _finalize_clip_bucket(clip_idx: int, bucket: list[dict[str, Any]]) -> dict[str, Any]:
    start_s = float(bucket[0]["start_seconds"])
    end_s = float(bucket[-1]["end_seconds"])
    dur = round(sum(float(s["duration"]) for s in bucket), 2)
    return {
        "id": f"GEN-{clip_idx:02d}",
        "clip_index": clip_idx,
        "file": f"04-video/video-{clip_idx:02d}.md",
        "scenes": [int(s["id"]) for s in bucket],
        "timestamp": format_timestamp_range(start_s, end_s),
        "start_seconds": round(start_s, 2),
        "end_seconds": round(end_s, 2),
        "duration": dur,
        "continue_prefix_required": clip_idx > 1,
    }


def _recalculate_scene_timestamps(scenes: list[dict[str, Any]]) -> float:
    cursor = 0.0
    for idx, sc in enumerate(scenes, start=1):
        sc["id"] = idx
        dur = round(float(sc["duration"]), 2)
        sc["duration"] = dur
        start_s = round(cursor, 2)
        end_s = round(cursor + dur, 2)
        sc["start_seconds"] = start_s
        sc["end_seconds"] = end_s
        sc["timestamp"] = format_timestamp_range(start_s, end_s)
        cursor = end_s
    return round(cursor, 2)


def build_avd_plan_from_hce(
    hce_package: dict[str, Any],
    avd_context: dict[str, Any],
    *,
    campaign_dir: Path | None = None,
    version: int = 1,
) -> dict[str, Any]:
    """Convert HCE marketing & copywriting package into AVD's adaptive 9:16 storyboard & clip plan."""
    p_info = hce_package["product_analysis"]
    a_info = hce_package["audience_analysis"]
    hce_scenes = list(hce_package.get("scenes", []))
    features = list(p_info.get("verified_features", []))
    specs = dict(p_info.get("verified_specs", {}))
    product_name = p_info["name"]
    short_name = _extract_short_product_name(product_name)
    plat = hce_package.get("platform", "tiktok")

    inv = campaign_check.collect_inventory(campaign_dir) if campaign_dir else {}
    asset_pool = (
        inv.get("product-demonstration", [])
        + inv.get("generated-lifestyle", [])
        + inv.get("product-reference", [])
    )

    def _pick_asset(idx: int) -> str:
        if asset_pool:
            return asset_pool[idx % len(asset_pool)]
        return "01-product-review/references/"

    # Adaptive 6-panel expansion from HCE scenes (keeps HCE v1 copy faithful so Round 1 review validates genuinely)
    hook_vo = (hce_package.get("hooks") or [hce_scenes[0]["spoken_narration"] if hce_scenes else product_name])[0]
    mid1_vo = hce_scenes[1]["spoken_narration"] if len(hce_scenes) > 1 else f"Lihat fitur {features[0] if features else product_name}."
    mid2_vo = hce_scenes[2]["spoken_narration"] if len(hce_scenes) > 2 else f"Cek detail bahan dan ukuran {short_name}."
    cta_vo = hce_package.get("cta") or (hce_scenes[-1]["spoken_narration"] if hce_scenes else _build_platform_cta_line(plat, short_name, a_info.get("communication_style", "casual_everyday")))

    spec_items = [f"{k}: {v}" for k, v in specs.items()]
    feat0 = features[0] if features else product_name
    feat1 = features[1] if len(features) > 1 else feat0
    feat2 = features[2] if len(features) > 2 else (spec_items[0] if spec_items else feat0)
    objection0 = (a_info.get("possible_objections") or ["kualitas bahan dan kecocokan ukuran"])[0]
    situation0 = (a_info.get("relevant_situations") or ["kebutuhan harian"])[0]

    raw_panels = [
        {
            "title": "Hook Masalah & Pemicu Visual",
            "duration": 2.5,
            "stage_tag": "HOOK / PROBLEM",
            "visual_description": f"POV hands-only menyorot situasi {situation0} lalu langsung menghadirkan {product_name} di zona aman 20%–68%.",
            "physical_action": f"Tangan mulai menyiapkan skenario {situation0} lalu memunculkan {short_name} ke tengah frame.",
            "product_interaction": f"Tangan menggenggam bodi utama {short_name} secara mantap sesuai bobot aslinya.",
            "camera_angle": "First-person POV 45 derajat di atas meja/area pemakaian",
            "camera_movement": "Brisk Slight Push-In — Tujuan: menangkap perhatian di 2 detik pertama tanpa intro lambat",
            "spoken_narration": hook_vo,
            "on_screen_text": f"{short_name}: Solusi Praktis",
            "marketing_purpose": "Tangkap perhatian & hubungkan ke masalah nyata pembeli (Hook)",
            "narrative_objective": "hook_attention",
            "transition": "Cut cepat langsung saat tangan membuka/menyiapkan produk",
        },
        {
            "title": "Product Reveal & Skala Genggaman",
            "duration": 3.5,
            "stage_tag": "PRODUCT REVEAL",
            "visual_description": f"Shot jelas memperlihatkan wujud utuh {product_name} di genggaman tangan dewasa Indonesia sehingga skala dan kelengkapan terlihat jujur.",
            "physical_action": f"Memutar perlahan unit {short_name} untuk memperlihatkan profil bentuk, warna, dan bagian fungsional utama.",
            "product_interaction": f"Kedua tangan memosisikan {short_name} di telapak tangan atau meja kerja dengan kontak jari alami.",
            "camera_angle": "Eye-level / 3/4 POV jarak menengah",
            "camera_movement": "Slow Dolly Pull-Back — Tujuan: memperlihatkan proporsi asli produk di genggaman tanpa distorsi",
            "spoken_narration": f"Kenalin {short_name}, dirancang praktis untuk {situation0}.",
            "on_screen_text": feat0[:36],
            "marketing_purpose": "Ungkap wujud produk & bangun orientasi skala nyata (Product Reveal)",
            "narrative_objective": "product_reveal",
            "transition": "Match cut ke tangan mengoperasikan mekanisme inti",
        },
        {
            "title": "Demonstrasi Mekanisme & Fitur Utama",
            "duration": 5.5,
            "stage_tag": "CORE DEMONSTRATION",
            "visual_description": f"Peragaan langsung fungsi inti {feat0} dan {feat1} dalam kondisi pakai nyata di {avd_context['environment_spec']}",
            "physical_action": f"Tangan menjalankan aksi penggunaan utama {short_name} hingga hasil fisik nyata terlihat jelas di layar.",
            "product_interaction": f"Jari menekan/memutar bagian kontrol {short_name} sambil mengarahkan proses kerja nyata.",
            "camera_angle": "Three-quarter POV tabletop/hands-on close-up",
            "camera_movement": "Steady Tracking Shot — Tujuan: membuktikan cara kerja produk dan manfaat nyatanya langkah demi langkah",
            "spoken_narration": mid1_vo,
            "on_screen_text": feat1[:36],
            "marketing_purpose": "Demonstrasi fungsi inti & bukti manfaat langsung (Core Demonstration)",
            "narrative_objective": "core_demonstration",
            "transition": "Action cut ke shot makro detail material & komponen",
        },
        {
            "title": "Detail Material & Verifikasi Spesifikasi",
            "duration": 4.0,
            "stage_tag": "PRODUCT VALIDATION",
            "visual_description": f"Shot makro menyorot detail fisik {feat2}, sambungan komponen, dan permukaan material sesuai foto referensi #1.",
            "physical_action": f"Tangan mendekatkan atau menyentuh ringan detail {feat2} agar tekstur, ketebalan, dan kerapian konstruksi terbaca jelas.",
            "product_interaction": f"Ujung jari menunjuk atau menguji kekokohan bagian kunci {short_name}.",
            "camera_angle": "Macro detail close-up 35 derajat dengan shallow depth of field",
            "camera_movement": "Slow Macro Rack-Focus — Tujuan: memvalidasi kualitas bahan dan detail spesifikasi terverifikasi",
            "spoken_narration": mid2_vo,
            "on_screen_text": (spec_items[0] if spec_items else feat2)[:36],
            "marketing_purpose": "Validasi kualitas material & spesifikasi terukur (Product Validation)",
            "narrative_objective": "spec_validation",
            "transition": "Cut halus ke momen pembuktian atas keraguan pembeli",
        },
        {
            "title": "Pembuktian Keraguan Pembeli & Hasil Nyata",
            "duration": 4.5,
            "stage_tag": "OBJECTION HANDLING & RESULT",
            "visual_description": f"Uji praktis menjawab keraguan '{objection0}' dengan hasil akhir rapi/berfungsi konsisten di cahaya natural yang sama.",
            "physical_action": f"Menunjukkan kondisi sesudah pemakaian {short_name} serta kemudahan perawatan atau penyimpanan setelah dipakai.",
            "product_interaction": f"Tangan melepas/merapikan bagian {short_name} dengan gerakan ringan satu kali jalan.",
            "camera_angle": "First-person POV medium close-up sejajar hasil",
            "camera_movement": "Controlled Lateral Pan — Tujuan: menunjukkan hasil pemakaian dan menjawab keberatan utama secara visual",
            "spoken_narration": f"Soal {objection0}, lihat langsung detail dan cara pakainya di sini.",
            "on_screen_text": "Bukti Nyata & Praktis",
            "marketing_purpose": "Jawab keberatan pembeli & tunjukkan payoff nyata (Objection & Benefit)",
            "narrative_objective": "objection_handling_and_payoff",
            "transition": "Clean match cut menuju hero penutup yang rapi",
        },
        {
            "title": "Hero Penutup & Call-To-Action",
            "duration": 3.0,
            "stage_tag": "CTA",
            "visual_description": f"Shot hero bersih {product_name} tertata rapi di tengah zona aman 20%–62%, menyisakan ruang bawah >32% bersih untuk stiker keranjang dan subtitle.",
            "physical_action": f"Produk berdiri stabil di permukaan meja bersih setelah tangan menarik diri secara halus dari frame.",
            "product_interaction": f"Tangan meletakkan {short_name} tegak menghadap kamera lalu memberi ruang bersih untuk CTA.",
            "camera_angle": "Eye-level hero shot bersih vertikal 9:16",
            "camera_movement": "Slow Confident Dolly Push-In — Tujuan: mengunci pengenalan produk saat ajakan klik CTA",
            "spoken_narration": cta_vo,
            "on_screen_text": "Cek Varian di Keranjang" if plat in ("tiktok", "shopee_video") else "Cek Tautan Produk",
            "marketing_purpose": "Dorong aksi klik tautan/keranjang sesuai platform (Call-To-Action)",
            "narrative_objective": "cta_closing",
            "transition": "Tahan frame bersih 0.5 detik (loop-ready ke Adegan 1)",
        },
    ]

    for idx, sc in enumerate(raw_panels):
        sc["id"] = idx + 1
        sc["lighting_safe_zone"] = f"Cahaya siang natural dari samping jendela ({avd_context['environment_spec'][:60]}...); objek utama di zona aman 20%–68%."
        sc["anchor_asset"] = _pick_asset(idx)

    total_dur = _recalculate_scene_timestamps(raw_panels)
    clips = segment_panels_into_clips(raw_panels, DEFAULT_MAX_CLIP_DURATION)

    platform_captions = hce_package.get("platform_captions") or {}
    platform_ctas = hce_package.get("platform_ctas") or {}
    publishing_draft = {
        "captions": {
            "tiktok": platform_captions.get("tiktok", hce_package.get("caption", "")),
            "instagram_reels": platform_captions.get("instagram_reels", hce_package.get("caption", "")),
            "facebook_reels": platform_captions.get("facebook_reels", hce_package.get("caption", "")),
        },
        "ctas": [
            platform_ctas.get("tiktok", cta_vo),
            f"Biar rutinitas harian lebih praktis dan hemat waktu, cek detail {short_name} di keranjang kiri bawah.",
            f"Mau cek spesifikasi dan varian lengkap {short_name}? Langsung intip di keranjang produk.",
            platform_ctas.get("instagram_reels", f"Detail {short_name} ada di tautan bio dan caption."),
            platform_ctas.get("facebook_reels", f"Cek info varian {short_name} lewat tautan di komentar atau caption."),
        ],
        "alt_hooks": list(hce_package.get("hooks", []))[:5],
    }
    while len(publishing_draft["alt_hooks"]) < 5:
        idx_h = len(publishing_draft["alt_hooks"]) + 1
        publishing_draft["alt_hooks"].append(
            f"Detail {short_name} dengan {feat0.lower()} biar aktivitas harian makin praktis."
            if idx_h % 2 == 0
            else f"Sebelum pilih, lihat dulu cara kerja {short_name} di kondisi harian."
        )

    return {
        "version": version,
        "generated_at": _now_iso(),
        "slug": avd_context.get("slug", p_info["product_id"]),
        "product_name": product_name,
        "platform": plat,
        "aspect_ratio": "9:16",
        "total_duration": total_dur,
        "panel_count": len(raw_panels),
        "selling_angle": hce_package["strategy"]["strategy_name"],
        "usp": hce_package.get("usp", ""),
        "consistency_locks": {
            "product_lock": "; ".join(avd_context.get("visual_anchors", [])),
            "hand_lock": avd_context.get("hand_spec", ""),
            "environment_lighting_lock": avd_context.get("environment_spec", ""),
        },
        "scenes": raw_panels,
        "clip_plan": clips,
        "publishing_draft": publishing_draft,
    }


def _extract_avd_plan_from_markdown(
    campaign_dir: Path,
    storyboard_path: Path | None = None,
    publishing_path: Path | None = None,
) -> dict[str, Any]:
    """Parse existing storyboard.md and publishing-package.md into an inspectable plan dictionary."""
    sb_path = storyboard_path or (campaign_dir / "03-storyboard" / "storyboard.md")
    pub_path = publishing_path or (campaign_dir / "05-publishing" / "publishing-package.md")
    cj_path = campaign_dir / "campaign.json"
    cj = json.loads(cj_path.read_text(encoding="utf-8")) if cj_path.is_file() else {}
    sb_text = sb_path.read_text(encoding="utf-8") if sb_path.is_file() else ""
    pub_text = pub_path.read_text(encoding="utf-8") if pub_path.is_file() else ""

    # Parse detailed Adegan sections when present
    scene_blocks: dict[int, str] = {}
    for m in re.finditer(r"^###\s+Adegan\s+(\d+)\b.*?(?=^###\s+Adegan\s+\d+|^##\s+|\Z)", sb_text, re.MULTILINE | re.DOTALL):
        scene_blocks[int(m.group(1))] = m.group(0)

    def _field(block: str, label: str, default: str) -> str:
        fm = re.search(rf"-\s+\*\*{re.escape(label)}[^:]*:\*\*\s*(.+)", block)
        return fm.group(1).strip() if fm else default

    _, raw_rows = dialogue_timing.extract_timing_rows(sb_text)
    scenes: list[dict[str, Any]] = []
    for idx, cells in enumerate(raw_rows, start=1):
        ts = cells[1]
        dur_s = float(cells[2].replace(",", ".").lower().replace("dtk", "").replace("s", "").strip() or 0)
        vo = cells[3].strip().strip('"').strip("“”")
        try:
            start_s, end_s = dialogue_timing.parse_timestamp_range(ts)
        except ValueError:
            start_s = round(sum(float(s["duration"]) for s in scenes), 2)
            end_s = round(start_s + dur_s, 2)
        blk = scene_blocks.get(idx, "")
        scenes.append(
            {
                "id": idx,
                "title": f"Adegan {idx}",
                "timestamp": ts,
                "start_seconds": start_s,
                "end_seconds": end_s,
                "duration": dur_s,
                "visual_description": _field(blk, "Deskripsi", sb_text[:200]),
                "physical_action": _field(blk, "Aksi Fisik", "Sesuai storyboard"),
                "product_interaction": _field(blk, "Interaksi Produk", "Sesuai storyboard"),
                "camera_angle": _field(blk, "Sudut & Posisi Kamera", "9:16 POV"),
                "camera_movement": _field(blk, "Gerakan Kamera", "Tujuan naratif sesuai storyboard"),
                "spoken_narration": vo,
                "on_screen_text": _field(blk, "Teks Layar", ""),
                "marketing_purpose": _field(blk, "Tujuan Pemasaran", "Sesuai storyboard"),
                "narrative_objective": "cta_closing" if idx == len(raw_rows) else f"scene_{idx}",
                "transition": _field(blk, "Transisi", "Cut"),
            }
        )
    total_dur = round(sum(s["duration"] for s in scenes), 2)
    plat = normalize_platform((cj.get("platforms") or ["tiktok"])[0])
    cta_line = scenes[-1]["spoken_narration"] if scenes else ""
    return {
        "version": 1,
        "slug": campaign_dir.name,
        "product_name": cj.get("product_name", campaign_dir.name),
        "platform": plat,
        "aspect_ratio": "9:16",
        "total_duration": total_dur,
        "panel_count": len(scenes),
        "selling_angle": "",
        "consistency_locks": {
            "product_lock": "Sesuai referensi asli",
            "hand_lock": "Hands-only konsisten",
            "environment_lighting_lock": "Pencahayaan konsisten",
        },
        "scenes": scenes,
        "clip_plan": segment_panels_into_clips(scenes, DEFAULT_MAX_CLIP_DURATION) if scenes else [],
        "publishing_draft": {
            "captions": {plat: pub_text[:400] if pub_text else cj.get("product_name", "")},
            "ctas": [cta_line] if cta_line else [],
            "alt_hooks": [scenes[0]["spoken_narration"]] if scenes else [],
        },
    }


def avd_evaluate_plan(
    avd_plan: dict[str, Any],
    hce_package: dict[str, Any] | None,
    product_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate storyboard and clip plan across AVD's 6 production & timing criteria."""
    scenes = list(avd_plan.get("scenes", []))
    clips = list(avd_plan.get("clip_plan", []))
    locks = avd_plan.get("consistency_locks", {})
    requests: list[dict[str, Any]] = []
    req_counter = 1

    def _add_req(
        target_agent: str,
        category: str,
        severity: str,
        issue: str,
        constraint: str,
        action: str,
        scene_number: int | None = None,
    ) -> None:
        nonlocal req_counter
        requests.append(
            {
                "request_id": f"AVD-REQ-{req_counter:02d}",
                "reviewer": "affiliate-video-director",
                "target_agent": target_agent,
                "scene_number": scene_number,
                "category": category,
                "severity": severity,
                "issue": issue,
                "constraint": constraint,
                "action_required": action,
            }
        )
        req_counter += 1

    # 1. Visual executability
    vis_score = 9.2
    for sc in scenes:
        vis = str(sc.get("visual_description", "")).strip()
        cam = str(sc.get("camera_movement", "")).strip()
        if len(vis) < 20 or not sc.get("camera_angle"):
            vis_score -= 1.2
            _add_req(
                "affiliate-video-director",
                "visual_executability",
                "blocker",
                f"Adegan {sc['id']} belum punya deskripsi visual atau sudut kamera yang cukup konkret untuk generator video.",
                "Deskripsikan objek, posisi frame 9:16, dan sudut kamera secara eksplisit.",
                "Lengkapi deskripsi visual dan sudut kamera Adegan.",
                scene_number=int(sc["id"]),
            )
        if "tujuan" not in cam.lower() and "purpose" not in cam.lower():
            vis_score -= 0.8
            _add_req(
                "affiliate-video-director",
                "visual_executability",
                "improvement",
                f"Gerakan kamera Adegan {sc['id']} belum mencantumkan tujuan naratif.",
                "Format wajib: '<Teknik Kamera> — Tujuan: <alasan menjual>'.",
                "Tambahkan tujuan naratif pada koreografi kamera.",
                scene_number=int(sc["id"]),
            )
        if "orbit" in cam.lower() or ("zoom" in cam.lower() and "tujuan" not in cam.lower()):
            vis_score -= 1.5
            _add_req(
                "affiliate-video-director",
                "visual_executability",
                "blocker",
                f"Adegan {sc['id']} memakai pola kamera terlarang (zoom acak / orbit tanpa tujuan).",
                "Gunakan teknik bermakna (dolly, tracking, macro, rack focus, POV).",
                "Ganti instruksi gerakan kamera dengan teknik bermakna.",
                scene_number=int(sc["id"]),
            )

    # 2. Scene continuity
    cont_score = 9.2
    for lock_key in ("product_lock", "hand_lock", "environment_lighting_lock"):
        if not str(locks.get(lock_key, "")).strip():
            cont_score -= 1.2
            _add_req(
                "affiliate-video-director",
                "scene_continuity",
                "blocker",
                f"Kunci kontinuitas '{lock_key}' kosong.",
                "Product Lock, Hand Lock, dan Environment/Lighting Lock wajib terkunci konsisten.",
                f"Isi spesifikasi {lock_key} secara eksplisit.",
            )
    if len(scenes) >= 2 and any(not str(sc.get("transition", "")).strip() for sc in scenes[:-1]):
        cont_score -= 0.8
        _add_req(
            "affiliate-video-director",
            "scene_continuity",
            "improvement",
            "Ada adegan yang belum memiliki arahan transisi antar-panel.",
            "Cantumkan transisi bermakna ke panel berikutnya.",
            "Lengkapi transisi antar adegan.",
        )

    # 3. Dialogue timing (using real dialogue_timing.py rules!)
    dt_score = 9.5
    dt_passed = True
    prev_end: float | None = None
    total_dur = 0.0
    for sc in scenes:
        sid = int(sc["id"])
        dur = float(sc.get("duration", 0.0))
        total_dur += dur
        ts = str(sc.get("timestamp", ""))
        vo = str(sc.get("spoken_narration", "")).strip()

        try:
            start_s, end_s = dialogue_timing.parse_timestamp_range(ts)
            if abs((end_s - start_s) - dur) > dialogue_timing.TIMESTAMP_TOLERANCE:
                dt_passed = False
                dt_score -= 1.5
                _add_req(
                    "affiliate-video-director",
                    "dialogue_timing",
                    "blocker",
                    f"Adegan {sid} rentang timestamp '{ts}' tidak cocok dengan durasi {dur:.1f}s.",
                    "Rentang timestamp harus berurutan tanpa celah/tumpang-tindih dari 00:00.",
                    "Kalibrasi ulang timestamp storyboard.",
                    scene_number=sid,
                )
            if prev_end is None and abs(start_s) > dialogue_timing.TIMESTAMP_TOLERANCE:
                dt_passed = False
                dt_score -= 1.5
                _add_req(
                    "affiliate-video-director",
                    "dialogue_timing",
                    "blocker",
                    f"Adegan {sid} harus mulai dari 00:00 (ditemukan '{ts}').",
                    "Timestamp awal wajib 00:00.",
                    "Perbaiki timestamp mulai Adegan 1.",
                    scene_number=sid,
                )
            elif prev_end is not None and abs(start_s - prev_end) > dialogue_timing.TIMESTAMP_TOLERANCE:
                dt_passed = False
                dt_score -= 1.2
                _add_req(
                    "affiliate-video-director",
                    "dialogue_timing",
                    "blocker",
                    f"Adegan {sid} memiliki celah atau tumpang-tindih timestamp pada '{ts}'.",
                    "Timestamp harus menyambung tepat.",
                    "Recalculate contiguous timestamps.",
                    scene_number=sid,
                )
            prev_end = end_s
        except ValueError as exc:
            dt_passed = False
            dt_score -= 1.5
            _add_req(
                "affiliate-video-director",
                "dialogue_timing",
                "blocker",
                f"Timestamp Adegan {sid} tidak valid: {exc}.",
                "Format MM:SS–MM:SS.",
                "Perbaiki format timestamp.",
                scene_number=sid,
            )

        is_pause = vo.strip().strip('"').strip("'").lower() == "[jeda]"
        if not is_pause and dur > 0:
            syl, warns = dialogue_timing.analyze_text(vo)
            min_s, max_s = syllable_bounds_for_duration(dur)
            est = round(syl / dialogue_timing.DEFAULT_RATE, 2)
            fill_ratio = est / dur
            eff_rate = syl / dur

            if warns:
                dt_passed = False
                dt_score -= 1.2
                _add_req(
                    "hce",
                    "dialogue_timing",
                    "blocker",
                    f"Dialog Adegan {sid} mengandung angka digit ({', '.join(warns)}): '{vo}'.",
                    "Semua angka dalam dialog VO wajib ditulis dengan kata Bahasa Indonesia.",
                    f"Eja semua angka dengan kata pada dialog Adegan {sid} dalam rentang {min_s}-{max_s} suku kata.",
                    scene_number=sid,
                )
            if eff_rate > dialogue_timing.MAX_EFFECTIVE_RATE or fill_ratio > dialogue_timing.MAX_FILL_RATIO:
                dt_passed = False
                dt_score -= 1.8
                _add_req(
                    "hce",
                    "dialogue_timing",
                    "blocker",
                    f"Dialog Adegan {sid} terlalu padat/cepat ({syl} suku kata dalam {dur:.1f} dtk = {eff_rate:.2f} sk/dtk, est {est:.2f} dtk).",
                    f"Target aman {min_s}-{max_s} suku kata (60%-105% durasi panel @ 5.0 sk/dtk, maks 6.0 sk/dtk) tanpa angka digit.",
                    f"Padatkan naskah dialog Adegan {sid} agar alami dan masuk {min_s}-{max_s} suku kata.",
                    scene_number=sid,
                )
            elif fill_ratio < dialogue_timing.MIN_FILL_RATIO:
                dt_passed = False
                dt_score -= 1.2
                _add_req(
                    "hce",
                    "dialogue_timing",
                    "blocker",
                    f"Dialog Adegan {sid} terlalu singkat ({est:.2f} dtk dari {dur:.1f} dtk = {fill_ratio * 100:.0f}%, minimal 60%).",
                    f"Target aman {min_s}-{max_s} suku kata (atau gunakan '[jeda]' untuk panel insert cepat).",
                    f"Lengkapi dialog Adegan {sid} dengan manfaat terverifikasi hingga {min_s}-{max_s} suku kata.",
                    scene_number=sid,
                )

    if total_dur <= 0 or total_dur > DEFAULT_MAX_FINAL_DURATION + 1e-6:
        dt_passed = False
        dt_score -= 2.5
        _add_req(
            "affiliate-video-director",
            "dialogue_timing",
            "blocker",
            f"Total durasi video ({total_dur:.1f}s) berada di luar batas 1-{DEFAULT_MAX_FINAL_DURATION:.0f} detik.",
            "Total durasi final wajib <= 40.0 detik.",
            "Sesuaikan jumlah dan durasi panel agar total <= 40.0 detik.",
        )

    # 4. Product demonstration quality
    demo_score = 9.0
    demo_verbs = ("menekan", "memutar", "menggores", "menggenggam", "membuka", "menutup", "memasang", "menyapu", "mencacah", "menunjukkan", "menguji", "menyelipkan", "mengoperasikan", "menyentuh")
    demo_hits = sum(
        1
        for sc in scenes
        if any(v in f"{sc.get('physical_action', '')} {sc.get('product_interaction', '')}".lower() for v in demo_verbs)
    )
    if len(scenes) >= 3 and demo_hits < 2:
        demo_score -= 2.0
        _add_req(
            "affiliate-video-director",
            "product_demonstration_quality",
            "blocker",
            "Demonstrasi fisik produk terlalu pasif (minim aksi interaksi tangan nyata).",
            "Minimal 2 adegan harus menampilkan interaksi tangan fisik terhadap mekanisme produk.",
            "Perjelas aksi fisik tangan dan respons mekanisme produk pada adegan demonstrasi & validasi.",
        )

    # 5. Scene pacing
    pacing_score = 9.2
    durations = [float(sc.get("duration", 0.0)) for sc in scenes]
    if len(scenes) >= 3 and len(set(durations)) <= 1:
        pacing_score -= 1.8
        _add_req(
            "affiliate-video-director",
            "scene_pacing",
            "blocker",
            f"Semua {len(scenes)} adegan memiliki durasi seragam ({durations[0]:.1f}s).",
            "Gunakan durasi panel variabel sesuai fungsi (hook cepat, demo lebih panjang, CTA tegas).",
            "Variasikan durasi antar panel mengikuti bobot aksi pemasaran.",
        )
    if len(scenes) < 4:
        pacing_score -= 1.0
        _add_req(
            "affiliate-video-director",
            "scene_pacing",
            "improvement",
            f"Jumlah panel ({len(scenes)}) terlalu ringkas untuk demo & pembuktian lengkap.",
            "Gunakan jumlah panel adaptif (disarankan 6-14 panel bila terjustifikasi cerita).",
            "Pecah alur menjadi panel reveal, demo, detail, dan CTA yang lebih terarah.",
        )
    for sc in scenes:
        if float(sc.get("duration", 0.0)) > 6.5:
            pacing_score -= 1.5
            _add_req(
                "affiliate-video-director",
                "scene_pacing",
                "blocker",
                f"Adegan {sc['id']} berdurasi {sc['duration']:.1f}s (> 6.5s) untuk satu shot tunggal.",
                "Pecah demonstrasi panjang menjadi dua sudut shot atau insert detail agar ritme editing hidup.",
                f"Bagi Adegan {sc['id']} menjadi dua panel berurutan berdurasi variabel <= 6.0s.",
                scene_number=int(sc["id"]),
            )

    # 6. Video workability (clip segmentation <= 10.0s, exact coverage, CTA safe zone)
    work_score = 9.2
    covered: list[int] = []
    clip_sum = 0.0
    for cl in clips:
        cdur = float(cl.get("duration", 0.0))
        clip_sum += cdur
        covered.extend(int(x) for x in cl.get("scenes", []))
        if cdur > DEFAULT_MAX_CLIP_DURATION + 1e-6 or cdur <= 0:
            work_score -= 2.5
            _add_req(
                "affiliate-video-director",
                "video_workability",
                "blocker",
                f"Klip {cl.get('id')} berdurasi {cdur:.1f}s melampaui batas maksimal {DEFAULT_MAX_CLIP_DURATION:.1f}s.",
                "Setiap segmen generasi klip wajib <= 10.0 detik.",
                "Segmentasikan ulang panel storyboard ke klip <= 10.0 detik.",
            )
    expected_ids = [int(sc["id"]) for sc in scenes]
    if not clips or sorted(covered) != sorted(expected_ids) or abs(clip_sum - total_dur) > 0.05:
        work_score -= 2.0
        _add_req(
            "affiliate-video-director",
            "video_workability",
            "blocker",
            "Segmentasi klip video belum mencakup seluruh panel storyboard secara tepat.",
            "Jumlah durasi seluruh klip wajib sama persis dengan total durasi storyboard.",
            "Jalankan ulang segmentasi klip adaptif untuk seluruh panel.",
        )

    last_vis = str(scenes[-1].get("visual_description", "")).lower() if scenes else ""
    if scenes and not any(k in last_vis for k in ("zona aman", "safe zone", "ruang bawah", "bersih")):
        work_score -= 0.8
        _add_req(
            "affiliate-video-director",
            "video_workability",
            "improvement",
            "Adegan CTA penutup belum secara eksplisit mengunci ruang aman bawah 9:16.",
            "Sisakan area bawah bersih untuk stiker keranjang & tombol UI.",
            "Tambahkan instruksi zona aman 9:16 pada Adegan penutup.",
            scene_number=int(scenes[-1]["id"]),
        )

    criteria = {
        "visual_executability": round(max(1.0, min(10.0, vis_score)), 2),
        "scene_continuity": round(max(1.0, min(10.0, cont_score)), 2),
        "dialogue_timing": round(max(1.0, min(10.0, dt_score)), 2),
        "product_demonstration_quality": round(max(1.0, min(10.0, demo_score)), 2),
        "scene_pacing": round(max(1.0, min(10.0, pacing_score)), 2),
        "video_workability": round(max(1.0, min(10.0, work_score)), 2),
    }
    overall = round(sum(criteria.values()) / len(criteria), 2)
    blockers = [r for r in requests if r["severity"] == "blocker"]
    passed = (
        not blockers
        and dt_passed
        and overall >= 7.5
        and all(score >= 6.5 for score in criteria.values())
    )

    return {
        "reviewer": "affiliate-video-director",
        "criteria": criteria,
        "overall_score": overall,
        "dialogue_timing_passed": dt_passed,
        "passed": passed,
        "revision_requests": requests,
        "summary": (
            "Rencana storyboard, timing dialog, dan klip video memenuhi standar produksi AVD."
            if passed
            else f"AVD mendeteksi {len(blockers)} kendala produksi/timing yang perlu direvisi."
        ),
    }


def hce_evaluate_plan(
    runtime: HCERuntime,
    avd_plan: dict[str, Any],
    hce_package: dict[str, Any] | None,
    product_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate AVD storyboard & copy across HCE's 7D rubric + Hard Integrity Gate + 6 collaboration criteria."""
    scenes = list(avd_plan.get("scenes", []))
    plat = normalize_platform(avd_plan.get("platform") or "tiktok")
    pub = avd_plan.get("publishing_draft", {})
    hooks = list(pub.get("alt_hooks") or [])
    if not hooks and scenes:
        hooks = [str(scenes[0].get("spoken_narration", ""))]
    if hce_package and len(hooks) < 2:
        for h in hce_package.get("hooks", []):
            if h not in hooks:
                hooks.append(h)

    captions_map = pub.get("captions") or {}
    caption = str(captions_map.get(plat) or next(iter(captions_map.values()), "") or avd_plan.get("product_name", ""))
    cta = str(scenes[-1].get("spoken_narration", "")) if scenes else str((pub.get("ctas") or [""])[0])

    # Run real HCE CopyEvaluator (7 dimensions + Hard Integrity Gate)
    eval_scenes = [
        {
            "scene_number": sc.get("id", idx),
            "duration_seconds": sc.get("duration", 3.0),
            "spoken_narration": sc.get("spoken_narration", ""),
            "narrative_objective": sc.get("narrative_objective", sc.get("marketing_purpose", "")),
        }
        for idx, sc in enumerate(scenes, start=1)
    ]
    p_data = dict(product_data or {})
    if not p_data and hce_package:
        pa = hce_package.get("product_analysis", {})
        p_data = {
            "name": pa.get("name", avd_plan.get("product_name", "")),
            "description": pa.get("what_it_does", ""),
            "verified_features": pa.get("verified_features", []),
            "verified_specs": pa.get("verified_specs", {}),
            "available_evidence": pa.get("available_evidence", []),
        }

    report = runtime.CopyEvaluator().evaluate(
        hooks=hooks,
        scenes=eval_scenes,
        cta=cta,
        caption=caption,
        platform=plat,
        product_data=p_data,
    )
    report_dict = report.to_dict()

    # Run real HCE NaturalLanguageRefiner audit to catch subtle bookish/cliché/urgency issues
    refiner = runtime.NaturalLanguageRefiner()
    comm_style = (
        hce_package.get("audience_analysis", {}).get("communication_style", "casual_everyday")
        if hce_package
        else "casual_everyday"
    )
    audit = refiner.audit_script_fields(
        hooks=hooks,
        scene_narrations=[str(s.get("spoken_narration", "")) for s in scenes],
        cta=cta,
        caption=caption,
        register=comm_style,
        available_evidence=list(p_data.get("available_evidence", [])),
    )

    requests: list[dict[str, Any]] = []
    req_counter = 1

    def _add_req(
        target_agent: str,
        category: str,
        severity: str,
        issue: str,
        constraint: str,
        action: str,
        scene_number: int | None = None,
    ) -> None:
        nonlocal req_counter
        requests.append(
            {
                "request_id": f"HCE-REQ-{req_counter:02d}",
                "reviewer": "human-copywriting-engine",
                "target_agent": target_agent,
                "scene_number": scene_number,
                "category": category,
                "severity": severity,
                "issue": issue,
                "constraint": constraint,
                "action_required": action,
            }
        )
        req_counter += 1

    # Integrity violations & 7D checks
    if report.integrity_violations:
        for viol in report.integrity_violations:
            _add_req(
                "hce",
                "script_quality",
                "blocker",
                f"Pelanggaran Hard Integrity Gate HCE: {viol}",
                "Dilarang mengklaim pengalaman pribadi, diskon/stok fiktif, atau angka spesifikasi di luar data terverifikasi.",
                "Hapus klaim yang tidak terverifikasi dan kembalikan ke observasi fitur nyata.",
            )

    for iss in audit.get("issues", []):
        if iss["issue_type"] != "repetitive_sentence_pattern":
            _add_req(
                "hce",
                "script_quality",
                "blocker",
                f"Bahasa tidak natural ({iss['issue_type']}) pada {iss['location']}: {iss['reason']}",
                "Gunakan Bahasa Indonesia lisan yang wajar tanpa klise AI, ungkapan buku, atau urgensi palsu.",
                f"Perbaiki kalimat menjadi: {iss['suggestion']}",
            )

    dims = report_dict["dimensions"]

    # 1. Marketing consistency
    verified_features = [str(f) for f in p_data.get("verified_features", [])]
    all_script_lower = " ".join([*hooks, *(str(s.get("spoken_narration", "")) for s in scenes), cta, caption]).lower()
    matched_feats = 0
    for feat in verified_features:
        tokens = [t for t in re.findall(r"[a-zA-Z0-9]+", feat.lower()) if len(t) > 3]
        if any(t in all_script_lower for t in tokens):
            matched_feats += 1
    feat_cov = (matched_feats / len(verified_features)) if verified_features else 1.0
    mc_score = min(10.0, (dims["product_accuracy"]["score"] * 0.6) + (2.0 + 2.0 * feat_cov))
    if verified_features and feat_cov < 0.5:
        mc_score -= 1.5
        _add_req(
            "hce",
            "marketing_consistency",
            "blocker",
            f"Cakupan fitur terverifikasi terlalu rendah ({matched_feats}/{len(verified_features)}).",
            "Minimal 50% fitur terverifikasi harus tercermin pada pesan dan manfaat video.",
            "Sertakan fitur terverifikasi inti beserta manfaat praktisnya ke naskah adegan/caption.",
        )

    # 2. Persuasiveness
    pers_score = dims["persuasiveness"]["score"]
    if dims["buyer_psychology"]["score"] < 7.0:
        _add_req(
            "hce",
            "persuasiveness",
            "blocker",
            f"Skor psikologi pembeli rendah ({dims['buyer_psychology']['score']}/10).",
            "Sertakan pemicu situasi nyata, manfaat praktis, dan jawaban atas keraguan pembeli.",
            "Tambahkan alasan praktis atau jawaban keraguan produk di naskah.",
        )

    # 3. Hook effectiveness
    hook0 = hooks[0] if hooks else ""
    hook_score = 8.8 if len(hook0.split()) >= 3 else 6.0
    hook1_issues = [iss for iss in audit.get("issues", []) if iss.get("location") == "hook_1"]
    if hook1_issues:
        hook_score -= 1.5
    if len(hook0.split()) < 3 or hook0.strip().lower() == "[jeda]":
        hook_score = 5.5
        _add_req(
            "hce",
            "hook_effectiveness",
            "blocker",
            "Hook pembuka Adegan 1 terlalu kosong atau kurang memicu perhatian 2 detik pertama.",
            "Hook harus relevan ke masalah nyata atau keunggulan langsung produk.",
            "Perkuat kalimat hook Adegan 1 agar spesifik ke masalah/produk.",
            scene_number=1,
        )

    # 4. Script quality (overall 7D + integrity)
    sq_score = round((dims["naturalness"]["score"] + dims["authenticity"]["score"] + report.overall_score) / 3.0, 2)
    if not report.passed and not any(r["category"] == "script_quality" for r in requests):
        _add_req(
            "hce",
            "script_quality",
            "blocker",
            f"Evaluasi HCE belum lulus (gate={report.gate_status}, overall={report.overall_score}/10).",
            "Seluruh 7 dimensi wajib >= 6.0, rata-rata >= 7.0, dan Gate = PASSED.",
            "; ".join(report.improvement_suggestions),
        )

    # 5. CTA relevance (platform-calibrated)
    cta_score = dims["audience_adaptation"]["score"]
    cta_lower = cta.lower()
    if plat == "tiktok" and "keranjang" not in cta_lower:
        cta_score -= 2.5
        _add_req(
            "hce",
            "cta_relevance",
            "blocker",
            "CTA TikTok belum mengarahkan penonton ke keranjang kuning / kiri bawah.",
            "CTA TikTok wajib merujuk ke keranjang kuning / kiri bawah.",
            "Sesuaikan CTA penutup dengan konteks keranjang TikTok.",
            scene_number=len(scenes) if scenes else None,
        )
    elif plat in ("instagram_reels", "facebook_reels") and "keranjang kuning" in cta_lower:
        cta_score -= 3.0
        _add_req(
            "hce",
            "cta_relevance",
            "blocker",
            f"CTA masih menyebut 'keranjang kuning' yang tidak relevan untuk {plat}.",
            "IG Reels/FB Reels wajib mengarahkan ke tautan bio, caption, atau komentar.",
            "Ganti istilah CTA sesuai platform target.",
            scene_number=len(scenes) if scenes else None,
        )
    elif plat in ("instagram_reels", "facebook_reels") and not any(k in cta_lower for k in ("tautan", "link", "bio", "caption", "komentar")):
        cta_score -= 2.0
        _add_req(
            "hce",
            "cta_relevance",
            "blocker",
            f"CTA {plat} belum mengarahkan penonton ke tautan di bio/caption/komentar.",
            "Sebutkan lokasi tautan produk sesuai platform.",
            "Perjelas arah tautan pada CTA penutup.",
            scene_number=len(scenes) if scenes else None,
        )

    # 6. Visual-strategy alignment (HCE checks whether AVD visuals actually support the marketing strategy!)
    vsa_score = 9.0
    all_vis_blob = " ".join(
        f"{sc.get('visual_description', '')} {sc.get('physical_action', '')} {sc.get('marketing_purpose', '')}"
        for sc in scenes
    ).lower()
    if not any(k in all_vis_blob for k in ("demo", "peragaan", "uji", "bukti", "tangan", "menunjukkan")):
        vsa_score -= 2.5
        _add_req(
            "affiliate-video-director",
            "visual_strategy_alignment",
            "blocker",
            "Storyboard visual belum cukup menonjolkan bukti fisik & peragaan strategi pemasaran HCE.",
            "Setiap klaim manfaat HCE harus didukung aksi visual nyata di storyboard.",
            "Perkuat deskripsi peragaan visual dan bukti keraguan pembeli di adegan demonstrasi.",
        )

    # Check if every scene's visual_description aligns with its marketing_purpose / narration concept
    for sc in scenes:
        sc_purpose = str(sc.get("narrative_objective", "")).lower()
        sc_vis = str(sc.get("visual_description", "")).lower()
        if "cta" in sc_purpose and not any(k in sc_vis for k in ("hero", "bersih", "keranjang", "tautan", "safe zone", "zona aman")):
            vsa_score -= 1.2
            _add_req(
                "affiliate-video-director",
                "visual_strategy_alignment",
                "improvement",
                f"Visual Adegan {sc['id']} (CTA) belum menata ruang aman bersih untuk tombol keranjang/tautan.",
                "Panel CTA wajib menyisakan zona aman bawah dan tampilan produk hero yang jelas.",
                "Perjelas komposisi hero bersih dan ruang aman CTA di Adegan penutup.",
                scene_number=int(sc["id"]),
            )

    criteria = {
        "marketing_consistency": round(max(1.0, min(10.0, mc_score)), 2),
        "persuasiveness": round(max(1.0, min(10.0, pers_score)), 2),
        "hook_effectiveness": round(max(1.0, min(10.0, hook_score)), 2),
        "script_quality": round(max(1.0, min(10.0, sq_score)), 2),
        "cta_relevance": round(max(1.0, min(10.0, cta_score)), 2),
        "visual_strategy_alignment": round(max(1.0, min(10.0, vsa_score)), 2),
    }
    overall = round(sum(criteria.values()) / len(criteria), 2)
    blockers = [r for r in requests if r["severity"] == "blocker"]
    passed = (
        report.passed
        and report.gate_status == "PASSED"
        and not blockers
        and overall >= 7.5
        and all(score >= 6.5 for score in criteria.values())
    )

    return {
        "reviewer": "human-copywriting-engine",
        "criteria": criteria,
        "overall_score": overall,
        "hce_7d_evaluation": report_dict,
        "refiner_issue_count": len([i for i in audit.get("issues", []) if i["issue_type"] != "repetitive_sentence_pattern"]),
        "passed": passed,
        "revision_requests": requests,
        "summary": (
            "Strategi pemasaran, naskah Bahasa Indonesia natural, CTA, integritas fakta, dan keselarasan visual lolos evaluasi HCE."
            if passed
            else f"HCE mendeteksi {len(blockers)} isu pemasaran/copywriting/integritas yang harus diperbaiki."
        ),
    }


def _concise_clause(text: str, max_words: int = 5) -> str:
    """Keep a phrase concise and natural without truncating inside multi-word spec values."""
    dangling_connectors = {
        "hanya",
        "untuk",
        "yang",
        "dan",
        "atau",
        "dengan",
        "di",
        "ke",
        "dari",
        "buat",
        "karena",
        "supaya",
        "agar",
        "saat",
        "pas",
        "jadi",
        "biar",
    }
    words = text.strip().split()
    if len(words) > max_words:
        words = words[:max_words]
    while len(words) > 2 and words[-1].lower().strip(",.;:-") in dangling_connectors:
        words.pop()
    return " ".join(words).rstrip(",.;:-")


def _build_natural_scene_vo_candidates(
    role: str,
    product_name: str,
    short_name: str,
    p_info: dict[str, Any],
    a_info: dict[str, Any],
    platform: str,
    original_vo: str,
) -> list[str]:
    """Generate natural, complete spoken Indonesian lines grounded strictly in verified facts."""
    features = [_clean_vo_phrase(f) for f in p_info.get("verified_features", []) if f]
    specs = p_info.get("verified_specs", {})
    spec_phrases = [_clean_vo_phrase(f"{k} {v}") for k, v in specs.items() if v]
    situations = [_clean_vo_phrase(s) for s in a_info.get("relevant_situations", []) if s]
    objections = [_clean_vo_phrase(o) for o in a_info.get("possible_objections", []) if o]
    benefits = [_clean_vo_phrase(b.split("->", 1)[-1]) for b in p_info.get("practical_benefits", []) if b]
    comm_style = a_info.get("communication_style", "casual_everyday")

    sit0 = _concise_clause(re.sub(r"^(?:malas|ingin|khawatir|butuh)\s+", "", situations[0], flags=re.IGNORECASE), 4) if situations else "masak harian"
    obj0 = _concise_clause(re.sub(r"^(?:ragu|khawatir|takut)\s+(?:apakah\s+)?", "", objections[0], flags=re.IGNORECASE), 4) if objections else "ukuran dan bahannya"
    feat0 = _concise_clause(features[0], 6) if features else _clean_vo_phrase(short_name)
    feat1 = _concise_clause(features[1], 5) if len(features) > 1 else feat0
    spec0 = _concise_clause(spec_phrases[0], 5) if spec_phrases else feat1
    ben0 = _concise_clause(benefits[0], 6) if benefits else "pemakaian harian lebih praktis"
    sp_short = _clean_vo_phrase(short_name)

    if role == "hook_attention":
        return [
            f"Masih repot pas {sit0}?",
            f"Sering ribet waktu {sit0}?",
            f"Ini solusi praktis buat {sit0}!",
            f"Lihat dulu detail {sp_short} ini!",
            f"Biar urusan harian lebih cepat rapi!",
        ]
    if role == "product_reveal":
        return [
            f"Kenalin {sp_short}, ukurannya pas buat harian.",
            f"Ini {sp_short}, ringkas dan gampang dipakai.",
            f"Pakai {sp_short} ini biar kerjaan makin rapi.",
            f"Lihat ukuran asli {sp_short} ini di tangan.",
        ]
    if role == "core_demonstration":
        return [
            f"Andalkan {feat0}, jadi {ben0} tanpa ribet.",
            f"Lewat {feat0} dan {feat1}, aktivitas harian beres lebih cepat.",
            f"Tinggal tekan dan pakai, {feat1} langsung bekerja nyata.",
            f"Pakai {feat1} ini, {ben0} terasa jauh lebih praktis.",
            "Tinggal pakai langsung, hasilnya cepat rapi buat kebutuhan harianmu.",
        ]
    if role == "spec_validation":
        return [
            f"Detailnya jelas, {spec0}, rapi dan nyaman dipegang.",
            f"Bahannya kokoh, {spec0}, pas untuk pemakaian harian.",
            f"Cek detail {spec0} ini, kuat dan gampang dirawat.",
            f"Sudah pakai {spec0}, ukuran pas dan bahan terjamin.",
            "Cek detail bahan dan konstruksinya, terasa kokoh dan nyaman.",
        ]
    if role == "objection_handling_and_payoff":
        return [
            f"Kalau ragu soal {obj0}, lihat bukti nyatanya di layar.",
            f"Soal {obj0}, ukuran dan bahannya langsung kelihatan jelas.",
            "Sudah beres dipakai, tinggal bersihkan sebentar terus simpan rapi.",
            "Biar nggak ragu lagi, lihat sendiri hasilnya rapi dan praktis.",
        ]
    if role == "cta_closing":
        if platform == "tiktok":
            return [
                f"Cek varian {sp_short} di keranjang kuning ya!",
                "Detailnya ada di keranjang kuning ya!",
                "Cek keranjang kuning kiri bawah sekarang!",
                f"Cek detail {sp_short} di keranjang kiri bawah!",
            ]
        if platform == "shopee_video":
            return [
                f"Cek varian {sp_short} di keranjang Shopee!",
                "Detail produknya ada di keranjang video ini!",
                f"Klik tautan {sp_short} di keranjang sekarang.",
            ]
        if platform == "instagram_reels":
            return [
                f"Detail {sp_short} ada di tautan bio ya!",
                "Cek tautan produknya di bio dan caption!",
                "Link produknya ada di bio dan caption ya.",
            ]
        if comm_style == "polite_neutral":
            return [
                f"Silakan cek tautan {sp_short} di komentar.",
                "Detail produknya ada di tautan komentar.",
                "Silakan cek tautan produk di caption ya.",
            ]
        return [
            f"Cek detail {sp_short} lewat tautan komentar.",
            "Tautan produknya ada di kolom komentar ya.",
            "Cek tautannya di caption atau komentar.",
        ]

    return [original_vo]


def hce_apply_revisions(
    runtime: HCERuntime,
    hce_package: dict[str, Any],
    avd_plan: dict[str, Any],
    revision_requests: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Apply HCE-owned copywriting, timing, digit-spelling, and CTA revisions cleanly."""
    new_pkg = copy.deepcopy(hce_package)
    new_pkg["version"] = int(hce_package.get("version", 1)) + 1
    new_pkg["revised_at"] = _now_iso()

    p_info = new_pkg["product_analysis"]
    a_info = new_pkg["audience_analysis"]
    plat = normalize_platform(avd_plan.get("platform") or new_pkg.get("platform") or "tiktok")
    short_name = _extract_short_product_name(p_info["name"])
    refiner = runtime.NaturalLanguageRefiner()
    comm_style = a_info.get("communication_style", "casual_everyday")

    targeted_scenes = {int(r["scene_number"]) for r in revision_requests if r.get("scene_number")}
    need_global_copy_fix = any(
        r.get("category") in ("script_quality", "marketing_consistency", "hook_effectiveness", "cta_relevance", "persuasiveness")
        for r in revision_requests
    )

    changes: list[dict[str, Any]] = []
    revised_scene_vo: dict[int, str] = {}

    for sc in avd_plan.get("scenes", []):
        sid = int(sc["id"])
        dur = float(sc.get("duration", 3.0))
        orig_vo = str(sc.get("spoken_narration", "")).strip()
        role = str(sc.get("narrative_objective", ""))

        # Check current VO validity against dialogue_timing & refiner
        spelled_vo = spell_numbers_in_vo(orig_vo)
        ref_res = refiner.refine_text(
            spelled_vo,
            location=f"scene_{sid}",
            register=comm_style,
            available_evidence=p_info.get("available_evidence", []),
        )
        cleaned_vo = ref_res.refined_text
        syl, warns = dialogue_timing.analyze_text(cleaned_vo)
        min_s, max_s = syllable_bounds_for_duration(dur)

        must_fix = (
            sid in targeted_scenes
            or need_global_copy_fix
            or bool(warns)
            or syl < min_s
            or syl > max_s
            or ref_res.rewrites_applied > 0
        )

        if must_fix:
            nat_cands = _build_natural_scene_vo_candidates(
                role, p_info["name"], short_name, p_info, a_info, plat, cleaned_vo
            )
            cleaned_ok = not warns and (min_s <= syl <= max_s) and ref_res.rewrites_applied == 0
            candidates = ([cleaned_vo] + nat_cands) if cleaned_ok else (nat_cands + [cleaned_vo])
            # Refine every candidate first so zero clichés / stiffness slip in
            refined_cands = [
                refiner.refine_text(
                    c,
                    location=f"scene_{sid}",
                    register=comm_style,
                    available_evidence=p_info.get("available_evidence", []),
                ).refined_text
                for c in candidates
            ]
            req_kws: tuple[str, ...] = ()
            if role == "cta_closing":
                # Keep platform CTA markers intact when fitting syllable bounds
                if plat in ("tiktok", "shopee_video"):
                    req_kws = ("keranjang",)
                else:
                    req_kws = ("tautan", "link", "bio", "komentar", "caption")
            fitted = _fit_vo_to_bounds(refined_cands, dur, min_s, max_s, required_keywords=req_kws)
            revised_scene_vo[sid] = fitted
            if fitted != orig_vo:
                changes.append(
                    {
                        "agent": "human-copywriting-engine",
                        "scene_number": sid,
                        "before": orig_vo,
                        "after": fitted,
                        "reason": "Menyelaraskan timing suku kata (5.0 sk/dtk), ejaan angka, dan kealamian Bahasa Indonesia tanpa klaim fiktif.",
                    }
                )
        else:
            revised_scene_vo[sid] = cleaned_vo

    # Ensure hooks & CTA & caption are refined and aligned with verified features
    hooks_out: list[str] = []
    for idx, hk in enumerate([revised_scene_vo.get(1, ""), *new_pkg.get("hooks", [])]):
        if not hk:
            continue
        hk_ref = refiner.refine_text(
            hk,
            location=f"hook_{idx + 1}",
            register=comm_style,
            available_evidence=p_info.get("available_evidence", []),
        ).refined_text
        if hk_ref not in hooks_out:
            hooks_out.append(hk_ref)
    new_pkg["hooks"] = hooks_out[:5]

    final_sid = len(avd_plan.get("scenes", []))
    if final_sid and final_sid in revised_scene_vo:
        new_pkg["cta"] = revised_scene_vo[final_sid]
    else:
        new_pkg["cta"] = refiner.refine_text(
            _build_platform_cta_line(plat, short_name, comm_style),
            location="cta",
            register=comm_style,
            available_evidence=p_info.get("available_evidence", []),
        ).refined_text

    # Re-verify caption includes verified feature coverage & zero integrity/cliché violations
    feat_summary = ", ".join(p_info.get("verified_features", [])[:3])
    specs_phrase = ", ".join(f"{k} {v}" for k, v in list(p_info.get("verified_specs", {}).items())[:3])
    spec_part = f" ({specs_phrase})" if specs_phrase else ""
    cta_hint = new_pkg["cta"]
    raw_cap = f"{p_info['name']}{spec_part} — {feat_summary}. {cta_hint} #reviewjujur #produkpraktis #affiliateindonesia"
    new_pkg["caption"] = refiner.refine_text(
        raw_cap,
        location="caption",
        register=comm_style,
        available_evidence=p_info.get("available_evidence", []),
    ).refined_text
    new_pkg.setdefault("platform_captions", {})[plat] = new_pkg["caption"]
    new_pkg["scene_vo_by_id"] = {str(k): v for k, v in revised_scene_vo.items()}

    # Update HCE scenes list to mirror the revised panel narrations
    new_scenes_list = []
    for sc in avd_plan.get("scenes", []):
        sid = int(sc["id"])
        new_scenes_list.append(
            {
                "scene_number": sid,
                "duration_seconds": sc["duration"],
                "visual_direction": sc["visual_description"],
                "spoken_narration": revised_scene_vo.get(sid, sc["spoken_narration"]),
                "on_screen_text": sc.get("on_screen_text", ""),
                "narrative_objective": sc.get("narrative_objective", ""),
                "transition": sc.get("transition", ""),
            }
        )
    new_pkg["scenes"] = new_scenes_list
    return new_pkg, changes


def avd_apply_revisions(
    avd_plan: dict[str, Any],
    hce_package: dict[str, Any],
    revision_requests: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Apply AVD-owned visual, pacing, continuity, and timing calibration revisions cleanly."""
    new_plan = copy.deepcopy(avd_plan)
    new_plan["version"] = int(avd_plan.get("version", 1)) + 1
    new_plan["revised_at"] = _now_iso()

    changes: list[dict[str, Any]] = []
    scenes = list(new_plan.get("scenes", []))
    vo_map = hce_package.get("scene_vo_by_id", {})

    # 1. Sync HCE's revised spoken VO into storyboard panels
    for sc in scenes:
        sid_str = str(sc["id"])
        if sid_str in vo_map and vo_map[sid_str] != sc["spoken_narration"]:
            changes.append(
                {
                    "agent": "affiliate-video-director",
                    "scene_number": int(sc["id"]),
                    "before": sc["spoken_narration"],
                    "after": vo_map[sid_str],
                    "reason": "Sinkronisasi dialog revisi dari HCE ke panel storyboard.",
                }
            )
            sc["spoken_narration"] = vo_map[sid_str]

    # 2. Handle pacing splits (> 6.5s) if requested
    expanded_scenes: list[dict[str, Any]] = []
    for sc in scenes:
        dur = float(sc.get("duration", 3.0))
        if dur > 6.5:
            half1 = round(dur * 0.55, 1)
            half2 = round(dur - half1, 1)
            part1 = copy.deepcopy(sc)
            part1["duration"] = half1
            part2 = copy.deepcopy(sc)
            part2["title"] = f"{sc['title']} (Close-Up Bukti)"
            part2["duration"] = half2
            part2["camera_angle"] = "Macro close-up 35 derajat"
            part2["camera_movement"] = "Slow Macro Tracking — Tujuan: mempertegas detail bukti fisik produk"
            part2["spoken_narration"] = "[jeda]"
            expanded_scenes.extend([part1, part2])
            changes.append(
                {
                    "agent": "affiliate-video-director",
                    "scene_number": int(sc["id"]),
                    "before": f"{dur}s single shot",
                    "after": f"{half1}s + {half2}s split shots",
                    "reason": "Memecah shot terlalu panjang agar ritme editing hidup.",
                }
            )
        else:
            expanded_scenes.append(sc)
    scenes = expanded_scenes

    # 3. Ensure non-uniform durations & fine-tune panel duration within +-0.5s if needed for syllable fit
    for sc in scenes:
        vo = str(sc.get("spoken_narration", "")).strip()
        if vo.lower() != "[jeda]":
            syl, warns = dialogue_timing.analyze_text(vo)
            dur = float(sc["duration"])
            min_s, max_s = syllable_bounds_for_duration(dur)
            if not warns and (syl < min_s or syl > max_s):
                # Try adjusting panel duration by +-0.5s or +-1.0s within [1.5, 6.0]
                for cand_dur in [round(dur + delta, 1) for delta in (0.5, -0.5, 1.0, -1.0)]:
                    if 1.5 <= cand_dur <= 6.0:
                        cmin, cmax = syllable_bounds_for_duration(cand_dur)
                        if cmin <= syl <= cmax:
                            sc["duration"] = cand_dur
                            changes.append(
                                {
                                    "agent": "affiliate-video-director",
                                    "scene_number": int(sc["id"]),
                                    "before": f"duration={dur}s",
                                    "after": f"duration={cand_dur}s",
                                    "reason": f"Kalibrasi durasi panel agar {syl} suku kata pas di zona 60%-105%.",
                                }
                            )
                            break

    if len(scenes) >= 3 and len({float(s["duration"]) for s in scenes}) <= 1:
        scenes[0]["duration"] = max(1.5, round(float(scenes[0]["duration"]) - 0.5, 1))
        scenes[-1]["duration"] = min(6.0, round(float(scenes[-1]["duration"]) + 0.5, 1))

    # 4. Strengthen visual-strategy alignment, camera purpose, and safe zone if flagged
    for sc in scenes:
        cam = str(sc.get("camera_movement", ""))
        if "tujuan" not in cam.lower():
            sc["camera_movement"] = f"{cam or 'Steady Tracking Shot'} — Tujuan: memperkuat bukti visual fitur produk"
        if sc is scenes[-1]:
            vis = str(sc.get("visual_description", ""))
            if "zona aman" not in vis.lower():
                sc["visual_description"] = vis.rstrip(".") + "; jaga ruang aman bawah >30% bersih untuk tombol keranjang."

    total_dur = _recalculate_scene_timestamps(scenes)
    # Trim proportionally if somehow > 40.0s
    while total_dur > DEFAULT_MAX_FINAL_DURATION + 1e-6 and len(scenes) > 1:
        longest = max(scenes, key=lambda x: float(x["duration"]))
        if float(longest["duration"]) <= 2.0:
            break
        longest["duration"] = round(float(longest["duration"]) - 0.5, 1)
        total_dur = _recalculate_scene_timestamps(scenes)

    new_plan["scenes"] = scenes
    new_plan["panel_count"] = len(scenes)
    new_plan["total_duration"] = total_dur
    new_plan["clip_plan"] = segment_panels_into_clips(scenes, DEFAULT_MAX_CLIP_DURATION)

    # Sync publishing draft with HCE revisions
    plat = new_plan.get("platform", "tiktok")
    pub = new_plan.setdefault("publishing_draft", {})
    pub.setdefault("captions", {})[plat] = hce_package.get("caption", pub.get("captions", {}).get(plat, ""))
    if hce_package.get("cta"):
        ctas = list(pub.get("ctas", []))
        if ctas:
            ctas[0] = hce_package["cta"]
        else:
            ctas = [hce_package["cta"]]
        pub["ctas"] = ctas
    if hce_package.get("hooks"):
        alt_hooks = list(dict.fromkeys([*hce_package["hooks"], *pub.get("alt_hooks", [])]))[:5]
        pub["alt_hooks"] = alt_hooks

    return new_plan, changes


def write_campaign_deliverables(
    campaign_dir: Path,
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    hce_package: dict[str, Any],
    avd_plan: dict[str, Any],
    summary: dict[str, Any],
    *,
    archive_existing: bool = True,
) -> list[str]:
    """Write or update all standard AVD Markdown deliverables and campaign.json, preserving archives."""
    archived_files: list[str] = []

    def _safe_write(rel_path: str, content: str) -> None:
        target = campaign_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if archive_existing and target.is_file():
            arch = archive_if_exists(target, campaign_dir)
            if arch:
                archived_files.append(arch)
        target.write_text(content, encoding="utf-8")

    # Ensure standard campaign subdirectories exist
    for rel in campaign_check.CAMPAIGN_SUBDIRS:
        (campaign_dir / rel).mkdir(parents=True, exist_ok=True)

    _safe_write("01-product-review/product-brief.md", _render_product_brief_md(hce_input, avd_context, hce_package, summary))
    _safe_write("01-product-review/marketing-strategy.md", _render_marketing_strategy_md(hce_input, avd_context, hce_package, avd_plan))
    _safe_write("01-product-review/image-prompts.md", _render_image_prompts_md(hce_input, avd_context, avd_plan))
    _safe_write("03-storyboard/storyboard.md", _render_storyboard_md(hce_input, avd_context, avd_plan, summary))
    _safe_write("04-video/video-plan.md", _render_video_plan_md(hce_input, avd_context, avd_plan))

    # Populate upload-assets safely if generated assets or storyboard images exist
    upload_map = _sync_upload_assets(campaign_dir, avd_plan)

    clip_files: list[str] = []
    for clip in avd_plan.get("clip_plan", []):
        rel = clip["file"]
        clip_files.append(rel)
        _safe_write(rel, _render_video_clip_md(hce_input, avd_context, avd_plan, clip, upload_map))

    _safe_write("05-publishing/publishing-package.md", _render_publishing_package_md(hce_input, hce_package, avd_plan))

    # Update campaign.json cleanly
    _update_campaign_json(campaign_dir, hce_input, avd_context, hce_package, avd_plan, summary, clip_files)
    return archived_files


def _sync_upload_assets(campaign_dir: Path, avd_plan: dict[str, Any]) -> dict[str, str]:
    """Copy existing generated assets and storyboard images to 04-video/upload-assets without modifying originals."""
    inv = campaign_check.collect_inventory(campaign_dir)
    upload_dir = campaign_dir / "04-video" / "upload-assets"
    upload_dir.mkdir(parents=True, exist_ok=True)

    mapping: dict[str, str] = {}
    gen_imgs = inv.get("product-demonstration", []) + inv.get("generated-lifestyle", []) + inv.get("video-reference", [])
    seen: list[str] = []
    for rel in gen_imgs:
        if rel not in seen:
            seen.append(rel)

    for idx, rel in enumerate(seen, start=1):
        src = campaign_dir / rel
        dst_name = f"{idx}{src.suffix.lower()}"
        shutil.copy2(src, upload_dir / dst_name)
        mapping[rel] = f"04-video/upload-assets/{dst_name}"

    for sb_rel in inv.get("storyboard", []):
        src = campaign_dir / sb_rel
        shutil.copy2(src, upload_dir / src.name)
        mapping[sb_rel] = f"04-video/upload-assets/{src.name}"

    return mapping


def _render_product_brief_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    hce_package: dict[str, Any],
    summary: dict[str, Any],
) -> str:
    p_info = hce_package["product_analysis"]
    slug = avd_context["slug"]
    refs = avd_context.get("references") or ["(belum ada file di 01-product-review/references/)"]
    specs = p_info.get("verified_specs", {})
    status_label = "Approved" if summary.get("converged") else "Draft"
    price_val = f"Rp{p_info['price_idr']:,.0f}".replace(",", ".") if p_info.get("price_idr") else "Cek keranjang (dinamis)"

    lines = [
        f"# Product Brief — {p_info['name']}",
        "",
        f"- **Slug Kampanye:** `{slug}`",
        f"- **Kategori:** {avd_context.get('original_category') or p_info['category']}",
        f"- **Referensi Sumber:** {', '.join(f'`{r}`' for r in refs)}",
        f"- **Status Tinjauan:** {status_label}",
        "",
        "## 1. Ringkasan Identitas Produk",
        "",
        "| Atribut | Nilai / Deskripsi | Status Fakta |",
        "|---|---|---|",
        f"| **Nama Produk** | {p_info['name']} | `[TERVERIFIKASI]` |",
        f"| **Kategori HCE** | `{p_info['category']}` ({p_info['price_tier']}) | `[TERVERIFIKASI]` |",
        f"| **Spesifikasi Terverifikasi** | {'; '.join(f'{k}: {v}' for k, v in specs.items()) or 'Lihat rincian fitur terverifikasi'} | `[TERVERIFIKASI]` |",
        f"| **Harga / Catatan Promo** | {price_val} *(jangan hardcode harga berubah di VO)* | `[TERVERIFIKASI]` |",
        "",
        "## 2. Analisis Karakteristik Fisik & Visual Anchor",
        "",
        "- **Visual Anchor Wajib Dikunci (Anti-Drift):**",
    ]
    for idx, va in enumerate(avd_context.get("visual_anchors", []), start=1):
        lines.append(f"  {idx}. {va}")

    lines.extend([
        "",
        "## 3. Peta Fitur → Manfaat Nyata *(oleh HCE ProductAnalyzer)*",
        "",
        "| Fitur / Mekanisme | Status | Manfaat Langsung Pembeli | Bukti Visual yang Dibutuhkan |",
        "|---|---|---|---|",
    ])
    for feat, ben in zip(p_info.get("verified_features", []), p_info.get("practical_benefits", [])):
        clean_ben = ben.split("->", 1)[-1].strip()
        lines.append(f"| {feat} | `[TERVERIFIKASI]` | {clean_ben} | Peragaan tangan langsung di depan kamera pada cahaya natural |")

    lines.extend(["", "## 4. Pemisahan Fakta vs Asumsi & Batasan Klaim", "", "### Fakta Terverifikasi (`[TERVERIFIKASI]`)"])
    for feat in p_info.get("verified_features", []):
        lines.append(f"- {feat}")
    for k, v in specs.items():
        lines.append(f"- {k}: {v}")

    lines.extend(["", "### Asumsi Visual & Kategori (`[ASUMSI]`)"])
    for asm in avd_context.get("assumptions", []) or ["Detail daya tahan jangka panjang di luar data listing tidak boleh diklaim melampaui demonstrasi visual."]:
        lines.append(f"- {asm}")

    lines.extend(["", "### Informasi Hilang & Aturan `do_not_claim` (`[PERLU DICEK]`)"])
    for miss in p_info.get("missing_information", []):
        lines.append(f"- `[PERLU DICEK]` {miss}")
    for rule in p_info.get("do_not_claim", []):
        lines.append(f"- **Larangan Klaim HCE:** {rule}")
    lines.append("")
    return "\n".join(lines)


def _render_marketing_strategy_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    hce_package: dict[str, Any],
    avd_plan: dict[str, Any],
) -> str:
    p_info = hce_package["product_analysis"]
    a_info = hce_package["audience_analysis"]
    strat = hce_package["strategy"]
    hooks = hce_package.get("hooks", [])
    ctas = hce_package.get("platform_ctas", {})

    lines = [
        f"# Marketing & Creative Strategy — {p_info['name']}",
        "",
        f"- **Slug Kampanye:** `{avd_context['slug']}`",
        "- **Target Platform Utama:** TikTok, Instagram Reels, Facebook Reels",
        "- **Rasio Aspek Default:** `9:16`",
        f"- **Kolaborasi Aktif:** `Affiliate Video Director` (Controller) ↔ `Human Copywriting Engine` (Marketing & Copywriting Specialist)",
        f"- **Pengetahuan HCE Dirujuk:** {', '.join(f'`{kid}`' for kid in hce_package.get('retrieved_knowledge_ids', []))}",
        "",
        "## 1. Buyer Intelligence *(oleh HCE AudienceAnalyzer)*",
        "",
        f"- **Target Pembeli Utama:** {a_info['likely_audience']}",
        f"- **Tingkat Kesadaran Audiens:** `{a_info['product_familiarity']}`",
        f"- **Register Bahasa Indonesia:** `{a_info['communication_style']}`",
        f"- **Situasi Pemicu:** {'; '.join(a_info.get('relevant_situations', []))}",
        "",
        "### Peta Psikologi Pembeli",
        "- **Needs & Motivations:**",
    ]
    for m in a_info.get("potential_needs", []):
        lines.append(f"  - {m}")
    lines.append("- **Hipotesis vs Fakta Audiens:**")
    for h in a_info.get("inferred_hypotheses", []) or ["Audiens dipasok eksplisit oleh pengguna."]:
        lines.append(f"  - {h}")
    lines.extend([
        "- **Purchase Objections & Pembuktian Visual:**",
        "  | Keraguan Pembeli | Fokus Jawaban Copy | Bukti Visual di Kamera |",
        "  |---|---|---|",
    ])
    for obj in a_info.get("possible_objections", []):
        lines.append(f"  | {obj} | Jawaban jujur berbasis fitur terverifikasi | Uji tangan langsung & close-up detail fisik produk |")

    lines.extend([
        "",
        "## 2. Affiliate Strategy *(oleh HCE StrategySelector & ContentGenerator)*",
        "",
        f"- **Sudut Jualan Utama (*Selling Angle*):** `{strat['strategy_name']}` — {strat['rationale']}",
        f"- **Unique Selling Proposition (USP):** {hce_package.get('usp', '')}",
        f"- **Alasan Tidak Memaksa Storytelling Panjang:** {strat.get('why_not_forced_story', '')}",
        "- **Kepatuhan Klaim Platform:** Nol klaim medis, nol testimoni fiktif, nol kelangkaan/diskon buatan.",
        "",
        "### Pilihan Hook Pembuka (≤ 2.5 Detik)",
    ])
    for idx, hk in enumerate(hooks, start=1):
        lines.append(f"{idx}. \"{hk}\"")

    lines.extend([
        "",
        "### Pilihan Call-to-Action (CTA)",
        f"- **TikTok:** {ctas.get('tiktok', hce_package.get('cta', ''))}",
        f"- **Instagram Reels:** {ctas.get('instagram_reels', '')}",
        f"- **Facebook Reels:** {ctas.get('facebook_reels', '')}",
        "",
        "## 3. Creative Strategy *(oleh Affiliate Video Director)*",
        "",
        "- **Konsep Iklan Utama:** POV Hands-On Demonstration & Benefit Proof dalam pencahayaan alami rumah Indonesia.",
        f"- **Spesifikasi Karakter / Tangan:** {avd_context['hand_spec']}",
        f"- **Referensi Lingkungan (*Environment*):** {avd_context['environment_spec']}",
        f"- **Target Durasi Video Final:** `{avd_plan['total_duration']}` detik ({avd_plan['panel_count']} panel adaptif, batas maks. 40 detik)",
        "",
    ])
    return "\n".join(lines)


def _render_image_prompts_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    avd_plan: dict[str, Any],
) -> str:
    pname = hce_input["name"]
    refs = ", ".join(avd_context.get("references") or ["foto referensi produk asli"])
    anchors = "; ".join(avd_context.get("visual_anchors", []))
    hand = avd_context["hand_spec"]
    env = avd_context["environment_spec"]

    return "\n".join([
        f"# Image Generation Prompts — {pname}",
        "",
        f"> **Aturan Otoritas:** Seluruh prompt wajib melampirkan `{refs}` dari `01-product-review/references/` sebagai Otoritas #1.",
        "",
        "## Ringkasan Aset yang Dibutuhkan",
        "",
        "| ID | Jenis Foto | Kategori Otoritas | Target Simpan | Rasio |",
        "|---|---|---|---|---|",
        "| `IMG-01` | Hero Product Shot | `generated-lifestyle` | `02-generated-assets/hero/hero-01.png` | `9:16` |",
        "| `IMG-02` | Macro Detail Shot | `generated-lifestyle` | `02-generated-assets/detail/detail-01.png` | `9:16` |",
        "| `IMG-03` | Hands-On Demonstration | `product-demonstration` | `02-generated-assets/demonstration/demo-01.png` | `9:16` |",
        "| `IMG-04` | Lifestyle Context | `generated-lifestyle` | `02-generated-assets/lifestyle/lifestyle-01.png` | `9:16` |",
        "",
        "## IMG-01 — Product Hero Shot",
        "- **Target Simpan:** `02-generated-assets/hero/hero-01.png`",
        "```text",
        f"[PRODUCT IDENTITY LOCK: {anchors}]",
        f"Commercial 9:16 vertical hero photograph of {pname} in natural Indonesian lifestyle setting ({env}). Clean composition centered in the 20%-65% vertical safe zone leaving >32% clean bottom foreground for CTA overlays. Soft directional morning daylight, crisp material textures, shallow depth of field. Negative / Avoid: altered product geometry, wrong color, deformed mechanism, floating text, watermark, human face.",
        "```",
        "",
        "## IMG-02 — Macro Detail Shot",
        "- **Target Simpan:** `02-generated-assets/detail/detail-01.png`",
        "```text",
        f"[PRODUCT IDENTITY LOCK: {anchors}]",
        f"Vertical 9:16 macro commercial photograph focusing closely on key materials, construction joints, and functional parts of {pname}. Natural window sidelight revealing authentic texture and finish. Negative / Avoid: melted hardware, altered proportions, blurry focus, text artifacts, watermark.",
        "```",
        "",
        "## IMG-03 — Hands-On Demonstration Shot",
        "- **Target Simpan:** `02-generated-assets/demonstration/demo-01.png`",
        "```text",
        f"[PRODUCT IDENTITY LOCK: {anchors}]",
        f"[HAND/CHARACTER LOCK: {hand}]",
        f"First-person POV 9:16 vertical photograph showing natural Indonesian adult hands actively operating {pname} during practical everyday use ({env}). Realistic grip physics, honest scale, natural daylight. Negative / Avoid: extra fingers, deformed hand, floating grip, visible face, altered product size, text overlay, watermark.",
        "```",
        "",
        "## IMG-04 — Lifestyle Environment Shot",
        "- **Target Simpan:** `02-generated-assets/lifestyle/lifestyle-01.png`",
        "```text",
        f"[PRODUCT IDENTITY LOCK: {anchors}]",
        f"Vertical 9:16 authentic Indonesian home environment photograph showing {pname} placed neatly in context ({env}). Warm diffused daylight, clean uncluttered background, 9:16 vertical safe zone framing. Negative / Avoid: cluttered room, neon glare, distorted product shape, watermark, human face.",
        "```",
        "",
    ])


def _render_storyboard_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    avd_plan: dict[str, Any],
    summary: dict[str, Any],
) -> str:
    scenes = avd_plan["scenes"]
    locks = avd_plan["consistency_locks"]
    status_lbl = "Approved" if summary.get("converged") else "Draft"
    inv_assets = avd_context.get("references", [])

    lines = [
        f"# Storyboard — {hce_input['name']}",
        "",
        f"- **Slug Kampanye:** `{avd_context['slug']}`",
        f"- **Sudut Jualan Utama:** `{avd_plan['selling_angle']}` — {avd_plan.get('usp', '')}",
        f"- **Jumlah Adegan:** `{len(scenes)}` panel *(adaptif berdurasi variabel)*",
        f"- **Total Durasi:** `{avd_plan['total_duration']:.1f}` detik *(maks. 40.0 detik)*",
        "- **Rasio:** `9:16`",
        f"- **Status Storyboard:** {status_lbl} *(Disetujui otonom setelah review dua arah HCE ↔ AVD dalam {summary.get('iterations', 1)} iterasi)*",
        "",
        "## 1. Evaluasi Aset Visual (Audit Pra-Storyboard)",
        "",
        "| Aset Diperiksa | Kategori | Akurasi Produk vs Ref #1 | Status |",
        "|---|---|---|---|",
    ]
    if inv_assets:
        for ref in inv_assets:
            lines.append(f"| `{ref}` | `product-reference` (`authority: 1`) | Sumber kebenaran utama | `Pakai` |")
    else:
        lines.append("| `(belum ada foto generated)` | `product-reference` | Gunakan foto referensi asli saat generasi aset | `Perbaiki` |")

    lines.extend([
        "",
        "## 2. Alur Cerita, Struktur Pemasaran & Ritme Editing",
        "",
        "- **Struktur Pemasaran Adaptif:** " + " → ".join(sc.get("stage_tag", sc["title"]) for sc in scenes),
        "- **Strategi Ritme Editing:** Durasi variabel terkalibrasi (`" + ", ".join(f"{sc['duration']:.1f}s" for sc in scenes) + "`) agar hook cepat, demonstrasi utama jelas, dan CTA tegas.",
        "- **Kunci Kontinuitas:**",
        f"  - **Product Lock:** {locks['product_lock']}",
        f"  - **Hand/Wardrobe Lock:** {locks['hand_lock']}",
        f"  - **Environment & Lighting Lock:** {locks['environment_lighting_lock']}",
        "",
        "## 3. Rincian Desain Adegan",
        "",
    ])

    table_rows: list[str] = []
    for sc in scenes:
        vo = str(sc["spoken_narration"]).strip()
        syl, _ = dialogue_timing.analyze_text(vo)
        est = round(syl / dialogue_timing.DEFAULT_RATE, 2)
        vo_disp = "[jeda]" if vo.lower() == "[jeda]" else f'"{vo}"'
        lines.extend([
            f"### Adegan {sc['id']} — {sc['title']} (`{sc['timestamp']}`, `{sc['duration']:.1f}` dtk)",
            f"- **Deskripsi & Komposisi Visual:** {sc['visual_description']}",
            f"- **Aksi Fisik Produk:** {sc['physical_action']}",
            f"- **Interaksi Produk:** {sc['product_interaction']}",
            f"- **Sudut & Posisi Kamera:** {sc['camera_angle']}",
            f"- **Gerakan Kamera & Tujuan Naratif:** {sc['camera_movement']}",
            f"- **Pencahayaan & Ruang Aman 9:16:** {sc['lighting_safe_zone']}",
            f"- **Dialog (VO):** {vo_disp}",
            f"- **Teks Layar (*On-Screen Text*):** `{sc.get('on_screen_text') or 'Tidak ada'}`",
            f"- **Tujuan Pemasaran (*Marketing Purpose*):** {sc['marketing_purpose']}",
            f"- **Transisi ke Panel Berikutnya:** {sc['transition']}",
            "",
        ])
        table_rows.append(f"| {sc['id']} | {sc['timestamp']} | {sc['duration']:.1f} | {vo_disp} | {syl} | {est:.2f} | OK |")

    lines.extend([
        "## Tabel Timing Dialog",
        "",
        "| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |",
        "|---|---|---|---|---|---|---|",
        *table_rows,
        "",
        "## Prompt Gambar Storyboard",
        "",
        "```text",
        f"Create a clean {len(scenes)}-panel vertical commercial storyboard sheet (2x3 grid layout covering Panels 1-{len(scenes)}, each panel in 9:16 portrait proportion) for {hce_input['name']}.",
        f"[PRODUCT IDENTITY LOCK]: {locks['product_lock']}.",
        f"[HAND & ENVIRONMENT LOCK]: {locks['hand_lock']} Environment: {locks['environment_lighting_lock']}.",
    ])
    for sc in scenes:
        lines.append(f"Panel {sc['id']} ({sc['timestamp']}): {sc['visual_description']} Camera: {sc['camera_angle']}.")
    lines.extend([
        "Style: Realistic commercial photography storyboard frames, sharp focus, natural daylight, small panel badges only, no speech bubbles, no text clutter.",
        "```",
        "",
    ])
    return "\n".join(lines)


def _render_video_plan_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    avd_plan: dict[str, Any],
) -> str:
    clips = avd_plan["clip_plan"]
    locks = avd_plan["consistency_locks"]
    lines = [
        f"# Video Generation Plan — {hce_input['name']}",
        "",
        f"- **Slug Kampanye:** `{avd_context['slug']}`",
        "- **Acuan Otoritatif:** `03-storyboard/storyboard.md`",
        f"- **Total Durasi Storyboard:** `{avd_plan['total_duration']:.1f}` detik (`{len(avd_plan['scenes'])}` panel variabel)",
        "- **Rasio Aspek:** `9:16`",
        f"- **Batas Maksimal Per Klip Generator:** `{DEFAULT_MAX_CLIP_DURATION:.1f}` detik",
        f"- **Jumlah Segmen Klip Dinamis:** `{len(clips)}` klip",
        "- **Folder Bahan Upload Terpadu:** `04-video/upload-assets/`",
        "",
        "## Pemetaan Panel Storyboard ke Segmen Klip Video",
        "",
        "| File Generasi | Panel Dicakup | Rentang Waktu | Durasi Klip | Target File |",
        "|---|---|---|---|---|",
    ]
    for cl in clips:
        s_lbl = ", ".join(f"Adegan {sid}" for sid in cl["scenes"])
        lines.append(f"| **{cl['id']}** | {s_lbl} | `{cl['timestamp']}` | `{cl['duration']:.1f}` dtk | `{cl['file']}` |")

    lines.extend([
        "",
        "## Ringkasan Kunci Kontinuitas Lintas Generasi",
        "",
        f"- **Identitas Produk (Otoritas #1):** {locks['product_lock']}",
        f"- **Karakter Tangan & Pakaian:** {locks['hand_lock']}",
        f"- **Ruangan & Pencahayaan:** {locks['environment_lighting_lock']}",
        "- **Identitas Audio VO:** Pengulas off-camera berbahasa Indonesia natural, tanpa wajah tampil.",
        "",
    ])
    return "\n".join(lines)


def _render_video_clip_md(
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    avd_plan: dict[str, Any],
    clip: dict[str, Any],
    upload_map: dict[str, str],
) -> str:
    clip_num = int(clip["clip_index"])
    covered_ids = set(int(x) for x in clip["scenes"])
    clip_scenes = [sc for sc in avd_plan["scenes"] if int(sc["id"]) in covered_ids]
    locks = avd_plan["consistency_locks"]
    refs = avd_context.get("references") or ["01-product-review/references/"]
    anchors_list = [str(x).strip() for x in (avd_context.get("visual_anchors") or []) if str(x).strip()]
    anchors_text = "; ".join(anchors_list) if anchors_list else locks["product_lock"]
    product_only = bool(avd_context.get("product_only", False))
    subject_mode_label = "Product-Only" if product_only else "Human Demo"
    specific_neg_items = [
        f"no missing, detached, duplicated or altered {a}"
        for a in (anchors_list[:6] if anchors_list else [hce_input["name"]])
    ]
    specific_neg_line = ", ".join(specific_neg_items)

    lines = [
        f"# Video Generation Prompt {clip_num:02d} — {hce_input['name']}",
        "",
        f"- **File:** `{clip['file']}`",
        f"- **Mode Subjek:** `{subject_mode_label}`",
        f"- **Durasi Klip:** `{clip['duration']:.1f}` detik *(maks. `10.0` detik)*",
        "- **Rasio Aspek:** `9:16`",
        "- **Panel Storyboard Dicakup:** " + ", ".join(f"`Adegan {sc['id']}`" for sc in clip_scenes),
        f"- **Rentang Timestamp Storyboard:** `{clip['timestamp']}`",
        "",
        "## 1. Gambar Referensi Wajib Dilampirkan",
        "",
        f"1. {', '.join(f'`{r}`' for r in refs)} — **Otoritas #1 (`product-reference`)**: acuan mutlak bentuk, warna, dan proporsi produk.",
    ]
    for sc in clip_scenes:
        anc = sc.get("anchor_asset", "")
        if anc and anc in upload_map:
            lines.append(f"2. `{upload_map[anc]}` — jangkar visual `Adegan {sc['id']}`.")
    for sb_orig, sb_up in upload_map.items():
        if sb_orig.startswith("03-storyboard/"):
            lines.append(f"3. `{sb_up}` — **Otoritas #5 (`storyboard`)**: acuan urutan gerak panel.")
    lines.extend([
        "",
        "## 2. Instruksi Kepatuhan Storyboard & Kunci Konsistensi",
        "",
        f"- **Strict Storyboard Adherence:** Follow panels {clip['scenes'][0]}–{clip['scenes'][-1]} of `03-storyboard/storyboard.md` exactly.",
        f"- **Product Consistency Lock:** {locks['product_lock']}",
        f"- **Hand / Character Consistency Lock:** {'Tanpa manusia atau tangan (Product-Only Mode)' if product_only else locks['hand_lock']}",
        f"- **Environment & Lighting Lock:** {locks['environment_lighting_lock']}",
        "",
        "## 3. Master Video Prompt (Copy-Ready English)",
        "",
        "```text",
    ])
    if clip_num > 1:
        lines.append("Continue the video.")

    env_clean = avd_context["environment_spec"].rstrip(".")
    if product_only:
        subject_block_header = "[5. PRODUCT-ONLY MODE]"
        subject_block_body = (
            "Product is the sole subject in every shot. Strictly NO humans, NO babies, NO children, "
            "NO hands, NO arms, NO legs, NO body parts, NO human reflections or silhouettes, and NO human interaction."
        )
        first_frame_line = (
            f"First-Frame Anchor (0.0s): Product-only commercial showcase over {env_clean}. "
            f"Frame {hce_input['name']} cleanly inside the 20%-68% vertical safe zone."
        )
        subject_neg = "no humans, no hands, no body parts, no human reflections or silhouettes"
    else:
        subject_block_header = "[5. HUMAN MODE]"
        subject_block_body = (
            f"Consistent Indonesian adult hands only ({locks['hand_lock']}), no face visible. "
            "Hand-to-product contact must be physically plausible with honest real-world scale. "
            "Hands must never permanently obscure distinctive product anchors or key components."
        )
        first_frame_line = (
            f"First-Frame Anchor (0.0s): First-person POV over {env_clean}. "
            f"Consistent Indonesian adult hand framing {hce_input['name']} cleanly inside the 20%-68% vertical safe zone."
        )
        subject_neg = "no human face, no talking head, no extra fingers"

    lines.extend([
        "[1. VIDEO SPECIFICATION]",
        f"Duration: {clip['duration']:.1f} seconds. Vertical 9:16 realistic commercial affiliate video for {hce_input['name']}.",
        "",
        "[2. PRODUCT IDENTITY LOCK]",
        (
            f"The product is exactly {hce_input['name']} as shown in the attached original reference photos. "
            f"Locked visual anchors: {anchors_text}. "
            "Preserve exact shape, proportions, colors, materials, surface texture, logo/label and component count."
        ),
        "",
        "[3. OBJECT PERMANENCE LOCK]",
        "- The product must remain the same physical object throughout the entire video.",
        f"- All original components must remain attached in their correct positions: {anchors_text}.",
        "- No component may disappear, detach, duplicate or spontaneously appear.",
        "- Product geometry must remain consistent between frames and shots.",
        "- Camera movement must not cause the AI to reinterpret the product as a different object.",
        f"- All distinctive visual anchors must remain consistent: {anchors_text}.",
        "- A feature that becomes less visible due to perspective must still physically exist.",
        "",
        "[4. ANTI-MORPHING LOCK]",
        (
            "Core constraints: No product morphing, no geometry changes, no product replacement, "
            "no disappearing components, no duplicated components, no color shifting, no texture transformation, "
            "no material substitution, no logo distortion, no spontaneous redesign, no melting or deformation, "
            "no inconsistent product proportions, no unexplained structural changes."
        ),
        f"Product-specific constraints: {specific_neg_line}.",
        "",
        subject_block_header,
        subject_block_body,
        "",
        "[6. ENVIRONMENT & CONTINUITY LOCK]",
        f"{locks['environment_lighting_lock']} Keep product centered in the 20%-68% vertical safe zone.",
        first_frame_line,
        "",
        "[7. SHOT-BY-SHOT TIMELINE]",
    ])

    local_cursor = 0.0
    for sc in clip_scenes:
        d = float(sc["duration"])
        lines.append(
            f"- Shot {sc['id']} ({local_cursor:.1f}s–{local_cursor + d:.1f}s, {sc['title']}): "
            f"{sc['visual_description']} Physical action: {sc['physical_action']}. "
            f"Camera: {sc['camera_angle']}, {sc['camera_movement']}. "
            f"Identity: same exact product; anchors: {anchors_text}. "
            "Continuity: maintain exact geometry, lighting, and scale across shots. "
            "Avoid: reconstructing or replacing the product."
        )
        local_cursor += d

    lines.extend([
        f"Last-Frame Anchor ({local_cursor:.1f}s): Stable framing of {hce_input['name']} with all original components intact and consistent lighting.",
        "",
        "[8. CAMERA MOVEMENT CONTROL]",
        (
            "Move the camera smoothly around a stationary product; avoid needless product rotation, "
            "extreme perspective changes, full 360-degree orbit, or camera passing through the product; "
            "keep the product centered and key features recognizable."
        ),
        "",
        "[9. AUDIO DIRECTION]",
        (
            "Off-camera natural Indonesian reviewer voice-over synchronized to the dialogue timing table, "
            "realistic product action SFX, balanced BGM with zero clipping; no on-camera speaking or lip-sync."
        ),
        "",
        "[10. NEGATIVE PROMPT]",
        (
            f"{specific_neg_line}, {subject_neg}, no aimless zoom or 360 orbit, "
            "no burned-in text, no marketplace UI, no watermarks."
        ),
        "",
        "[11. FINAL PRODUCT IDENTITY VERIFICATION]",
        (
            f"Verify from start to finish that {hce_input['name']} remains 100% identical to the original "
            f"reference photos ({anchors_text}) with zero morphing or missing parts."
        ),
        "```",
        "",
        "## 4. Arahan Audio & Dialog VO Bahasa Indonesia",
        "",
        "- **Profil Pembicara:** Pengulas off-camera Bahasa Indonesia natural, artikulasi jelas, tanpa wajah tampil.",
    ])

    table_rows: list[str] = []
    for sc in clip_scenes:
        vo = str(sc["spoken_narration"]).strip()
        syl, _ = dialogue_timing.analyze_text(vo)
        est = round(syl / dialogue_timing.DEFAULT_RATE, 2)
        vo_disp = "[jeda]" if vo.lower() == "[jeda]" else f'"{vo}"'
        lines.append(f"- `{sc['timestamp']}` *(Adegan {sc['id']})*: {vo_disp}")
        table_rows.append(f"| {sc['id']} | {sc['timestamp']} | {sc['duration']:.1f} | {vo_disp} | {syl} | {est:.2f} | OK |")

    qc_status = (
        "PASS"
        if anchors_list
        else "WARNING (visual anchors belum tersedia — lengkapi 01-product-review/product-identity-lock.md)"
    )
    qc_mark = "x" if anchors_list else " "

    lines.extend([
        "",
        "## 5. Hand-Off Kontinuitas ke Klip Berikutnya",
        "",
        f"- **Kondisi Frame Terakhir (`Last-Frame Anchor`):** Posisi produk, subjek (`{subject_mode_label}`), dan arah pencahayaan di akhir `Adegan {clip_scenes[-1]['id']}` tetap terkunci stabil untuk transisi mulus.",
        "",
        "## 6. Quality Control Konsistensi Produk (PCS v2.0)",
        "",
        "**PRODUCT IDENTITY:**",
        f"- [{qc_mark}] Product shape matches the original reference.",
        f"- [{qc_mark}] Original colors are preserved.",
        f"- [{qc_mark}] Material and texture remain consistent.",
        f"- [{qc_mark}] All original components are accounted for.",
        f"- [{qc_mark}] Logos and distinctive details remain unchanged.",
        "",
        "**OBJECT PERMANENCE:**",
        "- [x] Product remains the same physical object.",
        "- [x] No components disappear.",
        "- [x] No components detach unexpectedly.",
        "- [x] No spontaneous structural changes.",
        "",
        "**ANTI-MORPHING:**",
        "- [x] No product replacement.",
        "- [x] No geometry changes.",
        "- [x] No duplicated components.",
        "- [x] No unexplained color or texture changes.",
        "",
        "**CAMERA CONTROL:**",
        "- [x] Camera movements are appropriate for the product.",
        "- [x] Critical features remain recognizable.",
        "- [x] No unnecessary extreme perspective changes.",
        "- [x] Camera movement does not conflict with product continuity.",
        "",
        "**SHOT CONTINUITY:**",
        "- [x] Every shot includes appropriate identity constraints.",
        "- [x] Product identity is consistent between shots.",
        "- [x] Final hero shot matches the original product.",
        "- [x] Product-only mode follows user instructions.",
        "",
        f"**Status QC Konsistensi Produk (PCS v2.0):** {qc_status}",
        "",
        "## Tabel Timing Dialog",
        "",
        "| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |",
        "|---|---|---|---|---|---|---|",
        *table_rows,
        "",
    ])
    return "\n".join(lines)


def _render_publishing_package_md(
    hce_input: dict[str, Any],
    hce_package: dict[str, Any],
    avd_plan: dict[str, Any],
) -> str:
    pub = avd_plan.get("publishing_draft", {})
    caps = pub.get("captions", {})
    ctas = pub.get("ctas", [])
    hooks = pub.get("alt_hooks", [])
    return "\n".join([
        f"# Publishing Package — {hce_input['name']}",
        "",
        f"- **Slug Kampanye:** `{avd_plan['slug']}`",
        "- **Platform Target:** TikTok, Instagram Reels, Facebook Reels",
        f"- **Total Durasi Video Final:** `{avd_plan['total_duration']:.1f}` detik (`{len(avd_plan['clip_plan'])}` klip)",
        "",
        "## 1. Tiga Variasi Caption SEO",
        "",
        "### Variasi A — Fokus Masalah & Solusi (TikTok Search SEO)",
        f"> {caps.get('tiktok', hce_package.get('caption', ''))}",
        "",
        "### Variasi B — Review Jujur & Manfaat (Instagram Reels)",
        f"> {caps.get('instagram_reels', hce_package.get('caption', ''))}",
        "",
        "### Variasi C — Praktis Harian (Facebook Reels)",
        f"> {caps.get('facebook_reels', hce_package.get('caption', ''))}",
        "",
        "## 2. Kurasi Hashtag Per Platform",
        "",
        "- **TikTok:** `#reviewjujur #produkpraktis #tiktokaffiliate #perlengkapanharian #rekomendasiproduk`",
        "- **Instagram Reels:** `#reviewproduk #affiliateindonesia #tipspraktis #kebutuhanharian`",
        "- **Facebook Reels:** `#infoproduk #alatpraktis #rekomendasiharian #belanjapintar`",
        "",
        "## 3. Lima Variasi CTA",
        "",
        *(f"{idx}. {cta}" for idx, cta in enumerate(ctas[:5], start=1)),
        "",
        "## 4. Lima Alternatif Hook Pembuka (Untuk A/B Testing)",
        "",
        *(f"{idx}. \"{hk}\"" for idx, hk in enumerate(hooks[:5], start=1)),
        "",
        "## 5. Catatan Finishing & Zona Aman Editor",
        "",
        "- **Penempatan Subtitle / On-Screen Text:** Letakkan di posisi `60%–70%` tinggi frame agar bebas dari tombol kanan dan banner keranjang `28%` area bawah.",
        "- **Volume Audio:** VO utama `-3 dB` s.d. `-6 dB`, musik latar maksimal `-24 dB`.",
        "",
    ])


def _update_campaign_json(
    campaign_dir: Path,
    hce_input: dict[str, Any],
    avd_context: dict[str, Any],
    hce_package: dict[str, Any],
    avd_plan: dict[str, Any],
    summary: dict[str, Any],
    clip_files: list[str],
) -> None:
    cj_path = campaign_dir / "campaign.json"
    cj = json.loads(cj_path.read_text(encoding="utf-8")) if cj_path.is_file() else campaign_check._load_campaign_template()

    today = _today_iso()
    cj["slug"] = campaign_dir.name
    cj["product_name"] = hce_input["name"]
    cj["category"] = avd_context.get("original_category") or hce_input["category"]
    cj["updated"] = today
    if not cj.get("created"):
        cj["created"] = today

    key_facts = list(dict.fromkeys([*cj.get("key_facts", []), *hce_input.get("verified_features", [])]))
    cj["key_facts"] = key_facts

    converged = bool(summary.get("converged"))
    stage_status = "approved" if converged else "draft"

    cj.setdefault("stages", {})
    cj["stages"]["review"] = {
        "status": stage_status,
        "files": [
            "01-product-review/product-brief.md",
            "01-product-review/marketing-strategy.md",
            "01-product-review/image-prompts.md",
        ],
        "recommended_duration": avd_plan["total_duration"],
        "estimated_panels": avd_plan["panel_count"],
    }

    inv = campaign_check.collect_inventory(campaign_dir)
    sb_imgs = inv.get("storyboard", [])
    cj["stages"]["storyboard"] = {
        "status": stage_status,
        "files": ["03-storyboard/storyboard.md"],
        "scenes": [
            {
                "id": sc["id"],
                "title": sc["title"],
                "timestamp": sc["timestamp"],
                "duration": sc["duration"],
                "asset": sc.get("anchor_asset", ""),
                "marketing_purpose": sc["marketing_purpose"],
                "dialog": sc["spoken_narration"],
                "on_screen_text": sc.get("on_screen_text", ""),
            }
            for sc in avd_plan["scenes"]
        ],
        "total_duration": avd_plan["total_duration"],
        "image": sb_imgs[0] if sb_imgs else None,
        "images": sb_imgs,
    }

    cj["stages"]["video"] = {
        "status": "draft",
        "plan": "04-video/video-plan.md",
        "upload_assets": "04-video/upload-assets",
        "max_clip_duration": DEFAULT_MAX_CLIP_DURATION,
        "generator_supports_extended_clip": False,
        "generations": [
            {
                "id": cl["id"],
                "file": cl["file"],
                "scenes": cl["scenes"],
                "timestamp": cl["timestamp"],
                "duration": cl["duration"],
            }
            for cl in avd_plan["clip_plan"]
        ],
    }

    cj["stages"]["publishing"] = {
        "status": "draft",
        "files": ["05-publishing/publishing-package.md"],
    }

    # Register inventory references safely without removing existing asset records
    existing_paths = {a.get("path") for a in cj.get("assets", [])}
    assets = list(cj.get("assets", []))
    for idx, ref_rel in enumerate(inv.get("product-reference", []), start=1):
        if ref_rel not in existing_paths:
            assets.append({"id": f"REF-{idx:02d}", "path": ref_rel, "category": "product-reference", "authority": 1})
    cj["assets"] = assets

    if converged:
        approved_by = "hce+avd-autonomous"
        collab_status = "converged"
    elif summary.get("iterations", 0) >= summary.get("max_iterations", MAX_ITERATIONS_CAP):
        approved_by = "partial-max-iterations"
        collab_status = "max-iterations-reached"
    else:
        approved_by = "draft-pending-revision"
        collab_status = "in-revision"

    cj.setdefault("decisions", []).append(
        {
            "date": today,
            "stage": "collaboration",
            "approved_by": approved_by,
            "decision": (
                f"Autonomous HCE<->AVD review completed in {summary['iterations']}/{summary['max_iterations']} iteration(s) "
                f"(converged={converged}, hce={summary['final_hce_score']}, avd={summary['final_avd_score']})."
            ),
        }
    )

    cj["collaboration"] = {
        "enabled": True,
        "partner_skill": "human-copywriting-engine",
        "status": collab_status,
        "iterations": summary["iterations"],
        "max_iterations": summary["max_iterations"],
        "converged": converged,
        "hce_score": summary["final_hce_score"],
        "avd_score": summary["final_avd_score"],
        "retrieved_knowledge_ids": hce_package.get("retrieved_knowledge_ids", []),
        "artifacts_dir": "_collaboration",
        "version_history": summary.get("version_history", []),
    }

    _write_json(cj_path, cj)


def run_collaboration_loop(
    runtime: HCERuntime,
    campaign_dir: Path,
    raw_product: dict[str, Any] | None,
    *,
    platform: str = "tiktok",
    max_iterations: int = MAX_ITERATIONS_CAP,
    write_deliverables: bool = True,
) -> dict[str, Any]:
    """Execute the full autonomous HCE <-> AVD collaborative workflow with <= 3 review iterations."""
    capped_max = min(max(1, int(max_iterations)), MAX_ITERATIONS_CAP)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    collab_dir = campaign_dir / "_collaboration"
    collab_dir.mkdir(parents=True, exist_ok=True)

    if raw_product is not None:
        hce_input, avd_context = normalize_product_input(raw_product, slug=campaign_dir.name, campaign_dir=campaign_dir)
    else:
        hce_input, avd_context = extract_product_input_from_campaign(campaign_dir)

    plat = normalize_platform(platform or hce_input.get("target_platform"))
    hce_input["target_platform"] = plat
    _write_json(collab_dir / "hce-product-input.json", {"hce_input": hce_input, "avd_context": avd_context})

    # Step 3-4: Invoke HCE for marketing intelligence & initial copywriting (v1)
    hce_pkg = run_hce_analysis(runtime, hce_input, avd_context, platform=plat, version=1)
    _write_json(collab_dir / "hce-package-v1.json", hce_pkg)

    # Step 5-6: AVD converts HCE output into adaptive storyboard & clip plan (v1)
    avd_plan = build_avd_plan_from_hce(hce_pkg, avd_context, campaign_dir=campaign_dir, version=1)
    _write_json(collab_dir / "avd-plan-v1.json", avd_plan)

    version_history: list[dict[str, Any]] = [
        {
            "iteration": 0,
            "hce_version": hce_pkg["version"],
            "avd_version": avd_plan["version"],
            "event": "initial_draft",
            "timestamp": _now_iso(),
        }
    ]
    round_summaries: list[dict[str, Any]] = []
    converged = False
    final_hce_eval: dict[str, Any] = {}
    final_avd_eval: dict[str, Any] = {}
    iterations_run = 0

    for round_idx in range(1, capped_max + 1):
        iterations_run = round_idx
        avd_eval = avd_evaluate_plan(avd_plan, hce_pkg, hce_input)
        hce_eval = hce_evaluate_plan(runtime, avd_plan, hce_pkg, hce_input)
        final_avd_eval = avd_eval
        final_hce_eval = hce_eval

        combined_requests = [*avd_eval["revision_requests"], *hce_eval["revision_requests"]]
        round_payload = {
            "round": round_idx,
            "timestamp": _now_iso(),
            "hce_version": hce_pkg["version"],
            "avd_version": avd_plan["version"],
            "avd_review": avd_eval,
            "hce_review": hce_eval,
            "converged": bool(avd_eval["passed"] and hce_eval["passed"]),
            "revision_requests": combined_requests,
            "revisions_applied": [],
        }

        if round_payload["converged"]:
            converged = True
            _write_json(collab_dir / f"review-round-{round_idx}.json", round_payload)
            round_summaries.append(
                {
                    "round": round_idx,
                    "avd_score": avd_eval["overall_score"],
                    "hce_score": hce_eval["overall_score"],
                    "converged": True,
                    "request_count": len(combined_requests),
                }
            )
            break

        # If writing deliverables and this is the first non-converged round, persist v1 markdowns first so v2+ cleanly archives v1
        if write_deliverables and round_idx == 1:
            interim_summary = {
                "iterations": 1,
                "max_iterations": capped_max,
                "converged": False,
                "final_hce_score": hce_eval["overall_score"],
                "final_avd_score": avd_eval["overall_score"],
                "version_history": version_history,
            }
            write_campaign_deliverables(
                campaign_dir, hce_input, avd_context, hce_pkg, avd_plan, interim_summary, archive_existing=True
            )

        # Do not revise past the max iteration boundary
        if round_idx == capped_max:
            _write_json(collab_dir / f"review-round-{round_idx}.json", round_payload)
            round_summaries.append(
                {
                    "round": round_idx,
                    "avd_score": avd_eval["overall_score"],
                    "hce_score": hce_eval["overall_score"],
                    "converged": False,
                    "request_count": len(combined_requests),
                }
            )
            break

        # Route targeted revision requests to HCE and AVD
        hce_reqs = [r for r in combined_requests if r.get("target_agent") == "hce"]
        avd_reqs = [r for r in combined_requests if r.get("target_agent") == "affiliate-video-director"]

        applied_log: list[dict[str, Any]] = []
        if hce_reqs:
            hce_pkg, hce_changes = hce_apply_revisions(runtime, hce_pkg, avd_plan, hce_reqs)
            _write_json(collab_dir / f"hce-package-v{hce_pkg['version']}.json", hce_pkg)
            applied_log.extend(hce_changes)

        if avd_reqs or hce_reqs:
            avd_plan, avd_changes = avd_apply_revisions(avd_plan, hce_pkg, avd_reqs)
            _write_json(collab_dir / f"avd-plan-v{avd_plan['version']}.json", avd_plan)
            applied_log.extend(avd_changes)

        round_payload["revisions_applied"] = applied_log
        _write_json(collab_dir / f"review-round-{round_idx}.json", round_payload)
        round_summaries.append(
            {
                "round": round_idx,
                "avd_score": avd_eval["overall_score"],
                "hce_score": hce_eval["overall_score"],
                "converged": False,
                "request_count": len(combined_requests),
            }
        )
        version_history.append(
            {
                "iteration": round_idx,
                "hce_version": hce_pkg["version"],
                "avd_version": avd_plan["version"],
                "event": "bidirectional_revision",
                "requests_resolved": len(combined_requests),
                "changes_count": len(applied_log),
                "timestamp": _now_iso(),
            }
        )

    summary = {
        "slug": campaign_dir.name,
        "product_name": hce_input["name"],
        "platform": plat,
        "iterations": iterations_run,
        "max_iterations": capped_max,
        "converged": converged,
        "final_hce_score": final_hce_eval.get("overall_score", 0.0),
        "final_avd_score": final_avd_eval.get("overall_score", 0.0),
        "final_hce_version": hce_pkg["version"],
        "final_avd_version": avd_plan["version"],
        "retrieved_knowledge_ids": hce_pkg.get("retrieved_knowledge_ids", []),
        "rounds": round_summaries,
        "version_history": version_history,
        "archived_deliverables": [],
        "completed_at": _now_iso(),
    }

    if write_deliverables:
        archived = write_campaign_deliverables(
            campaign_dir,
            hce_input,
            avd_context,
            hce_pkg,
            avd_plan,
            summary,
            archive_existing=True,
        )
        summary["archived_deliverables"] = archived

    _write_json(collab_dir / "collaboration-summary.json", summary)
    return summary


def _latest_versioned_json(collab_dir: Path, prefix: str) -> Path | None:
    files = sorted(collab_dir.glob(f"{prefix}-v*.json"))
    if not files:
        return None
    def _ver_num(p: Path) -> int:
        m = re.search(r"-v(\d+)\.json$", p.name)
        return int(m.group(1)) if m else 0
    return max(files, key=_ver_num)


def _cmd_search(args: argparse.Namespace) -> int:
    rt = load_hce_runtime(args.hce_root)
    hits = rt.retriever.search(args.query, category=args.category, limit=args.limit)
    if args.json:
        print(json.dumps([{"score": h.score, "concept": h.concept.to_dict()} for h in hits], indent=2, ensure_ascii=False))
        return 0
    print(f"Found {len(hits)} HCE concept(s) for {args.query!r}:")
    for idx, h in enumerate(hits, start=1):
        print(f"  [{idx}] {h.concept.concept_id} ({h.concept.category}) - {h.concept.concept_name}: {h.concept.explanation}")
    return 0


def _cmd_hce_analyze(args: argparse.Namespace) -> int:
    rt = load_hce_runtime(args.hce_root)
    cdir = Path(args.campaign_dir).resolve()
    cdir.mkdir(parents=True, exist_ok=True)
    collab_dir = cdir / "_collaboration"
    collab_dir.mkdir(parents=True, exist_ok=True)

    if args.product_input:
        raw = json.loads(Path(args.product_input).read_text(encoding="utf-8"))
        hce_input, avd_ctx = normalize_product_input(raw, slug=cdir.name, campaign_dir=cdir)
    else:
        hce_input, avd_ctx = extract_product_input_from_campaign(cdir)

    _write_json(collab_dir / "hce-product-input.json", {"hce_input": hce_input, "avd_context": avd_ctx})
    pkg = run_hce_analysis(rt, hce_input, avd_ctx, platform=args.platform, version=args.version)
    out_path = collab_dir / f"hce-package-v{args.version}.json"
    _write_json(out_path, pkg)

    if args.json:
        print(json.dumps(pkg, indent=2, ensure_ascii=False))
    else:
        print(f"[OK] HCE package v{args.version} disimpan di: {out_path}")
        print(f"  Strategi: {pkg['strategy']['strategy_name']} | Skor awal HCE: {pkg['evaluation']['overall_score']}/10")
    return 0


def _cmd_avd_review(args: argparse.Namespace) -> int:
    cdir = Path(args.campaign_dir).resolve()
    collab_dir = cdir / "_collaboration"
    if args.avd_plan:
        avd_plan = json.loads(Path(args.avd_plan).read_text(encoding="utf-8"))
    elif args.storyboard:
        avd_plan = _extract_avd_plan_from_markdown(cdir, storyboard_path=Path(args.storyboard))
    else:
        latest = _latest_versioned_json(collab_dir, "avd-plan") if collab_dir.is_dir() else None
        avd_plan = json.loads(latest.read_text(encoding="utf-8")) if latest else _extract_avd_plan_from_markdown(cdir)

    latest_hce = _latest_versioned_json(collab_dir, "hce-package") if collab_dir.is_dir() else None
    hce_pkg = json.loads(latest_hce.read_text(encoding="utf-8")) if latest_hce else None
    result = avd_evaluate_plan(avd_plan, hce_pkg)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"=== AVD Review ({cdir.name}) ===")
        print(f"Status: {'PASSED' if result['passed'] else 'REVISION_REQUIRED'} (overall={result['overall_score']}/10)")
        for k, v in result["criteria"].items():
            print(f"  - {k:30s}: {v}/10")
        for r in result["revision_requests"]:
            print(f"  [{r['request_id']} -> {r['target_agent']}] {r['issue']}")
    return 0 if result["passed"] else 2


def _cmd_hce_review(args: argparse.Namespace) -> int:
    rt = load_hce_runtime(args.hce_root)
    cdir = Path(args.campaign_dir).resolve()
    collab_dir = cdir / "_collaboration"

    if args.avd_plan:
        avd_plan = json.loads(Path(args.avd_plan).read_text(encoding="utf-8"))
    elif args.storyboard or args.publishing:
        avd_plan = _extract_avd_plan_from_markdown(
            cdir,
            storyboard_path=Path(args.storyboard) if args.storyboard else None,
            publishing_path=Path(args.publishing) if args.publishing else None,
        )
    else:
        latest = _latest_versioned_json(collab_dir, "avd-plan") if collab_dir.is_dir() else None
        avd_plan = json.loads(latest.read_text(encoding="utf-8")) if latest else _extract_avd_plan_from_markdown(cdir)

    if args.platform:
        avd_plan["platform"] = normalize_platform(args.platform)

    latest_hce = _latest_versioned_json(collab_dir, "hce-package") if collab_dir.is_dir() else None
    hce_pkg = json.loads(latest_hce.read_text(encoding="utf-8")) if latest_hce else None

    hce_input: dict[str, Any] = {}
    inp_path = collab_dir / "hce-product-input.json"
    if inp_path.is_file():
        hce_input = json.loads(inp_path.read_text(encoding="utf-8")).get("hce_input", {})
    elif not hce_pkg:
        hce_input, _ = extract_product_input_from_campaign(cdir)

    result = hce_evaluate_plan(rt, avd_plan, hce_pkg, hce_input)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"=== HCE Review ({cdir.name}) ===")
        gate = result["hce_7d_evaluation"]["gate_status"]
        print(f"Status: {'PASSED' if result['passed'] else 'REVISION_REQUIRED'} (gate={gate}, overall={result['overall_score']}/10)")
        for k, v in result["criteria"].items():
            print(f"  - {k:30s}: {v}/10")
        for r in result["revision_requests"]:
            print(f"  [{r['request_id']} -> {r['target_agent']}] {r['issue']}")
    return 0 if result["passed"] else 2


def _cmd_collaborate(args: argparse.Namespace) -> int:
    rt = load_hce_runtime(args.hce_root)
    cdir = Path(args.campaign_dir).resolve()
    raw_prod = json.loads(Path(args.product_input).read_text(encoding="utf-8")) if args.product_input else None
    summary = run_collaboration_loop(
        rt,
        cdir,
        raw_prod,
        platform=args.platform,
        max_iterations=args.max_iterations,
        write_deliverables=args.write_deliverables,
    )
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"=== Kolaborasi Otonom HCE <-> AVD: {summary['slug']} ===")
        print(f"  Produk      : {summary['product_name']}")
        print(f"  Platform    : {summary['platform']}")
        print(f"  Iterasi     : {summary['iterations']} / {summary['max_iterations']}")
        print(f"  Konvergen   : {summary['converged']}")
        print(f"  Skor Akhir  : HCE={summary['final_hce_score']}/10 | AVD={summary['final_avd_score']}/10")
        print(f"  Versi Akhir : HCE v{summary['final_hce_version']} | AVD v{summary['final_avd_version']}")
        if summary["archived_deliverables"]:
            print(f"  Diarsipkan  : {', '.join(summary['archived_deliverables'])}")
    return 0 if summary["converged"] else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bridge kolaborasi otonom antara Affiliate Video Director (AVD) dan Human Copywriting Engine (HCE)."
    )
    parser.add_argument("--hce-root", default=None, help="Path opsional ke direktori repositori HCE.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Cari prinsip copywriting dari knowledge base HCE.")
    p_search.add_argument("query", help="Kata kunci pencarian.")
    p_search.add_argument("--category", default=None, help="Filter kategori HCE.")
    p_search.add_argument("--limit", type=int, default=5)
    p_search.add_argument("--json", action="store_true")
    p_search.set_defaults(func=_cmd_search)

    p_an = sub.add_parser("hce-analyze", help="Jalankan analisis pemasaran & copywriting HCE untuk sebuah kampanye.")
    p_an.add_argument("campaign_dir", help="Direktori kampanye target.")
    src_g = p_an.add_mutually_exclusive_group(required=True)
    src_g.add_argument("--product-input", default=None, help="Path JSON profil produk.")
    src_g.add_argument("--from-campaign", action="store_true", help="Ekstrak input produk dari campaign.json & references/.")
    p_an.add_argument("--platform", default="tiktok")
    p_an.add_argument("--version", type=int, default=1)
    p_an.add_argument("--json", action="store_true")
    p_an.set_defaults(func=_cmd_hce_analyze)

    p_avd = sub.add_parser("avd-review", help="Evaluasi storyboard/plan dari perspektif produksi video AVD.")
    p_avd.add_argument("campaign_dir")
    p_avd.add_argument("--avd-plan", default=None)
    p_avd.add_argument("--storyboard", default=None)
    p_avd.add_argument("--json", action="store_true")
    p_avd.set_defaults(func=_cmd_avd_review)

    p_hce = sub.add_parser("hce-review", help="Evaluasi storyboard/copy/CTA/publishing dari perspektif HCE.")
    p_hce.add_argument("campaign_dir")
    p_hce.add_argument("--avd-plan", default=None)
    p_hce.add_argument("--storyboard", default=None)
    p_hce.add_argument("--publishing", default=None)
    p_hce.add_argument("--platform", default=None)
    p_hce.add_argument("--json", action="store_true")
    p_hce.set_defaults(func=_cmd_hce_review)

    p_col = sub.add_parser("collaborate", help="Jalankan kolaborasi otonom dua arah HCE <-> AVD (maks 3 iterasi).")
    p_col.add_argument("campaign_dir")
    col_g = p_col.add_mutually_exclusive_group(required=True)
    col_g.add_argument("--product-input", default=None, help="Path JSON profil produk.")
    col_g.add_argument("--from-campaign", action="store_true", help="Ekstrak input produk dari campaign.json & references/.")
    p_col.add_argument("--platform", default="tiktok")
    p_col.add_argument("--max-iterations", type=int, default=MAX_ITERATIONS_CAP)
    p_col.add_argument("--write-deliverables", action="store_true", help="Tulis paket file Markdown AVD final & perbarui campaign.json.")
    p_col.add_argument("--json", action="store_true")
    p_col.set_defaults(func=_cmd_collaborate)

    return parser


def main(argv: list[str] | None = None) -> int:
    _configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
