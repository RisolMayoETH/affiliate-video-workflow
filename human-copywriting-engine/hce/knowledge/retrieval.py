"""Dynamic knowledge retrieval interface and local keyword implementation."""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hce.knowledge.repository import KnowledgeRepository
from hce.models import ConceptRecord

# Bilingual Indonesian <-> English keyword bridges for cross-language copywriting queries
BILINGUAL_SYNONYMS: dict[str, tuple[str, ...]] = {
    "buyer": ("pembeli", "konsumen", "calon", "keputusan", "ragu"),
    "pembeli": ("buyer", "konsumen", "hesitation", "trust"),
    "psychology": ("psikologi", "emosional", "rasional", "keraguan", "kepercayaan"),
    "psikologi": ("psychology", "emotional", "rational", "trust"),
    "hook": ("pembuka", "scroll", "detik", "perhatian"),
    "storytelling": ("cerita", "narasi", "momen", "alur", "adegan"),
    "cerita": ("storytelling", "narrative", "moment"),
    "natural": ("alami", "lisan", "sehari", "mengalir", "wajar"),
    "alami": ("natural", "spoken", "conversational"),
    "trust": ("kepercayaan", "kejujuran", "bukti", "autentik"),
    "kepercayaan": ("trust", "authenticity", "honest"),
    "objection": ("keberatan", "ragu", "keraguan", "khawatir"),
    "keberatan": ("objection", "hesitation", "risk"),
    "persuasive": ("persuasif", "manfaat", "fitur", "argumen", "cta"),
    "persuasif": ("persuasive", "benefit", "value", "cta"),
    "audience": ("audiens", "segmen", "platform", "register", "pembeli"),
    "audiens": ("audience", "segment", "platform", "register"),
    "evaluation": ("evaluasi", "rubrik", "integritas", "akurasi", "repetisi"),
    "evaluasi": ("evaluation", "rubric", "integrity", "accuracy"),
    "cta": ("ajakan", "keranjang", "tautan", "checkout"),
    "tiktok": ("platform", "keranjang", "pendek"),
    "shopee": ("platform", "keranjang", "video", "fungsi"),
}


@dataclass
class RetrievalHit:
    concept: ConceptRecord
    score: float
    matched_terms: list[str]


