"""Tests for configuration loading, env overrides, and SQLite database persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from hce.config import HCEConfig, write_default_config
from hce.models import ChunkRecord, LearningTask, ProcessingJob, SourceRecord
from hce.storage.db import Database


def test_config_load_and_env_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_path = write_default_config(tmp_path / "config" / "hce.toml")
    monkeypatch.setenv("HCE_WHISPER_MODEL", "small")
    monkeypatch.setenv("HCE_CHUNK_DURATION", "180")
    monkeypatch.setenv("HCE_REASONING_ADAPTER", "file_exchange")

    cfg = HCEConfig.load(root_dir=tmp_path, config_path=cfg_path)
    assert cfg.whisper.model_size == "small"
    assert cfg.pipeline.chunk_duration_seconds == 180
    assert cfg.reasoning.adapter == "file_exchange"
    assert cfg.storage.db_path == tmp_path / "data" / "db" / "hce.sqlite3"


def test_invalid_whisper_model_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    write_default_config(tmp_path / "config" / "hce.toml")
    monkeypatch.setenv("HCE_WHISPER_MODEL", "ultra-mega")
    with pytest.raises(ValueError, match="Invalid whisper.model_size"):
        HCEConfig.load(root_dir=tmp_path)


def test_database_tables_and_lifecycle(tmp_path: Path) -> None:
    db = Database(tmp_path / "db" / "hce.sqlite3")
    db.init_schema()

    src = SourceRecord(
        source_id="src_abc123",
        file_path=str(tmp_path / "demo.mp4"),
        file_name="demo.mp4",
        file_hash="a" * 64,
        file_size=12345,
        duration_seconds=120.0,
        media_type="video",
        status="pending",
    )
    db.upsert_source(src)
    assert db.get_source_by_hash("a" * 64) is not None

    job = ProcessingJob(job_id="job_1", source_id="src_abc123", total_chunks=2)
    db.upsert_job(job)
    db.create_chunks(
        [
            ChunkRecord("c0", "job_1", "src_abc123", 0, 0.0, 60.0),
            ChunkRecord("c1", "job_1", "src_abc123", 1, 60.0, 120.0),
        ]
    )
    assert len(db.get_chunks_for_job("job_1")) == 2

    task = LearningTask(
        task_id="task_1",
        source_id="src_abc123",
        source_file_name="demo.mp4",
        topic_id="t0",
        title_hint="Intro",
        language="id",
        start_seconds=0.0,
        end_seconds=30.0,
        source_timestamp="00:00:00-00:00:30",
        transcript_excerpt="Contoh transkrip.",
    )
    db.upsert_learning_task(task, tmp_path / "task_1.json")
    db.add_log("INFO", "test", "Database test log", source_id="src_abc123")

    summary = db.get_status_summary()
    assert summary["sources_by_status"]["pending"] == 1
    assert summary["jobs_by_status"]["pending"] == 1
    assert summary["tasks_by_status"]["queued"] == 1
