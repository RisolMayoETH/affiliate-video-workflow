"""Grounded product analyzer that maps verified features to practical benefits without fabrication."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ProductInput:
    product_id: str
    name: str
    category: str
    description: str
    verified_features: list[str]
    price_idr: float | int | None = None
    verified_specs: dict[str, Any] = field(default_factory=dict)
    available_evidence: list[str] = field(default_factory=list)
    target_platform: str = "tiktok"
    supplied_audience: dict[str, Any] | None = None
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProductInput:
        return cls(
            product_id=str(data["product_id"]),
            name=str(data["name"]),
            category=str(data["category"]),
            description=str(data["description"]),
            verified_features=[str(x) for x in data.get("verified_features", [])],
            price_idr=data.get("price_idr"),
            verified_specs=dict(data.get("verified_specs", {})),
            available_evidence=[str(x) for x in data.get("available_evidence", [])],
            target_platform=str(data.get("target_platform", "tiktok")),
            supplied_audience=data.get("supplied_audience"),
            notes=str(data.get("notes", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProductAnalysis:
    product_id: str
    name: str
    category: str
    price_idr: float | int | None
    price_tier: str
    what_it_is: str
    what_it_does: str
    verified_features: list[str]
    verified_specs: dict[str, Any]
    practical_benefits: list[str]
    differentiating_characteristics: list[str]
    potential_buyer_motivations: list[str]
    available_evidence: list[str]
    missing_information: list[str]
    do_not_claim: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


FEATURE_BENEFIT_MAP: tuple[tuple[tuple[str, ...], str], ...] = (
    (
        ("tanpa bor", "tempel", "perekat"),
        "bisa dipasang di permukaan keramik atau dinding halus tanpa melubangi tembok",
    ),
    (
        ("stainless", "anti karat"),
        "lebih aman terkena air atau kelembapan harian dibanding bahan besi biasa",
    ),
    (
        ("usb", "rechargeable", "isi ulang", "cas"),
        "bisa dipakai lebih fleksibel di berbagai sudut tanpa harus terus menempel ke stopkontak",
    ),
    (
        ("lipat", "ringkas", "portable"),
        "mudah dirapikan atau dibawa sehingga tidak makan banyak ruang",
    ),
    (
        ("spf", "uv", "pa++"),
        "membantu melindungi kulit dari paparan sinar UV saat beraktivitas di luar ruangan",
    ),
    (
        ("gel", "ringan", "cepat meresap"),
        "terasa lebih ringan di kulit dan nyaman untuk pemakaian harian",
    ),
    (
        ("anti percikan", "tahan percikan", "water-repellent"),
        "membantu melindungi barang bawaan dari gerimis ringan atau cipratan air di perjalanan",
    ),
    (
        ("vacuum", "insulated", "tahan suhu"),
        "membantu menjaga minuman dingin atau hangat lebih stabil saat dibawa beraktivitas",
    ),
    (
        ("mata pisau", "chopper", "bumbu"),
        "mempercepat pencacahan bumbu dapur porsi harian tanpa perlu mengeluarkan blender besar",
    ),
    (
        ("3 mode", "mode cahaya", "dimmable", "led"),
        "pencahayaan bisa diatur menyesuaikan kondisi kerja, belajar, atau suasana santai",
    ),
)

CATEGORY_MOTIVATION_MAP: dict[str, list[str]] = {
    "household": [
        "ingin area rumah atau kamar mandi terlihat lebih rapi dan lega",
        "menghindari pemasangan rumit atau merusak tembok sewa/kos",
    ],
    "kitchen": [
        "menghemat waktu persiapan masak porsi harian",
        "mencari alat yang praktis dibersihkan setelah dipakai",
    ],
    "beauty_personal_care": [
        "mencari perlindungan atau perawatan harian yang nyaman dipakai tanpa rasa berat",
        "khawatir produk terasa lengket atau mengganggu rutinitas pagi",
    ],
    "fashion": [
        "butuh barang yang fungsional untuk mobilitas harian namun tetap enak dipadukan",
        "membutuhkan ruang penyimpanan cukup untuk barang penting sehari-hari",
    ],
    "electronics": [
        "ingin pencahayaan atau perangkat kerja yang praktis dan minim kabel berantakan",
        "membutuhkan kontrol fungsi yang sesuai aktivitas belajar atau kerja",
    ],
    "everyday_consumer": [
        "ingin barang tahan pakai untuk menemani aktivitas kerja, kuliah, atau perjalanan",
        "menginginkan kepraktisan perawatan dan ukuran yang pas dibawa",
    ],
}


def _classify_price_tier(price_idr: float | int | None) -> str:
    if price_idr is None:
        return "unknown"
    val = float(price_idr)
    if val < 100_000:
        return "budget"
    if val <= 300_000:
        return "mid"
    return "premium"


def _translate_feature_to_benefit(feature: str) -> str:
    low = feature.lower()
    for keywords, benefit in FEATURE_BENEFIT_MAP:
        if any(k in low for k in keywords):
            return f"{feature} -> {benefit}"
    return f"{feature} -> mendukung pemakaian harian secara lebih praktis"


class ProductAnalyzer:
    """Extracts verified capabilities, practical benefits, and strict truth boundaries."""

    def analyze(self, product: ProductInput) -> ProductAnalysis:
        price_tier = _classify_price_tier(product.price_idr)
        practical_benefits = [
            _translate_feature_to_benefit(f) for f in product.verified_features
        ]

        differentiators: list[str] = []
        for feat in product.verified_features[:3]:
            differentiators.append(feat)
        for key, val in list(product.verified_specs.items())[:2]:
            differentiators.append(f"{key}: {val}")

        motivations = list(
            CATEGORY_MOTIVATION_MAP.get(
                product.category,
                ["membutuhkan solusi praktis untuk aktivitas sehari-hari"],
            )
        )

        missing: list[str] = []
        if product.price_idr is None:
            missing.append("price_idr belum tersedia; jangan menyebut kisaran harga atau promo.")
        if not product.verified_specs:
            missing.append("verified_specs kosong; hindari mengarang ukuran atau kapasitas angka.")
        if not product.available_evidence:
            missing.append("available_evidence kosong; fokus pada fakta fitur dan jangan mengarang testimoni atau durasi pemakaian pribadi.")
        if not product.supplied_audience:
            missing.append("supplied_audience tidak disediakan; profil audiens harus ditandai sebagai hipotesis.")

        evidence_blob = " ".join(product.available_evidence).lower()
        do_not_claim = [
            "Jangan mengarang diskon, flash sale, atau batas stok yang tidak ada di data.",
            "Jangan menambahkan spesifikasi angka atau sertifikasi di luar verified_specs dan description.",
        ]
        if not any(k in evidence_blob for k in ("pengalaman", "pribadi", "tested", "pemakaian")):
            do_not_claim.append(
                "Jangan mengaku sudah memakai produk secara pribadi dalam jangka waktu tertentu."
            )
        if not any(k in evidence_blob for k in ("testimoni", "ulasan", "review")):
            do_not_claim.append("Jangan mengutip testimoni pembeli fiktif.")

        return ProductAnalysis(
            product_id=product.product_id,
            name=product.name,
            category=product.category,
            price_idr=product.price_idr,
            price_tier=price_tier,
            what_it_is=product.name,
            what_it_does=product.description.strip(),
            verified_features=list(product.verified_features),
            verified_specs=dict(product.verified_specs),
            practical_benefits=practical_benefits,
            differentiating_characteristics=differentiators,
            potential_buyer_motivations=motivations,
            available_evidence=list(product.available_evidence),
            missing_information=missing,
            do_not_claim=do_not_claim,
        )
