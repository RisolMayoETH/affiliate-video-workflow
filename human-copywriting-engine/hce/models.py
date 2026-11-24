"""Core typed domain models for Human Copywriting Engine (HCE)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

KNOWLEDGE_CATEGORIES = (
    "human_language",
    "buyer_psychology",
    "persuasive_writing",
    "storytelling",
    "audience_adaptation",
    "creative_evaluation",
)

STATEMENT_TYPES = (
    "direct_instructor_statement",
    "inferred_explanation",
    "verified_fact",
    "subjective_opinion",
    "practical_demonstration",
)

VALIDATION_STATUSES = (
    "pending",
    "validated",
    "contested",
    "rejected",
)


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def format_timestamp(seconds: float) -> str:
    """Format seconds into HH:MM:SS."""
    total = max(0, int(round(seconds)))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


@dataclass
class SourceRecord:
    source_id: str
    file_path: str
    file_name: str
    file_hash: str
    file_size: int
    duration_seconds: float | None = None
    media_type: str = "video"
    status: str = "pending"
    error_message: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SourceRecord:
        return cls(**data)


@dataclass
class ProcessingJob:
    job_id: str
    source_id: str
    stage: str = "transcription"
    status: str = "pending"
    total_chunks: int = 0
    completed_chunks: int = 0
    started_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    finished_at: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ChunkRecord:
    chunk_id: str
    job_id: str
    source_id: str
    chunk_index: int
    start_seconds: float
    end_seconds: float
    status: str = "pending"
    transcript_json: str | None = None
    error_message: str | None = None
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TranscriptSegment:
    id: int
    start: float
    end: float
    text: str
    chunk_index: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TranscriptSegment:
        return cls(
            id=int(data["id"]),
            start=float(data["start"]),
            end=float(data["end"]),
            text=str(data["text"]).strip(),
            chunk_index=int(data.get("chunk_index", 0)),
        )


@dataclass
class TranscriptDocument:
    source_id: str
    file_name: str
    language: str
    duration_seconds: float
    model_size: str
    segments: list[TranscriptSegment]
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "file_name": self.file_name,
            "language": self.language,
            "duration_seconds": self.duration_seconds,
            "model_size": self.model_size,
            "created_at": self.created_at,
            "segments": [seg.to_dict() for seg in self.segments],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TranscriptDocument:
        return cls(
            source_id=str(data["source_id"]),
            file_name=str(data["file_name"]),
            language=str(data.get("language", "unknown")),
            duration_seconds=float(data.get("duration_seconds", 0.0)),
            model_size=str(data.get("model_size", "unknown")),
            created_at=str(data.get("created_at", utc_now_iso())),
            segments=[TranscriptSegment.from_dict(s) for s in data.get("segments", [])],
        )


@dataclass
class TopicSegment:
    topic_id: str
    source_id: str
    topic_index: int
    title_hint: str
    start_seconds: float
    end_seconds: float
    text: str
    segment_indices: list[int] = field(default_factory=list)
    word_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TopicSegment:
        return cls(
            topic_id=str(data["topic_id"]),
            source_id=str(data["source_id"]),
            topic_index=int(data["topic_index"]),
            title_hint=str(data["title_hint"]),
            start_seconds=float(data["start_seconds"]),
            end_seconds=float(data["end_seconds"]),
            text=str(data["text"]),
            segment_indices=[int(i) for i in data.get("segment_indices", [])],
            word_count=int(data.get("word_count", 0)),
        )


@dataclass
class LearningTask:
    task_id: str
    source_id: str
    source_file_name: str
    topic_id: str
    title_hint: str
    language: str
    start_seconds: float
    end_seconds: float
    source_timestamp: str
    transcript_excerpt: str
    related_existing_concepts: list[dict[str, Any]] = field(default_factory=list)
    extraction_instructions: str = ""
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LearningTask:
        return cls(
            task_id=str(data["task_id"]),
            source_id=str(data["source_id"]),
            source_file_name=str(data.get("source_file_name", "")),
            topic_id=str(data["topic_id"]),
            title_hint=str(data.get("title_hint", "")),
            language=str(data.get("language", "id")),
            start_seconds=float(data.get("start_seconds", 0.0)),
            end_seconds=float(data.get("end_seconds", 0.0)),
            source_timestamp=str(data.get("source_timestamp", "00:00:00-00:00:00")),
            transcript_excerpt=str(data["transcript_excerpt"]),
            related_existing_concepts=list(data.get("related_existing_concepts", [])),
            extraction_instructions=str(data.get("extraction_instructions", "")),
            created_at=str(data.get("created_at", utc_now_iso())),
        )


@dataclass
class ConceptRecord:
    concept_id: str
    concept_name: str
    category: str
    explanation: str
    underlying_psychology: str
    application_conditions: list[str]
    implementation: list[str]
    examples: list[str]
    counterexamples: list[str]
    limitations: list[str]
    related_concepts: list[str]
    source_id: str
    source_timestamp: str
    extraction_confidence: float
    validation_status: str = "pending"
    statement_type: str = "direct_instructor_statement"
    competing_viewpoints: list[dict[str, Any]] = field(default_factory=list)
    provenance_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConceptRecord:
        return cls(
            concept_id=str(data["concept_id"]),
            concept_name=str(data["concept_name"]),
            category=str(data["category"]),
            explanation=str(data["explanation"]),
            underlying_psychology=str(data["underlying_psychology"]),
            application_conditions=[str(x) for x in data.get("application_conditions", [])],
            implementation=[str(x) for x in data.get("implementation", [])],
            examples=[str(x) for x in data.get("examples", [])],
            counterexamples=[str(x) for x in data.get("counterexamples", [])],
            limitations=[str(x) for x in data.get("limitations", [])],
            related_concepts=[str(x) for x in data.get("related_concepts", [])],
            source_id=str(data["source_id"]),
            source_timestamp=str(data["source_timestamp"]),
            extraction_confidence=float(data.get("extraction_confidence", 0.5)),
            validation_status=str(data.get("validation_status", "pending")),
            statement_type=str(data.get("statement_type", "direct_instructor_statement")),
            competing_viewpoints=list(data.get("competing_viewpoints", [])),
            provenance_refs=list(data.get("provenance_refs", [])),
        )


@dataclass
class ExtractionResult:
    task_id: str
    source_id: str
    adapter_name: str
    concepts: list[ConceptRecord] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "source_id": self.source_id,
            "adapter_name": self.adapter_name,
            "concepts": [c.to_dict() for c in self.concepts],
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExtractionResult:
        return cls(
            task_id=str(data["task_id"]),
            source_id=str(data["source_id"]),
            adapter_name=str(data.get("adapter_name", "external")),
            concepts=[ConceptRecord.from_dict(c) for c in data.get("concepts", [])],
            notes=str(data.get("notes", "")),
            created_at=str(data.get("created_at", utc_now_iso())),
        )


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    adjusted_status: str | None = None
