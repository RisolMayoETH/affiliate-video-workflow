"""Cross-source synthesis, duplicate prevention, and competing-viewpoint preservation."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from hce.models import ConceptRecord


@dataclass
class SynthesisDecision:
    action: str  # "create", "duplicate", "merge_or_compare"
    target_concept: ConceptRecord | None = None
    merged_concept: ConceptRecord | None = None
    conflicts_detected: list[str] = field(default_factory=list)
    notes: str = ""


def _tokenize(text: str) -> set[str]:
    return {
        tok
        for tok in re.findall(r"[a-zA-Z0-9_]+", text.lower())
        if len(tok) > 2
    }


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _merge_unique_str(existing: list[str], additions: list[str]) -> list[str]:
    seen = {item.strip().lower(): item for item in existing}
    result = list(existing)
    for item in additions:
        key = item.strip().lower()
        if key and key not in seen:
            seen[key] = item
            result.append(item)
    return result


class KnowledgeSynthesizer:
    """Compares incoming concepts against existing knowledge without overwriting validated history."""

    def compute_content_hash(self, concept: ConceptRecord) -> str:
        canonical = "|".join(
            [
                concept.category.strip().lower(),
                re.sub(r"\s+", " ", concept.concept_name.strip().lower()),
                re.sub(r"\s+", " ", concept.explanation.strip().lower()),
                re.sub(r"\s+", " ", concept.underlying_psychology.strip().lower()),
            ]
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _has_opposing_guidance(self, a: ConceptRecord, b: ConceptRecord) -> str | None:
        text_a = f"{a.explanation} {' '.join(a.implementation)}".lower()
        text_b = f"{b.explanation} {' '.join(b.implementation)}".lower()
        opposition_pairs = [
            ("selalu", "hindari"),
            ("wajib", "jangan"),
            ("cerita panjang", "langsung"),
            ("storytelling", "penjelasan langsung"),
            ("slang", "formal"),
            ("always", "never"),
            ("avoid", "use"),
        ]
        for left, right in opposition_pairs:
            if (left in text_a and right in text_b) or (right in text_a and left in text_b):
                return f"Contrasting emphasis detected ({left!r} vs {right!r})"
        return None

    def synthesize(
        self,
        incoming: ConceptRecord,
        existing_concepts: list[ConceptRecord],
    ) -> SynthesisDecision:
        incoming_hash = self.compute_content_hash(incoming)

        best_match: ConceptRecord | None = None
        best_score = 0.0

        incoming_name_tokens = _tokenize(incoming.concept_name)
        incoming_body_tokens = _tokenize(
            f"{incoming.concept_name} {incoming.explanation} {incoming.underlying_psychology}"
        )

        for existing in existing_concepts:
            if self.compute_content_hash(existing) == incoming_hash:
                return SynthesisDecision(
                    action="duplicate",
                    target_concept=existing,
                    notes=f"Exact canonical match with existing concept {existing.concept_id}.",
                )

            if (
                existing.concept_id == incoming.concept_id
                and existing.source_id == incoming.source_id
                and existing.source_timestamp == incoming.source_timestamp
            ):
                return SynthesisDecision(
                    action="duplicate",
                    target_concept=existing,
                    notes=f"Duplicate provenance extraction for {existing.concept_id}.",
                )

            name_sim = _jaccard(incoming_name_tokens, _tokenize(existing.concept_name))
            body_sim = _jaccard(
                incoming_body_tokens,
                _tokenize(
                    f"{existing.concept_name} {existing.explanation} {existing.underlying_psychology}"
                ),
            )
            combined = 0.55 * name_sim + 0.45 * body_sim
            if existing.category == incoming.category and combined > best_score:
                best_score = combined
                best_match = existing

        if best_match is not None and (best_score >= 0.45 or incoming.concept_id == best_match.concept_id):
            conflicts: list[str] = []
            conflict = self._has_opposing_guidance(best_match, incoming)
            if conflict:
                conflicts.append(conflict)

            # Never silently overwrite validated explanation; preserve competing viewpoints
            merged_provenance = list(best_match.provenance_refs)
            if not merged_provenance:
                merged_provenance.append(
                    {
                        "source_id": best_match.source_id,
                        "source_timestamp": best_match.source_timestamp,
                        "statement_type": best_match.statement_type,
                    }
                )
            new_ref = {
                "source_id": incoming.source_id,
                "source_timestamp": incoming.source_timestamp,
                "statement_type": incoming.statement_type,
                "concept_name": incoming.concept_name,
            }
            if new_ref not in merged_provenance:
                merged_provenance.append(new_ref)

            competing = list(best_match.competing_viewpoints)
            if conflict or incoming.explanation.strip() != best_match.explanation.strip():
                competing.append(
                    {
                        "source_id": incoming.source_id,
                        "source_timestamp": incoming.source_timestamp,
                        "statement_type": incoming.statement_type,
                        "viewpoint": incoming.explanation,
                        "conditions": incoming.application_conditions,
                        "conflict_note": conflict or "Contextual refinement / alternative emphasis",
                    }
                )

            validation_status = best_match.validation_status
            if conflicts and validation_status == "validated":
                validation_status = "contested"

            merged = ConceptRecord(
                concept_id=best_match.concept_id,
                concept_name=best_match.concept_name,
                category=best_match.category,
                explanation=best_match.explanation,
                underlying_psychology=best_match.underlying_psychology,
                application_conditions=_merge_unique_str(
                    best_match.application_conditions, incoming.application_conditions
                ),
                implementation=_merge_unique_str(
                    best_match.implementation, incoming.implementation
                ),
                examples=_merge_unique_str(best_match.examples, incoming.examples),
                counterexamples=_merge_unique_str(
                    best_match.counterexamples, incoming.counterexamples
                ),
                limitations=_merge_unique_str(
                    best_match.limitations, incoming.limitations
                ),
                related_concepts=_merge_unique_str(
                    best_match.related_concepts, incoming.related_concepts
                ),
                source_id=best_match.source_id,
                source_timestamp=best_match.source_timestamp,
                extraction_confidence=max(
                    best_match.extraction_confidence, incoming.extraction_confidence
                ),
                validation_status=validation_status,
                statement_type=best_match.statement_type,
                competing_viewpoints=competing,
                provenance_refs=merged_provenance,
            )
            return SynthesisDecision(
                action="merge_or_compare",
                target_concept=best_match,
                merged_concept=merged,
                conflicts_detected=conflicts,
                notes=(
                    f"Merged/compared with {best_match.concept_id} (similarity={best_score:.2f}); "
                    f"preserved original core explanation and logged provenance from {incoming.source_id}."
                ),
            )

        return SynthesisDecision(
            action="create",
            merged_concept=incoming,
            notes="New distinct concept.",
        )
