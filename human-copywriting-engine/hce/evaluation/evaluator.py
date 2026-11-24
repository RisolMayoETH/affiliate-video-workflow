"""Seven-dimension copy evaluation rubric with mandatory accuracy/authenticity integrity gate."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

from hce.language.refiner import (
    ARTIFICIAL_URGENCY_PATTERNS,
    CLICHE_PATTERNS,
    GENERIC_AI_INTRO_PATTERNS,
    PERSONAL_CLAIM_PATTERNS,
)

EVALUATION_DIMENSIONS = (
    "naturalness",
    "buyer_psychology",
    "persuasiveness",
    "storytelling",
    "audience_adaptation",
    "product_accuracy",
    "authenticity",
)

UNVERIFIED_DISCOUNT_PATTERNS = (
    re.compile(r"\bdiskon\s+\d+%", re.IGNORECASE),
    re.compile(r"\bpotongan\s+harga\b", re.IGNORECASE),
    re.compile(r"\bpromo\s+gila\b", re.IGNORECASE),
    re.compile(r"\bgaransi\s+seumur\s+hidup\b", re.IGNORECASE),
    re.compile(r"\bterbukti\s+klinis\b", re.IGNORECASE),
)

PSYCHOLOGY_MARKERS = (
    "kalau",
    "sering",
    "takut",
    "ragu",
    "nyaman",
    "praktis",
    "cocok",
    "bantu",
    "hemat",
    "rapi",
    "aman",
    "kapasitas",
    "ukuran",
    "bahan",
)

CTA_MARKERS = ("keranjang", "tautan", "link", "cek", "varian", "detail", "ukuran", "warna")


@dataclass
class DimensionScore:
    score: float
    rationale: str
    suggestions: list[str] = field(default_factory=list)


@dataclass
class EvaluationReport:
    dimensions: dict[str, DimensionScore]
    overall_score: float
    passed: bool
    gate_status: str
    integrity_violations: list[str] = field(default_factory=list)
    improvement_suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimensions": {k: asdict(v) for k, v in self.dimensions.items()},
            "overall_score": self.overall_score,
            "passed": self.passed,
            "gate_status": self.gate_status,
            "integrity_violations": self.integrity_violations,
            "improvement_suggestions": self.improvement_suggestions,
        }


def _clamp(val: float) -> float:
    return round(max(1.0, min(10.0, val)), 2)


class CopyEvaluator:
    """Evaluates affiliate scripts across 7 distinct dimensions (1-10) without compromising truth."""

    def evaluate(
        self,
        *,
        hooks: list[str],
        scenes: list[dict[str, Any]],
        cta: str,
        caption: str,
        platform: str = "tiktok",
        product_data: dict[str, Any] | None = None,
    ) -> EvaluationReport:
        narrations = [str(s.get("spoken_narration", "")).strip() for s in scenes]
        all_text = " ".join([*hooks, *narrations, cta, caption]).strip()
        all_lower = all_text.lower()

        product_data = product_data or {}
        verified_features = [str(x) for x in product_data.get("verified_features", [])]
        verified_specs = product_data.get("verified_specs") or {}
        available_evidence = [str(x) for x in product_data.get("available_evidence", [])]
        evidence_lower = " ".join(available_evidence).lower()
        product_truth_blob = " ".join(
            [
                str(product_data.get("name", "")),
                str(product_data.get("description", "")),
                *verified_features,
                *(f"{k} {v}" for k, v in verified_specs.items()),
                *available_evidence,
            ]
        ).lower()

        integrity_violations: list[str] = []

        # ------------------------------------------------------------------
        # 1. Naturalness
        # ------------------------------------------------------------------
        nat_score = 9.0
        nat_suggestions: list[str] = []
        cliche_hits = sum(1 for pat, _, _ in CLICHE_PATTERNS if pat.search(all_text))
        ai_intro_hits = sum(1 for pat, _ in GENERIC_AI_INTRO_PATTERNS if pat.search(all_text))
        if cliche_hits:
            nat_score -= 1.5 * cliche_hits
            nat_suggestions.append("Hapus frasa template klise ('Guys!', 'Wajib banget!', 'Worth it parah!') dan ganti dengan pengamatan produk yang spesifik.")
        if ai_intro_hits:
            nat_score -= 1.2 * ai_intro_hits
            nat_suggestions.append("Ubah pembuka AI generik menjadi kalimat lisan langsung.")

        sentences = [s.strip() for s in re.split(r"[.!?]+", all_text) if s.strip()]
        openers = [" ".join(s.lower().split()[:2]) for s in sentences if len(s.split()) >= 2]
        repeated_openers = [op for op, cnt in Counter(openers).items() if cnt >= 3]
        if repeated_openers:
            nat_score -= 1.0
            nat_suggestions.append(f"Variasikan pembuka kalimat yang berulang ({', '.join(repeated_openers)}).")

        if " anda " in f" {all_lower} ":
            nat_score -= 0.7
            nat_suggestions.append("Ganti kata 'Anda' yang kaku untuk short-video menjadi sapaan sehari-hari yang lebih luwes.")

        # ------------------------------------------------------------------
        # 2. Buyer Psychology
        # ------------------------------------------------------------------
        psych_hits = sum(1 for m in PSYCHOLOGY_MARKERS if m in all_lower)
        psych_score = 5.5 + min(3.8, psych_hits * 0.55)
        psych_suggestions: list[str] = []
        if psych_hits < 3:
            psych_suggestions.append("Tambahkan alasan praktis atau jawaban atas keraguan pembeli (ukuran, cara pakai, atau kecocokan situasi).")

        # ------------------------------------------------------------------
        # 3. Persuasiveness
        # ------------------------------------------------------------------
        pers_score = 6.0
        pers_suggestions: list[str] = []
        if len(hooks) >= 2:
            pers_score += 0.8
        else:
            pers_suggestions.append("Sediakan minimal 2-3 variasi hook yang relevan ke produk.")
        if any(m in cta.lower() for m in CTA_MARKERS):
            pers_score += 1.2
        else:
            pers_suggestions.append("Perjelas CTA agar pembeli tahu di mana melihat detail varian dan harga.")

        # Reward grounding in verified features
        matched_features = 0
        for feat in verified_features:
            tokens = [t for t in re.findall(r"[a-zA-Z0-9]+", feat.lower()) if len(t) > 3]
            if any(t in all_lower for t in tokens):
                matched_features += 1
        if verified_features:
            coverage = matched_features / len(verified_features)
            pers_score += min(1.8, coverage * 2.0)
            if coverage < 0.4:
                pers_suggestions.append("Masukkan lebih banyak fitur terverifikasi produk dan terjemahkan menjadi manfaat nyata.")

        # ------------------------------------------------------------------
        # 4. Storytelling & Pacing
        # ------------------------------------------------------------------
        story_score = 6.0
        story_suggestions: list[str] = []
        if len(scenes) >= 3:
            story_score += 1.2
        else:
            story_suggestions.append("Strukturkan minimal 3 adegan agar alur pembuka, penjelasan/demo, dan penutup jelas.")
        durations = [float(s.get("duration_seconds", 0)) for s in scenes]
        if len(set(durations)) > 1:
            story_score += 1.0  # Flexible non-uniform scene pacing
        else:
            story_score -= 0.5
            story_suggestions.append("Sesuaikan durasi masing-masing adegan dengan bobot visual dan narasinya, jangan disamaratakan.")
        objectives = [str(s.get("narrative_objective", "")).strip() for s in scenes]
        if all(objectives):
            story_score += 0.8

        # ------------------------------------------------------------------
        # 5. Audience Adaptation
        # ------------------------------------------------------------------
        adapt_score = 7.5
        adapt_suggestions: list[str] = []
        plat = platform.lower()
        if plat == "tiktok" and "keranjang oranye" in all_lower:
            adapt_score -= 2.0
            adapt_suggestions.append("Sesuaikan penyebutan CTA dengan TikTok (keranjang kuning/tautan kiri bawah), bukan keranjang oranye.")
        elif plat in ("instagram_reels", "facebook_reels") and "keranjang kuning" in all_lower:
            adapt_score -= 2.0
            adapt_suggestions.append(f"Hapus istilah 'keranjang kuning' karena tidak sesuai dengan platform {platform}.")
        elif plat == "shopee_video" and "keranjang kuning" in all_lower:
            adapt_score -= 1.5
            adapt_suggestions.append("Gunakan istilah keranjang/tautan produk Shopee Video alih-alih keranjang kuning TikTok.")
        if not caption.strip():
            adapt_score -= 1.0
            adapt_suggestions.append("Tambahkan caption singkat berbahasa Indonesia alami yang sesuai dengan platform.")

        # ------------------------------------------------------------------
        # 6 & 7. Product Accuracy & Authenticity (MANDATORY HARD GATE)
        # ------------------------------------------------------------------
        acc_score = 9.3
        auth_score = 9.3
        acc_suggestions: list[str] = []
        auth_suggestions: list[str] = []

        has_personal_evidence = any(
            k in evidence_lower for k in ("pengalaman", "pribadi", "tested", "pemakaian", "personal")
        )
        if not has_personal_evidence:
            for pat in PERSONAL_CLAIM_PATTERNS:
                if pat.search(all_text):
                    integrity_violations.append(
                        f"Klaim pengalaman pribadi atau testimoni tanpa bukti terverifikasi ({pat.pattern})."
                    )
                    auth_score -= 4.0
                    auth_suggestions.append("Hapus klaim 'aku udah pakai' atau testimoni jika tidak ada di available_evidence.")

        has_promo_evidence = any(k in evidence_lower for k in ("diskon", "promo", "stok"))
        if not has_promo_evidence:
            for pat in [*ARTIFICIAL_URGENCY_PATTERNS, *UNVERIFIED_DISCOUNT_PATTERNS]:
                if pat.search(all_text):
                    integrity_violations.append(
                        f"Klaim diskon/kelangkaan tanpa bukti pada data produk ({pat.pattern})."
                    )
                    acc_score -= 3.5
                    auth_score -= 3.0
                    acc_suggestions.append("Hapus klaim diskon, garansi, atau stok terbatas yang tidak tercatat di profil produk.")

        # Check numeric claims with units (ml, watt, jam, hari, tahun, bulan, %, spf, kg, gram)
        if product_truth_blob:
            numeric_claims = re.findall(
                r"\b(\d+(?:[.,]\d+)?)\s*(ml|l|liter|watt|w|jam|hari|minggu|bulan|tahun|kg|gram|gr|%|mode|mata pisau)\b",
                all_lower,
            )
            for num, unit in numeric_claims:
                # allow scene durations outside narration; numeric_claims came from spoken/written copy
                if f"{num} {unit}" not in product_truth_blob and f"{num}{unit}" not in product_truth_blob and num not in product_truth_blob:
                    integrity_violations.append(
                        f"Angka/spesifikasi '{num} {unit}' disebut di naskah tetapi tidak ada di data produk terverifikasi."
                    )
                    acc_score -= 3.5
                    acc_suggestions.append(f"Verifikasi atau hapus angka '{num} {unit}' agar sesuai data produk.")

        dimensions = {
            "naturalness": DimensionScore(
                _clamp(nat_score),
                "Menilai ritme lisan, ketiadaan klise AI, dan variasi pola kalimat.",
                nat_suggestions,
            ),
            "buyer_psychology": DimensionScore(
                _clamp(psych_score),
                "Menilai relevansi kebutuhan pembeli, pengurangan keraguan, dan kepercayaan.",
                psych_suggestions,
            ),
            "persuasiveness": DimensionScore(
                _clamp(pers_score),
                "Menilai kekuatan hook, terjemahan fitur ke manfaat, dan kejelasan CTA.",
                pers_suggestions,
            ),
            "storytelling": DimensionScore(
                _clamp(story_score),
                "Menilai alur adegan, fleksibilitas durasi, dan kejelasan tujuan tiap adegan.",
                story_suggestions,
            ),
            "audience_adaptation": DimensionScore(
                _clamp(adapt_score),
                f"Menilai kecocokan gaya bahasa dan struktur dengan platform {platform}.",
                adapt_suggestions,
            ),
            "product_accuracy": DimensionScore(
                _clamp(acc_score),
                "Menilai kesesuaian klaim dan spesifikasi dengan fakta produk yang diberikan.",
                acc_suggestions,
            ),
            "authenticity": DimensionScore(
                _clamp(auth_score),
                "Menilai kejujuran narasi tanpa testimoni, urgensi, atau pengalaman fiktif.",
                auth_suggestions,
            ),
        }

        overall = round(
            sum(d.score for d in dimensions.values()) / len(dimensions), 2
        )

        # Hard Integrity Gate: persuasion/conversion cannot compensate for fabricated claims
        if (
            integrity_violations
            or dimensions["product_accuracy"].score < 7.0
            or dimensions["authenticity"].score < 7.0
        ):
            passed = False
            gate_status = "FAILED_INTEGRITY_GATE"
        elif overall >= 7.0 and all(d.score >= 6.0 for d in dimensions.values()):
            passed = True
            gate_status = "PASSED"
        else:
            passed = False
            gate_status = "NEEDS_REVISION"

        all_suggestions: list[str] = []
        for dim_name, dim_val in dimensions.items():
            for sug in dim_val.suggestions:
                all_suggestions.append(f"[{dim_name}] {sug}")
        if not all_suggestions:
            all_suggestions.append(
                "Naskah sudah memenuhi seluruh kriteria kealamian, akurasi produk, dan struktur platform."
            )

        return EvaluationReport(
            dimensions=dimensions,
            overall_score=overall,
            passed=passed,
            gate_status=gate_status,
            integrity_violations=integrity_violations,
            improvement_suggestions=all_suggestions,
        )
