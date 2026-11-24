"""Benchmark loader and multi-category regression helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_benchmark_products(fixtures_path: Path) -> list[dict[str, Any]]:
    data = json.loads(fixtures_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "products" in data:
        return list(data["products"])
    if isinstance(data, list):
        return data
    raise ValueError(f"Unexpected benchmark fixture format in {fixtures_path}")
