"""Dynamic creative strategy selection backed by retrieved copywriting principles."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from hce.execution.audience_analyzer import AudienceAnalysis
from hce.execution.product_analyzer import ProductAnalysis
from hce.knowledge.retrieval import KnowledgeRetriever

SUPPORTED_PLATFORMS = (
    "tiktok",
    "shopee_video",
    "instagram_reels",
    "facebook_reels",
)

STRATEGIES = (
    "problem_solution",
    "product_demonstration",
    "everyday_experience",
    "curiosity",
    "feature_benefit_explanation",
    "comparison",
    "storytelling",
    "objection_handling",
    "practical_recommendation",
)


@dataclass
class CreativeStrategy:
    strategy_name: str
    rationale: str
    why_not_forced_story: str
    platform: str
    scene_count: int
    scene_durations: list[int]
    scene_purposes: list[str]
    retrieved_concept_ids: list[str] = field(default_factory=list)
    retrieved_context_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class StrategySelector:
    """Selects creative strategy, scene count, and flexible pacing per product & platform."""

    def select(
        self,
        product: ProductAnalysis,
        audience: AudienceAnalysis,
        platform: str,
        retriever: KnowledgeRetriever,
    ) -> CreativeStrategy:
        plat = platform.lower()
        if plat not in SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Unsupported platform {platform!r}; choose one of {SUPPORTED_PLATFORMS}"
            )

        # Dynamically retrieve only relevant principles rather than loading the entire library
        queries = [
            ("hook product", "persuasive_writing"),
            ("hesitation risk trust", "buyer_psychology"),
            (f"{plat} pacing audience", "audience_adaptation"),
            ("storytelling direct demo", "storytelling"),
            ("spoken indonesian natural", "human_language"),
        ]
        hits = []
        seen_ids: set[str] = set()
        for q, cat in queries:
            for hit in retriever.search(q, category=cat, limit=2):
                if hit.concept.concept_id not in seen_ids:
                    seen_ids.add(hit.concept.concept_id)
                    hits.append(hit)

        retrieved_ids = [h.concept.concept_id for h in hits]
        context_summary = retriever.format_context(hits[:6])

        # Strategy selection logic — do not force one framework onto every product
        if plat == "shopee_video":
            if product.category in ("kitchen", "household", "electronics"):
                strategy_name = "product_demonstration"
                rationale = (
                    "Pembeli Shopee Video cenderung berniat belanja tinggi; demonstrasi fungsi "
                    "dan spesifikasi sejak detik pertama lebih efektif dibanding prolog panjang."
                )
                why_not_story = (
                    "Penjelasan visual langsung menghemat waktu dan langsung menjawab kecocokan barang."
                )
                durations = [3, 8, 6, 4]
                purposes = ["demo_hook", "core_function_demo", "spec_and_objection_answer", "direct_cta"]
            else:
                strategy_name = "feature_benefit_explanation"
                rationale = (
                    "Untuk kategori non-perkakas di Shopee Video, penerjemahan fitur ke manfaat "
                    "yang terstruktur membantu pembeli mengambil keputusan cepat."
                )
                why_not_story = "Fokus langsung pada detail bahan, ukuran, dan manfaat harian."
                durations = [3, 7, 5, 4]
                purposes = ["clarity_hook", "feature_benefit_pair", "detail_verification", "direct_cta"]

        elif product.category == "household":
            strategy_name = "problem_solution"
            rationale = (
                "Masalah ruang kamar mandi atau rumah yang sempit mudah dikenali secara visual "
                "di 2 detik pertama sebelum menunjukkan cara pemasangan produk."
            )
            why_not_story = (
                "Cukup 1 situasi masalah harian tanpa drama berkepanjangan agar langsung masuk ke fungsi."
            )
            durations = [3, 7, 6, 4]
            purposes = ["problem_hook", "solution_demonstration", "installation_and_material_trust", "natural_cta"]

        elif product.category == "kitchen":
            strategy_name = "product_demonstration"
            rationale = (
                "Alat dapur kecil paling meyakinkan saat penonton langsung melihat ukuran wadah, "
                "cara kerja pisau/motor, dan kemudahan dibersihkan."
            )
            why_not_story = (
                "Demo kerja alat langsung jauh lebih persuasif dibanding narasi cerita panjang."
            )
            durations = [3, 9, 5]
            purposes = ["visual_demo_hook", "usage_and_capacity_breakdown", "care_and_cta"]

        elif product.category == "beauty_personal_care":
            strategy_name = "objection_handling"
            rationale = (
                "Pembeli skincare di Indonesia sering ragu soal tekstur lengket atau rasa berat; "
                "mengakui keraguan tersebut lebih membangun rasa percaya."
            )
            why_not_story = (
                "Mengedepankan jawaban jujur atas kekhawatiran tekstur dan informasi label resmi tanpa melebih-lebihkan hasil."
            )
            durations = [3, 6, 7, 5, 4]
            purposes = ["hesitation_hook", "texture_and_finish_context", "verified_protection_benefits", "honest_boundary", "natural_cta"]

        elif product.category == "fashion":
            strategy_name = "everyday_experience"
            rationale = (
                "Produk fashion kasual seperti tas paling mudah dinilai lewat situasi mobilitas "
                "sehari-hari seperti perjalanan kerja/kuliah saat gerimis."
            )
            why_not_story = (
                "Menggunakan momen keseharian yang akrab tanpa mengarang cerita pengalaman fiktif."
            )
            durations = [3, 7, 6, 4]
            purposes = ["daily_moment_hook", "capacity_and_layout", "weather_protection_benefit", "natural_cta"]

        elif product.category == "electronics":
            strategy_name = "feature_benefit_explanation"
            rationale = (
                "Pembeli produk elektronik ringan butuh kejelasan mode fungsi, daya isi ulang, "
                "dan fleksibilitas penyimpanan secara terstruktur."
            )
            why_not_story = (
                "Pembeli elektronik lebih menghargai kejelasan fitur-manfaat praktis dibanding alur cerita emosional."
            )
            durations = [3, 8, 6, 4]
            purposes = ["workspace_hook", "lighting_modes_benefit", "rechargeable_portability", "natural_cta"]

        else:
            strategy_name = "practical_recommendation"
            rationale = (
                "Untuk barang konsumsi harian yang sudah dikenal fungsinya (product-aware), "
                "rekomendasi praktis berbasis kualitas bahan dan rutinitas kerja lebih tepat sasaran."
            )
            why_not_story = (
                "Menjelaskan kapan dan untuk siapa barang ini paling kepakai tanpa basa-basi."
            )
            durations = [3, 7, 5, 4]
            purposes = ["practical_hook", "material_and_insulation", "daily_fit_check", "natural_cta"]

        if plat == "facebook_reels" and len(durations) == 3:
            # Facebook Reels audience appreciates slightly clearer explanation pacing
            durations = [4, 8, 6, 5]
            purposes = ["relatable_hook", "clear_function_demo", "practical_detail", "clear_cta"]

        return CreativeStrategy(
            strategy_name=strategy_name,
            rationale=rationale,
            why_not_forced_story=why_not_story,
            platform=plat,
            scene_count=len(durations),
            scene_durations=durations,
            scene_purposes=purposes,
            retrieved_concept_ids=retrieved_ids,
            retrieved_context_summary=context_summary,
        )
