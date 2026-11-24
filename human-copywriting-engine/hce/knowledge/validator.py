"""Validation and epistemic guardrails for extracted copywriting concepts."""

from __future__ import annotations

from hce.models import (
    KNOWLEDGE_CATEGORIES,
    STATEMENT_TYPES,
    VALIDATION_STATUSES,
    ConceptRecord,
    ValidationResult,
)


class KnowledgeValidator:
    """Validates schema completeness, provenance, and epistemic status of ConceptRecord."""

    def validate(self, concept: ConceptRecord) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not concept.concept_id or len(concept.concept_id.strip()) < 3:
            errors.append("concept_id must be at least 3 characters.")
        if not concept.concept_name or len(concept.concept_name.strip()) < 3:
            errors.append("concept_name must be at least 3 characters.")
        if concept.category not in KNOWLEDGE_CATEGORIES:
            errors.append(
                f"Invalid category {concept.category!r}; expected one of {KNOWLEDGE_CATEGORIES}."
            )
        if not concept.explanation or len(concept.explanation.strip()) < 15:
            errors.append("explanation must be meaningful (>= 15 characters).")
        if not concept.underlying_psychology or len(concept.underlying_psychology.strip()) < 10:
            errors.append("underlying_psychology must be meaningful (>= 10 characters).")
        if not concept.source_id or not concept.source_id.strip():
            errors.append("source_id is required for provenance.")
        if not concept.source_timestamp or not concept.source_timestamp.strip():
            errors.append("source_timestamp is required for provenance.")
        if not (0.0 <= concept.extraction_confidence <= 1.0):
            errors.append("extraction_confidence must be between 0.0 and 1.0.")
        if concept.validation_status not in VALIDATION_STATUSES:
            errors.append(
                f"Invalid validation_status {concept.validation_status!r}; expected {VALIDATION_STATUSES}."
            )
        if concept.statement_type not in STATEMENT_TYPES:
            errors.append(
                f"Invalid statement_type {concept.statement_type!r}; expected {STATEMENT_TYPES}."
            )

        adjusted_status = concept.validation_status
        # Do not elevate subjective opinions or uncorroborated inferences into fully validated facts
        if concept.statement_type == "subjective_opinion" and concept.validation_status == "validated":
            warnings.append(
                "Subjective opinion cannot be auto-marked 'validated' without corroboration; kept as 'pending'."
            )
            adjusted_status = "pending"

        if concept.statement_type in ("inferred_explanation", "subjective_opinion") and not concept.limitations:
            warnings.append(
                f"Concept with statement_type={concept.statement_type!r} should list explicit limitations."
            )

        if not concept.implementation:
            warnings.append("implementation steps are empty; practical execution guidance is recommended.")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            adjusted_status=adjusted_status if not errors else "rejected",
        )
