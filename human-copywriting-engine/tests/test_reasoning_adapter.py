"""Tests for provider-independent reasoning adapters (none, file_exchange, command)."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from hce.config import HCEConfig
from hce.ingestion.pipeline import VideoLearningPipeline
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.models import ConceptRecord, ExtractionResult, LearningTask
from hce.reasoning.adapter import (
    CommandAdapter,
    FileExchangeAdapter,
    QueuedOnlyAdapter,
)
from hce.storage.db import Database


def _seed_env(tmp_path: Path) -> tuple[HCEConfig, Database, KnowledgeRepository, LocalKeywordRetriever]:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    cfg = HCEConfig.load(root_dir=tmp_path)
    cfg.ensure_directories()
    db = Database(cfg.storage.db_path)
    db.init_schema()
    repo = KnowledgeRepository(cfg.storage.knowledge_dir, db)
    repo.sync_seed_modules()
    return cfg, db, repo, LocalKeywordRetriever(repo)


def test_queued_only_adapter_not_configured() -> None:
    adapter = QueuedOnlyAdapter()
    assert not adapter.is_configured()


def test_file_exchange_adapter_processes_agent_result_with_provenance(tmp_path: Path) -> None:
    cfg, db, repo, retriever = _seed_env(tmp_path)

    from hce.models import SourceRecord

    db.upsert_source(
        SourceRecord(
            source_id="src_vid99",
            file_path=str(tmp_path / "vid99.mp4"),
            file_name="vid99.mp4",
            file_hash="9" * 64,
            file_size=5000,
            duration_seconds=90.0,
            status="transcribed_pending_reasoning",
        )
    )
    task = LearningTask(
        task_id="task_vid99_t0",
        source_id="src_vid99",
        source_file_name="vid99.mp4",
        topic_id="vid99_t0",
        title_hint="Hook awal berbasis keluhan nyata",
        language="id",
        start_seconds=12.0,
        end_seconds=55.0,
        source_timestamp="00:00:12-00:00:55",
        transcript_excerpt="Pembukaan paling cepat menarik perhatian adalah menunjukkan masalah nyata sebelum menyebut merek.",
    )
    task_path = cfg.storage.tasks_dir / f"{task.task_id}.json"
    task_path.write_text(json.dumps(task.to_dict(), ensure_ascii=False), encoding="utf-8")
    db.upsert_learning_task(task, task_path, status="queued")

    adapter = FileExchangeAdapter(cfg.storage.results_dir)
    pipeline = VideoLearningPipeline(
        cfg, db, retriever, repo, reasoning_adapter=adapter
    )

    # First run before agent writes result -> task remains queued cleanly
    pre = pipeline.run()
    assert pre.tasks_completed == 0
    assert db.get_source("src_vid99").status == "transcribed_pending_reasoning"

    # Now agent writes structured ExtractionResult JSON
    concept = ConceptRecord(
        concept_id="pw-problem-first-opening",
        concept_name="Pembukaan Masalah Nyata Sebelum Merek",
        category="persuasive_writing",
        explanation="Menunjukkan kondisi masalah yang akrab di awal video sebelum menyebut nama produk meningkatkan relevansi awal.",
        underlying_psychology="Penonton mengidentifikasi masalah pribadinya lebih cepat dibanding mengenali merek asing.",
        application_conditions=["Video short-form untuk audiens problem-aware"],
        implementation=["Visualkan masalah pada 2 detik pertama sebelum menampilkan nama produk"],
        examples=["Rak penuh di lantai kamar mandi sebelum menunjukkan rak tempel"],
        counterexamples=["Menyebut merek dan spesifikasi lengkap di detik pertama tanpa konteks"],
        limitations=["Untuk audiens yang sudah mencari produk spesifik, demo langsung bisa lebih cepat"],
        related_concepts=["pw-product-grounded-hooks"],
        source_id="src_vid99",
        source_timestamp="00:00:12-00:00:55",
        extraction_confidence=0.88,
        validation_status="validated",
        statement_type="direct_instructor_statement",
    )
    result_obj = ExtractionResult(
        task_id=task.task_id,
        source_id="src_vid99",
        adapter_name="file_exchange",
        concepts=[concept],
    )
    adapter.result_file_for(task.task_id).write_text(
        json.dumps(result_obj.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    post = pipeline.run()
    assert post.tasks_completed == 1
    assert post.concepts_stored == 1
    assert db.get_source("src_vid99").status == "completed"
    assert (cfg.storage.knowledge_dir / "extracted" / "pw-problem-first-opening.json").exists()
    assert (cfg.storage.knowledge_dir / "extracted" / "pw-problem-first-opening.md").exists()

    by_source = retriever.get_by_source("src_vid99")
    assert len(by_source) == 1
    assert by_source[0].source_timestamp == "00:00:12-00:00:55"


def test_command_adapter_subprocess_roundtrip(tmp_path: Path) -> None:
    helper = tmp_path / "dummy_reasoner.py"
    helper.write_text(
        """import json, sys
payload = json.loads(sys.stdin.read())
task = payload["task"]
out = {
    "task_id": task["task_id"],
    "source_id": task["source_id"],
    "adapter_name": "command",
    "concepts": [{
        "concept_id": "hl-cmd-extracted",
        "concept_name": "Kejelasan Kalimat Lisan",
        "category": "human_language",
        "explanation": "Gunakan kalimat pendek dan lugas agar nyaman didengar di video pendek.",
        "underlying_psychology": "Mengurangi beban kognitif pendengar saat menyimak sambil scroll.",
        "application_conditions": ["Semua skrip voice-over"],
        "implementation": ["Batasi satu gagasan per kalimat"],
        "examples": ["Pas buat bumbu harian."],
        "counterexamples": [],
        "limitations": [],
        "related_concepts": [],
        "source_id": task["source_id"],
        "source_timestamp": task["source_timestamp"],
        "extraction_confidence": 0.85,
        "validation_status": "validated",
        "statement_type": "practical_demonstration"
    }]
}
print(json.dumps(out))
""",
        encoding="utf-8",
    )
    adapter = CommandAdapter([sys.executable, str(helper)])
    task = LearningTask(
        task_id="t_cmd",
        source_id="src_cmd",
        source_file_name="cmd.mp4",
        topic_id="t0",
        title_hint="Test",
        language="id",
        start_seconds=0.0,
        end_seconds=10.0,
        source_timestamp="00:00:00-00:00:10",
        transcript_excerpt="Kalimat pendek lebih mudah diikuti penonton.",
    )
    res = adapter.extract_knowledge(task, [])
    assert res is not None
    assert len(res.concepts) == 1
    assert res.concepts[0].concept_id == "hl-cmd-extracted"
