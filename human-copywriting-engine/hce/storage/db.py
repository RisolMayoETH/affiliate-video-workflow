"""SQLite persistence for HCE jobs, sources, chunks, tasks, knowledge, and logs."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from hce.models import (
    ChunkRecord,
    ConceptRecord,
    LearningTask,
    ProcessingJob,
    SourceRecord,
    utc_now_iso,
)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_hash TEXT NOT NULL UNIQUE,
    file_size INTEGER NOT NULL,
    duration_seconds REAL,
    media_type TEXT NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processing_jobs (
    job_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    total_chunks INTEGER NOT NULL DEFAULT 0,
    completed_chunks INTEGER NOT NULL DEFAULT 0,
    started_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    finished_at TEXT,
    error_message TEXT,
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    start_seconds REAL NOT NULL,
    end_seconds REAL NOT NULL,
    status TEXT NOT NULL,
    transcript_json TEXT,
    error_message TEXT,
    updated_at TEXT NOT NULL,
    UNIQUE(job_id, chunk_index),
    FOREIGN KEY (job_id) REFERENCES processing_jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transcriptions (
    source_id TEXT PRIMARY KEY,
    transcript_json_path TEXT,
    transcript_md_path TEXT,
    language TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    model_size TEXT NOT NULL,
    segment_count INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS learning_tasks (
    task_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    start_seconds REAL NOT NULL,
    end_seconds REAL NOT NULL,
    payload_path TEXT NOT NULL,
    status TEXT NOT NULL,
    adapter_name TEXT,
    result_path TEXT,
    error_message TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS knowledge_items (
    concept_id TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    category TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_timestamp TEXT NOT NULL,
    statement_type TEXT NOT NULL,
    extraction_confidence REAL NOT NULL,
    validation_status TEXT NOT NULL,
    file_path TEXT NOT NULL,
    content_hash TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id TEXT NOT NULL,
    action TEXT NOT NULL,
    source_id TEXT NOT NULL,
    previous_summary TEXT,
    new_summary TEXT,
    notes TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processing_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT,
    job_id TEXT,
    level TEXT NOT NULL,
    stage TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);
CREATE INDEX IF NOT EXISTS idx_jobs_source ON processing_jobs(source_id);
CREATE INDEX IF NOT EXISTS idx_chunks_job ON chunks(job_id, chunk_index);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON learning_tasks(status);
CREATE INDEX IF NOT EXISTS idx_knowledge_cat ON knowledge_items(category);
"""


