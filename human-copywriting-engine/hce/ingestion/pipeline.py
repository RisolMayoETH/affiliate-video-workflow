"""Resumable local video-to-knowledge learning pipeline."""

from __future__ import annotations

import json
import tempfile
import uuid
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from hce.config import HCEConfig
from hce.ingestion.media import check_ffmpeg_available, extract_audio_chunk, plan_chunks
from hce.ingestion.scanner import IncomingScanner, ScanSummary
from hce.ingestion.segmenter import TopicSegmenter
from hce.ingestion.transcriber import FasterWhisperTranscriber, TranscriberProtocol
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import KnowledgeRetriever
from hce.models import (
    ChunkRecord,
    LearningTask,
    ProcessingJob,
    SourceRecord,
    TranscriptDocument,
    TranscriptSegment,
    format_timestamp,
    utc_now_iso,
)
from hce.reasoning.adapter import ReasoningAdapter, create_reasoning_adapter
from hce.storage.db import Database


@dataclass
class LearnRunSummary:
    scan_summary: ScanSummary
    sources_processed: list[str] = field(default_factory=list)
    chunks_transcribed: int = 0
    chunks_skipped_resume: int = 0
    interrupted_sources: list[str] = field(default_factory=list)
    failed_sources: list[dict[str, str]] = field(default_factory=list)
    transcripts_written: list[str] = field(default_factory=list)
    tasks_queued: int = 0
    tasks_completed: int = 0
    concepts_stored: int = 0
    reasoning_configured: bool = False
    warnings: list[str] = field(default_factory=list)


def _render_transcript_markdown(doc: TranscriptDocument) -> str:
    lines = [
        f"# Transcript: {doc.file_name}",
        "",
        f"- **Source ID:** `{doc.source_id}`",
        f"- **Language:** `{doc.language}`",
        f"- **Duration:** {format_timestamp(doc.duration_seconds)} ({doc.duration_seconds:.2f}s)",
        f"- **Whisper Model:** `{doc.model_size}`",
        f"- **Segments:** {len(doc.segments)}",
        "",
        "## Segments",
        "",
    ]
    for seg in doc.segments:
        lines.append(
            f"- **[{format_timestamp(seg.start)} - {format_timestamp(seg.end)}]** {seg.text}"
        )
    lines.append("")
    return "\n".join(lines)


