"""Configuration management for Human Copywriting Engine (HCE)."""

from __future__ import annotations

import os
import shlex
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

VALID_WHISPER_MODELS = ("tiny", "base", "small", "medium", "large-v3")
VALID_DEVICES = ("auto", "cpu", "cuda")
VALID_COMPUTE_TYPES = ("auto", "int8", "int8_float16", "float16", "float32")
VALID_OUTPUT_FORMATS = ("json", "markdown", "both")
VALID_REASONING_ADAPTERS = ("none", "file_exchange", "command")

DEFAULT_SUPPORTED_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".mp3",
    ".wav",
    ".m4a",
)

DEFAULT_TOML_CONTENT = """# Human Copywriting Engine (HCE) Default Configuration
# Environment variables (e.g. HCE_WHISPER_MODEL, HCE_REASONING_ADAPTER) override these settings.

[whisper]
model_size = "base"
device = "auto"
compute_type = "auto"
language = ""
batch_size = 8
beam_size = 5
vad_filter = true

[pipeline]
chunk_duration_seconds = 300
output_format = "both"
supported_extensions = [".mp4", ".mov", ".mkv", ".avi", ".webm", ".mp3", ".wav", ".m4a"]
min_topic_words = 120
max_topic_words = 550

[reasoning]
adapter = "none"
command = []
timeout_seconds = 120

[storage]
incoming_dir = "data/incoming"
transcripts_dir = "data/transcripts"
processed_dir = "data/processed"
db_path = "data/db/hce.sqlite3"
tmp_dir = "data/tmp"
knowledge_dir = "knowledge"
"""


@dataclass
class WhisperConfig:
    model_size: str = "base"
    device: str = "auto"
    compute_type: str = "auto"
    language: str | None = None
    batch_size: int = 8
    beam_size: int = 5
    vad_filter: bool = True

    def validate(self) -> None:
        if self.model_size not in VALID_WHISPER_MODELS:
            raise ValueError(
                f"Invalid whisper.model_size {self.model_size!r}; expected one of {VALID_WHISPER_MODELS}"
            )
        if self.device not in VALID_DEVICES:
            raise ValueError(
                f"Invalid whisper.device {self.device!r}; expected one of {VALID_DEVICES}"
            )
        if self.compute_type not in VALID_COMPUTE_TYPES:
            raise ValueError(
                f"Invalid whisper.compute_type {self.compute_type!r}; expected one of {VALID_COMPUTE_TYPES}"
            )
        if self.batch_size < 1:
            raise ValueError("whisper.batch_size must be >= 1")
        if self.beam_size < 1:
            raise ValueError("whisper.beam_size must be >= 1")


@dataclass
class PipelineConfig:
    chunk_duration_seconds: int = 300
    output_format: str = "both"
    supported_extensions: tuple[str, ...] = DEFAULT_SUPPORTED_EXTENSIONS
    min_topic_words: int = 120
    max_topic_words: int = 550

    def validate(self) -> None:
        if self.chunk_duration_seconds < 10:
            raise ValueError("pipeline.chunk_duration_seconds must be >= 10")
        if self.output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid pipeline.output_format {self.output_format!r}; expected one of {VALID_OUTPUT_FORMATS}"
            )
        if self.min_topic_words < 10 or self.max_topic_words <= self.min_topic_words:
            raise ValueError("Invalid topic word bounds in pipeline config")


@dataclass
class ReasoningConfig:
    adapter: str = "none"
    command: list[str] = field(default_factory=list)
    timeout_seconds: int = 120

    def validate(self) -> None:
        if self.adapter not in VALID_REASONING_ADAPTERS:
            raise ValueError(
                f"Invalid reasoning.adapter {self.adapter!r}; expected one of {VALID_REASONING_ADAPTERS}"
            )
        if self.adapter == "command" and not self.command:
            raise ValueError("reasoning.command must be non-empty when adapter='command'")
        if self.timeout_seconds < 5:
            raise ValueError("reasoning.timeout_seconds must be >= 5")


@dataclass
class StorageConfig:
    root_dir: Path
    incoming_dir: Path
    transcripts_dir: Path
    processed_dir: Path
    db_path: Path
    tmp_dir: Path
    knowledge_dir: Path

    @classmethod
    def from_raw(cls, root_dir: Path, raw: dict[str, Any] | None = None) -> StorageConfig:
        raw = raw or {}

        def _resolve(key: str, default: str) -> Path:
            val = Path(str(raw.get(key, default)))
            return val if val.is_absolute() else (root_dir / val)

        return cls(
            root_dir=root_dir,
            incoming_dir=_resolve("incoming_dir", "data/incoming"),
            transcripts_dir=_resolve("transcripts_dir", "data/transcripts"),
            processed_dir=_resolve("processed_dir", "data/processed"),
            db_path=_resolve("db_path", "data/db/hce.sqlite3"),
            tmp_dir=_resolve("tmp_dir", "data/tmp"),
            knowledge_dir=_resolve("knowledge_dir", "knowledge"),
        )

    @property
    def tasks_dir(self) -> Path:
        return self.processed_dir / "tasks"

    @property
    def results_dir(self) -> Path:
        return self.processed_dir / "results"


