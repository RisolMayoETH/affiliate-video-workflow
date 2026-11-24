"""FFmpeg and ffprobe wrappers for safe local media inspection and chunked audio extraction."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class MediaProbeError(RuntimeError):
    """Raised when a media file cannot be probed or lacks usable audio."""


class MediaExtractionError(RuntimeError):
    """Raised when FFmpeg fails to extract an audio chunk."""


@dataclass
class MediaInfo:
    duration_seconds: float
    size_bytes: int
    format_name: str
    has_audio: bool
    has_video: bool
    audio_codec: str | None = None
    sample_rate: int | None = None


def check_ffmpeg_available() -> tuple[bool, str]:
    """Verify both ffmpeg and ffprobe are reachable on PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if not ffmpeg_path or not ffprobe_path:
        missing = []
        if not ffmpeg_path:
            missing.append("ffmpeg")
        if not ffprobe_path:
            missing.append("ffprobe")
        return False, f"Missing required media binaries on PATH: {', '.join(missing)}"
    return True, f"ffmpeg={ffmpeg_path}, ffprobe={ffprobe_path}"


def probe_media(file_path: Path) -> MediaInfo:
    """Inspect a media file using ffprobe without loading media payload into memory."""
    if not file_path.exists():
        raise MediaProbeError(f"File does not exist: {file_path}")
    if file_path.stat().st_size <= 0:
        raise MediaProbeError(f"File is empty (0 bytes): {file_path.name}")

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size,format_name",
        "-show_entries",
        "stream=codec_type,codec_name,sample_rate,channels",
        "-of",
        "json",
        str(file_path),
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except FileNotFoundError as exc:
        raise MediaProbeError(
            "ffprobe executable not found on PATH. Install FFmpeg and add bin/ to PATH."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise MediaProbeError(f"ffprobe timed out inspecting {file_path.name}") from exc

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "Unknown ffprobe error").strip()
        raise MediaProbeError(f"Corrupted or unreadable media ({file_path.name}): {err}")

    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise MediaProbeError(f"Invalid ffprobe JSON output for {file_path.name}") from exc

    fmt = payload.get("format") or {}
    streams = payload.get("streams") or []

    duration_raw = fmt.get("duration")
    try:
        duration = float(duration_raw)
    except (TypeError, ValueError) as exc:
        raise MediaProbeError(f"Media duration unavailable or invalid for {file_path.name}") from exc

    if duration <= 0.0:
        raise MediaProbeError(f"Media duration must be positive for {file_path.name}")

    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    if not audio_streams:
        raise MediaProbeError(f"No audio stream found in {file_path.name}; cannot transcribe")

    first_audio = audio_streams[0]
    sr_raw = first_audio.get("sample_rate")
    sample_rate = int(sr_raw) if sr_raw and str(sr_raw).isdigit() else None

    return MediaInfo(
        duration_seconds=duration,
        size_bytes=int(fmt.get("size") or file_path.stat().st_size),
        format_name=str(fmt.get("format_name") or "unknown"),
        has_audio=True,
        has_video=bool(video_streams),
        audio_codec=first_audio.get("codec_name"),
        sample_rate=sample_rate,
    )


def plan_chunks(
    duration_seconds: float, chunk_duration_seconds: int
) -> list[tuple[int, float, float]]:
    """Partition [0, duration_seconds] into contiguous non-overlapping chunks."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if chunk_duration_seconds <= 0:
        raise ValueError("chunk_duration_seconds must be positive")

    chunks: list[tuple[int, float, float]] = []
    idx = 0
    start = 0.0
    while start < duration_seconds - 1e-6:
        end = min(duration_seconds, start + float(chunk_duration_seconds))
        chunks.append((idx, round(start, 3), round(end, 3)))
        idx += 1
        start = end
    return chunks


def extract_audio_chunk(
    source_path: Path,
    start_seconds: float,
    duration_seconds: float,
    output_wav: Path,
) -> Path:
    """Extract a mono 16kHz PCM WAV chunk using FFmpeg without loading the full media into memory."""
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start_seconds:.3f}",
        "-i",
        str(source_path),
        "-t",
        f"{duration_seconds:.3f}",
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-y",
        str(output_wav),
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
    except FileNotFoundError as exc:
        raise MediaExtractionError("ffmpeg executable not found on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        raise MediaExtractionError(
            f"FFmpeg timed out extracting chunk at {start_seconds:.1f}s from {source_path.name}"
        ) from exc

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "Unknown ffmpeg error").strip()
        raise MediaExtractionError(f"FFmpeg failed on {source_path.name}: {err}")

    if not output_wav.exists() or output_wav.stat().st_size <= 44:
        raise MediaExtractionError(
            f"Extracted WAV chunk is missing or empty: {output_wav}"
        )
    return output_wav
