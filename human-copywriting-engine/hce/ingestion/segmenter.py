"""Topic segmentation turning timestamped transcripts into coherent learning chunks."""

from __future__ import annotations

import re

from hce.models import TopicSegment, TranscriptDocument, TranscriptSegment

TRANSITION_CUES = (
    "selanjutnya",
    "berikutnya",
    "poin kedua",
    "poin ketiga",
    "langkah berikutnya",
    "sekarang kita bahas",
    "nah sekarang",
    "yang penting lagi",
    "kesalahan umum",
    "moving on",
    "next step",
    "another point",
    "chapter",
)


def _build_title_hint(text: str, topic_index: int) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return f"Topic {topic_index + 1}"
    first_sentence = re.split(r"[.!?]", cleaned, maxsplit=1)[0].strip()
    words = first_sentence.split()
    snippet = " ".join(words[:10])
    return snippet if len(words) <= 10 else f"{snippet}..."


class TopicSegmenter:
    """Segments a merged transcript into topic blocks with preserved timestamps."""

    def __init__(
        self,
        min_words: int = 120,
        max_words: int = 550,
        pause_threshold_seconds: float = 2.5,
    ) -> None:
        self.min_words = min_words
        self.max_words = max_words
        self.pause_threshold_seconds = pause_threshold_seconds

    def segment(self, transcript: TranscriptDocument) -> list[TopicSegment]:
        if not transcript.segments:
            return []

        topics: list[TopicSegment] = []
        bucket: list[TranscriptSegment] = []
        word_total = 0

        def _flush() -> None:
            nonlocal bucket, word_total
            if not bucket:
                return
            joined_text = " ".join(s.text.strip() for s in bucket if s.text.strip()).strip()
            topic_idx = len(topics)
            topics.append(
                TopicSegment(
                    topic_id=f"{transcript.source_id}_topic_{topic_idx:03d}",
                    source_id=transcript.source_id,
                    topic_index=topic_idx,
                    title_hint=_build_title_hint(joined_text, topic_idx),
                    start_seconds=bucket[0].start,
                    end_seconds=bucket[-1].end,
                    text=joined_text,
                    segment_indices=[s.id for s in bucket],
                    word_count=len(joined_text.split()),
                )
            )
            bucket = []
            word_total = 0

        for idx, seg in enumerate(transcript.segments):
            if bucket:
                prev = bucket[-1]
                pause_gap = seg.start - prev.end
                seg_lower = seg.text.lower()
                has_cue = any(cue in seg_lower for cue in TRANSITION_CUES)

                should_split = word_total >= self.max_words or (
                    word_total >= self.min_words
                    and (pause_gap >= self.pause_threshold_seconds or has_cue)
                )
                if should_split:
                    _flush()

            bucket.append(seg)
            word_total += len(seg.text.split())

            # Flush final segment at end
            if idx == len(transcript.segments) - 1:
                _flush()

        return topics
