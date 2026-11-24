"""Tests for Execution Engine, Natural Language Engine, Evaluation Rubric, and Integrity Gate."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from hce.evaluation.evaluator import CopyEvaluator
from hce.evaluation.human_eval import (
    HumanEvaluationRecord,
    load_human_evaluations,
    save_human_evaluation,
    summarize_human_evaluations,
)
from hce.execution.audience_analyzer import AudienceAnalyzer
from hce.execution.content_generator import AffiliateContentGenerator
from hce.execution.product_analyzer import ProductAnalyzer, ProductInput
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.language.refiner import NaturalLanguageRefiner
from hce.storage.db import Database


def _get_retriever(tmp_path: Path) -> LocalKeywordRetriever:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    db = Database(tmp_path / "data" / "db" / "hce.sqlite3")
    db.init_schema()
    repo = KnowledgeRepository(tmp_path / "knowledge", db)
    repo.sync_seed_modules()
    return LocalKeywordRetriever(repo)


def test_product_and_audience_separates_facts_and_hypotheses() -> None:
    prod = ProductInput(
        product_id="p1",
        name="Chopper Mini",
        category="kitchen",
        description="Alat cacah bumbu",
        verified_features=["Kapasitas 250 ml"],
    )
    pa = ProductAnalyzer().analyze(prod)
    assert any("available_evidence" in m for m in pa.missing_information)
    assert any("mengaku sudah memakai" in rule for rule in pa.do_not_claim)

    aa = AudienceAnalyzer().analyze(pa, supplied_audience={"segment": "Anak kos masak harian"}, platform="tiktok")
    assert aa.supplied_facts == {"segment": "Anak kos masak harian"}
    assert not any("Target audiens disimpulkan" in h for h in aa.inferred_hypotheses)
    assert any("Hipotesis" in h for h in aa.inferred_hypotheses)


def test_natural_language_refiner_rewrites_ai_cliches_and_fake_claims() -> None:
    refiner = NaturalLanguageRefiner()
    bad_text = (
        "Halo guys! Di era modern ini kamu wajib banget punya rak ini, worth it parah! "
        "Aku udah pakai 6 bulan dan buruan beli sebelum kehabisan! "
        "Jangan sampai ketinggalan produk ini yang menunjang produktivitas Anda secara optimal."
    )
    res = refiner.refine_text(bad_text, available_evidence=[])
    lower = res.refined_text.lower()
    assert "guys" not in lower
    assert "wajib banget" not in lower
    assert "worth it parah" not in lower
    assert "jangan sampai ketinggalan" not in lower
    assert "aku udah pakai" not in lower
    assert "sebelum kehabisan" not in lower
    assert res.rewrites_applied >= 5


def test_natural_language_refiner_rewrites_bookish_dictionary_phrases() -> None:
    refiner = NaturalLanguageRefiner()
    bookish_text = (
        "Oleh karena itu, botol ini merupakan pilihan yang tepat untuk berbagai macam kebutuhan. "
        "Namun demikian, tutup ulirnya dapat digunakan untuk menahan tumpahan sehingga Anda tidak perlu khawatir lagi. "
        "Dengan demikian, desain ini memungkinkan Anda untuk membawanya di dalam tas kerja."
    )
    casual_res = refiner.refine_text(bookish_text, register="casual_everyday", available_evidence=[])
    casual_lower = casual_res.refined_text.lower()
    assert "makanya," in casual_lower
    assert "cocok dipilih" in casual_lower
    assert "berbagai kebutuhan harian" in casual_lower
    assert "tapi, tutup" in casual_lower
    assert "bisa dipakai buat" in casual_lower
    assert "nggak perlu bingung lagi" in casual_lower
    assert "jadinya," in casual_lower
    assert "bikin kamu bisa" in casual_lower
    assert any(i.issue_type == "bookish_dictionary_phrase" for i in casual_res.issues)
    assert casual_res.rewrites_applied >= 7

    polite_res = refiner.refine_text(bookish_text, register="polite_neutral", available_evidence=[])
    assert "oleh karena itu" in polite_res.refined_text.lower()
    assert not any(i.issue_type == "bookish_dictionary_phrase" for i in polite_res.issues)


def test_integrity_gate_blocks_fabricated_claims_even_with_persuasive_cta() -> None:
    evaluator = CopyEvaluator()
    product_data = json.loads(Path("tests/fixtures/sample_single_product.json").read_text(encoding="utf-8"))
    report = evaluator.evaluate(
        hooks=["Rak kamar mandi rapi tanpa bor keramik."],
        scenes=[
            {
                "scene_number": 1,
                "duration_seconds": 3,
                "spoken_narration": "Aku udah pakai rak ini 12 bulan dan bahan stainless-nya dapat diskon 70% hari ini saja.",
            },
            {
                "scene_number": 2,
                "duration_seconds": 7,
                "spoken_narration": "Kapasitasnya muat 10 kg botol sabun keluarga.",
            },
        ],
        cta="Cek keranjang kuning di kiri bawah untuk lihat varian.",
        caption="Rak sudut stainless tempel tanpa bor.",
        platform="tiktok",
        product_data=product_data,
    )
    assert not report.passed
    assert report.gate_status == "FAILED_INTEGRITY_GATE"
    assert report.integrity_violations
    assert report.dimensions["product_accuracy"].score < 7.0 or report.dimensions["authenticity"].score < 7.0


def test_human_evaluation_logging(tmp_path: Path) -> None:
    log_path = tmp_path / "human_evals.jsonl"
    rec = HumanEvaluationRecord(
        eval_id="he-1",
        product_id="prod-household-rack",
        platform="tiktok",
        reviewer="kreator_1",
        scores={
            "naturalness": 8.5,
            "buyer_psychology": 8.0,
            "persuasiveness": 8.0,
            "storytelling": 7.5,
            "audience_adaptation": 8.5,
            "product_accuracy": 9.5,
            "authenticity": 9.5,
        },
        notes="Enak dibaca lisan, tidak lebay.",
        real_world_metrics={"ctr": 0.042, "watch_3s": 0.51},
    )
    save_human_evaluation(rec, log_path)
    loaded = load_human_evaluations(log_path)
    assert len(loaded) == 1
    summary = summarize_human_evaluations(loaded)
    assert summary["count"] == 1
    assert summary["averages"]["naturalness"] == 8.5
