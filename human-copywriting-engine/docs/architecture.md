# HCE System Architecture

HCE strictly separates **Knowledge Engineering** from **Execution**, and separates **Media Transcription** from **Conceptual Reasoning**.

## 1. Knowledge Engine

1. **Incoming Scanner (`hce/ingestion/scanner.py`)**: Streams SHA-256 hashes of supported media in `data/incoming/`, detects renamed duplicates, and validates streams via `ffprobe`.
2. **Chunked Transcription (`hce/ingestion/media.py`, `transcriber.py`, `pipeline.py`)**:
   - Long videos (hours long) are split into non-overlapping intervals (`chunk_duration_seconds`, default 300s).
   - Each chunk extracts only its segment to a temporary 16kHz mono WAV via `ffmpeg`, runs `faster-whisper`, offsets timestamps globally, saves the chunk transcript to SQLite `chunks`, and deletes the temp WAV immediately.
   - Completed chunks are never retranscribed on resume.
3. **Topic Segmentation (`hce/ingestion/segmenter.py`)**: Merges chunk segments with preserved timestamps and groups coherent topic blocks into `LearningTask` JSON files.
4. **Reasoning Adapter (`hce/reasoning/adapter.py`)**: Provider-independent interface (`QueuedOnlyAdapter`, `FileExchangeAdapter`, `CommandAdapter`) producing `ConceptRecord` objects with explicit epistemic `statement_type`.
5. **Validation, Cross-Source Synthesis & Repository (`hce/knowledge/`)**:
   - `KnowledgeValidator` enforces required fields, provenance, and prevents subjective opinions from being upgraded into verified facts.
   - `KnowledgeSynthesizer` detects exact duplicates, merges complementary examples/provenance, and preserves competing viewpoints instead of overwriting validated knowledge.
   - `LocalKeywordRetriever` uses `knowledge/index.json` for targeted selective retrieval without loading the entire knowledge library on every request.

## 2. Execution Engine

1. **`ProductAnalyzer`**: Maps verified features to grounded practical benefits and lists missing information / `do_not_claim` rules.
2. **`AudienceAnalyzer`**: Separates user-supplied audience facts from inferred hypotheses and selects an Indonesian communication register.
3. **`StrategySelector`**: Queries `KnowledgeRetriever` dynamically and chooses among 9 strategies (preferring direct demonstration when storytelling adds unnecessary fluff), flexible scene counts, and variable scene durations.
4. **`AffiliateContentGenerator`**: Generates hooks, flexible scenes, platform-aligned CTA, caption, and alternative angles.
5. **`NaturalLanguageRefiner` & `CopyEvaluator`**: Rewrites robotic/cliché patterns at sentence level and evaluates across 7 separate dimensions with a Hard Integrity Gate prohibiting fabricated claims.
