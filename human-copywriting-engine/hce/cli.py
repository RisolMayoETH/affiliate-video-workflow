"""Command-line interface for Human Copywriting Engine (HCE)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from hce.config import (
    VALID_COMPUTE_TYPES,
    VALID_DEVICES,
    VALID_WHISPER_MODELS,
    HCEConfig,
    write_default_config,
)
from hce.evaluation.evaluator import CopyEvaluator
from hce.execution.content_generator import AffiliateContentGenerator
from hce.execution.product_analyzer import ProductInput
from hce.execution.strategy_selector import SUPPORTED_PLATFORMS
from hce.ingestion.media import check_ffmpeg_available
from hce.ingestion.pipeline import VideoLearningPipeline
from hce.ingestion.scanner import IncomingScanner
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.models import KNOWLEDGE_CATEGORIES, format_timestamp
from hce.reasoning.adapter import create_reasoning_adapter
from hce.storage.db import Database


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _build_runtime(
    root: Path, config_path: Path | None
) -> tuple[HCEConfig, Database, KnowledgeRepository, LocalKeywordRetriever]:
    cfg = HCEConfig.load(root_dir=root, config_path=config_path)
    db = Database(cfg.storage.db_path)
    repo = KnowledgeRepository(cfg.storage.knowledge_dir, db)
    retriever = LocalKeywordRetriever(repo)
    return cfg, db, repo, retriever


def _cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config_path = Path(args.config).resolve() if args.config else root / "config" / "hce.toml"
    write_default_config(config_path, overwrite=False)
    cfg, db, repo, _ = _build_runtime(root, config_path)
    cfg.ensure_directories()
    db.init_schema()
    synced = repo.sync_seed_modules()
    ok_ffmpeg, ffmpeg_info = check_ffmpeg_available()

    print("HCE initialized successfully.")
    print(f"  Root directory : {cfg.root_dir}")
    print(f"  Config file    : {cfg.config_path}")
    print(f"  Database       : {cfg.storage.db_path}")
    print(f"  Knowledge sync : {synced} concept(s) indexed at {repo.index_path}")
    print(f"  FFmpeg check   : {'OK' if ok_ffmpeg else 'MISSING'} ({ffmpeg_info})")
    print(f"  Reasoning mode : {cfg.reasoning.adapter}")
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg, db, _, _ = _build_runtime(root, Path(args.config) if args.config else None)
    cfg.ensure_directories()
    scanner = IncomingScanner(cfg, db)
    summary = scanner.scan()

    print(f"Scanned supported media files: {summary.scanned_files}")
    print(f"  New sources registered : {len(summary.new_sources)}")
    for src in summary.new_sources:
        dur = format_timestamp(src.duration_seconds or 0.0)
        print(f"    + {src.source_id} | {src.file_name} | {dur} | {src.media_type}")
    print(f"  Already registered     : {len(summary.already_registered)}")
    print(f"  Duplicates skipped     : {len(summary.duplicates)}")
    for dup in summary.duplicates:
        print(
            f"    ! {dup['file_name']} matches existing {dup['duplicate_of_file']} ({dup['duplicate_of_source_id']})"
        )
    print(f"  Corrupted / invalid    : {len(summary.corrupted)}")
    for bad in summary.corrupted:
        print(f"    x {bad['file_name']}: {bad['error']}")
    if summary.skipped_unsupported:
        print(f"  Unsupported skipped    : {len(summary.skipped_unsupported)}")
    return 0


def _cmd_learn(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg, db, repo, retriever = _build_runtime(root, Path(args.config) if args.config else None)
    if args.model:
        cfg.whisper.model_size = args.model
    if args.device:
        cfg.whisper.device = args.device
    if args.compute_type:
        cfg.whisper.compute_type = args.compute_type
    if args.language is not None:
        cfg.whisper.language = args.language or None
    if args.beam_size:
        cfg.whisper.beam_size = args.beam_size
    if args.chunk_duration:
        cfg.pipeline.chunk_duration_seconds = args.chunk_duration
    cfg.validate()

    adapter = create_reasoning_adapter(cfg.reasoning, cfg.storage.processed_dir)
    pipeline = VideoLearningPipeline(
        cfg, db, retriever, repo, reasoning_adapter=adapter
    )
    summary = pipeline.run(source_id=args.source_id, max_chunks=args.max_chunks)
    _print_learn_summary(summary)
    return 1 if summary.failed_sources else 0


def _cmd_retry(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg, db, repo, retriever = _build_runtime(root, Path(args.config) if args.config else None)
    if args.model:
        cfg.whisper.model_size = args.model
    if args.device:
        cfg.whisper.device = args.device
    if args.compute_type:
        cfg.whisper.compute_type = args.compute_type
    if args.language is not None:
        cfg.whisper.language = args.language or None
    if args.beam_size:
        cfg.whisper.beam_size = args.beam_size
    cfg.validate()
    adapter = create_reasoning_adapter(cfg.reasoning, cfg.storage.processed_dir)
    pipeline = VideoLearningPipeline(
        cfg, db, retriever, repo, reasoning_adapter=adapter
    )
    summary = pipeline.retry(job_id=args.job_id, max_chunks=args.max_chunks)
    _print_learn_summary(summary)
    return 1 if summary.failed_sources else 0


def _print_learn_summary(summary: Any) -> None:
    print("HCE Learning Run Summary")
    print(f"  New sources scanned    : {len(summary.scan_summary.new_sources)}")
    print(f"  Duplicates detected    : {len(summary.scan_summary.duplicates)}")
    print(f"  Sources processed      : {len(summary.sources_processed)}")
    print(f"  Chunks transcribed     : {summary.chunks_transcribed}")
    print(f"  Chunks skipped (resume): {summary.chunks_skipped_resume}")
    print(f"  Transcripts written    : {len(summary.transcripts_written)}")
    print(f"  Learning tasks queued  : {summary.tasks_queued}")
    print(f"  Tasks completed        : {summary.tasks_completed}")
    print(f"  Concepts stored        : {summary.concepts_stored}")
    print(f"  Reasoning configured   : {'YES' if summary.reasoning_configured else 'NO'}")
    for sid in summary.interrupted_sources:
        print(f"  [INTERRUPTED] Source {sid} has pending chunks. Run `python -m hce learn` or `retry` to resume.")
    for fail in summary.failed_sources:
        print(f"  [FAILED] {fail['source_id']}: {fail['error']}")
    for warn in summary.warnings:
        print(f"  [NOTICE] {warn}")


def _cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg, db, _, _ = _build_runtime(root, Path(args.config) if args.config else None)
    db.ensure_initialized()
    summary = db.get_status_summary()
    sources = db.list_sources()
    jobs = db.list_jobs()
    tasks = db.list_learning_tasks()

    print("Human Copywriting Engine — Status")
    print(f"  Database          : {cfg.storage.db_path}")
    print(f"  Reasoning adapter : {cfg.reasoning.adapter}")
    print(f"  Sources           : {len(sources)} {summary['sources_by_status']}")
    print(f"  Jobs              : {len(jobs)} {summary['jobs_by_status']}")
    print(f"  Transcriptions    : {summary['total_transcriptions']}")
    print(f"  Learning tasks    : {len(tasks)} {summary['tasks_by_status']}")
    print(f"  Knowledge items   : {sum(summary['knowledge_by_category'].values())} {summary['knowledge_by_category']}")

    if sources:
        print("\nSources:")
        for s in sources:
            dur = format_timestamp(s.duration_seconds or 0.0) if s.duration_seconds else "--:--:--"
            print(f"  - {s.source_id} | {s.file_name} | {dur} | status={s.status}")
            if s.error_message:
                print(f"      note: {s.error_message}")

    if jobs:
        print("\nRecent Jobs:")
        for j in jobs[:10]:
            print(
                f"  - {j.job_id} | source={j.source_id} | status={j.status} | chunks={j.completed_chunks}/{j.total_chunks}"
            )
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    _, _, repo, retriever = _build_runtime(root, Path(args.config) if args.config else None)
    if not repo.index_path.exists():
        repo.sync_seed_modules()

    hits = retriever.search(
        args.query,
        category=args.category,
        min_confidence=args.min_confidence,
        limit=args.limit,
    )
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "score": h.score,
                        "matched_terms": h.matched_terms,
                        "concept": h.concept.to_dict(),
                    }
                    for h in hits
                ],
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    if not hits:
        print(f"No knowledge concepts matched query: {args.query!r}")
        return 0

    print(f"Found {len(hits)} concept(s) for {args.query!r}:")
    for idx, h in enumerate(hits, start=1):
        c = h.concept
        print(
            f"\n[{idx}] {c.concept_name} ({c.concept_id}) | category={c.category} "
            f"| status={c.validation_status} | conf={c.extraction_confidence:.2f} | score={h.score}"
        )
        print(f"    Statement type : {c.statement_type} | source={c.source_id} @ {c.source_timestamp}")
        print(f"    Explanation    : {c.explanation}")
        print(f"    Psychology     : {c.underlying_psychology}")
        if c.examples:
            print(f"    Example        : {c.examples[0]}")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg, db, repo, _ = _build_runtime(root, Path(args.config) if args.config else None)
    db.ensure_initialized()
    if not repo.index_path.exists():
        repo.sync_seed_modules()

    summary = db.get_status_summary()
    sources = db.list_sources()
    tasks = db.list_learning_tasks()
    history = db.list_knowledge_history(limit=20)
    concepts = repo.load_all_concepts()

    lines = [
        "# HCE Learning & Knowledge Progress Report",
        "",
        f"- **Configured Whisper Model:** `{cfg.whisper.model_size}` (device=`{cfg.whisper.device}`, compute=`{cfg.whisper.compute_type}`)",
        f"- **Reasoning Adapter:** `{cfg.reasoning.adapter}`",
        f"- **Registered Media Sources:** {len(sources)}",
        f"- **Completed Transcriptions:** {summary['total_transcriptions']}",
        f"- **Learning Tasks:** {len(tasks)} (`{summary['tasks_by_status']}`)",
        f"- **Total Knowledge Concepts:** {len(concepts)}",
        "",
        "## Knowledge Distribution by Module",
    ]
    for cat in KNOWLEDGE_CATEGORIES:
        cnt = sum(1 for c in concepts if c.category == cat)
        lines.append(f"- `{cat}`: {cnt} concept(s)")

    lines.extend(["", "## Media Sources & Processing State"])
    if not sources:
        lines.append("- No incoming media sources registered yet.")
    else:
        for s in sources:
            dur = format_timestamp(s.duration_seconds or 0.0) if s.duration_seconds else "--:--:--"
            lines.append(
                f"- `{s.source_id}` ({s.file_name}, {dur}): **{s.status}**"
                + (f" — {s.error_message}" if s.error_message else "")
            )

    lines.extend(["", "## Pending Learning Tasks"])
    queued = [t for t in tasks if t["status"] in ("queued", "failed")]
    if not queued:
        lines.append("- None.")
    else:
        for t in queued[:20]:
            lines.append(
                f"- `{t['task_id']}` (source=`{t['source_id']}`, status=`{t['status']}`): payload `{t['payload_path']}`"
            )

    lines.extend(["", "## Recent Knowledge History"])
    if not history:
        lines.append("- No extracted concept updates recorded yet.")
    else:
        for h in history[:10]:
            lines.append(
                f"- [{h['created_at']}] `{h['action']}` on `{h['concept_id']}` from `{h['source_id']}`: {h['notes']}"
            )

    report_text = "\n".join(lines) + "\n"
    print(report_text)

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = cfg.root_dir / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_text, encoding="utf-8")
        print(f"Report written to: {out_path}")
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    _, _, repo, retriever = _build_runtime(root, Path(args.config) if args.config else None)
    if not repo.index_path.exists():
        repo.sync_seed_modules()

    product_raw = json.loads(Path(args.product_file).read_text(encoding="utf-8"))
    product = ProductInput.from_dict(product_raw)
    generator = AffiliateContentGenerator(retriever)
    result = generator.generate(product, platform=args.platform)

    payload = result.to_dict()
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"=== HCE Affiliate Package: {product.name} ({result.strategy.platform}) ===")
    print(f"Strategy : {result.strategy.strategy_name}")
    print(f"Rationale: {result.strategy.rationale}")
    print(f"Retrieved: {', '.join(result.retrieved_knowledge_ids)}")
    print("\nHooks:")
    for idx, hook in enumerate(result.hooks, 1):
        print(f"  {idx}. {hook}")
    print("\nScenes:")
    for sc in result.scenes:
        print(f"  [Scene {sc.scene_number} | {sc.duration_seconds}s | {sc.narrative_objective}]")
        print(f"    Visual   : {sc.visual_direction}")
        print(f"    Narration: {sc.spoken_narration}")
        print(f"    On-screen: {sc.on_screen_text}")
    print(f"\nCTA    : {result.cta}")
    print(f"Caption: {result.caption}")
    if result.evaluation:
        ev = result.evaluation
        print(
            f"\nEvaluation: {ev.gate_status} (overall={ev.overall_score}/10, passed={ev.passed})"
        )
        for dim_name, dim_score in ev.dimensions.items():
            print(f"  - {dim_name:20s}: {dim_score.score}/10")
        if ev.integrity_violations:
            print("  Integrity violations:")
            for v in ev.integrity_violations:
                print(f"    ! {v}")
    return 0


def _cmd_evaluate(args: argparse.Namespace) -> int:
    script_data = json.loads(Path(args.script_file).read_text(encoding="utf-8"))
    product_data = (
        json.loads(Path(args.product_file).read_text(encoding="utf-8"))
        if args.product_file
        else {}
    )
    evaluator = CopyEvaluator()
    report = evaluator.evaluate(
        hooks=list(script_data.get("hooks", [])),
        scenes=list(script_data.get("scenes", [])),
        cta=str(script_data.get("cta", "")),
        caption=str(script_data.get("caption", "")),
        platform=args.platform or script_data.get("platform", "tiktok"),
        product_data=product_data,
    )
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Evaluation Gate: {report.gate_status} (overall={report.overall_score}/10)")
        for name, score in report.dimensions.items():
            print(f"  - {name:20s}: {score.score}/10 — {score.rationale}")
        if report.integrity_violations:
            print("Integrity Violations:")
            for v in report.integrity_violations:
                print(f"  ! {v}")
        print("Suggestions:")
        for sug in report.improvement_suggestions:
            print(f"  * {sug}")
    return 0 if report.passed else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hce",
        description="Human Copywriting Engine (HCE) — local Indonesian affiliate copywriting & video learning system.",
    )
    parser.add_argument("--root", default=".", help="Project root directory (default: current working dir)")
    parser.add_argument("--config", default=None, help="Optional path to hce.toml")

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize directories, config, database, and seed knowledge index")
    p_init.set_defaults(func=_cmd_init)

    p_scan = sub.add_parser("scan", help="Scan data/incoming/ for new or duplicate media files")
    p_scan.set_defaults(func=_cmd_scan)

    p_learn = sub.add_parser("learn", help="Process incoming media via FFmpeg, faster-whisper, and reasoning adapter")
    p_learn.add_argument("--source-id", default=None, help="Process only a specific source_id")
    p_learn.add_argument("--model", choices=VALID_WHISPER_MODELS, default=None)
    p_learn.add_argument("--device", choices=VALID_DEVICES, default=None)
    p_learn.add_argument("--compute-type", choices=VALID_COMPUTE_TYPES, default=None)
    p_learn.add_argument("--language", default=None, help="Override language code (e.g. 'id', 'en')")
    p_learn.add_argument("--beam-size", type=int, default=None, help="Whisper beam size (e.g. 1 for fast CPU decoding)")
    p_learn.add_argument("--chunk-duration", type=int, default=None, help="Chunk duration in seconds")
    p_learn.add_argument("--max-chunks", type=int, default=None, help="Process at most N chunks per source (for incremental batches)")
    p_learn.set_defaults(func=_cmd_learn)

    p_status = sub.add_parser("status", help="Show processing progress, pending tasks, and knowledge counts")
    p_status.set_defaults(func=_cmd_status)

    p_retry = sub.add_parser("retry", help="Resume interrupted/failed jobs and retry failed learning tasks")
    p_retry.add_argument("--job-id", default=None, help="Retry a specific job_id")
    p_retry.add_argument("--model", choices=VALID_WHISPER_MODELS, default=None)
    p_retry.add_argument("--device", choices=VALID_DEVICES, default=None)
    p_retry.add_argument("--compute-type", choices=VALID_COMPUTE_TYPES, default=None)
    p_retry.add_argument("--language", default=None, help="Override language code (e.g. 'id', 'en')")
    p_retry.add_argument("--beam-size", type=int, default=None, help="Whisper beam size (e.g. 1 for fast CPU decoding)")
    p_retry.add_argument("--max-chunks", type=int, default=None)
    p_retry.set_defaults(func=_cmd_retry)

    p_search = sub.add_parser("search", help="Search the local HCE knowledge library")
    p_search.add_argument("query", help="Keyword or phrase to search")
    p_search.add_argument("--category", choices=KNOWLEDGE_CATEGORIES, default=None)
    p_search.add_argument("--min-confidence", type=float, default=0.0)
    p_search.add_argument("--limit", type=int, default=5)
    p_search.add_argument("--json", action="store_true", help="Output JSON results")
    p_search.set_defaults(func=_cmd_search)

    p_report = sub.add_parser("report", help="Generate a learning progress and knowledge report")
    p_report.add_argument("--output", default=None, help="Optional Markdown file path to save the report")
    p_report.set_defaults(func=_cmd_report)

    p_gen = sub.add_parser("generate", help="Generate an Indonesian affiliate video package from a product JSON file")
    p_gen.add_argument("--product-file", required=True, help="Path to product JSON profile")
    p_gen.add_argument("--platform", choices=SUPPORTED_PLATFORMS, default=None)
    p_gen.add_argument("--output", default=None, help="Optional JSON file path to save output")
    p_gen.add_argument("--json", action="store_true", help="Print full JSON to stdout")
    p_gen.set_defaults(func=_cmd_generate)

    p_eval = sub.add_parser("evaluate", help="Evaluate an affiliate script JSON against 7 dimensions & accuracy gate")
    p_eval.add_argument("--script-file", required=True, help="Path to script JSON file")
    p_eval.add_argument("--product-file", default=None, help="Optional product JSON file for accuracy check")
    p_eval.add_argument("--platform", choices=SUPPORTED_PLATFORMS, default=None)
    p_eval.add_argument("--json", action="store_true")
    p_eval.set_defaults(func=_cmd_evaluate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
