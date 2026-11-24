"""Human-in-the-loop evaluation recording and feedback summary utilities."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from hce.evaluation.evaluator import EVALUATION_DIMENSIONS
from hce.models import utc_now_iso


@dataclass
class HumanEvaluationRecord:
    eval_id: str
    product_id: str
    platform: str
    reviewer: str
    scores: dict[str, float]
    notes: str = ""
    real_world_metrics: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def validate(self) -> None:
        for dim in EVALUATION_DIMENSIONS:
            if dim not in self.scores:
                raise ValueError(f"Missing required human evaluation dimension: {dim}")
            val = float(self.scores[dim])
            if not (1.0 <= val <= 10.0):
                raise ValueError(f"Score for {dim} must be between 1.0 and 10.0 (got {val})")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def save_human_evaluation(
    record: HumanEvaluationRecord, log_path: Path
) -> Path:
    record.validate()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return log_path


def load_human_evaluations(log_path: Path) -> list[HumanEvaluationRecord]:
    if not log_path.exists():
        return []
    records: list[HumanEvaluationRecord] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(HumanEvaluationRecord(**json.loads(line)))
    return records


def summarize_human_evaluations(records: list[HumanEvaluationRecord]) -> dict[str, Any]:
    if not records:
        return {"count": 0, "averages": {}}
    averages: dict[str, float] = {}
    for dim in EVALUATION_DIMENSIONS:
        vals = [float(r.scores[dim]) for r in records if dim in r.scores]
        averages[dim] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return {"count": len(records), "averages": averages}
