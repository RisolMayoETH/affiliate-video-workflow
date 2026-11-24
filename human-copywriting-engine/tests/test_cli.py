"""End-to-end CLI tests for `python -m hce <command>`."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from hce.cli import main


def test_cli_init_search_report_generate_evaluate(tmp_path: Path, capsys) -> None:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    shutil.copytree(Path("knowledge/schemas"), tmp_path / "knowledge" / "schemas")
    product_file = tmp_path / "prod.json"
    shutil.copy2(Path("tests/fixtures/sample_single_product.json"), product_file)

    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (tmp_path / "config" / "hce.toml").exists()
    assert (tmp_path / "data" / "db" / "hce.sqlite3").exists()
    assert (tmp_path / "knowledge" / "index.json").exists()

    capsys.readouterr()
    assert main(["--root", str(tmp_path), "search", "buyer psychology", "--json"]) == 0
    search_out = json.loads(capsys.readouterr().out)
    assert len(search_out) >= 1

    assert main(["--root", str(tmp_path), "scan"]) == 0
    assert main(["--root", str(tmp_path), "status"]) == 0

    report_out = tmp_path / "data" / "processed" / "report.md"
    assert main(["--root", str(tmp_path), "report", "--output", str(report_out)]) == 0
    assert report_out.exists()

    gen_out = tmp_path / "generated.json"
    assert main(
        [
            "--root",
            str(tmp_path),
            "generate",
            "--product-file",
            str(product_file),
            "--platform",
            "tiktok",
            "--output",
            str(gen_out),
            "--json",
        ]
    ) == 0
    gen_payload = json.loads(gen_out.read_text(encoding="utf-8"))
    assert gen_payload["evaluation"]["passed"] is True

    # Evaluate generated script directly via evaluate subcommand
    script_draft = {
        "hooks": gen_payload["hooks"],
        "scenes": gen_payload["scenes"],
        "cta": gen_payload["cta"],
        "caption": gen_payload["caption"],
        "platform": "tiktok",
    }
    draft_path = tmp_path / "draft.json"
    draft_path.write_text(json.dumps(script_draft, ensure_ascii=False), encoding="utf-8")
    assert main(
        [
            "--root",
            str(tmp_path),
            "evaluate",
            "--script-file",
            str(draft_path),
            "--product-file",
            str(product_file),
        ]
    ) == 0
