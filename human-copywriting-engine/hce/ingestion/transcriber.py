"""Local faster-whisper transcription engine with CPU/CUDA selection and timestamp preservation."""

from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from hce.config import WhisperConfig
from hce.models import TranscriptSegment


def _load_audio_input(wav_path: Path) -> Any:
    """Load 16kHz mono PCM16 WAV directly as float32 ndarray (avoids PyAV 19 `metadata_errors` issue)."""
    try:
        import numpy as np

        with wave.open(str(wav_path), "rb") as wf:
            if wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000:
                pcm_bytes = wf.readframes(wf.getnframes())
                return np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    except Exception:
        pass
    return str(wav_path)


@dataclass
class ChunkTranscriptionResult:
    segments: list[TranscriptSegment]
    language: str
    duration_seconds: float


class TranscriberProtocol(Protocol):
    """Protocol allowing real faster-whisper or deterministic test transcribers."""

    def transcribe_chunk(
        self,
        wav_path: Path,
        offset_seconds: float,
        chunk_index: int,
    ) -> ChunkTranscriptionResult:
        ...


class FasterWhisperTranscriber:
    """Local transcription using faster-whisper without cloud transcription APIs."""

    def __init__(self, config: WhisperConfig) -> None:
        self.config = config
        self._model: Any = None
        self._batched: Any = None
        self._resolved_device: str | None = None
        self._resolved_compute_type: str | None = None

    def _resolve_device_and_compute(self) -> tuple[str, str]:
        if self._resolved_device and self._resolved_compute_type:
            return self._resolved_device, self._resolved_compute_type

        device = self.config.device
        if device == "auto":
            try:
                import ctranslate2

                device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
            except Exception:
                device = "cpu"

        compute_type = self.config.compute_type
        if compute_type == "auto":
            compute_type = "float16" if device == "cuda" else "int8"

        self._resolved_device = device
        self._resolved_compute_type = compute_type
        return device, compute_type

    def _ensure_model(self) -> Any:
        if self._model is not None:
            return self._model

        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "faster-whisper is not installed. Run `pip install faster-whisper` "
                "(or `pip install -e .[transcription]`) inside your Python 3.11+ environment."
            ) from exc

        device, compute_type = self._resolve_device_and_compute()
        self._model = WhisperModel(
            self.config.model_size,
            device=device,
            compute_type=compute_type,
        )
        if self.config.batch_size > 1:
            try:
                from faster_whisper import BatchedInferencePipeline

                self._batched = BatchedInferencePipeline(model=self._model)
            except Exception:
                self._batched = None
        return self._model

    def transcribe_chunk(
        self,
        wav_path: Path,
        offset_seconds: float,
        chunk_index: int,
    ) -> ChunkTranscriptionResult:
        model = self._ensure_model()
        audio_input = _load_audio_input(wav_path)
        kwargs: dict[str, Any] = {
            "beam_size": self.config.beam_size,
            "vad_filter": self.config.vad_filter,
        }
        if self.config.language:
            kwargs["language"] = self.config.language

        try:
            if self._batched is not None and self.config.batch_size > 1:
                segments_iter, info = self._batched.transcribe(
                    audio_input,
                    batch_size=self.config.batch_size,
                    **kwargs,
                )
            else:
                segments_iter, info = model.transcribe(audio_input, **kwargs)
            raw_segments = list(segments_iter)
        except Exception:
            # Retry once without VAD / batched pipeline for short or sparse chunks
            fallback_kwargs = {"beam_size": self.config.beam_size, "vad_filter": False}
            if self.config.language:
                fallback_kwargs["language"] = self.config.language
            segments_iter, info = model.transcribe(audio_input, **fallback_kwargs)
            raw_segments = list(segments_iter)

        segments: list[TranscriptSegment] = []
        for idx, seg in enumerate(raw_segments):
            text = (getattr(seg, "text", "") or "").strip()
            if not text:
                continue
            start = round(float(seg.start) + offset_seconds, 3)
            end = round(float(seg.end) + offset_seconds, 3)
            segments.append(
                TranscriptSegment(
                    id=idx,
                    start=start,
                    end=max(start, end),
                    text=text,
                    chunk_index=chunk_index,
                )
            )

        detected_lang = str(
            getattr(info, "language", None) or self.config.language or "unknown"
        )
        duration = float(getattr(info, "duration", 0.0) or 0.0)
        return ChunkTranscriptionResult(
            segments=segments,
            language=detected_lang,
            duration_seconds=duration,
        )
