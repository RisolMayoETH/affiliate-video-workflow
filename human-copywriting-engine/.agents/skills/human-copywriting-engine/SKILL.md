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
- Processing local educational videos in `data/incoming/` or extracting structured copywriting knowledge from queued `LearningTask` files (see also `.agents/skills/belajar/SKILL.md`).
- Evaluating affiliate drafts on the 7-dimension rubric (`Naturalness`, `Buyer Psychology`, `Persuasiveness`, `Storytelling`, `Audience Adaptation`, `Product Accuracy`, `Authenticity`).

## Creative Decision Workflow

1. **Analyze the product (`ProductAnalyzer`)**: Separate verified features/specs and available evidence from missing information. Never invent specs, discounts, testimonials, or personal use duration.
2. **Analyze the audience (`AudienceAnalyzer`)**: Separate user-supplied audience facts from inferred hypotheses. Calibrate Indonesian register (do not assume all Indonesian buyers communicate alike or want heavy slang).
3. **Retrieve relevant knowledge dynamically**: Query the local knowledge index via CLI (`.\.venv\Scripts\python.exe -m hce search "<topic>" --limit 5` and `.\.venv\Scripts\python.exe -m hce search "bahasa obrolan natural" --category human_language --limit 5`) instead of loading all modules at once.
4. **Select creative strategy (`StrategySelector`)**: Choose from problem-solution, product demonstration, everyday experience, curiosity, feature-benefit explanation, comparison, storytelling, objection handling, or practical recommendation. Prefer direct demonstration when it outperforms forced storytelling.
5. **Generate flexible scenes**: Adapt scene count and per-scene duration to the narrative purpose; ensure hooks are product-grounded (no misleading clickbait).
6. **Natural language refinement (`NaturalLanguageRefiner`)**: Review complete sentences in context; apply spoken Indonesian principles (`satu opini utama + alasan + bukti`, bukan deskripsi datar ala buku/kamus), and strip generic AI intros, stiff corporate or textbook phrasing (`"oleh karena itu"`, `"namun demikian"`, `"dengan demikian"`), artificial urgency, and default cliché templates (`"Guys!"`, `"Wajib banget!"`, `"Auto tertarik!"`, `"Worth it parah!"`, `"Jangan sampai ketinggalan!"`).
7. **Evaluate with Hard Integrity Gate (`CopyEvaluator`)**: Score all 7 dimensions (1–10). Any ungrounded claim fails the gate regardless of persuasiveness.

## Invoking the Python Engine

```powershell
# Retrieve relevant knowledge dynamically before writing
.\.venv\Scripts\python.exe -m hce search "buyer psychology" --limit 5
.\.venv\Scripts\python.exe -m hce search "shopee video pacing" --category audience_adaptation

# Generate an evaluated Indonesian affiliate package from product JSON
.\.venv\Scripts\python.exe -m hce generate --product-file path/to/product.json --platform tiktok --json

# Evaluate an existing script draft against product facts
.\.venv\Scripts\python.exe -m hce evaluate --script-file draft.json --product-file product.json
```