@dataclass
class HCEConfig:
    root_dir: Path
    config_path: Path
    whisper: WhisperConfig
    pipeline: PipelineConfig
    reasoning: ReasoningConfig
    storage: StorageConfig

    @classmethod
    def load(
        cls,
        root_dir: Path | str | None = None,
        config_path: Path | str | None = None,
    ) -> HCEConfig:
        resolved_root = Path(root_dir).resolve() if root_dir else Path.cwd().resolve()
        resolved_config = (
            Path(config_path).resolve()
            if config_path
            else resolved_root / "config" / "hce.toml"
        )

        raw: dict[str, Any] = {}
        if resolved_config.exists():
            with resolved_config.open("rb") as f:
                raw = tomllib.load(f)

        w_raw = raw.get("whisper", {})
        lang_raw = str(w_raw.get("language", "") or "").strip()
        whisper = WhisperConfig(
            model_size=str(w_raw.get("model_size", "base")),
            device=str(w_raw.get("device", "auto")),
            compute_type=str(w_raw.get("compute_type", "auto")),
            language=lang_raw or None,
            batch_size=int(w_raw.get("batch_size", 8)),
            beam_size=int(w_raw.get("beam_size", 5)),
            vad_filter=bool(w_raw.get("vad_filter", True)),
        )

        p_raw = raw.get("pipeline", {})
        exts_raw = p_raw.get("supported_extensions", list(DEFAULT_SUPPORTED_EXTENSIONS))
        extensions = tuple(
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in exts_raw
        )
        pipeline = PipelineConfig(
            chunk_duration_seconds=int(p_raw.get("chunk_duration_seconds", 300)),
            output_format=str(p_raw.get("output_format", "both")),
            supported_extensions=extensions,
            min_topic_words=int(p_raw.get("min_topic_words", 120)),
            max_topic_words=int(p_raw.get("max_topic_words", 550)),
        )

        r_raw = raw.get("reasoning", {})
        cmd_raw = r_raw.get("command", [])
        if isinstance(cmd_raw, str):
            cmd_list = shlex.split(cmd_raw, posix=os.name != "nt")
        else:
            cmd_list = [str(item) for item in cmd_raw]
        reasoning = ReasoningConfig(
            adapter=str(r_raw.get("adapter", "none")),
            command=cmd_list,
            timeout_seconds=int(r_raw.get("timeout_seconds", 120)),
        )

        storage = StorageConfig.from_raw(resolved_root, raw.get("storage", {}))

        # Apply environment variable overrides
        if env_model := os.getenv("HCE_WHISPER_MODEL"):
            whisper.model_size = env_model.strip()
        if env_device := os.getenv("HCE_WHISPER_DEVICE"):
            whisper.device = env_device.strip()
        if env_compute := os.getenv("HCE_WHISPER_COMPUTE_TYPE"):
            whisper.compute_type = env_compute.strip()
        if "HCE_WHISPER_LANGUAGE" in os.environ:
            env_lang = os.environ["HCE_WHISPER_LANGUAGE"].strip()
            whisper.language = env_lang or None
        if env_batch := (os.getenv("HCE_WHISPER_BATCH_SIZE") or os.getenv("HCE_BATCH_SIZE")):
            whisper.batch_size = int(env_batch.strip())
        if env_chunk := os.getenv("HCE_CHUNK_DURATION"):
            pipeline.chunk_duration_seconds = int(env_chunk.strip())
        if env_fmt := os.getenv("HCE_OUTPUT_FORMAT"):
            pipeline.output_format = env_fmt.strip()
        if env_adapter := os.getenv("HCE_REASONING_ADAPTER"):
            reasoning.adapter = env_adapter.strip()
        if env_cmd := os.getenv("HCE_REASONING_COMMAND"):
            reasoning.command = shlex.split(env_cmd, posix=os.name != "nt")
        if env_db := os.getenv("HCE_DB_PATH"):
            db_p = Path(env_db.strip())
            storage.db_path = db_p if db_p.is_absolute() else (resolved_root / db_p)

        cfg = cls(
            root_dir=resolved_root,
            config_path=resolved_config,
            whisper=whisper,
            pipeline=pipeline,
            reasoning=reasoning,
            storage=storage,
        )
        cfg.validate()
        return cfg

    def validate(self) -> None:
        self.whisper.validate()
        self.pipeline.validate()
        self.reasoning.validate()

    def ensure_directories(self) -> None:
        dirs = [
            self.config_path.parent,
            self.storage.incoming_dir,
            self.storage.transcripts_dir,
            self.storage.processed_dir,
            self.storage.tasks_dir,
            self.storage.results_dir,
            self.storage.db_path.parent,
            self.storage.tmp_dir,
            self.storage.knowledge_dir,
            self.storage.knowledge_dir / "extracted",
            self.storage.knowledge_dir / "history",
            self.storage.knowledge_dir / "schemas",
            self.storage.knowledge_dir / "modules",
        ]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)


def write_default_config(config_path: Path, overwrite: bool = False) -> Path:
    """Create default `config/hce.toml` if missing or overwrite is True."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite or not config_path.exists():
        config_path.write_text(DEFAULT_TOML_CONTENT, encoding="utf-8")
    return config_path
