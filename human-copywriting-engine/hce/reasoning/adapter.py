"""Provider-independent reasoning adapter interface for HCE knowledge extraction."""

from __future__ import annotations

import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from hce.config import ReasoningConfig
from hce.knowledge.synthesizer import KnowledgeSynthesizer, SynthesisDecision
from hce.knowledge.validator import KnowledgeValidator
from hce.models import ConceptRecord, ExtractionResult, LearningTask, ValidationResult


class ReasoningAdapter(ABC):
    """Contract separating transcription from conceptual copywriting reasoning."""

    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True only when an actual reasoning mechanism is ready to process tasks."""
        ...

    @abstractmethod
    def extract_knowledge(
        self,
        task: LearningTask,
        existing_concepts: list[ConceptRecord],
    ) -> ExtractionResult | None:
        """Process a LearningTask and return extracted concepts, or None if still pending."""
        ...

    def compare_and_synthesize(
        self,
        new_concept: ConceptRecord,
        existing_concepts: list[ConceptRecord],
    ) -> SynthesisDecision:
        """Default local cross-source comparison delegating to KnowledgeSynthesizer."""
        return KnowledgeSynthesizer().synthesize(new_concept, existing_concepts)

    def validate_concept(self, concept: ConceptRecord) -> ValidationResult:
        """Default schema + epistemic validation delegating to KnowledgeValidator."""
        return KnowledgeValidator().validate(concept)


class QueuedOnlyAdapter(ReasoningAdapter):
    """Default safe adapter when no AI provider is configured; leaves tasks queued honestly."""

    name = "none"

    def is_configured(self) -> bool:
        return False

    def extract_knowledge(
        self,
        task: LearningTask,
        existing_concepts: list[ConceptRecord],
    ) -> ExtractionResult | None:
        return None


class FileExchangeAdapter(ReasoningAdapter):
    """Consumes structured ExtractionResult JSON written by a custom agent in `results/<task_id>.json`."""

    name = "file_exchange"

    def __init__(self, results_dir: Path) -> None:
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def is_configured(self) -> bool:
        return True

    def result_file_for(self, task_id: str) -> Path:
        return self.results_dir / f"{task_id}.json"

    def extract_knowledge(
        self,
        task: LearningTask,
        existing_concepts: list[ConceptRecord],
    ) -> ExtractionResult | None:
        result_file = self.result_file_for(task.task_id)
        if not result_file.exists():
            # Task has not been answered by the custom agent yet; keep it queued cleanly.
            return None
        raw = json.loads(result_file.read_text(encoding="utf-8"))
        raw.setdefault("task_id", task.task_id)
        raw.setdefault("source_id", task.source_id)
        raw.setdefault("adapter_name", self.name)
        return ExtractionResult.from_dict(raw)


class CommandAdapter(ReasoningAdapter):
    """Pipes a LearningTask JSON payload to a configured local CLI command via stdin/stdout."""

    name = "command"

    def __init__(self, command: list[str], timeout_seconds: int = 120) -> None:
        self.command = list(command)
        self.timeout_seconds = timeout_seconds

    def is_configured(self) -> bool:
        return bool(self.command)

    def extract_knowledge(
        self,
        task: LearningTask,
        existing_concepts: list[ConceptRecord],
    ) -> ExtractionResult | None:
        if not self.command:
            return None

        payload = {
            "task": task.to_dict(),
            "existing_concept_summaries": [
                {
                    "concept_id": c.concept_id,
                    "concept_name": c.concept_name,
                    "category": c.category,
                    "explanation": c.explanation,
                    "validation_status": c.validation_status,
                }
                for c in existing_concepts
            ],
        }
        proc = subprocess.run(
            self.command,
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout_seconds,
        )
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or f"exit code {proc.returncode}").strip()
            raise RuntimeError(f"Reasoning command failed for task {task.task_id}: {err}")

        raw = json.loads(proc.stdout)
        raw.setdefault("task_id", task.task_id)
        raw.setdefault("source_id", task.source_id)
        raw.setdefault("adapter_name", self.name)
        return ExtractionResult.from_dict(raw)


def create_reasoning_adapter(config: ReasoningConfig, processed_dir: Path) -> ReasoningAdapter:
    """Instantiate the configured reasoning adapter without hardcoding any cloud AI endpoint."""
    if config.adapter == "none":
        return QueuedOnlyAdapter()
    if config.adapter == "file_exchange":
        return FileExchangeAdapter(processed_dir / "results")
    if config.adapter == "command":
        return CommandAdapter(config.command, timeout_seconds=config.timeout_seconds)
    raise ValueError(f"Unsupported reasoning adapter: {config.adapter!r}")
