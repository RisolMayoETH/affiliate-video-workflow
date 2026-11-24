"""Incoming directory scanner with SHA-256 hash-based duplicate detection."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from hce.config import HCEConfig
from hce.ingestion.media import MediaProbeError, probe_media
from hce.models import SourceRecord
from hce.storage.db import Database


def compute_file_hash(file_path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 hash in streaming chunks so large videos use constant memory."""
    digest = hashlib.sha256()
    with file_path.open("rb") as f:
        while block := f.read(chunk_size):
            digest.update(block)
    return digest.hexdigest()


@dataclass
class ScanSummary:
    scanned_files: int = 0
    new_sources: list[SourceRecord] = field(default_factory=list)
    already_registered: list[str] = field(default_factory=list)
    duplicates: list[dict[str, str]] = field(default_factory=list)
    corrupted: list[dict[str, str]] = field(default_factory=list)
    skipped_unsupported: list[str] = field(default_factory=list)


class IncomingScanner:
    """Scans `data/incoming/`, validates media files, and detects duplicates via file hash."""

    def __init__(self, config: HCEConfig, db: Database) -> None:
        self.config = config
        self.db = db

    def scan(self) -> ScanSummary:
        self.db.ensure_initialized()
        incoming_dir = self.config.storage.incoming_dir
        incoming_dir.mkdir(parents=True, exist_ok=True)
        supported = {ext.lower() for ext in self.config.pipeline.supported_extensions}

        summary = ScanSummary()
        candidates = sorted(
            p for p in incoming_dir.rglob("*") if p.is_file() and not p.name.startswith(".")
        )

        for path in candidates:
            if path.suffix.lower() not in supported:
                summary.skipped_unsupported.append(str(path))
                continue

            summary.scanned_files += 1
            resolved_path = str(path.resolve())
            file_hash = compute_file_hash(path)
            existing = self.db.get_source_by_hash(file_hash)

            if existing is not None:
                if Path(existing.file_path).resolve() == path.resolve():
                    summary.already_registered.append(existing.source_id)
                else:
                    summary.duplicates.append(
                        {
                            "file_path": resolved_path,
                            "file_name": path.name,
                            "duplicate_of_source_id": existing.source_id,
                            "duplicate_of_file": existing.file_name,
                            "file_hash": file_hash,
                        }
                    )
                    self.db.add_log(
                        "WARNING",
                        "scan",
                        f"Duplicate media detected: '{path.name}' matches '{existing.file_name}' ({existing.source_id}).",
                        source_id=existing.source_id,
                    )
                continue

            source_id = f"src_{file_hash[:12]}"
            file_size = path.stat().st_size

            try:
                info = probe_media(path)
                record = SourceRecord(
                    source_id=source_id,
                    file_path=resolved_path,
                    file_name=path.name,
                    file_hash=file_hash,
                    file_size=file_size,
                    duration_seconds=info.duration_seconds,
                    media_type="video" if info.has_video else "audio",
                    status="pending",
                )
                self.db.upsert_source(record)
                self.db.add_log(
                    "INFO",
                    "scan",
                    f"Registered {record.media_type} source '{path.name}' ({info.duration_seconds:.1f}s).",
                    source_id=source_id,
                )
                summary.new_sources.append(record)
            except MediaProbeError as exc:
                record = SourceRecord(
                    source_id=source_id,
                    file_path=resolved_path,
                    file_name=path.name,
                    file_hash=file_hash,
                    file_size=file_size,
                    duration_seconds=None,
                    media_type="unknown",
                    status="corrupted",
                    error_message=str(exc),
                )
                self.db.upsert_source(record)
                self.db.add_log(
                    "ERROR",
                    "scan",
                    str(exc),
                    source_id=source_id,
                )
                summary.corrupted.append(
                    {
                        "source_id": source_id,
                        "file_name": path.name,
                        "error": str(exc),
                    }
                )

        return summary