class KnowledgeRetriever(ABC):
    """Provider-independent knowledge retrieval abstraction (extensible to semantic search)."""

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        category: str | None = None,
        min_confidence: float = 0.0,
        validation_statuses: tuple[str, ...] | None = None,
        limit: int = 5,
    ) -> list[RetrievalHit]:
        ...

    @abstractmethod
    def get_related(self, concept_id: str, limit: int = 5) -> list[ConceptRecord]:
        ...

    @abstractmethod
    def get_by_source(self, source_id: str) -> list[ConceptRecord]:
        ...

    @abstractmethod
    def get_examples(
        self,
        query: str,
        *,
        category: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        ...

    def format_context(self, hits: list[RetrievalHit]) -> str:
        """Render concise retrieved principles suitable for downstream prompts/reasoning."""
        if not hits:
            return "(no matching knowledge concepts retrieved)"
        lines: list[str] = []
        for hit in hits:
            c = hit.concept
            impl = "; ".join(c.implementation[:2]) if c.implementation else ""
            lines.append(
                f"- [{c.concept_id} | {c.category} | {c.validation_status} | conf={c.extraction_confidence:.2f}] "
                f"{c.concept_name}: {c.explanation}"
                + (f" Impl: {impl}" if impl else "")
            )
        return "\n".join(lines)


class LocalKeywordRetriever(KnowledgeRetriever):
    """Selective index-backed keyword & category retriever (does not load full library eagerly)."""

    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def _load_index(self) -> dict[str, Any]:
        if not self.repository.index_path.exists():
            self.repository.rebuild_index()
        return json.loads(self.repository.index_path.read_text(encoding="utf-8"))

    def _load_concept_from_index_entry(self, entry: dict[str, Any]) -> ConceptRecord | None:
        rel_path = entry.get("file_path", "")
        if not rel_path:
            return self.repository.load_concept_by_id(entry["concept_id"])
        full_path = Path(rel_path)
        if not full_path.is_absolute():
            full_path = self.repository.knowledge_dir / rel_path
        if not full_path.exists():
            return self.repository.load_concept_by_id(entry["concept_id"])
        return ConceptRecord.from_dict(json.loads(full_path.read_text(encoding="utf-8")))

    def _expand_query_terms(self, query: str) -> tuple[list[str], list[str]]:
        base_terms = [
            tok for tok in re.findall(r"[a-zA-Z0-9_]+", query.lower()) if len(tok) > 1
        ]
        expanded: list[str] = []
        for term in base_terms:
            for syn in BILINGUAL_SYNONYMS.get(term, ()):
                if syn not in base_terms and syn not in expanded:
                    expanded.append(syn)
        return base_terms, expanded

    def search(
        self,
        query: str,
        *,
        category: str | None = None,
        min_confidence: float = 0.0,
        validation_statuses: tuple[str, ...] | None = None,
        limit: int = 5,
    ) -> list[RetrievalHit]:
        index = self._load_index()
        entries: dict[str, dict[str, Any]] = index.get("concepts", {})
        base_terms, expanded_terms = self._expand_query_terms(query)
        query_lower = query.strip().lower()

        scored: list[tuple[float, list[str], dict[str, Any]]] = []
        for concept_id, entry in entries.items():
            if category and entry.get("category") != category:
                continue
            conf = float(entry.get("extraction_confidence", 0.0))
            if conf < min_confidence:
                continue
            status = entry.get("validation_status", "pending")
            if validation_statuses and status not in validation_statuses:
                continue

            name_lower = str(entry.get("concept_name", "")).lower()
            cat_lower = str(entry.get("category", "")).lower().replace("_", " ")
            summary_lower = str(entry.get("summary", "")).lower()
            token_set = set(entry.get("tokens", []))

            score = 0.0
            matched: list[str] = []

            if query_lower and (query_lower in name_lower or query_lower in cat_lower):
                score += 4.0
                matched.append(query_lower)

            for term in base_terms:
                if term in name_lower:
                    score += 2.5
                    matched.append(term)
                elif term in cat_lower:
                    score += 2.2
                    matched.append(term)
                elif term in token_set or term in summary_lower:
                    score += 1.4
                    matched.append(term)

            for syn in expanded_terms:
                if syn in name_lower:
                    score += 1.3
                    matched.append(f"~{syn}")
                elif syn in token_set or syn in summary_lower:
                    score += 0.8
                    matched.append(f"~{syn}")

            if score <= 0.0 and not base_terms and category:
                score = 1.0

            if score > 0.0:
                if status == "validated":
                    score += 0.25
                score += conf * 0.2
                dedup_matched = list(dict.fromkeys(matched))
                scored.append((score, dedup_matched, entry))

        scored.sort(key=lambda item: item[0], reverse=True)
        hits: list[RetrievalHit] = []
        for score, matched, entry in scored[:limit]:
            concept = self._load_concept_from_index_entry(entry)
            if concept is not None:
                hits.append(RetrievalHit(concept=concept, score=round(score, 3), matched_terms=matched))
        return hits

    def get_related(self, concept_id: str, limit: int = 5) -> list[ConceptRecord]:
        index = self._load_index()
        entry = index.get("concepts", {}).get(concept_id)
        if not entry:
            return []
        related_ids = list(entry.get("related_concepts", []))[:limit]
        results: list[ConceptRecord] = []
        for rid in related_ids:
            rel_entry = index.get("concepts", {}).get(rid)
            if rel_entry:
                concept = self._load_concept_from_index_entry(rel_entry)
                if concept:
                    results.append(concept)
        return results

    def get_by_source(self, source_id: str) -> list[ConceptRecord]:
        index = self._load_index()
        concept_ids = index.get("by_source", {}).get(source_id, [])
        results: list[ConceptRecord] = []
        for cid in concept_ids:
            entry = index.get("concepts", {}).get(cid)
            if entry:
                concept = self._load_concept_from_index_entry(entry)
                if concept:
                    results.append(concept)
        return results

    def get_examples(
        self,
        query: str,
        *,
        category: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        hits = self.search(query, category=category, limit=limit)
        examples: list[dict[str, Any]] = []
        for hit in hits:
            for ex in hit.concept.examples:
                examples.append(
                    {
                        "concept_id": hit.concept.concept_id,
                        "concept_name": hit.concept.concept_name,
                        "category": hit.concept.category,
                        "example": ex,
                    }
                )
                if len(examples) >= limit:
                    return examples
        return examples
