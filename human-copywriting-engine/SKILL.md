---
name: human-copywriting-engine
description: Indonesian affiliate marketing copywriting knowledge and execution system (HCE). Use when generating, refining, or evaluating Indonesian affiliate video scripts, hooks, CTAs, and captions, or when learning copywriting principles from local educational videos.
---

# Human Copywriting Engine (HCE)

HCE is a local-first Indonesian affiliate copywriting knowledge and execution engine. It decides strategy before writing, retrieves relevant principles dynamically rather than dumping all files, writes natural spoken Indonesian, and strictly prohibits fabricated product claims.

## Priority Hierarchy

1. Natural Indonesian language (sounds real when read aloud by an ordinary creator).
2. Buyer psychology (real needs, honest risk reduction, trust).
3. Persuasive effectiveness and conversion.
4. Storytelling (only when narrative outperforms direct demonstration).
5. Audience adaptation (segment, price positioning, platform).
6. **Product accuracy and authenticity (non-negotiable constraints — never sacrifice truth for conversion).**

## When to Activate

- Creating or reviewing affiliate video scripts, hooks, scene plans, CTAs, or captions for **TikTok**, **Shopee Video**, **Instagram Reels**, or **Facebook Reels**.
- Processing local educational videos in `data/incoming/` or extracting structured copywriting knowledge from queued `LearningTask` files.
- Evaluating affiliate drafts on the 7-dimension rubric (`Naturalness`, `Buyer Psychology`, `Persuasiveness`, `Storytelling`, `Audience Adaptation`, `Product Accuracy`, `Authenticity`).

## Creative Decision Workflow

1. **Analyze the product (`ProductAnalyzer`)**: Separate verified features/specs and available evidence from missing information. Never invent specs, discounts, testimonials, or personal use duration.
2. **Analyze the audience (`AudienceAnalyzer`)**: Separate user-supplied audience facts from inferred hypotheses. Calibrate Indonesian register (do not assume all Indonesian buyers communicate alike or want heavy slang).
3. **Retrieve relevant knowledge dynamically**: Query the local knowledge index via CLI (`python -m hce search "<topic>" --limit 5`) or `LocalKeywordRetriever` instead of loading all modules at once.
4. **Select creative strategy (`StrategySelector`)**: Choose from problem-solution, product demonstration, everyday experience, curiosity, feature-benefit explanation, comparison, storytelling, objection handling, or practical recommendation. Prefer direct demonstration when it outperforms forced storytelling.
5. **Generate flexible scenes**: Adapt scene count and per-scene duration to the narrative purpose; ensure hooks are product-grounded (no misleading clickbait).
6. **Natural language refinement (`NaturalLanguageRefiner`)**: Review complete sentences in context; strip generic AI intros, stiff corporate phrasing, artificial urgency, and default cliché templates (`"Guys!"`, `"Wajib banget!"`, `"Auto tertarik!"`, `"Worth it parah!"`, `"Jangan sampai ketinggalan!"`).
7. **Evaluate with Hard Integrity Gate (`CopyEvaluator`)**: Score all 7 dimensions (1–10). Any ungrounded claim fails the gate regardless of persuasiveness.

## Six Knowledge Modules

- `knowledge/modules/01_human_language/` — Spoken Indonesian rhythm, register vs slang, anti-AI templates.
- `knowledge/modules/02_buyer_psychology/` — Risk reduction, balanced triggers, trust & honesty.
- `knowledge/modules/03_persuasive_writing/` — Grounded hooks, feature-to-benefit translation, objection handling, non-pushy CTAs.
- `knowledge/modules/04_storytelling/` — Everyday micro-stories, direct vs narrative choice, variable pacing.
- `knowledge/modules/05_audience_adaptation/` — Segment registers, price positioning, TikTok/Shopee/IG/FB pacing.
- `knowledge/modules/06_creative_evaluation/` — 7-dimension rubric, integrity gate, anti-repetition checks.

## Invoking the Python Engine

```powershell
# 1. Initialize workspace, DB, and knowledge index
python -m hce init

# 2. Retrieve relevant knowledge dynamically before writing
python -m hce search "buyer psychology" --limit 5
python -m hce search "shopee video pacing" --category audience_adaptation

# 3. Generate an evaluated Indonesian affiliate package from product JSON
python -m hce generate --product-file path/to/product.json --platform tiktok --json

# 4. Evaluate an existing script draft against product facts
python -m hce evaluate --script-file draft.json --product-file product.json

# 5. Process local educational videos & check status/report
python -m hce scan
python -m hce learn
python -m hce status
python -m hce report
```

## Provider-Independent Reasoning Adapter (Custom Agent Integration)

Whisper handles **transcription only**. Conceptual extraction runs through `ReasoningAdapter`:

- `none` (default): Saves transcripts and queues structured tasks in `data/processed/tasks/*.json`; sets source status to `transcribed_pending_reasoning` without falsely marking learning complete.
- `file_exchange`: Any custom agent reads queued `data/processed/tasks/<task_id>.json`, writes schema-valid `ExtractionResult` JSON (`knowledge/schemas/extraction_result.schema.json`) to `data/processed/results/<task_id>.json`, and runs `python -m hce learn` to validate, synthesize across sources, and store concepts with provenance.
- `command`: Pipes task JSON via `stdin` to a local CLI script/agent and parses `ExtractionResult` JSON from `stdout`.
