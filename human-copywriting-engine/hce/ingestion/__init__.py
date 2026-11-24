"""Local video and audio ingestion package."""

from hce.ingestion.media import MediaInfo, check_ffmpeg_available, extract_audio_chunk, plan_chunks, probe_media
from hce.ingestion.pipeline import VideoLearningPipeline
from hce.ingestion.scanner import IncomingScanner, ScanSummary, compute_file_hash
from hce.ingestion.segmenter import TopicSegmenter
from hce.ingestion.transcriber import ChunkTranscriptionResult, FasterWhisperTranscriber, TranscriberProtocol

__all__ = [
    "ChunkTranscriptionResult",
    "FasterWhisperTranscriber",
    "IncomingScanner",
    "MediaInfo",
    "ScanSummary",
    "TopicSegmenter",
    "TranscriberProtocol",
    "VideoLearningPipeline",
    "check_ffmpeg_available",
    "compute_file_hash",
    "extract_audio_chunk",
    "plan_chunks",
    "probe_media",
]
