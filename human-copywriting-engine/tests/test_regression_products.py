"""Regression tests across all 6 required Indonesian affiliate product categories."""

from __future__ import annotations

import shutil
from pathlib import Path

from hce.evaluation.benchmarks import load_benchmark_products
from hce.execution.content_generator import AffiliateContentGenerator
from hce.execution.product_analyzer import ProductInput
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.storage.db import Database

BANNED_DEFAULT_CLICHES = (
    "guys!",
    "wajib banget",
    "auto tertarik",
    "worth it parah",
    "jangan sampai ketinggalan",
)


def test_six_category_affiliate_generation_regression(tmp_path: Path) -> None:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    db = Database(tmp_path / "data" / "db" / "hce.sqlite3")
    db.init_schema()
    repo = KnowledgeRepository(tmp_path / "knowledge", db)
    repo.sync_seed_modules()
    retriever = LocalKeywordRetriever(repo)

    products_raw = load_benchmark_products(Path("tests/fixtures/test_products.json"))
    assert len(products_raw) == 6

    generator = AffiliateContentGenerator(retriever)
    chosen_strategies: set[str] = set()

    for raw in products_raw:
        product = ProductInput.from_dict(raw)
        output = generator.generate(product)
        chosen_strategies.add(output.strategy.strategy_name)

        # Must dynamically retrieve principles
        assert len(output.retrieved_knowledge_ids) >= 3
        assert len(output.hooks) == 3
        assert len(output.alternative_angles) >= 2

        # Flexible scene durations (not all equal)
        durations = [s.duration_seconds for s in output.scenes]
        assert len(durations) >= 3
        assert len(set(durations)) > 1

        # No banned default clichés anywhere
        full_copy = " ".join(
            [*output.hooks, *(s.spoken_narration for s in output.scenes), output.cta, output.caption]
        ).lower()
        for cliche in BANNED_DEFAULT_CLICHES:
            assert cliche not in full_copy, f"Found banned cliche {cliche!r} in {product.product_id}"

        # Must pass 7-dimension evaluation AND integrity gate
        assert output.evaluation is not None
        assert output.evaluation.passed, (
            f"{product.product_id} failed gate: {output.evaluation.gate_status} "
            f"violations={output.evaluation.integrity_violations}"
        )
        assert output.evaluation.gate_status == "PASSED"
        assert output.evaluation.dimensions["product_accuracy"].score >= 8.0
        assert output.evaluation.dimensions["authenticity"].score >= 8.0

    # Must NOT force the exact same strategy onto all 6 categories
    assert len(chosen_strategies) >= 4
