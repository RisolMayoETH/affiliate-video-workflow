"""Tests for topic segmentation, validation, cross-source synthesis, repository, and retrieval."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from hce.ingestion.segmenter import TopicSegmenter
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.knowledge.synthesizer import KnowledgeSynthesizer
from hce.knowledge.validator import KnowledgeValidator
from hce.models import ConceptRecord, TranscriptDocument, TranscriptSegment
from hce.storage.db import Database


def _setup_repo(tmp_path: Path) -> tuple[KnowledgeRepository, LocalKeywordRetriever, Database]:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    db = Database(tmp_path / "data" / "db" / "hce.sqlite3")
    db.init_schema()
    repo = KnowledgeRepository(tmp_path / "knowledge", db)
    repo.sync_seed_modules()
    retriever = LocalKeywordRetriever(repo)
    return repo, retriever, db


def test_topic_segmenter_preserves_timestamps() -> None:
    segs = [
        TranscriptSegment(0, 0.0, 5.0, " ".join(["kata"] * 70), 0),
        TranscriptSegment(1, 5.1, 10.0, " ".join(["materi"] * 70), 0),
        TranscriptSegment(2, 14.0, 20.0, "Selanjutnya kita bahas contoh kedua secara ringkas.", 0),
    ]
    doc = TranscriptDocument("src_1", "test.mp4", "id", 20.0, "base", segs)
    topics = TopicSegmenter(min_words=100, max_words=300, pause_threshold_seconds=2.5).segment(doc)
    assert len(topics) == 2
    assert topics[0].start_seconds == 0.0
    assert topics[1].start_seconds == 14.0


def test_validator_enforces_epistemic_guardrails() -> None:
    validator = KnowledgeValidator()

    bad = ConceptRecord(
        concept_id="x",
        concept_name="Bad",
        category="invalid_cat",
        explanation="short",
        underlying_psychology="short",
        application_conditions=[],
        implementation=[],
        examples=[],
        counterexamples=[],
        limitations=[],
        related_concepts=[],
        source_id="",
        source_timestamp="",
        extraction_confidence=1.5,
        validation_status="validated",
        statement_type="subjective_opinion",
    )
    res_bad = validator.validate(bad)
    assert not res_bad.valid
    assert len(res_bad.errors) >= 4

    opinion = ConceptRecord(
        concept_id="op-custom-hook",
        concept_name="Opini Hook Cepat",
        category="persuasive_writing",
        explanation="Menurut opini pembicara, hook berdurasi dua detik selalu lebih bagus dari tiga detik.",
        underlying_psychology="Perhatian pemirsa bergerak sangat cepat di layar ponsel.",
        application_conditions=["Video pendek"],
        implementation=["Buat kalimat pembuka singkat"],
        examples=["Contoh pembuka 4 kata"],
        counterexamples=[],
        limitations=[],
        related_concepts=[],
        source_id="src_demo",
        source_timestamp="00:01:00-00:02:00",
        extraction_confidence=0.7,
        validation_status="validated",
        statement_type="subjective_opinion",
    )
    res_op = validator.validate(opinion)
    assert res_op.valid
    assert res_op.adjusted_status == "pending"


def test_cross_source_synthesis_preserves_validated_and_conflicts(tmp_path: Path) -> None:
    repo, retriever, db = _setup_repo(tmp_path)
    existing = repo.load_all_concepts()

    # Conflicting / alternative viewpoint on direct vs story
    incoming = ConceptRecord(
        concept_id="st-direct-vs-story-alt",
        concept_name="Kapan Penjelasan Langsung Lebih Efektif dari Storytelling",
        category="storytelling",
        explanation="Selalu gunakan storytelling emosional panjang bahkan untuk produk dapur sederhana agar penonton terharu.",
        underlying_psychology="Cerita emosional selalu meningkatkan keterlibatan penonton.",
        application_conditions=["Produk dapur"],
        implementation=["Selalu mulai dengan cerita panjang sebelum demo"],
        examples=["Contoh cerita panjang sebelum chopper"],
        counterexamples=[],
        limitations=["Bisa terlalu lama jika audiens sudah siap beli"],
        related_concepts=["st-direct-vs-story"],
        source_id="src_video_2",
        source_timestamp="00:05:10-00:07:00",
        extraction_confidence=0.75,
        validation_status="pending",
        statement_type="direct_instructor_statement",
    )

    synth = KnowledgeSynthesizer()
    decision = synth.synthesize(incoming, existing)
    assert decision.action == "merge_or_compare"
    assert decision.conflicts_detected
    merged = decision.merged_concept
    assert merged is not None
    # Original explanation must NOT be silently overwritten
    assert "Tidak semua produk cocok dipaksakan" in merged.explanation
    assert merged.validation_status == "contested"
    assert len(merged.competing_viewpoints) >= 1

    repo.save_concept(merged, action=decision.action, notes=decision.notes)
    history = db.list_knowledge_history()
    assert any(h["concept_id"] == merged.concept_id for h in history)

    # Exact duplicate prevention check
    dup_decision = synth.synthesize(existing[0], existing)
    assert dup_decision.action == "duplicate"


def test_bilingual_retrieval_and_filtering(tmp_path: Path) -> None:
    _, retriever, _ = _setup_repo(tmp_path)

    hits_en = retriever.search("buyer psychology", limit=5)
    assert hits_en
    assert any(h.concept.category == "buyer_psychology" for h in hits_en)

    hits_id = retriever.search("psikologi pembeli ragu", category="buyer_psychology", limit=3)
    assert hits_id

    by_src = retriever.get_by_source("hce-seed-core")
    assert len(by_src) >= 15

    examples = retriever.get_examples("hook", category="persuasive_writing", limit=3)
    assert examples