class VideoLearningPipeline:
    """Executes all 21 ingestion, chunked transcription, segmentation, and learning stages."""

    def __init__(
        self,
        config: HCEConfig,
        db: Database,
        retriever: KnowledgeRetriever,
        repository: KnowledgeRepository,
        *,
        transcriber: TranscriberProtocol | None = None,
        reasoning_adapter: ReasoningAdapter | None = None,
    ) -> None:
        self.config = config
        self.db = db
        self.retriever = retriever
        self.repository = repository
        self._transcriber = transcriber
        self._reasoning_adapter = reasoning_adapter or create_reasoning_adapter(
            config.reasoning, config.storage.processed_dir
        )

    @property
    def transcriber(self) -> TranscriberProtocol:
        if self._transcriber is None:
            self._transcriber = FasterWhisperTranscriber(self.config.whisper)
        return self._transcriber

    def run(
        self,
        *,
        source_id: str | None = None,
        max_chunks: int | None = None,
        include_failed: bool = False,
    ) -> LearnRunSummary:
        self.config.ensure_directories()
        self.db.ensure_initialized()

        scanner = IncomingScanner(self.config, self.db)
        scan_summary = scanner.scan()

        summary = LearnRunSummary(
            scan_summary=scan_summary,
            reasoning_configured=self._reasoning_adapter.is_configured(),
        )

        # Determine candidate sources for transcription
        transcribe_statuses = ("pending", "interrupted", "transcribing")
        if include_failed:
            transcribe_statuses = ("pending", "interrupted", "transcribing", "failed")

        sources = self.db.list_sources(statuses=transcribe_statuses)
        if source_id:
            sources = [s for s in sources if s.source_id == source_id]

        if sources and self._transcriber is None:
            ok, msg = check_ffmpeg_available()
            if not ok:
                raise RuntimeError(msg)

        for source in sources:
            self._process_source_transcription(source, summary, max_chunks=max_chunks)

        # Run reasoning stage on queued tasks (or pending sources)
        self._process_reasoning_queue(summary, source_id=source_id, include_failed=include_failed)

        if not self._reasoning_adapter.is_configured() and summary.tasks_queued > 0:
            summary.warnings.append(
                "No reasoning provider is configured (reasoning.adapter='none'). "
                "Transcripts and learning tasks were saved and queued; source status remains "
                "'transcribed_pending_reasoning' until a reasoning adapter processes the tasks."
            )

        return summary

    def retry(self, *, job_id: str | None = None, max_chunks: int | None = None) -> LearnRunSummary:
        self.db.ensure_initialized()
        target_source_id: str | None = None
        if job_id:
            job = self.db.get_job(job_id)
            if job is None:
                raise ValueError(f"Job not found: {job_id}")
            target_source_id = job.source_id
            if job.status == "failed":
                self.db.update_job(job.job_id, status="interrupted", error_message=None)
                for chunk in self.db.get_chunks_for_job(job.job_id):
                    if chunk.status == "failed":
                        self.db.update_chunk(chunk.chunk_id, status="pending", error_message=None)
            self.db.update_source_status(job.source_id, "interrupted", error_message=None)
        else:
            for failed_job in self.db.list_jobs(statuses=("failed",)):
                self.db.update_job(failed_job.job_id, status="interrupted", error_message=None)
                for chunk in self.db.get_chunks_for_job(failed_job.job_id):
                    if chunk.status == "failed":
                        self.db.update_chunk(chunk.chunk_id, status="pending", error_message=None)
            for failed_task in self.db.list_learning_tasks(statuses=("failed",)):
                self.db.update_learning_task_status(
                    failed_task["task_id"], "queued", error_message=None
                )

        return self.run(
            source_id=target_source_id,
            max_chunks=max_chunks,
            include_failed=True,
        )

    def _get_or_create_job(self, source: SourceRecord) -> tuple[ProcessingJob, list[ChunkRecord]]:
        existing_job = self.db.get_latest_job_for_source(source.source_id, stage="transcription")
        if existing_job and existing_job.status != "completed":
            chunks = self.db.get_chunks_for_job(existing_job.job_id)
            if chunks:
                return existing_job, chunks

        if not source.duration_seconds or source.duration_seconds <= 0:
            raise RuntimeError(
                f"Source {source.source_id} has invalid duration ({source.duration_seconds})."
            )

        planned = plan_chunks(
            source.duration_seconds, self.config.pipeline.chunk_duration_seconds
        )
        job_id = f"job_{source.source_id}_{uuid.uuid4().hex[:8]}"
        job = ProcessingJob(
            job_id=job_id,
            source_id=source.source_id,
            stage="transcription",
            status="running",
            total_chunks=len(planned),
            completed_chunks=0,
        )
        self.db.upsert_job(job)

        chunk_records = [
            ChunkRecord(
                chunk_id=f"{job_id}_c{idx:04d}",
                job_id=job_id,
                source_id=source.source_id,
                chunk_index=idx,
                start_seconds=start,
                end_seconds=end,
                status="pending",
            )
            for idx, start, end in planned
        ]
        self.db.create_chunks(chunk_records)
        return job, chunk_records

    def _process_source_transcription(
        self,
        source: SourceRecord,
        summary: LearnRunSummary,
        *,
        max_chunks: int | None = None,
    ) -> None:
        source_path = Path(source.file_path)
        if not source_path.exists():
            msg = f"Media file missing on disk: {source_path}"
            self.db.update_source_status(source.source_id, "failed", error_message=msg)
            self.db.add_log("ERROR", "transcription", msg, source_id=source.source_id)
            summary.failed_sources.append({"source_id": source.source_id, "error": msg})
            return

        job, chunks = self._get_or_create_job(source)
        self.db.update_source_status(source.source_id, "transcribing", error_message=None)
        self.db.update_job(job.job_id, status="running", error_message=None)
        summary.sources_processed.append(source.source_id)

        completed_count = sum(1 for c in chunks if c.status == "completed")
        processed_in_run = 0
        interrupted_early = False
        had_failure = False

        for chunk in chunks:
            if chunk.status == "completed":
                summary.chunks_skipped_resume += 1
                continue

            if max_chunks is not None and processed_in_run >= max_chunks:
                interrupted_early = True
                break

            try:
                with tempfile.TemporaryDirectory(dir=self.config.storage.tmp_dir) as tmp_dir:
                    wav_path = Path(tmp_dir) / f"chunk_{chunk.chunk_index:04d}.wav"
                    extract_audio_chunk(
                        source_path=source_path,
                        start_seconds=chunk.start_seconds,
                        duration_seconds=max(0.1, chunk.end_seconds - chunk.start_seconds),
                        output_wav=wav_path,
                    )
                    result = self.transcriber.transcribe_chunk(
                        wav_path=wav_path,
                        offset_seconds=chunk.start_seconds,
                        chunk_index=chunk.chunk_index,
                    )

                payload = json.dumps(
                    {
                        "language": result.language,
                        "segments": [s.to_dict() for s in result.segments],
                    },
                    ensure_ascii=False,
                )
                self.db.update_chunk(
                    chunk.chunk_id,
                    status="completed",
                    transcript_json=payload,
                    error_message=None,
                )
                completed_count += 1
                processed_in_run += 1
                summary.chunks_transcribed += 1
                self.db.update_job(job.job_id, completed_chunks=completed_count)
            except KeyboardInterrupt:
                self.db.update_job(
                    job.job_id,
                    status="interrupted",
                    completed_chunks=completed_count,
                    error_message="Interrupted by user signal",
                )
                self.db.update_source_status(
                    source.source_id,
                    "interrupted",
                    error_message="Interrupted during chunk transcription",
                )
                self.db.add_log(
                    "WARNING",
                    "transcription",
                    f"Interrupted at chunk {chunk.chunk_index}/{len(chunks)}",
                    source_id=source.source_id,
                    job_id=job.job_id,
                )
                summary.interrupted_sources.append(source.source_id)
                raise
            except Exception as exc:
                had_failure = True
                err_msg = f"Chunk {chunk.chunk_index} failed: {exc}"
                self.db.update_chunk(chunk.chunk_id, status="failed", error_message=err_msg)
                self.db.update_job(
                    job.job_id,
                    status="failed",
                    completed_chunks=completed_count,
                    error_message=err_msg,
                )
                self.db.update_source_status(
                    source.source_id, "failed", error_message=err_msg
                )
                self.db.add_log(
                    "ERROR",
                    "transcription",
                    err_msg,
                    source_id=source.source_id,
                    job_id=job.job_id,
                )
                summary.failed_sources.append(
                    {"source_id": source.source_id, "error": err_msg}
                )
                break

        if had_failure:
            return

        if interrupted_early:
            msg = f"Paused after max_chunks={max_chunks} ({completed_count}/{len(chunks)} chunks done)."
            self.db.update_job(
                job.job_id,
                status="interrupted",
                completed_chunks=completed_count,
                error_message=msg,
            )
            self.db.update_source_status(source.source_id, "interrupted", error_message=msg)
            self.db.add_log(
                "INFO", "transcription", msg, source_id=source.source_id, job_id=job.job_id
            )
            summary.interrupted_sources.append(source.source_id)
            return

        # All chunks complete -> merge transcript, segment into topics, generate learning tasks
        latest_chunks = self.db.get_chunks_for_job(job.job_id)
        if any(c.status != "completed" for c in latest_chunks):
            self.db.update_job(job.job_id, status="interrupted")
            self.db.update_source_status(source.source_id, "interrupted")
            summary.interrupted_sources.append(source.source_id)
            return

        merged_segments: list[TranscriptSegment] = []
        lang_votes: Counter[str] = Counter()
        global_id = 0
        for ch in latest_chunks:
            chunk_data = json.loads(ch.transcript_json or "{}")
            lang = chunk_data.get("language")
            if lang and lang != "unknown":
                lang_votes[lang] += 1
            for raw_seg in chunk_data.get("segments", []):
                seg = TranscriptSegment.from_dict(raw_seg)
                seg.id = global_id
                merged_segments.append(seg)
                global_id += 1

        primary_language = (
            lang_votes.most_common(1)[0][0]
            if lang_votes
            else (self.config.whisper.language or "unknown")
        )
        doc = TranscriptDocument(
            source_id=source.source_id,
            file_name=source.file_name,
            language=primary_language,
            duration_seconds=float(source.duration_seconds or 0.0),
            model_size=self.config.whisper.model_size,
            segments=merged_segments,
        )

        json_path: Path | None = None
        md_path: Path | None = None
        fmt = self.config.pipeline.output_format
        if fmt in ("json", "both"):
            json_path = self.config.storage.transcripts_dir / f"{source.source_id}.json"
            json_path.write_text(
                json.dumps(doc.to_dict(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            summary.transcripts_written.append(str(json_path))
        if fmt in ("markdown", "both"):
            md_path = self.config.storage.transcripts_dir / f"{source.source_id}.md"
            md_path.write_text(_render_transcript_markdown(doc), encoding="utf-8")
            summary.transcripts_written.append(str(md_path))

        self.db.upsert_transcription(
            source_id=source.source_id,
            transcript_json_path=str(json_path) if json_path else None,
            transcript_md_path=str(md_path) if md_path else None,
            language=doc.language,
            duration_seconds=doc.duration_seconds,
            model_size=doc.model_size,
            segment_count=len(doc.segments),
            status="completed",
        )
        self.db.update_job(
            job.job_id,
            status="completed",
            completed_chunks=len(latest_chunks),
            finished_at=utc_now_iso(),
            error_message=None,
        )

        # Stage 11-12: Segment into topics & build structured LearningTasks
        segmenter = TopicSegmenter(
            min_words=self.config.pipeline.min_topic_words,
            max_words=self.config.pipeline.max_topic_words,
        )
        topics = segmenter.segment(doc)
        topics_path = self.config.storage.processed_dir / f"{source.source_id}_topics.json"
        topics_path.write_text(
            json.dumps([t.to_dict() for t in topics], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        for topic in topics:
            hits = self.retriever.search(topic.text[:400], limit=3)
            related_summaries = [
                {
                    "concept_id": h.concept.concept_id,
                    "concept_name": h.concept.concept_name,
                    "category": h.concept.category,
                    "explanation": h.concept.explanation,
                }
                for h in hits
            ]
            task = LearningTask(
                task_id=f"task_{topic.topic_id}",
                source_id=source.source_id,
                source_file_name=source.file_name,
                topic_id=topic.topic_id,
                title_hint=topic.title_hint,
                language=doc.language,
                start_seconds=topic.start_seconds,
                end_seconds=topic.end_seconds,
                source_timestamp=f"{format_timestamp(topic.start_seconds)}-{format_timestamp(topic.end_seconds)}",
                transcript_excerpt=topic.text,
                related_existing_concepts=related_summaries,
                extraction_instructions=(
                    "Extract Indonesian affiliate copywriting concepts with provenance, "
                    "epistemic statement_type, underlying_psychology, examples, counterexamples, "
                    "and limitations. Never mark subjective opinion as verified_fact."
                ),
            )
            task_path = self.config.storage.tasks_dir / f"{task.task_id}.json"
            task_path.write_text(
                json.dumps(task.to_dict(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            self.db.upsert_learning_task(task, payload_path=task_path, status="queued")
            summary.tasks_queued += 1

        # Never pretend reasoning/extraction is finished before reasoning runs
        self.db.update_source_status(source.source_id, "transcribed_pending_reasoning")
        self.db.add_log(
            "INFO",
            "segmentation",
            f"Completed transcription ({len(doc.segments)} segments) and queued {len(topics)} learning tasks.",
            source_id=source.source_id,
            job_id=job.job_id,
        )

    def _process_reasoning_queue(
        self,
        summary: LearnRunSummary,
        *,
        source_id: str | None = None,
        include_failed: bool = False,
    ) -> None:
        statuses = ("queued", "failed") if include_failed else ("queued",)
        tasks = self.db.list_learning_tasks(statuses=statuses, source_id=source_id)
        if not tasks:
            return

        if not self._reasoning_adapter.is_configured():
            # Count already queued tasks accurately if not counted during this transcription run
            if summary.tasks_queued == 0:
                summary.tasks_queued = len(tasks)
            return

        existing_concepts = self.repository.load_all_concepts()
        touched_sources: set[str] = set()

        for row in tasks:
            payload_path = Path(row["payload_path"])
            if not payload_path.exists():
                self.db.update_learning_task_status(
                    row["task_id"],
                    "failed",
                    error_message=f"Task payload missing: {payload_path}",
                )
                continue

            task = LearningTask.from_dict(
                json.loads(payload_path.read_text(encoding="utf-8"))
            )
            try:
                extraction = self._reasoning_adapter.extract_knowledge(
                    task, existing_concepts
                )
                if extraction is None:
                    # Adapter deferred (e.g. file_exchange result not written yet)
                    continue

                result_path = (
                    self.config.storage.results_dir / f"{task.task_id}.json"
                )
                if not result_path.exists():
                    result_path.write_text(
                        json.dumps(extraction.to_dict(), indent=2, ensure_ascii=False)
                        + "\n",
                        encoding="utf-8",
                    )

                for raw_concept in extraction.concepts:
                    # Enforce source provenance
                    if not raw_concept.source_id:
                        raw_concept.source_id = task.source_id
                    if not raw_concept.source_timestamp:
                        raw_concept.source_timestamp = task.source_timestamp

                    val = self._reasoning_adapter.validate_concept(raw_concept)
                    if not val.valid:
                        self.db.add_log(
                            "WARNING",
                            "knowledge_validation",
                            f"Rejected invalid concept {raw_concept.concept_id}: {val.errors}",
                            source_id=task.source_id,
                        )
                        continue
                    if val.adjusted_status:
                        raw_concept.validation_status = val.adjusted_status

                    decision = self._reasoning_adapter.compare_and_synthesize(
                        raw_concept, existing_concepts
                    )
                    if decision.action == "duplicate":
                        self.db.add_log(
                            "INFO",
                            "synthesis",
                            decision.notes,
                            source_id=task.source_id,
                        )
                        continue

                    to_save = decision.merged_concept or raw_concept
                    prev_summary = (
                        f"{decision.target_concept.concept_name} ({decision.target_concept.validation_status})"
                        if decision.target_concept
                        else None
                    )
                    self.repository.save_concept(
                        to_save,
                        action=decision.action,
                        previous_summary=prev_summary,
                        notes=decision.notes,
                        rebuild=False,
                    )
                    summary.concepts_stored += 1
                    # Refresh in-memory list for subsequent comparisons in same batch
                    existing_concepts = [
                        c for c in existing_concepts if c.concept_id != to_save.concept_id
                    ] + [to_save]

                self.db.update_learning_task_status(
                    task.task_id,
                    "completed",
                    adapter_name=self._reasoning_adapter.name,
                    result_path=str(result_path),
                    error_message=None,
                )
                summary.tasks_completed += 1
                touched_sources.add(task.source_id)
            except Exception as exc:
                self.db.update_learning_task_status(
                    task.task_id,
                    "failed",
                    adapter_name=self._reasoning_adapter.name,
                    error_message=str(exc),
                )
                self.db.add_log(
                    "ERROR",
                    "reasoning",
                    f"Task {task.task_id} failed: {exc}",
                    source_id=task.source_id,
                )
                touched_sources.add(task.source_id)

        if summary.concepts_stored > 0:
            self.repository.rebuild_index()

        for sid in touched_sources:
            all_tasks = self.db.list_learning_tasks(source_id=sid)
            if all_tasks and all(t["status"] == "completed" for t in all_tasks):
                self.db.update_source_status(sid, "completed", error_message=None)
            elif any(t["status"] == "failed" for t in all_tasks):
                self.db.update_source_status(
                    sid,
                    "partial_learning_errors",
                    error_message="Some learning tasks failed during reasoning.",
                )
            else:
                self.db.update_source_status(sid, "transcribed_pending_reasoning")
