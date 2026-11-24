# Human Copywriting Engine (HCE)

Local-first Indonesian affiliate marketing knowledge and execution engine built in Python 3.11+.

HCE separates **Knowledge Engineering** (local video transcription via FFmpeg + `faster-whisper`, topic segmentation, provider-independent reasoning extraction, validation, cross-source synthesis, and keyword retrieval) from **Content Execution** (product/audience analysis, creative strategy selection, natural Indonesian script generation, full-sentence refinement, and 7-dimension quality evaluation).

---

## Repository Structure

```text
human-copywriting-engine/
├── SKILL.md                        # Concise AI agent skill entrypoint
├── pyproject.toml                  # Package definition & CLI script (`hce`)
├── config/hce.toml                 # Whisper, pipeline, reasoning, and storage config
├── hce/
│   ├── cli.py                      # `python -m hce <command>` CLI
│   ├── config.py                   # TOML + env var configuration loader
│   ├── models.py                   # Typed domain dataclasses & enums
│   ├── storage/db.py               # SQLite persistence (8 tables, WAL mode)
│   ├── ingestion/                  # FFmpeg probing/chunking, scanner, faster-whisper, segmenter, resumable pipeline
│   ├── reasoning/adapter.py        # Provider-independent ReasoningAdapter (none, file_exchange, command)
│   ├── knowledge/                  # Validator, cross-source synthesizer, repository, keyword retriever
│   ├── execution/                  # Product analyzer, audience analyzer, strategy selector, content generator
│   ├── language/refiner.py         # Context-aware Indonesian natural language refinement
│   └── evaluation/                 # 7-dimension rubric + Hard Integrity Gate + human eval logger
├── knowledge/
│   ├── schemas/                    # Draft 2020-12 JSON schemas
│   ├── modules/01..06/             # Six Indonesian affiliate copywriting domains (seed concepts)
│   ├── extracted/                  # Agent-extracted concepts (JSON + Markdown)
│   └── history/                    # Audit trail (learning_history.jsonl)
├── data/
│   ├── incoming/                   # Drop local MP4/MOV/MKV/AVI/WEBM/MP3/WAV/M4A files here
│   ├── transcripts/                # Merged transcripts (.json and .md)
│   ├── processed/                  # Topics, queued tasks/, reasoning results/, reports
│   ├── db/                         # SQLite database
│   └── tmp/                        # Temporary per-chunk WAV files (cleaned up immediately)
├── docs/                           # Architecture, reasoning adapter contract, evaluation guide
└── tests/                          # Unit, integration, and 6-category regression tests
```

---

## Windows 10/11 Installation

### 1. Python 3.11+ & Virtual Environment

```powershell
python --version   # Verify Python 3.11 or 3.12+
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[transcription,dev]"
```

### 2. FFmpeg & FFprobe (Required for Local Video/Audio Ingestion)

Install FFmpeg via WinGet (or download a static Windows build and add its `bin/` folder to `PATH`):

```powershell
winget install Gyan.FFmpeg
```

Verify installation in a fresh terminal:

```powershell
ffmpeg -version
ffprobe -version
```

### 3. CPU vs CUDA Configuration for `faster-whisper`

Edit `config/hce.toml` or set environment variables:

- **Typical consumer CPU (default, conservative):**
  ```toml
  [whisper]
  model_size = "base"      # or "tiny" for fast testing, "small" for higher accuracy
  device = "cpu"           # or "auto"
  compute_type = "int8"    # lowest RAM/CPU cost
  ```
- **NVIDIA GPU with CUDA (faster & supports `small`/`medium`/`large-v3`):**
  Ensure CUDA toolkit / cuDNN runtime libraries compatible with `ctranslate2` are installed, then:
  ```toml
  [whisper]
  model_size = "medium"
  device = "cuda"
  compute_type = "float16"
  ```

Environment variable overrides:
- `HCE_WHISPER_MODEL`, `HCE_WHISPER_DEVICE`, `HCE_WHISPER_COMPUTE_TYPE`, `HCE_WHISPER_LANGUAGE`
- `HCE_CHUNK_DURATION`, `HCE_BATCH_SIZE`, `HCE_OUTPUT_FORMAT`
- `HCE_REASONING_ADAPTER`, `HCE_REASONING_COMMAND`, `HCE_DB_PATH`

---

## Usage Quickstart

```powershell
# Initialize workspace, SQLite DB, and seed knowledge index
python -m hce init

# Add educational videos/audio into data\incoming\ and scan
python -m hce scan

# Run chunked FFmpeg audio extraction + local faster-whisper transcription + topic segmentation
python -m hce learn

# Inspect current jobs, chunks, transcriptions, and queued learning tasks
python -m hce status

# Resume interrupted or failed jobs
python -m hce retry

# Search local copywriting principles
python -m hce search "buyer psychology"

# Generate learning progress report
python -m hce report --output data/processed/learning_report.md

# Generate an evaluated Indonesian affiliate script from a product profile JSON
python -m hce generate --product-file tests/fixtures/test_products.json ...
```

---

## Copyright, Privacy, and Honest Status Guarantee

- `.gitignore` excludes local media files (`*.mp4`, `*.wav`, etc.), `data/incoming/*`, `data/transcripts/*`, `data/processed/*`, and `data/db/*`.
- Never redistribute copyrighted books or course recordings; HCE stores structured learning concepts with source IDs and timestamps instead of verbatim course dumps.
- When `reasoning.adapter = "none"` (default), HCE **never** claims knowledge extraction is complete: sources stop at `transcribed_pending_reasoning` and queued tasks remain visible in `hce status` and `hce report`.
