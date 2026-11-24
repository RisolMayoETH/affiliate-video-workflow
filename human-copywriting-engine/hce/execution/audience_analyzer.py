"""Audience analyzer separating supplied facts from inferred Indonesian buyer hypotheses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from hce.execution.product_analyzer import ProductAnalysis


@dataclass
class AudienceAnalysis:
    supplied_facts: dict[str, Any]
    inferred_hypotheses: list[str]
    likely_audience: str
    potential_needs: list[str]
    relevant_situations: list[str]
    purchase_motivations: list[str]
    possible_objections: list[str]
    product_familiarity: str
    communication_style: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


CATEGORY_AUDIENCE_PROFILES: dict[str, dict[str, Any]] = {
    "household": {
        "likely_audience": "Penghuni kos, kontrakan, atau keluarga muda di Indonesia yang ingin menata ruangan tetap rapi",
        "situations": [
            "botol sabun atau perlengkapan mandi sering menumpuk di lantai",
            "tidak diperbolehkan mengebor dinding keramik tempat tinggal",
        ],
        "objections": [
            "khawatir perekat cepat lepas di area kamar mandi yang lembap",
            "ragu apakah ukuran rak muat untuk botol ukuran standar",
        ],
        "familiarity": "solution_aware",
        "style": "practical_direct",
    },
    "kitchen": {
        "likely_audience": "Pekerja sibuk, anak kos, atau ibu rumah tangga yang memasak porsi harian",
        "situations": [
            "malas mengeluarkan blender besar hanya untuk mencacah sedikit bawang dan cabai",
            "butuh alat dapur ringkas yang cepat dicuci setelah dipakai",
        ],
        "objections": [
            "ragu kapasitas kecil cukup untuk kebutuhan masak harian",
            "khawatir daya tahan baterai dan kemudahan membersihkan pisau",
        ],
        "familiarity": "solution_aware",
        "style": "practical_direct",
    },
    "beauty_personal_care": {
        "likely_audience": "Pengguna perawatan kulit harian yang sering beraktivitas di luar maupun dalam ruangan",
        "situations": [
            "terburu-buru di pagi hari dan ingin sunscreen yang cepat meresap",
            "khawatir wajah terasa lengket atau berminyak setelah pemakaian",
        ],
        "objections": [
            "ragu apakah teksturnya benar-benar ringan dan nyaman dipakai ulang",
            "mempertanyakan kesesuaian dengan kondisi kulit pribadi",
        ],
        "familiarity": "problem_aware",
        "style": "friendly_informative",
    },
    "fashion": {
        "likely_audience": "Mahasiswa dan pekerja komuter harian yang membawa perlengkapan esensial",
        "situations": [
            "perjalanan berangkat kerja atau kuliah saat cuaca gerimis tipis",
            "butuh tas kasual ringan yang muat barang penting tanpa terlihat terlalu besar",
        ],
        "objections": [
            "khawatir bahan kain mudah tembus air saat gerimis",
            "ragu ruang kompartemen cukup untuk dompet, ponsel, dan barang harian",
        ],
        "familiarity": "solution_aware",
        "style": "casual_everyday",
    },
    "electronics": {
        "likely_audience": "Pelajar, mahasiswa, dan pekerja remote yang belajar atau bekerja di meja terbatas",
        "situations": [
            "pencahayaan kamar kurang nyaman untuk membaca atau mengetik malam hari",
            "stopkontak jauh dari posisi meja kerja atau tidak ingin kabel berserakan",
        ],
        "objections": [
            "ragu apakah tingkat terang cahaya cukup untuk kerja maupun baca",
            "ingin tahu fleksibilitas pengisian daya dan posisi lipatnya",
        ],
        "familiarity": "product_aware",
        "style": "friendly_informative",
    },
    "everyday_consumer": {
        "likely_audience": "Pekerja kantoran, mahasiswa, dan pengguna mobilitas harian yang membawa minuman sendiri",
        "situations": [
            "ingin minuman dingin atau hangat tetap nyaman diminum sepanjang jam kerja/kuliah",
            "mengurangi beli minuman kemasan di jalan tanpa bawa botol yang terlalu berat",
        ],
        "objections": [
            "ragu apakah tutup rapat tidak mudah bocor di dalam tas",
            "mempertimbangkan ukuran 500 ml cukup untuk aktivitas setengah hari",
        ],
        "familiarity": "product_aware",
        "style": "casual_everyday",
    },
}


class AudienceAnalyzer:
    """Separates user-supplied audience facts from grounded Indonesian audience hypotheses."""

    def analyze(
        self,
        product: ProductAnalysis,
        supplied_audience: dict[str, Any] | None = None,
        platform: str = "tiktok",
    ) -> AudienceAnalysis:
        supplied = {k: v for k, v in (supplied_audience or {}).items() if v}
        profile = CATEGORY_AUDIENCE_PROFILES.get(
            product.category,
            {
                "likely_audience": "Pembeli online Indonesia yang mencari perlengkapan harian praktis",
                "situations": ["menginginkan solusi yang mudah dipakai dalam rutinitas harian"],
                "objections": ["ingin memastikan fungsi, ukuran, dan kualitas bahan sesuai kebutuhan"],
                "familiarity": "solution_aware",
                "style": "casual_everyday",
            },
        )

        likely_audience = str(supplied.get("segment") or profile["likely_audience"])
        familiarity = str(supplied.get("familiarity") or profile["familiarity"])

        style = str(supplied.get("tone") or profile["style"])
        if platform == "facebook_reels" and not supplied.get("tone"):
            style = "polite_neutral"
        elif platform == "shopee_video" and not supplied.get("tone"):
            style = "practical_direct"

        inferred: list[str] = []
        if "segment" not in supplied:
            inferred.append(
                f"[Hipotesis] Target audiens disimpulkan dari kategori '{product.category}': {likely_audience}."
            )
        if "objections" not in supplied:
            inferred.append(
                f"[Hipotesis] Potensi keraguan pembeli disimpulkan dari sifat produk dan kategori."
            )
        if "familiarity" not in supplied:
            inferred.append(
                f"[Hipotesis] Tingkat kesadaran audiens diperkirakan pada tahap '{familiarity}'."
            )

        custom_objections = supplied.get("objections")
        objections = (
            [str(x) for x in custom_objections]
            if isinstance(custom_objections, list) and custom_objections
            else list(profile["objections"])
        )

        return AudienceAnalysis(
            supplied_facts=supplied,
            inferred_hypotheses=inferred,
            likely_audience=likely_audience,
            potential_needs=list(product.potential_buyer_motivations),
            relevant_situations=list(profile["situations"]),
            purchase_motivations=list(product.practical_benefits[:3]),
            possible_objections=objections,
            product_familiarity=familiarity,
            communication_style=style,
        )
