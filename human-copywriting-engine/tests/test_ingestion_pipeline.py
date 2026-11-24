"""Integration tests for media probing, duplicate detection, chunking, and resumable learning."""

from __future__ import annotations

import json
import math
import shutil
import struct
import wave
from pathlib import Path

from hce.config import HCEConfig
from hce.ingestion.media import check_ffmpeg_available, plan_chunks, probe_media
from hce.ingestion.pipeline import VideoLearningPipeline
from hce.ingestion.scanner import IncomingScanner
from hce.ingestion.transcriber import ChunkTranscriptionResult, _load_audio_input
from hce.knowledge.repository import KnowledgeRepository
from hce.knowledge.retrieval import LocalKeywordRetriever
from hce.models import TranscriptSegment
from hce.reasoning.adapter import QueuedOnlyAdapter
from hce.storage.db import Database


def _create_synthetic_wav(path: Path, duration_sec: float = 5.0, sample_rate: int = 16000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n_frames = int(duration_sec * sample_rate)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_frames):
            val = int(8000 * math.sin(2 * math.pi * 440.0 * (i / sample_rate)))
            frames.extend(struct.pack("<h", val))
        wf.writeframes(bytes(frames))


class CountingFakeTranscriber:
    """Deterministic local test transcriber verifying chunk offsets and resume skipping."""

    def __init__(self) -> None:
        self.calls: list[int] = []

    def transcribe_chunk(
        self, wav_path: Path, offset_seconds: float, chunk_index: int
    ) -> ChunkTranscriptionResult:
        assert wav_path.exists() and wav_path.stat().st_size > 44
        self.calls.append(chunk_index)
        return ChunkTranscriptionResult(
            segments=[
                TranscriptSegment(
                    id=0,
                    start=round(offset_seconds + 0.1, 3),
                    end=round(offset_seconds + 1.8, 3),
                    text=f"Materi bagian {chunk_index + 1} tentang cara menyusun hook dan psikologi pembeli di Indonesia.",
                    chunk_index=chunk_index,
                )
            ],
            language="id",
            duration_seconds=2.0,
        )


def _prepare_workspace(tmp_path: Path) -> tuple[HCEConfig, Database, KnowledgeRepository, LocalKeywordRetriever]:
    shutil.copytree(Path("knowledge/modules"), tmp_path / "knowledge" / "modules")
    cfg = HCEConfig.load(root_dir=tmp_path)
    cfg.pipeline.chunk_duration_seconds = 10  # test uses override below
    cfg.ensure_directories()
    db = Database(cfg.storage.db_path)
    db.init_schema()
    repo = KnowledgeRepository(cfg.storage.knowledge_dir, db)
    repo.sync_seed_modules()
    retriever = LocalKeywordRetriever(repo)
    return cfg, db, repo, retriever


def test_plan_chunks_contiguous() -> None:
    chunks = plan_chunks(125.0, 50)
    assert chunks == [(0, 0.0, 50.0), (1, 50.0, 100.0), (2, 100.0, 125.0)]


def test_scanner_detects_duplicates_and_corrupted_files(tmp_path: Path) -> None:
    ok_ffmpeg, _ = check_ffmpeg_available()
    assert ok_ffmpeg

    cfg, db, _, _ = _prepare_workspace(tmp_path)
    orig = cfg.storage.incoming_dir / "lesson_a.wav"
    dup = cfg.storage.incoming_dir / "lesson_a_renamed.wav"
    corrupt = cfg.storage.incoming_dir / "broken.mp4"

    _create_synthetic_wav(orig, duration_sec=4.0)
    shutil.copy2(orig, dup)
    corrupt.write_bytes(b"NOT A VALID MP4 FILE PAYLOAD")

    scanner = IncomingScanner(cfg, db)
    summary = scanner.scan()

    assert len(summary.new_sources) == 1
    assert len(summary.duplicates) == 1
    assert len(summary.corrupted) == 1
    assert db.get_source(summary.corrupted[0]["source_id"]).status == "corrupted"


def test_chunked_transcription_interruption_resume_and_honest_queue(tmp_path: Path) -> None:
    cfg, db, repo, retriever = _prepare_workspace(tmp_path)
    cfg.pipeline.chunk_duration_seconds = 2  # 5s WAV -> 3 chunks (0-2, 2-4, 4-5)
    cfg.pipeline.min_topic_words = 10
    cfg.pipeline.max_topic_words = 60

    media_path = cfg.storage.incoming_dir / "copywriting_lesson.wav"
    _create_synthetic_wav(media_path, duration_sec=5.0)
    info = probe_media(media_path)
    assert info.has_audio and info.duration_seconds > 4.5

    fake_transcriber = CountingFakeTranscriber()
    pipeline = VideoLearningPipeline(
        cfg,
        db,
        retriever,
        repo,
        transcriber=fake_transcriber,
        reasoning_adapter=QueuedOnlyAdapter(),
    )

    # Run only 1 chunk to simulate interruption
    first_run = pipeline.run(max_chunks=1)
    assert fake_transcriber.calls == [0]
    assert first_run.chunks_transcribed == 1
    assert len(first_run.interrupted_sources) == 1
    assert list(cfg.storage.tmp_dir.iterdir()) == []
    src_id = first_run.sources_processed[0]
    assert db.get_source(src_id).status == "interrupted"

    # Resume: must NOT retranscribe chunk 0
    resumed_run = pipeline.run()
    assert fake_transcriber.calls == [0, 1, 2]
    assert resumed_run.chunks_skipped_resume == 1
    assert resumed_run.chunks_transcribed == 2
    assert not resumed_run.interrupted_sources

    # Verify timestamps preserved and merged cleanly
    transcript_json = cfg.storage.transcripts_dir / f"{src_id}.json"
    transcript_md = cfg.storage.transcripts_dir / f"{src_id}.md"
    assert transcript_json.exists() and transcript_md.exists()

    doc = json.loads(transcript_json.read_text(encoding="utf-8"))
    starts = [seg["start"] for seg in doc["segments"]]
    assert starts == [0.1, 2.1, 4.1]

    # Verify honest queuing when reasoning adapter is "none"
    assert db.get_source(src_id).status == "transcribed_pending_reasoning"
    queued = db.list_learning_tasks(statuses=("queued",), source_id=src_id)
    assert len(queued) >= 1
    assert Path(queued[0]["payload_path"]).exists()


def test_load_audio_input_returns_normalized_float32_ndarray(tmp_path: Path) -> None:
    import numpy as np

    wav_path = tmp_path / "sample.wav"
    _create_synthetic_wav(wav_path, duration_sec=1.0, sample_rate=16000)
    arr = _load_audio_input(wav_path)
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == np.float32
    assert arr.shape == (16000,)
    assert float(arr.max()) <= 1.0 and float(arr.min()) >= -1.0

