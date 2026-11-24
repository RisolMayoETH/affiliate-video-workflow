"""Autonomous Indonesian affiliate video script, hook, CTA, and caption generator."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from hce.evaluation.evaluator import CopyEvaluator, EvaluationReport
from hce.execution.audience_analyzer import AudienceAnalysis, AudienceAnalyzer
from hce.execution.product_analyzer import ProductAnalysis, ProductAnalyzer, ProductInput
from hce.execution.strategy_selector import CreativeStrategy, StrategySelector
from hce.knowledge.retrieval import KnowledgeRetriever
from hce.language.refiner import NaturalLanguageRefiner


@dataclass
class VideoScene:
    scene_number: int
    duration_seconds: int
    visual_direction: str
    spoken_narration: str
    on_screen_text: str
    narrative_objective: str
    transition: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GeneratedAffiliateContent:
    product_analysis: ProductAnalysis
    audience_analysis: AudienceAnalysis
    strategy: CreativeStrategy
    hooks: list[str]
    scenes: list[VideoScene]
    cta: str
    caption: str
    alternative_angles: list[dict[str, str]]
    retrieved_knowledge_ids: list[str] = field(default_factory=list)
    refinement_report: dict[str, Any] = field(default_factory=dict)
    evaluation: EvaluationReport | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_analysis": self.product_analysis.to_dict(),
            "audience_analysis": self.audience_analysis.to_dict(),
            "strategy": self.strategy.to_dict(),
            "hooks": self.hooks,
            "scenes": [s.to_dict() for s in self.scenes],
            "cta": self.cta,
            "caption": self.caption,
            "alternative_angles": self.alternative_angles,
            "retrieved_knowledge_ids": self.retrieved_knowledge_ids,
            "refinement_report": self.refinement_report,
            "evaluation": self.evaluation.to_dict() if self.evaluation else None,
        }


def _platform_cta(platform: str, product_name: str, style: str) -> str:
    if platform == "tiktok":
        return (
            f"Kalau pas sama kebutuhan harianmu, detail varian dan ukuran {product_name} "
            "bisa langsung dicek lewat keranjang kuning di kiri bawah."
        )
    if platform == "shopee_video":
        return (
            f"Buat yang mau lihat pilihan varian dan spesifikasi lengkap {product_name}, "
            "tinggal klik tautan produk di keranjang video ini."
        )
    if platform == "instagram_reels":
        return (
            f"Detail lengkap {product_name} sudah dicantumkan di tautan pada bio dan caption "
            "kalau kamu ingin cek sebelum menentukan pilihan."
        )
    # facebook_reels
    if style == "polite_neutral":
        return (
            f"Untuk melihat detail ukuran, bahan, dan variasi {product_name}, "
            "silakan cek tautan produk yang tercantum di caption atau kolom komentar."
        )
    return (
        f"Detail variasi dan ukuran {product_name} bisa dilihat lewat tautan di caption "
        "atau kolom komentar."
    )


def _format_specs_phrase(specs: dict[str, Any]) -> str:
    if not specs:
        return ""
    parts = [f"{k} {v}" for k, v in list(specs.items())[:3]]
    return ", ".join(parts)


class AffiliateContentGenerator:
    """Produces complete, natural, accuracy-checked Indonesian affiliate content."""

    def __init__(
        self,
        retriever: KnowledgeRetriever,
        refiner: NaturalLanguageRefiner | None = None,
        evaluator: CopyEvaluator | None = None,
    ) -> None:
        self.retriever = retriever
        self.refiner = refiner or NaturalLanguageRefiner()
        self.evaluator = evaluator or CopyEvaluator()
        self.product_analyzer = ProductAnalyzer()
        self.audience_analyzer = AudienceAnalyzer()
        self.strategy_selector = StrategySelector()

    def generate(
        self,
        product: ProductInput,
        *,
        platform: str | None = None,
    ) -> GeneratedAffiliateContent:
        target_platform = (platform or product.target_platform or "tiktok").lower()
        p_analysis = self.product_analyzer.analyze(product)
        a_analysis = self.audience_analyzer.analyze(
            p_analysis, supplied_audience=product.supplied_audience, platform=target_platform
        )
        strategy = self.strategy_selector.select(
            p_analysis, a_analysis, target_platform, self.retriever
        )

        hooks = self._build_hooks(p_analysis, a_analysis, strategy)
        scenes = self._build_scenes(p_analysis, a_analysis, strategy, hooks[0])
        cta = _platform_cta(target_platform, product.name, a_analysis.communication_style)
        caption = self._build_caption(p_analysis, a_analysis, target_platform)
        alt_angles = self._build_alternative_angles(p_analysis, strategy)

        # Pass generated spoken & written lines through NaturalLanguageRefiner
        audit = self.refiner.audit_script_fields(
            hooks=hooks,
            scene_narrations=[s.spoken_narration for s in scenes],
            cta=cta,
            caption=caption,
            register=a_analysis.communication_style,
            available_evidence=p_analysis.available_evidence,
        )
        hooks = audit["hooks"]
        for idx, refined_narr in enumerate(audit["scene_narrations"]):
            scenes[idx].spoken_narration = refined_narr
        cta = audit["cta"]
        caption = audit["caption"]

        evaluation = self.evaluator.evaluate(
            hooks=hooks,
            scenes=[s.to_dict() for s in scenes],
            cta=cta,
            caption=caption,
            platform=target_platform,
            product_data=product.to_dict(),
        )

        return GeneratedAffiliateContent(
            product_analysis=p_analysis,
            audience_analysis=a_analysis,
            strategy=strategy,
            hooks=hooks,
            scenes=scenes,
            cta=cta,
            caption=caption,
            alternative_angles=alt_angles,
            retrieved_knowledge_ids=strategy.retrieved_concept_ids,
            refinement_report=audit,
            evaluation=evaluation,
        )

    def _build_hooks(
        self,
        p: ProductAnalysis,
        a: AudienceAnalysis,
        s: CreativeStrategy,
    ) -> list[str]:
        feat0 = p.verified_features[0] if p.verified_features else p.what_it_does
        sit0 = a.relevant_situations[0] if a.relevant_situations else "kebutuhan harian"
        obj0 = a.possible_objections[0] if a.possible_objections else "kualitas bahan dan fungsinya"

        if s.strategy_name == "problem_solution":
            h1 = f"Kalau {sit0}, coba perhatikan desain {p.name} ini."
            h2 = f"Solusi simpel tanpa ribet buat masalah {sit0}: {feat0}."
            h3 = f"Banyak yang sering {obj0}, nah ini detail {p.name} yang perlu dilihat dulu."
        elif s.strategy_name == "product_demonstration":
            h1 = f"Lihat langsung cara kerja {p.name} dengan fitur {feat0}."
            h2 = f"Untuk kebutuhan harian yang sering terhambat karena {sit0}, cek fungsi nyatanya di sini."
            h3 = f"Ringkas, jelas, dan praktis: begini detail {p.name} saat dipakai."
        elif s.strategy_name == "objection_handling":
            h1 = f"Sering {obj0} waktu pilih produk sejenis?"
            h2 = f"Kalau {sit0}, fitur {feat0} ini cukup membantu bikin pemakaian lebih nyaman."
            h3 = f"Sebelum beli, lihat dulu kecocokan {p.name} dengan rutinitas harianmu."
        elif s.strategy_name == "everyday_experience":
            h1 = f"Pas lagi menghadapi {sit0}, fitur {feat0} ini kerasa paling kepakai."
            h2 = f"Buat mobilitas harian yang ringkas, ini detail {p.name} yang patut dicek."
            h3 = f"Sederhana tapi membantu saat {sit0}."
        else:
            h1 = f"Buat yang lagi cari perlengkapan praktis saat {sit0}, cek detail {p.name} ini."
            h2 = f"Nilai utamanya ada di {feat0} supaya pemakaian harian lebih rapi dan nyaman."
            h3 = f"Sebelum menentukan pilihan, lihat fungsi dan detail {p.name} berikut."

        return [h1, h2, h3]

    def _build_scenes(
        self,
        p: ProductAnalysis,
        a: AudienceAnalysis,
        s: CreativeStrategy,
        primary_hook: str,
    ) -> list[VideoScene]:
        durations = s.scene_durations
        purposes = s.scene_purposes
        benefits = p.practical_benefits or [p.what_it_does]
        features = p.verified_features or [p.what_it_does]
        specs_phrase = _format_specs_phrase(p.verified_specs)
        objection = a.possible_objections[0] if a.possible_objections else "kecocokan ukuran dan bahan"
        situation = a.relevant_situations[0] if a.relevant_situations else "aktivitas harian"

        scenes: list[VideoScene] = []
        total = len(durations)

        for idx, (dur, purpose) in enumerate(zip(durations, purposes)):
            scene_num = idx + 1
            if idx == 0:
                scenes.append(
                    VideoScene(
                        scene_number=scene_num,
                        duration_seconds=dur,
                        visual_direction=f"Close-up langsung {p.name} di konteks {situation}; gerak kamera jelas tanpa efek berlebihan.",
                        spoken_narration=primary_hook,
                        on_screen_text=features[0][:42],
                        narrative_objective=purpose,
                        transition="Cut cepat langsung ke detail utama produk",
                    )
                )
            elif idx == total - 1:
                cta_line = _platform_cta(s.platform, p.name, a.communication_style)
                scenes.append(
                    VideoScene(
                        scene_number=scene_num,
                        duration_seconds=dur,
                        visual_direction=f"Shot utuh {p.name} beserta varian/tampilan rapi dengan petunjuk arah tautan produk.",
                        spoken_narration=cta_line,
                        on_screen_text="Cek detail & varian produk",
                        narrative_objective=purpose,
                        transition="Tahan visual produk 1 detik di akhir",
                    )
                )
            elif idx == 1:
                b0 = benefits[0].split("->", 1)[-1].strip()
                b1 = benefits[1].split("->", 1)[-1].strip() if len(benefits) > 1 else ""
                narr = f"Dari detail produknya, {p.name} punya {features[0].lower()} sehingga {b0}."
                if b1:
                    narr += f" Ditambah {features[1].lower()} yang bikin {b1}."
                scenes.append(
                    VideoScene(
                        scene_number=scene_num,
                        duration_seconds=dur,
                        visual_direction=f"Peragaan bagian utama: sorot {features[0]} dan cara penggunaannya di situasi nyata.",
                        spoken_narration=narr,
                        on_screen_text=(features[1] if len(features) > 1 else features[0])[:42],
                        narrative_objective=purpose,
                        transition="Transisi geser ke sudut dekat bagian detail",
                    )
                )
            elif idx == 2:
                extra_feat = features[2] if len(features) > 2 else features[-1]
                spec_part = f" Spesifikasi tercatatnya meliputi {specs_phrase}." if specs_phrase else ""
                narr = (
                    f"Soal pertanyaan soal {objection}, produk ini mengandalkan {extra_feat.lower()}."
                    f"{spec_part} Jadi lebih jelas sebelum dipakai untuk kebutuhan harian."
                )
                scenes.append(
                    VideoScene(
                        scene_number=scene_num,
                        duration_seconds=dur,
                        visual_direction=f"Shot jarak dekat tekstur, sambungan, atau detail {extra_feat} untuk menjawab keraguan pembeli.",
                        spoken_narration=narr,
                        on_screen_text=(specs_phrase[:42] if specs_phrase else extra_feat[:42]),
                        narrative_objective=purpose,
                        transition="Potong halus ke adegan ringkasan manfaat",
                    )
                )
            else:
                evidence_line = (
                    f"Informasi yang tersedia menekankan {p.available_evidence[0]}."
                    if p.available_evidence
                    else "Pastikan cara pasang atau pemakaian mengikuti petunjuk produk agar hasilnya optimal."
                )
                scenes.append(
                    VideoScene(
                        scene_number=scene_num,
                        duration_seconds=dur,
                        visual_direction="Perlihatkan ukuran produk dalam genggaman atau posisi terpasang agar skala terlihat jujur.",
                        spoken_narration=f"Hal penting yang perlu diperhatikan, sesuaikan pilihan ini dengan kondisi pemakaianmu. {evidence_line}",
                        on_screen_text="Sesuaikan dengan kebutuhan",
                        narrative_objective=purpose,
                        transition="Cut rapi menuju penutup",
                    )
                )

        return scenes

    def _build_caption(
        self,
        p: ProductAnalysis,
        a: AudienceAnalysis,
        platform: str,
    ) -> str:
        feat_summary = ", ".join(p.verified_features[:2])
        specs_summary = _format_specs_phrase(p.verified_specs)
        spec_clause = f" ({specs_summary})" if specs_summary else ""
        if platform == "shopee_video":
            return (
                f"{p.name}{spec_clause} — mengandalkan {feat_summary}. "
                "Cocok buat yang butuh solusi rapi untuk kebutuhan harian. Detail varian ada di tautan produk. "
                "#rekomendasiproduk #shopeevideo #perlengkapanharian"
            )
        if platform == "facebook_reels":
            return (
                f"Berbagi info praktis tentang {p.name}{spec_clause}. "
                f"Fitur utamanya ada di {feat_summary}. Silakan cek tautan di kolom komentar atau caption untuk detail lengkap. "
                "#infoproduk #kebutuhanharian"
            )
        if platform == "instagram_reels":
            return (
                f"{p.name}{spec_clause}: ringkas dengan {feat_summary}. "
                "Detail produk dan pilihan variannya bisa dilihat lewat tautan di bio/caption. "
                "#affiliateindonesia #reviewjujur #produkpraktis"
            )
        return (
            f"{p.name}{spec_clause} — bantu bikin {a.relevant_situations[0] if a.relevant_situations else 'aktivitas harian'} lebih rapi dengan {feat_summary}. "
            "Cek detail varian di keranjang kiri bawah. #tiktokaffiliate #perlengkapanharian #infoproduk"
        )

    def _build_alternative_angles(
        self,
        p: ProductAnalysis,
        chosen: CreativeStrategy,
    ) -> list[dict[str, str]]:
        candidates = [
            (
                "comparison",
                "Perbandingan Kondisi Sebelum vs Sesudah Penataan",
                f"Bandingkan kondisi tanpa {p.name} dengan kondisi setelah ditata memakai fitur {p.verified_features[0] if p.verified_features else p.name} secara visual tanpa klaim berlebihan.",
            ),
            (
                "curiosity",
                "Sudut Detail Teknis yang Sering Terlewat",
                f"Mulai dari satu detail spesifik ({next(iter(p.verified_specs.items()), ('desain', p.name))}) lalu jelaskan mengapa detail itu berdampak ke pemakaian harian.",
            ),
            (
                "objection_handling",
                "Sudut Menjawab Keraguan Pembeli Pertama Kali",
                f"Langsung bahas keraguan utama soal {p.category} sebelum menjelaskan manfaat inti dan mengarahkan ke keranjang.",
            ),
        ]
        alternatives = [
            {"strategy": st, "angle_title": title, "outline": outline}
            for st, title, outline in candidates
            if st != chosen.strategy_name
        ]
        return alternatives[:2]