class Database:
    """SQLite database helper for HCE state and provenance tracking."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_done = False

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        with self.transaction() as conn:
            conn.executescript(SCHEMA_SQL)
        self._init_done = True

    def ensure_initialized(self) -> None:
        if not self._init_done:
            self.init_schema()

    # ------------------------------------------------------------------
    # Sources
    # ------------------------------------------------------------------

    def get_source_by_hash(self, file_hash: str) -> SourceRecord | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sources WHERE file_hash = ?", (file_hash,)
            ).fetchone()
            return self._row_to_source(row) if row else None

    def get_source(self, source_id: str) -> SourceRecord | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sources WHERE source_id = ?", (source_id,)
            ).fetchone()
            return self._row_to_source(row) if row else None

    def upsert_source(self, source: SourceRecord) -> None:
        self.ensure_initialized()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO sources (
                    source_id, file_path, file_name, file_hash, file_size,
                    duration_seconds, media_type, status, error_message, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    file_path = excluded.file_path,
                    file_name = excluded.file_name,
                    file_size = excluded.file_size,
                    duration_seconds = excluded.duration_seconds,
                    media_type = excluded.media_type,
                    status = excluded.status,
                    error_message = excluded.error_message,
                    updated_at = excluded.updated_at
                """,
                (
                    source.source_id,
                    source.file_path,
                    source.file_name,
                    source.file_hash,
                    source.file_size,
                    source.duration_seconds,
                    source.media_type,
                    source.status,
                    source.error_message,
                    source.created_at,
                    source.updated_at,
                ),
            )

    def update_source_status(
        self,
        source_id: str,
        status: str,
        error_message: str | None = None,
        duration_seconds: float | None = None,
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            if duration_seconds is not None:
                conn.execute(
                    """
                    UPDATE sources
                    SET status = ?, error_message = ?, duration_seconds = ?, updated_at = ?
                    WHERE source_id = ?
                    """,
                    (status, error_message, duration_seconds, now, source_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE sources
                    SET status = ?, error_message = ?, updated_at = ?
                    WHERE source_id = ?
                    """,
                    (status, error_message, now, source_id),
                )

    def list_sources(self, statuses: tuple[str, ...] | None = None) -> list[SourceRecord]:
        self.ensure_initialized()
        with self._connect() as conn:
            if statuses:
                placeholders = ",".join("?" for _ in statuses)
                rows = conn.execute(
                    f"SELECT * FROM sources WHERE status IN ({placeholders}) ORDER BY created_at ASC",
                    statuses,
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM sources ORDER BY created_at ASC"
                ).fetchall()
            return [self._row_to_source(r) for r in rows]

    @staticmethod
    def _row_to_source(row: sqlite3.Row) -> SourceRecord:
        return SourceRecord(
            source_id=row["source_id"],
            file_path=row["file_path"],
            file_name=row["file_name"],
            file_hash=row["file_hash"],
            file_size=row["file_size"],
            duration_seconds=row["duration_seconds"],
            media_type=row["media_type"],
            status=row["status"],
            error_message=row["error_message"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    # ------------------------------------------------------------------
    # Jobs and Chunks
    # ------------------------------------------------------------------

    def get_latest_job_for_source(
        self, source_id: str, stage: str = "transcription"
    ) -> ProcessingJob | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM processing_jobs
                WHERE source_id = ? AND stage = ?
                ORDER BY started_at DESC LIMIT 1
                """,
                (source_id, stage),
            ).fetchone()
            return self._row_to_job(row) if row else None

    def get_job(self, job_id: str) -> ProcessingJob | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM processing_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            return self._row_to_job(row) if row else None

    def upsert_job(self, job: ProcessingJob) -> None:
        self.ensure_initialized()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO processing_jobs (
                    job_id, source_id, stage, status, total_chunks, completed_chunks,
                    started_at, updated_at, finished_at, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    status = excluded.status,
                    total_chunks = excluded.total_chunks,
                    completed_chunks = excluded.completed_chunks,
                    updated_at = excluded.updated_at,
                    finished_at = excluded.finished_at,
                    error_message = excluded.error_message
                """,
                (
                    job.job_id,
                    job.source_id,
                    job.stage,
                    job.status,
                    job.total_chunks,
                    job.completed_chunks,
                    job.started_at,
                    job.updated_at,
                    job.finished_at,
                    job.error_message,
                ),
            )

    def update_job(
        self,
        job_id: str,
        *,
        status: str | None = None,
        completed_chunks: int | None = None,
        finished_at: str | None = None,
        error_message: str | None = None,
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        fields: list[str] = ["updated_at = ?"]
        params: list[Any] = [now]
        if status is not None:
            fields.append("status = ?")
            params.append(status)
        if completed_chunks is not None:
            fields.append("completed_chunks = ?")
            params.append(completed_chunks)
        if finished_at is not None:
            fields.append("finished_at = ?")
            params.append(finished_at)
        if error_message is not None:
            fields.append("error_message = ?")
            params.append(error_message)
        params.append(job_id)
        with self.transaction() as conn:
            conn.execute(
                f"UPDATE processing_jobs SET {', '.join(fields)} WHERE job_id = ?",
                tuple(params),
            )

    def list_jobs(self, statuses: tuple[str, ...] | None = None) -> list[ProcessingJob]:
        self.ensure_initialized()
        with self._connect() as conn:
            if statuses:
                placeholders = ",".join("?" for _ in statuses)
                rows = conn.execute(
                    f"SELECT * FROM processing_jobs WHERE status IN ({placeholders}) ORDER BY started_at DESC",
                    statuses,
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM processing_jobs ORDER BY started_at DESC"
                ).fetchall()
            return [self._row_to_job(r) for r in rows]

    @staticmethod
    def _row_to_job(row: sqlite3.Row) -> ProcessingJob:
        return ProcessingJob(
            job_id=row["job_id"],
            source_id=row["source_id"],
            stage=row["stage"],
            status=row["status"],
            total_chunks=row["total_chunks"],
            completed_chunks=row["completed_chunks"],
            started_at=row["started_at"],
            updated_at=row["updated_at"],
            finished_at=row["finished_at"],
            error_message=row["error_message"],
        )

    def create_chunks(self, chunks: list[ChunkRecord]) -> None:
        self.ensure_initialized()
        with self.transaction() as conn:
            for c in chunks:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO chunks (
                        chunk_id, job_id, source_id, chunk_index,
                        start_seconds, end_seconds, status, transcript_json,
                        error_message, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        c.chunk_id,
                        c.job_id,
                        c.source_id,
                        c.chunk_index,
                        c.start_seconds,
                        c.end_seconds,
                        c.status,
                        c.transcript_json,
                        c.error_message,
                        c.updated_at,
                    ),
                )

    def get_chunks_for_job(self, job_id: str) -> list[ChunkRecord]:
        self.ensure_initialized()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chunks WHERE job_id = ? ORDER BY chunk_index ASC",
                (job_id,),
            ).fetchall()
            return [self._row_to_chunk(r) for r in rows]

    def update_chunk(
        self,
        chunk_id: str,
        *,
        status: str,
        transcript_json: str | None = None,
        error_message: str | None = None,
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                UPDATE chunks
                SET status = ?, transcript_json = COALESCE(?, transcript_json),
                    error_message = ?, updated_at = ?
                WHERE chunk_id = ?
                """,
                (status, transcript_json, error_message, now, chunk_id),
            )

    @staticmethod
    def _row_to_chunk(row: sqlite3.Row) -> ChunkRecord:
        return ChunkRecord(
            chunk_id=row["chunk_id"],
            job_id=row["job_id"],
            source_id=row["source_id"],
            chunk_index=row["chunk_index"],
            start_seconds=row["start_seconds"],
            end_seconds=row["end_seconds"],
            status=row["status"],
            transcript_json=row["transcript_json"],
            error_message=row["error_message"],
            updated_at=row["updated_at"],
        )

    # ------------------------------------------------------------------
    # Transcriptions
    # ------------------------------------------------------------------

    def upsert_transcription(
        self,
        *,
        source_id: str,
        transcript_json_path: str | None,
        transcript_md_path: str | None,
        language: str,
        duration_seconds: float,
        model_size: str,
        segment_count: int,
        status: str = "completed",
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO transcriptions (
                    source_id, transcript_json_path, transcript_md_path, language,
                    duration_seconds, model_size, segment_count, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    transcript_json_path = excluded.transcript_json_path,
                    transcript_md_path = excluded.transcript_md_path,
                    language = excluded.language,
                    duration_seconds = excluded.duration_seconds,
                    model_size = excluded.model_size,
                    segment_count = excluded.segment_count,
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    source_id,
                    transcript_json_path,
                    transcript_md_path,
                    language,
                    duration_seconds,
                    model_size,
                    segment_count,
                    status,
                    now,
                    now,
                ),
            )

    def get_transcription(self, source_id: str) -> dict[str, Any] | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM transcriptions WHERE source_id = ?", (source_id,)
            ).fetchone()
            return dict(row) if row else None

    # ------------------------------------------------------------------
    # Learning Tasks
    # ------------------------------------------------------------------

    def upsert_learning_task(
        self,
        task: LearningTask,
        payload_path: Path,
        status: str = "queued",
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO learning_tasks (
                    task_id, source_id, topic_id, start_seconds, end_seconds,
                    payload_path, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    payload_path = excluded.payload_path,
                    updated_at = excluded.updated_at
                """,
                (
                    task.task_id,
                    task.source_id,
                    task.topic_id,
                    task.start_seconds,
                    task.end_seconds,
                    str(payload_path),
                    status,
                    now,
                    now,
                ),
            )

    def update_learning_task_status(
        self,
        task_id: str,
        status: str,
        *,
        adapter_name: str | None = None,
        result_path: str | None = None,
        error_message: str | None = None,
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                UPDATE learning_tasks
                SET status = ?,
                    adapter_name = COALESCE(?, adapter_name),
                    result_path = COALESCE(?, result_path),
                    error_message = ?,
                    updated_at = ?
                WHERE task_id = ?
                """,
                (status, adapter_name, result_path, error_message, now, task_id),
            )

    def list_learning_tasks(
        self,
        statuses: tuple[str, ...] | None = None,
        source_id: str | None = None,
    ) -> list[dict[str, Any]]:
        self.ensure_initialized()
        clauses: list[str] = []
        params: list[Any] = []
        if statuses:
            placeholders = ",".join("?" for _ in statuses)
            clauses.append(f"status IN ({placeholders})")
            params.extend(statuses)
        if source_id:
            clauses.append("source_id = ?")
            params.append(source_id)
        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM learning_tasks {where_sql} ORDER BY created_at ASC",
                tuple(params),
            ).fetchall()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Knowledge Metadata & History
    # ------------------------------------------------------------------

    def upsert_knowledge_item(
        self,
        concept: ConceptRecord,
        file_path: Path,
        content_hash: str,
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO knowledge_items (
                    concept_id, concept_name, category, source_id, source_timestamp,
                    statement_type, extraction_confidence, validation_status,
                    file_path, content_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(concept_id) DO UPDATE SET
                    concept_name = excluded.concept_name,
                    category = excluded.category,
                    source_id = excluded.source_id,
                    source_timestamp = excluded.source_timestamp,
                    statement_type = excluded.statement_type,
                    extraction_confidence = excluded.extraction_confidence,
                    validation_status = excluded.validation_status,
                    file_path = excluded.file_path,
                    content_hash = excluded.content_hash,
                    updated_at = excluded.updated_at
                """,
                (
                    concept.concept_id,
                    concept.concept_name,
                    concept.category,
                    concept.source_id,
                    concept.source_timestamp,
                    concept.statement_type,
                    concept.extraction_confidence,
                    concept.validation_status,
                    str(file_path),
                    content_hash,
                    now,
                    now,
                ),
            )

    def get_knowledge_by_content_hash(self, content_hash: str) -> dict[str, Any] | None:
        self.ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM knowledge_items WHERE content_hash = ?", (content_hash,)
            ).fetchone()
            return dict(row) if row else None

    def append_knowledge_history(
        self,
        *,
        concept_id: str,
        action: str,
        source_id: str,
        previous_summary: str | None = None,
        new_summary: str | None = None,
        notes: str = "",
    ) -> None:
        self.ensure_initialized()
        now = utc_now_iso()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO knowledge_history (
                    concept_id, action, source_id, previous_summary, new_summary, notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (concept_id, action, source_id, previous_summary, new_summary, notes, now),
            )

    def list_knowledge_history(self, limit: int = 100) -> list[dict[str, Any]]:
        self.ensure_initialized()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM knowledge_history ORDER BY history_id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Logs & Summary
    # ------------------------------------------------------------------

    def add_log(
        self,
        level: str,
        stage: str,
        message: str,
        *,
        source_id: str | None = None,
        job_id: str | None = None,
    ) -> None:
        self.ensure_initialized()
        with self.transaction() as conn:
            conn.execute(
                """
                INSERT INTO processing_logs (source_id, job_id, level, stage, message, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (source_id, job_id, level, stage, message, utc_now_iso()),
            )

    def list_logs(self, limit: int = 50) -> list[dict[str, Any]]:
        self.ensure_initialized()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM processing_logs ORDER BY log_id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_status_summary(self) -> dict[str, Any]:
        self.ensure_initialized()
        with self._connect() as conn:
            sources_by_status = {
                row["status"]: row["cnt"]
                for row in conn.execute(
                    "SELECT status, COUNT(*) AS cnt FROM sources GROUP BY status"
                ).fetchall()
            }
            jobs_by_status = {
                row["status"]: row["cnt"]
                for row in conn.execute(
                    "SELECT status, COUNT(*) AS cnt FROM processing_jobs GROUP BY status"
                ).fetchall()
            }
            tasks_by_status = {
                row["status"]: row["cnt"]
                for row in conn.execute(
                    "SELECT status, COUNT(*) AS cnt FROM learning_tasks GROUP BY status"
                ).fetchall()
            }
            knowledge_by_category = {
                row["category"]: row["cnt"]
                for row in conn.execute(
                    "SELECT category, COUNT(*) AS cnt FROM knowledge_items GROUP BY category"
                ).fetchall()
            }
            total_transcriptions = conn.execute(
                "SELECT COUNT(*) AS cnt FROM transcriptions"
            ).fetchone()["cnt"]
            return {
                "sources_by_status": sources_by_status,
                "jobs_by_status": jobs_by_status,
                "tasks_by_status": tasks_by_status,
                "knowledge_by_category": knowledge_by_category,
                "total_transcriptions": total_transcriptions,
            }
