"""Context-aware Indonesian natural language refinement engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Cliché templates forbidden as default phrases
CLICHE_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"\b(?:halo|hai)?\s*guys[!,.]*\s*", re.IGNORECASE),
        "default_cliche_guys",
        "Hindari sapaan default 'Guys!'; mulai langsung dengan konteks masalah atau fungsi produk.",
    ),
    (
        re.compile(r"\bwajib banget(?:\s+punya|\s+beli|\s+coba)?[!,.]*", re.IGNORECASE),
        "default_cliche_wajib",
        "Ganti 'wajib banget' dengan alasan praktis mengapa produk ini relevan bagi pembeli tertentu.",
    ),
    (
        re.compile(r"\bauto tertarik[!,.]*", re.IGNORECASE),
        "default_cliche_auto_tertarik",
        "Hapus klaim 'auto tertarik' dan biarkan penjelasan fungsi berbicara sendiri.",
    ),
    (
        re.compile(r"\bworth it parah[!,.]*", re.IGNORECASE),
        "default_cliche_worth_it",
        "Ganti 'worth it parah' dengan nilai guna konkret dari spesifikasi produk.",
    ),
    (
        re.compile(r"\bjangan sampai ketinggalan[!,.]*", re.IGNORECASE),
        "default_cliche_ketinggalan",
        "Hapus urgensi klise 'jangan sampai ketinggalan' dan arahkan ke informasi detail produk.",
    ),
]

GENERIC_AI_INTRO_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bdi era modern ini\b[, ]*", re.IGNORECASE), "Pembuka AI generik 'di era modern ini'"),
    (re.compile(r"\bapakah anda sering\b", re.IGNORECASE), "Pembuka terjemahan kaku 'apakah Anda sering'"),
    (re.compile(r"\bapakah kamu pernah merasa\b", re.IGNORECASE), "Pembuka template 'apakah kamu pernah merasa'"),
    (re.compile(r"\bhadir sebagai solusi\b", re.IGNORECASE), "Frasa iklan korporat 'hadir sebagai solusi'"),
    (re.compile(r"\bmenjawab kebutuhan anda\b", re.IGNORECASE), "Frasa brosur kaku 'menjawab kebutuhan Anda'"),
]

CORPORATE_STIFF_REWRITES: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"\bmenunjang produktivitas anda secara optimal\b", re.IGNORECASE),
        "bikin kerja di meja jadi lebih nyaman",
        "Bahasa korporat kaku menjadi bahasa lisan wajar.",
    ),
    (
        re.compile(r"\bsangat direkomendasikan untuk\b", re.IGNORECASE),
        "cukup cocok buat",
        "Nada brosur resmi menjadi rekomendasi natural.",
    ),
    (
        re.compile(r"\bdirancang secara ergonomis\b", re.IGNORECASE),
        "dibentuk supaya nyaman dipakai",
        "Istilah teknis kaku menjadi penjelasan lisan.",
    ),
    (
        re.compile(r"\bmemberikan performa maksimal\b", re.IGNORECASE),
        "bekerja cukup stabil untuk pemakaian harian",
        "Klaim hiperbolis korporat menjadi pernyataan wajar.",
    ),
    (
        re.compile(r"\bAnda\b"),
        "kamu",
        "Mengubah sapaan kaku 'Anda' menjadi 'kamu' pada konteks video pendek kasual.",
    ),
]

BOOKISH_DICTIONARY_REWRITES: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"\b(?:oleh karena itu|maka dari itu)\b", re.IGNORECASE),
        "makanya",
        "Penghubung bahasa buku ('oleh karena itu'/'maka dari itu') diganti kata obrolan normal 'makanya'.",
    ),
    (
        re.compile(r"\bnamun demikian\b", re.IGNORECASE),
        "tapi",
        "Penghubung buku kaku 'namun demikian' diganti 'tapi'.",
    ),
    (
        re.compile(r"\bdengan demikian\b", re.IGNORECASE),
        "jadinya",
        "Penghubung buku kaku 'dengan demikian' diganti 'jadinya'.",
    ),
    (
        re.compile(r"\bmerupakan pilihan yang tepat\b", re.IGNORECASE),
        "cocok dipilih",
        "Ungkapan brosur/kamus 'merupakan pilihan yang tepat' diganti kalimat lisan wajar.",
    ),
    (
        re.compile(r"\bmemungkinkan\s+(?:Anda|kamu)\s+untuk\b", re.IGNORECASE),
        "bikin kamu bisa",
        "Frasa kamus/terjemahan 'memungkinkan ... untuk' diganti ke bahasa obrolan sehari-hari.",
    ),
    (
        re.compile(r"\btidak perlu khawatir lagi\b", re.IGNORECASE),
        "nggak perlu bingung lagi",
        "Ungkapan buku 'tidak perlu khawatir lagi' diganti ke ucapan lisan normal.",
    ),
    (
        re.compile(r"\bberbagai macam kebutuhan\b", re.IGNORECASE),
        "berbagai kebutuhan harian",
        "Frasa brosur kaku 'berbagai macam kebutuhan' disederhanakan ke bahasa lisan.",
    ),
    (
        re.compile(r"\bdapat digunakan untuk\b", re.IGNORECASE),
        "bisa dipakai buat",
        "Bentuk pasif buku 'dapat digunakan untuk' diganti ke kata percakapan biasa.",
    ),
    (
        re.compile(r"\bhal ini dikarenakan\b", re.IGNORECASE),
        "soalnya",
        "Frasa laporan resmi 'hal ini dikarenakan' diganti penghubung lisan 'soalnya'.",
    ),
]

ARTIFICIAL_URGENCY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bburuan(?:\s+beli|\s+checkout)?\s+sebelum kehabisan[!.]*", re.IGNORECASE),
    re.compile(r"\bstok\s+(?:sangat\s+)?terbatas[^.!?]*[.!?]?", re.IGNORECASE),
    re.compile(r"\bkhusus\s+hari\s+ini[^.!?]*[.!?]?", re.IGNORECASE),
    re.compile(r"\bharga\s+(?:akan\s+)?naik[^.!?]*[.!?]?", re.IGNORECASE),
]

EXCESSIVE_ADJECTIVES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bsuper duper\b", re.IGNORECASE), "cukup"),
    (re.compile(r"\bluar biasa canggih\b", re.IGNORECASE), "praktis"),
    (re.compile(r"\bsempurna banget\b", re.IGNORECASE), "pas"),
    (re.compile(r"\bterbaik sepanjang masa\b", re.IGNORECASE), "layak dipertimbangkan"),
]

PERSONAL_CLAIM_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(?:aku|saya|gue)\s+(?:udah|sudah)\s+(?:pakai|coba|buktikan)\b", re.IGNORECASE),
    re.compile(r"\btestimoni\s+pembeli\b", re.IGNORECASE),
    re.compile(r"\b100%\s+(?:ampuh|berhasil|original|aman)\b", re.IGNORECASE),
]


@dataclass
class LanguageIssue:
    location: str
    issue_type: str
    original_sentence: str
    suggestion: str
    reason: str


@dataclass
class RefinementResult:
    original_text: str
    refined_text: str
    issues: list[LanguageIssue] = field(default_factory=list)
    rewrites_applied: int = 0


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _apply_case_preserving_rewrite(
    pattern: re.Pattern[str], replacement: str, text: str
) -> str:
    """Replace matched phrase while preserving sentence-initial capitalization."""

    def _sub(match: re.Match[str]) -> str:
        matched = match.group(0)
        if matched and matched[0].isupper() and replacement:
            return replacement[0].upper() + replacement[1:]
        return replacement

    return pattern.sub(_sub, text)


class NaturalLanguageRefiner:
    """Reviews Indonesian affiliate copy at full-sentence level and rewrites robotic patterns."""

    def refine_text(
        self,
        text: str,
        *,
        location: str = "script",
        register: str = "casual_everyday",
        available_evidence: list[str] | None = None,
    ) -> RefinementResult:
        evidence_text = " ".join(available_evidence or []).lower()
        has_personal_evidence = any(
            k in evidence_text for k in ("pengalaman", "pribadi", "tested", "pemakaian", "personal")
        )
        has_promo_evidence = any(
            k in evidence_text for k in ("diskon", "promo", "stok", "flash sale")
        )

        sentences = _split_sentences(text)
        refined_sentences: list[str] = []
        issues: list[LanguageIssue] = []
        rewrites = 0
        previous_opener = ""

        for idx, sent in enumerate(sentences):
            current = sent
            loc = f"{location}#s{idx + 1}"

            # 1. Default AI/affiliate clichés
            for pat, issue_type, reason in CLICHE_PATTERNS:
                if pat.search(current):
                    new_sent = pat.sub("", current).strip(" ,!-")
                    if new_sent:
                        new_sent = new_sent[0].upper() + new_sent[1:]
                    else:
                        new_sent = "Langsung lihat cara kerja produknya di situasi harian."
                    issues.append(
                        LanguageIssue(loc, issue_type, current, new_sent, reason)
                    )
                    current = new_sent
                    rewrites += 1

            # 2. Generic AI openings
            for pat, reason in GENERIC_AI_INTRO_PATTERNS:
                if pat.search(current):
                    new_sent = pat.sub("", current).strip(" ,?-")
                    if pat.pattern.startswith(r"\bapakah"):
                        new_sent = f"Kalau sering mengalami kondisi ini, {new_sent.lower()}."
                    elif new_sent:
                        new_sent = new_sent[0].upper() + new_sent[1:]
                    issues.append(
                        LanguageIssue(loc, "generic_ai_intro", current, new_sent, reason)
                    )
                    current = new_sent
                    rewrites += 1

            # 3. Corporate / translationese rewrites
            for pat, replacement, reason in CORPORATE_STIFF_REWRITES:
                if pat.search(current):
                    if pat.pattern == r"\bAnda\b" and register == "polite_neutral":
                        continue
                    new_sent = pat.sub(replacement, current)
                    if new_sent != current:
                        issues.append(
                            LanguageIssue(loc, "stiff_or_corporate", current, new_sent, reason)
                        )
                        current = new_sent
                        rewrites += 1

            # 3b. Bookish / dictionary phrasing rewrites (casual registers)
            if register != "polite_neutral":
                for pat, replacement, reason in BOOKISH_DICTIONARY_REWRITES:
                    if pat.search(current):
                        new_sent = _apply_case_preserving_rewrite(pat, replacement, current)
                        if new_sent != current:
                            issues.append(
                                LanguageIssue(
                                    loc,
                                    "bookish_dictionary_phrase",
                                    current,
                                    new_sent,
                                    reason,
                                )
                            )
                            current = new_sent
                            rewrites += 1

            # 4. Unverified urgency / scarcity
            if not has_promo_evidence:
                for pat in ARTIFICIAL_URGENCY_PATTERNS:
                    if pat.search(current):
                        new_sent = pat.sub(
                            "Cek detail varian dan ketersediaannya di tautan produk.",
                            current,
                        ).strip()
                        issues.append(
                            LanguageIssue(
                                loc,
                                "artificial_urgency",
                                current,
                                new_sent,
                                "Menghapus urgensi/kelangkaan buatan yang tidak didukung bukti.",
                            )
                        )
                        current = new_sent
                        rewrites += 1

            # 5. Excessive adjective exaggeration
            for pat, replacement in EXCESSIVE_ADJECTIVES:
                if pat.search(current):
                    new_sent = pat.sub(replacement, current)
                    issues.append(
                        LanguageIssue(
                            loc,
                            "excessive_adjectives",
                            current,
                            new_sent,
                            "Mengurangi kata sifat berlebihan agar terdengar seperti ulasan wajar.",
                        )
                    )
                    current = new_sent
                    rewrites += 1

            # 6. Fabricated personal experience / testimonials when evidence lacks it
            if not has_personal_evidence:
                for pat in PERSONAL_CLAIM_PATTERNS:
                    if pat.search(current):
                        new_sent = pat.sub("Dari detail produknya,", current)
                        issues.append(
                            LanguageIssue(
                                loc,
                                "unverified_experience_or_claim",
                                current,
                                new_sent,
                                "Mengganti klaim pengalaman/testimoni tanpa bukti menjadi observasi produk yang jujur.",
                            )
                        )
                        current = new_sent
                        rewrites += 1

            # 7. Repetitive sentence openers
            words = current.split()
            opener = " ".join(words[:2]).lower() if len(words) >= 2 else current.lower()
            if opener and opener == previous_opener and opener in (
                "selain itu",
                "produk ini",
                "dengan fitur",
                "tidak hanya",
            ):
                alt_map = {
                    "selain itu": "Bagian praktisnya,",
                    "produk ini": "Barang ini",
                    "dengan fitur": "Lewat fitur",
                    "tidak hanya": "Bukan cuma itu,",
                }
                rest = " ".join(words[2:])
                new_sent = f"{alt_map[opener]} {rest}".strip()
                issues.append(
                    LanguageIssue(
                        loc,
                        "repetitive_sentence_pattern",
                        current,
                        new_sent,
                        f"Menghindari pengulangan pembuka kalimat '{opener}'.",
                    )
                )
                current = new_sent
                rewrites += 1
            previous_opener = " ".join(current.split()[:2]).lower()

            current = re.sub(r"\s+", " ", current).strip()
            if current and current[-1] not in ".!?":
                current += "."
            refined_sentences.append(current)

        return RefinementResult(
            original_text=text,
            refined_text=" ".join(refined_sentences),
            issues=issues,
            rewrites_applied=rewrites,
        )

    def audit_script_fields(
        self,
        *,
        hooks: list[str],
        scene_narrations: list[str],
        cta: str,
        caption: str,
        register: str = "casual_everyday",
        available_evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        """Run contextual refinement across all affiliate script fields."""
        all_issues: list[LanguageIssue] = []
        total_rewrites = 0

        refined_hooks: list[str] = []
        for idx, hook in enumerate(hooks):
            res = self.refine_text(
                hook,
                location=f"hook_{idx + 1}",
                register=register,
                available_evidence=available_evidence,
            )
            refined_hooks.append(res.refined_text)
            all_issues.extend(res.issues)
            total_rewrites += res.rewrites_applied

        refined_scenes: list[str] = []
        for idx, narr in enumerate(scene_narrations):
            res = self.refine_text(
                narr,
                location=f"scene_{idx + 1}",
                register=register,
                available_evidence=available_evidence,
            )
            refined_scenes.append(res.refined_text)
            all_issues.extend(res.issues)
            total_rewrites += res.rewrites_applied

        cta_res = self.refine_text(
            cta, location="cta", register=register, available_evidence=available_evidence
        )
        cap_res = self.refine_text(
            caption, location="caption", register=register, available_evidence=available_evidence
        )
        all_issues.extend(cta_res.issues)
        all_issues.extend(cap_res.issues)
        total_rewrites += cta_res.rewrites_applied + cap_res.rewrites_applied

        return {
            "hooks": refined_hooks,
            "scene_narrations": refined_scenes,
            "cta": cta_res.refined_text,
            "caption": cap_res.refined_text,
            "rewrites_applied": total_rewrites,
            "issues": [
                {
                    "location": i.location,
                    "issue_type": i.issue_type,
                    "original": i.original_sentence,
                    "suggestion": i.suggestion,
                    "reason": i.reason,
                }
                for i in all_issues
            ],
        }
