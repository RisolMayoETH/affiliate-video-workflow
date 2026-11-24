# Evaluation Guide (1–10 Rubric & Human Review)

HCE evaluates Indonesian affiliate copy across **7 independent dimensions** (scale 1.0–10.0):

1. **Naturalness**: Spoken Indonesian flow, varied sentence rhythm, absence of AI clichés (`"Guys!"`, `"Wajib banget!"`, `"Auto tertarik!"`, `"Worth it parah!"`, `"Jangan sampai ketinggalan!"`) and translationese.
2. **Buyer Psychology**: Addresses real situations, practical/emotional motivations, and purchase hesitation honestly.
3. **Persuasiveness**: Product-relevant hook, clear feature-to-benefit translation, and clear non-pushy CTA.
4. **Storytelling**: Clear scene progression, purposeful non-uniform scene durations, and visual-narration alignment.
5. **Audience Adaptation**: Matches Indonesian buyer register and platform conventions (`tiktok`, `shopee_video`, `instagram_reels`, `facebook_reels`).
6. **Product Accuracy**: Every feature, dimension, capacity, and benefit traces strictly to verified product inputs.
7. **Authenticity**: Zero fabricated personal experience, fake testimonials, invented discounts, or artificial scarcity.

## Hard Integrity Gate

High persuasiveness or hook scores **never** compensate for fabricated claims:
- If any integrity violation is detected, OR `product_accuracy < 7.0`, OR `authenticity < 7.0`, evaluation immediately returns `passed = false` and `gate_status = "FAILED_INTEGRITY_GATE"`.

## Human Evaluation & Real-World Feedback

Automated scoring catches structural, linguistic, and factual errors, but real Indonesian human reviewers should periodically review generated scripts for vocal cadence, regional nuance, and actual affiliate conversion metrics (`CTR`, `watch_time`, `add_to_cart`), recording entries using `hce.evaluation.human_eval.save_human_evaluation(...)` into `data/processed/human_evaluations.jsonl`.
