# Reasoning Adapter Contract

Whisper performs **speech-to-text transcription only**. Conceptual copywriting analysis, buyer psychology interpretation, and knowledge extraction are performed by a `ReasoningAdapter`.

## Available Adapters (`config/hce.toml` -> `[reasoning]`)

### 1. `adapter = "none"` (Default)
- Transcripts and topic segments are saved locally.
- Structured `LearningTask` JSON files are written to `data/processed/tasks/<task_id>.json` and tracked in SQLite as `queued`.
- Sources are marked `transcribed_pending_reasoning` — never falsely marked `completed`.

### 2. `adapter = "file_exchange"` (Recommended for Custom AI Agents)
1. Configure `adapter = "file_exchange"` in `config/hce.toml` or `HCE_REASONING_ADAPTER=file_exchange`.
2. Inspect queued tasks in `data/processed/tasks/<task_id>.json` (matching `knowledge/schemas/learning_task.schema.json`).
3. Have your custom reasoning agent write an `ExtractionResult` JSON file to `data/processed/results/<task_id>.json` matching `knowledge/schemas/extraction_result.schema.json`.
4. Run `python -m hce learn` to validate, synthesize against existing knowledge, store concepts in `knowledge/extracted/`, record `learning_history.jsonl`, and mark tasks `completed`.

### 3. `adapter = "command"` (Local CLI / Script Bridge)
Configure `command = ["python", "path/to/your_agent_bridge.py"]`:
- HCE invokes the command once per queued task, sending JSON via `stdin`:
  ```json
  {
    "task": { "...LearningTask fields..." },
    "existing_concept_summaries": [ { "concept_id": "...", "concept_name": "...", ... } ]
  }
  ```
- Your command must output valid `ExtractionResult` JSON on `stdout` and exit `0`.

## Required `ConceptRecord` Fields

Every extracted concept must include:
`concept_id`, `concept_name`, `category`, `explanation`, `underlying_psychology`, `application_conditions`, `implementation`, `examples`, `counterexamples`, `limitations`, `related_concepts`, `source_id`, `source_timestamp`, `extraction_confidence`, `validation_status`, and `statement_type` (`direct_instructor_statement`, `inferred_explanation`, `verified_fact`, `subjective_opinion`, or `practical_demonstration`).
