"""Knowledge repository managing structured JSON concepts, Markdown notes, index, and history."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from hce.knowledge.synthesizer import KnowledgeSynthesizer
from hce.models import ConceptRecord, utc_now_iso
from hce.storage.db import Database


def _concept_to_markdown(concept: ConceptRecord) -> str:
    lines = [
        f"# {concept.concept_name}",
        "",
        f"- **Concept ID:** `{concept.concept_id}`",
        f"- **Category:** `{concept.category}`",
        f"- **Statement Type:** `{concept.statement_type}`",
        f"- **Validation Status:** `{concept.validation_status}`",
        f"- **Confidence:** {concept.extraction_confidence:.2f}",
        f"- **Source:** `{concept.source_id}` @ `{concept.source_timestamp}`",
        "",
        "## Explanation",
        concept.explanation,
        "",
        "## Underlying Psychology",
        concept.underlying_psychology,
        "",
        "## Application Conditions",
        *(f"- {item}" for item in (concept.application_conditions or ["(none specified)"])),
        "",
        "## Implementation",
        *(f"- {item}" for item in (concept.implementation or ["(none specified)"])),
        "",
        "## Examples",
        *(f"- {item}" for item in (concept.examples or ["(none specified)"])),
        "",
        "## Counterexamples",
        *(f"- {item}" for item in (concept.counterexamples or ["(none specified)"])),
        "",
        "## Limitations",
        *(f"- {item}" for item in (concept.limitations or ["(none specified)"])),
    ]
    if concept.competing_viewpoints:
        lines.extend(["", "## Competing or Contextual Viewpoints"])
        for vp in concept.competing_viewpoints:
            lines.append(
                f"- [{vp.get('source_id', '?')} @ {vp.get('source_timestamp', '?')}] "
                f"({vp.get('conflict_note', 'note')}): {vp.get('viewpoint', '')}"
            )
    if concept.related_concepts:
        lines.extend(["", "## Related Concepts", ", ".join(f"`{r}`" for r in concept.related_concepts)])
    lines.append("")
    return "\n".join(lines)


class KnowledgeRepository:
    """Stores, indexes, and tracks provenance of seed and extracted HCE concepts."""

    def __init__(self, knowledge_dir: Path, db: Database) -> None:
        self.knowledge_dir = Path(knowledge_dir)
        self.db = db
        self.synthesizer = KnowledgeSynthesizer()

    @property
    def index_path(self) -> Path:
        return self.knowledge_dir / "index.json"

    @property
    def extracted_dir(self) -> Path:
        return self.knowledge_dir / "extracted"

    @property
    def history_log_path(self) -> Path:
        return self.knowledge_dir / "history" / "learning_history.jsonl"

    def iter_concept_files(self) -> list[Path]:
        files: list[Path] = []
        modules_dir = self.knowledge_dir / "modules"
        if modules_dir.exists():
            files.extend(sorted(modules_dir.glob("*/concepts/*.json")))
        if self.extracted_dir.exists():
            files.extend(sorted(self.extracted_dir.glob("*.json")))
        return files

    def load_all_concepts(self, category: str | None = None) -> list[ConceptRecord]:
        concepts_by_id: dict[str, ConceptRecord] = {}
        for path in self.iter_concept_files():
            data = json.loads(path.read_text(encoding="utf-8"))
            concept = ConceptRecord.from_dict(data)
            if category and concept.category != category:
                continue
            # Extracted/updated version overrides initial seed metadata when same ID was enriched
            concepts_by_id[concept.concept_id] = concept
        return list(concepts_by_id.values())

    def _concept_file_map(self) -> dict[str, Path]:
        mapping: dict[str, Path] = {}
        for path in self.iter_concept_files():
            data = json.loads(path.read_text(encoding="utf-8"))
            mapping[str(data["concept_id"])] = path
        return mapping

    def load_concept_by_id(self, concept_id: str) -> ConceptRecord | None:
        file_map = self._concept_file_map()
        path = file_map.get(concept_id)
        if not path or not path.exists():
            return None
        return ConceptRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def sync_seed_modules(self) -> int:
        """Ensure all module and extracted JSON concepts are registered in SQLite and index.json."""
        self.db.ensure_initialized()
        count = 0
        for path in self.iter_concept_files():
            concept = ConceptRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))
            content_hash = self.synthesizer.compute_content_hash(concept)
            existing_hash_row = self.db.get_knowledge_by_content_hash(content_hash)
            if existing_hash_row and existing_hash_row["concept_id"] != concept.concept_id:
                continue
            self.db.upsert_knowledge_item(concept, path, content_hash)
            count += 1
        self.rebuild_index()
        return count

    def save_concept(
        self,
        concept: ConceptRecord,
        *,
        action: str = "create",
        previous_summary: str | None = None,
        notes: str = "",
        rebuild: bool = True,
    ) -> Path:
        """Persist concept JSON + Markdown note and record provenance in SQLite & learning_history."""
        self.db.ensure_initialized()
        self.extracted_dir.mkdir(parents=True, exist_ok=True)
        self.history_log_path.parent.mkdir(parents=True, exist_ok=True)

        safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", concept.concept_id)
        json_path = self.extracted_dir / f"{safe_id}.json"
        md_path = self.extracted_dir / f"{safe_id}.md"

        json_path.write_text(
            json.dumps(concept.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        md_path.write_text(_concept_to_markdown(concept), encoding="utf-8")

        content_hash = self.synthesizer.compute_content_hash(concept)
        self.db.upsert_knowledge_item(concept, json_path, content_hash)
        new_summary = f"{concept.concept_name} ({concept.validation_status})"
        self.db.append_knowledge_history(
            concept_id=concept.concept_id,
            action=action,
            source_id=concept.source_id,
            previous_summary=previous_summary,
            new_summary=new_summary,
            notes=notes,
        )

        history_entry = {
            "timestamp": utc_now_iso(),
            "concept_id": concept.concept_id,
            "action": action,
            "source_id": concept.source_id,
            "source_timestamp": concept.source_timestamp,
            "validation_status": concept.validation_status,
            "notes": notes,
        }
        with self.history_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(history_entry, ensure_ascii=False) + "\n")

        if rebuild:
            self.rebuild_index()
        return json_path

    def rebuild_index(self) -> Path:
        """Generate `knowledge/index.json` for fast selective retrieval without loading all full payloads."""
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        file_map = self._concept_file_map()
        concepts = self.load_all_concepts()

        entries: dict[str, dict[str, Any]] = {}
        by_category: dict[str, list[str]] = {}
        by_source: dict[str, list[str]] = {}
        keyword_index: dict[str, list[str]] = {}

        for concept in concepts:
            path = file_map.get(concept.concept_id)
            rel_path = (
                str(path.relative_to(self.knowledge_dir))
                if path and path.is_relative_to(self.knowledge_dir)
                else str(path or "")
            )
            searchable_text = " ".join(
                [
                    concept.concept_id,
                    concept.concept_name,
                    concept.category,
                    concept.explanation,
                    concept.underlying_psychology,
                    " ".join(concept.application_conditions),
                    " ".join(concept.implementation),
                ]
            )
            tokens = sorted(
                {
                    tok
                    for tok in re.findall(r"[a-zA-Z0-9_]+", searchable_text.lower())
                    if len(tok) > 2
                }
            )
            entries[concept.concept_id] = {
                "concept_id": concept.concept_id,
                "concept_name": concept.concept_name,
                "category": concept.category,
                "source_id": concept.source_id,
                "source_timestamp": concept.source_timestamp,
                "statement_type": concept.statement_type,
                "extraction_confidence": concept.extraction_confidence,
                "validation_status": concept.validation_status,
                "related_concepts": concept.related_concepts,
                "file_path": rel_path.replace("\\", "/"),
                "summary": concept.explanation[:220],
                "tokens": tokens,
            }
            by_category.setdefault(concept.category, []).append(concept.concept_id)
            by_source.setdefault(concept.source_id, []).append(concept.concept_id)
            for ref in concept.provenance_refs:
                sid = ref.get("source_id")
                if sid and concept.concept_id not in by_source.get(sid, []):
                    by_source.setdefault(sid, []).append(concept.concept_id)
            for tok in tokens:
                keyword_index.setdefault(tok, []).append(concept.concept_id)

        payload = {
            "updated_at": utc_now_iso(),
            "total_concepts": len(entries),
            "concepts": entries,
            "by_category": by_category,
            "by_source": by_source,
            "keyword_index": keyword_index,
        }
        self.index_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return self.index_path
