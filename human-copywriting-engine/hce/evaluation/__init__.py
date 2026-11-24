"""Evaluation framework for Indonesian affiliate copy quality and accuracy."""

from hce.evaluation.evaluator import CopyEvaluator, DimensionScore, EvaluationReport
from hce.evaluation.human_eval import (
    HumanEvaluationRecord,
    load_human_evaluations,
    save_human_evaluation,
    summarize_human_evaluations,
)

__all__ = [
    "CopyEvaluator",
    "DimensionScore",
    "EvaluationReport",
    "HumanEvaluationRecord",
    "load_human_evaluations",
    "save_human_evaluation",
    "summarize_human_evaluations",
]
