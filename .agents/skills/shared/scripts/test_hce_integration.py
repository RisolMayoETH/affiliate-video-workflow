#!/usr/bin/env python3
"""Integration tests for Affiliate Video Director <-> Human Copywriting Engine (HCE) collaboration."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import campaign_check  # noqa: E402
import dialogue_timing  # noqa: E402
import hce_bridge  # noqa: E402

WORKSPACE_ROOT = SCRIPT_DIR.parents[3]


class TestHCEAVDIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = hce_bridge.load_hce_runtime()

    def test_hce_standalone_search_and_generate(self) -> None:
        hits = self.runtime.retriever.search("buyer psychology", limit=3)
        self.assertGreaterEqual(len(hits), 1)
        sample_product = json.loads(
            (self.runtime.hce_root / "tests" / "fixtures" / "sample_single_product.json").read_text(encoding="utf-8")
        )
        hce_in, avd_ctx = hce_bridge.normalize_product_input(sample_product, slug="rak-sudut")
        pkg = hce_bridge.run_hce_analysis(self.runtime, hce_in, avd_ctx, platform="tiktok")
        self.assertEqual(pkg["version"], 1)
        self.assertTrue(pkg["hooks"])
        self.assertTrue(pkg["retrieved_knowledge_ids"])
        self.assertEqual(pkg["evaluation"]["gate_status"], "PASSED")

    def test_structured_exchange_preserves_verified_facts(self) -> None:
        raw = {
            "product_id": "chopper-250",
            "name": "Chopper Mini USB 250 ml",
            "category": "Peralatan Dapur Ringkas",
            "price_idr": 69000,
            "description": "Chopper bumbu mini USB berkapasitas 250 ml dengan 3 mata pisau stainless steel.",
            "verified_features": [
                "Kapasitas mangkuk 250 ml",
                "Tiga mata pisau stainless steel",
                "Pengisian daya USB 30 watt",
            ],
            "verified_specs": {"kapasitas": "250 ml", "daya": "30 watt"},
            "target_platform": "instagram-reels",
        }
        hce_in, avd_ctx = hce_bridge.normalize_product_input(raw, slug="chopper-mini")
        self.assertEqual(hce_in["category"], "kitchen")
        self.assertEqual(hce_in["target_platform"], "instagram_reels")
        self.assertEqual(avd_ctx["original_category"], "Peralatan Dapur Ringkas")
        pkg = hce_bridge.run_hce_analysis(self.runtime, hce_in, avd_ctx, platform="instagram-reels")
        self.assertEqual(pkg["product_analysis"]["verified_specs"]["kapasitas"], "250 ml")
        self.assertTrue(any("diskon" in r.lower() for r in pkg["product_analysis"]["do_not_claim"]))

    def test_avd_review_detects_timing_digits_and_pacing_issues(self) -> None:
        bad_plan = {
            "version": 1,
            "slug": "bad-timing-test",
            "product_name": "Chopper Mini",
            "platform": "tiktok",
            "total_duration": 15.0,
            "consistency_locks": {"product_lock": "ok", "hand_lock": "ok", "environment_lighting_lock": "ok"},
            "scenes": [
                {
                    "id": 1,
                    "title": "Hook",
                    "timestamp": "00:00–00:02",
                    "duration": 2.0,
                    "visual_description": "POV di atas meja dapur Indonesia terang alami.",
                    "physical_action": "Tangan menekan tombol",
                    "product_interaction": "Memegang wadah",
                    "camera_angle": "POV 45 derajat",
                    "camera_movement": "Push-In — Tujuan: tarik perhatian",
                    "spoken_narration": "Ini chopper kapasitas 250 ml dengan 3 mata pisau super cepat yang harus dicoba banget hari ini juga.",
                    "marketing_purpose": "Hook",
                    "transition": "Cut",
                },
                {
                    "id": 2,
                    "title": "Demo",
                    "timestamp": "00:02–00:11",
                    "duration": 9.0,
                    "visual_description": "POV di atas meja dapur Indonesia terang alami.",
                    "physical_action": "Tangan mengoperasikan alat",
                    "product_interaction": "Menekan tombol",
                    "camera_angle": "POV 45 derajat",
                    "camera_movement": "Tracking — Tujuan: demo",
                    "spoken_narration": "Lihat hasilnya.",
                    "marketing_purpose": "Demo",
                    "transition": "Cut",
                },
                {
                    "id": 3,
                    "title": "CTA",
                    "timestamp": "00:11–00:15",
                    "duration": 4.0,
                    "visual_description": "Hero bersih dengan zona aman bawah untuk keranjang.",
                    "physical_action": "Meletakkan produk",
                    "product_interaction": "Produk rapi",
                    "camera_angle": "Eye level",
                    "camera_movement": "Dolly — Tujuan: CTA",
                    "spoken_narration": "Cek keranjang kuning kiri bawah sekarang juga ya.",
                    "marketing_purpose": "CTA",
                    "transition": "Hold",
                },
            ],
            "clip_plan": [
                {"id": "GEN-01", "file": "04-video/video-01.md", "scenes": [1, 2], "duration": 11.0},
                {"id": "GEN-02", "file": "04-video/video-02.md", "scenes": [3], "duration": 4.0},
            ],
        }
        ev = hce_bridge.avd_evaluate_plan(bad_plan, None)
        self.assertFalse(ev["passed"])
        categories = {r["category"] for r in ev["revision_requests"]}
        targets = {r["target_agent"] for r in ev["revision_requests"]}
        self.assertIn("dialogue_timing", categories)
        self.assertIn("scene_pacing", categories)
        self.assertIn("video_workability", categories)
        self.assertIn("hce", targets)
        self.assertIn("affiliate-video-director", targets)

    def test_hce_review_detects_cliches_integrity_violations_and_cta_mismatch(self) -> None:
        bad_plan = {
            "version": 1,
            "slug": "bad-copy-test",
            "product_name": "Chopper Mini",
            "platform": "instagram_reels",
            "total_duration": 10.0,
            "scenes": [
                {
                    "id": 1,
                    "title": "Hook",
                    "timestamp": "00:00–00:03",
                    "duration": 3.0,
                    "visual_description": "Produk diam di atas meja putih polos.",
                    "physical_action": "Diam saja",
                    "spoken_narration": "Halo guys! Wajib banget punya chopper ini!",
                    "narrative_objective": "hook_attention",
                    "marketing_purpose": "Hook",
                },
                {
                    "id": 2,
                    "title": "Body",
                    "timestamp": "00:03–00:07",
                    "duration": 4.0,
                    "visual_description": "Produk diam dari sudut berbeda.",
                    "physical_action": "Diam saja",
                    "spoken_narration": "Aku udah pakai enam bulan dan lagi diskon 70% stok terbatas.",
                    "narrative_objective": "core_demonstration",
                    "marketing_purpose": "Demo",
                },
                {
                    "id": 3,
                    "title": "CTA",
                    "timestamp": "00:07–00:10",
                    "duration": 3.0,
                    "visual_description": "Produk di meja.",
                    "physical_action": "Diam saja",
                    "spoken_narration": "Buruan cek keranjang kuning sekarang!",
                    "narrative_objective": "cta_closing",
                    "marketing_purpose": "CTA",
                },
            ],
            "publishing_draft": {
                "captions": {"instagram_reels": "Halo guys! Wajib banget beli chopper diskon 70%!"},
                "ctas": ["Cek keranjang kuning!"],
                "alt_hooks": ["Halo guys!"],
            },
        }
        prod_data = {
            "name": "Chopper Mini",
            "description": "Chopper bumbu mini USB",
            "verified_features": ["Kapasitas 250 ml", "Tiga mata pisau stainless"],
            "verified_specs": {"kapasitas": "250 ml"},
            "available_evidence": [],
        }
        ev = hce_bridge.hce_evaluate_plan(self.runtime, bad_plan, None, prod_data)
        self.assertFalse(ev["passed"])
        self.assertEqual(ev["hce_7d_evaluation"]["gate_status"], "FAILED_INTEGRITY_GATE")
        cats = {r["category"] for r in ev["revision_requests"]}
        self.assertIn("script_quality", cats)
        self.assertIn("cta_relevance", cats)
        self.assertIn("visual_strategy_alignment", cats)

    def test_autonomous_bidirectional_collaboration_and_version_history(self) -> None:
        raw_mock = {
            "product_id": "chopper-mini-250",
            "name": "Chopper Mini USB 250 ml",
            "category": "Peralatan Dapur Ringkas",
            "price_idr": 69000,
            "description": "Chopper bumbu mini USB berkapasitas 250 ml dengan 3 mata pisau stainless steel.",
            "verified_features": [
                "Kapasitas mangkuk 250 ml untuk bumbu harian",
                "Tiga mata pisau stainless steel",
                "Pengisian daya USB 30 watt tanpa kabel panjang",
                "Mangkuk transparan mudah dilepas dan dicuci",
            ],
            "verified_specs": {"kapasitas": "250 ml", "daya": "30 watt", "pisau": "3 mata pisau stainless"},
            "available_evidence": ["Spesifikasi listing: mangkuk 250 ml, 3 mata pisau stainless, pengisian USB 30 watt"],
            "target_platform": "tiktok",
        }
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_root = Path(tmp) / "campaigns"
            campaigns_root.mkdir()
            rc = campaign_check.init_campaign(campaigns_root, "chopper-test", raw_mock["name"], raw_mock["category"])
            self.assertEqual(rc, 0)
            cdir = campaigns_root / "chopper-test"
            ref_file = cdir / "01-product-review" / "references" / "listing-info.txt"
            ref_file.write_text("Chopper Mini 250 ml 3 mata pisau USB 30 watt", encoding="utf-8")

            summary = hce_bridge.run_collaboration_loop(
                self.runtime,
                cdir,
                raw_mock,
                platform="tiktok",
                max_iterations=3,
                write_deliverables=True,
            )
            self.assertTrue(summary["converged"])
            self.assertLessEqual(summary["iterations"], 3)
            self.assertGreaterEqual(summary["iterations"], 2)  # v1 triggered real revision -> v2 converged
            self.assertTrue((cdir / "_collaboration" / "review-round-1.json").is_file())
            self.assertTrue((cdir / "_collaboration" / "hce-package-v2.json").is_file())
            self.assertTrue((cdir / "_collaboration" / "avd-plan-v2.json").is_file())
            self.assertTrue((cdir / "_archive" / "storyboard.v1.md").is_file())

            timing_errs = campaign_check.validate_campaign_timing(cdir)
            self.assertEqual(timing_errs, [], f"Timing errors: {timing_errs}")
            collab_errs = campaign_check.validate_collaboration(cdir)
            self.assertEqual(collab_errs, [], f"Collab errors: {collab_errs}")

            # Verify video-02+ starts with Continue the video. and video-01 does not
            v1_text = (cdir / "04-video" / "video-01.md").read_text(encoding="utf-8")
            self.assertNotIn("Continue the video.", v1_text)
            v2_path = cdir / "04-video" / "video-02.md"
            if v2_path.is_file():
                v2_text = v2_path.read_text(encoding="utf-8")
                self.assertIn("```text\nContinue the video.", v2_text)

    def test_max_three_iterations_no_endless_loop(self) -> None:
        raw_mock = {
            "product_id": "loop-cap-prod",
            "name": "Rak Dapur Mini",
            "category": "household",
            "description": "Rak bumbu tempel dinding.",
            "verified_features": ["Pemasangan tempel tanpa bor"],
        }
        orig_avd_eval = hce_bridge.avd_evaluate_plan
        try:
            # Force AVD evaluator to always emit an unresolvable blocker to test hard cap = 3
            def _always_fail(plan, pkg, pdata=None):
                res = orig_avd_eval(plan, pkg, pdata)
                res["passed"] = False
                res["revision_requests"].append(
                    {
                        "request_id": "AVD-REQ-99",
                        "reviewer": "affiliate-video-director",
                        "target_agent": "affiliate-video-director",
                        "scene_number": 1,
                        "category": "visual_executability",
                        "severity": "blocker",
                        "issue": "Simulated persistent failure.",
                        "constraint": "Must resolve.",
                        "action_required": "Retry.",
                    }
                )
                return res

            hce_bridge.avd_evaluate_plan = _always_fail
            with tempfile.TemporaryDirectory() as tmp:
                cdir = Path(tmp) / "loop-cap-test"
                summary = hce_bridge.run_collaboration_loop(
                    self.runtime,
                    cdir,
                    raw_mock,
                    platform="tiktok",
                    max_iterations=10,  # Should be strictly clamped to 3
                    write_deliverables=False,
                )
                self.assertEqual(summary["max_iterations"], 3)
                self.assertEqual(summary["iterations"], 3)
                self.assertFalse(summary["converged"])
                self.assertTrue((cdir / "_collaboration" / "review-round-3.json").is_file())
                self.assertFalse((cdir / "_collaboration" / "review-round-4.json").exists())
        finally:
            hce_bridge.avd_evaluate_plan = orig_avd_eval

    def test_campaign_isolation_and_error_preservation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "campaigns"
            root.mkdir()
            campaign_check.init_campaign(root, "camp-a", "Produk A", "household")
            campaign_check.init_campaign(root, "camp-b", "Produk B", "kitchen")
            sentinel = root / "camp-b" / "01-product-review" / "references" / "keep.txt"
            sentinel.write_text("ORIGINAL_REF_DO_NOT_TOUCH", encoding="utf-8")

            # Run collaboration on camp-a only
            hce_bridge.run_collaboration_loop(
                self.runtime,
                root / "camp-a",
                {
                    "product_id": "prod-a",
                    "name": "Produk A Stainless",
                    "category": "household",
                    "description": "Rak tempel stainless tanpa bor.",
                    "verified_features": ["Tempel tanpa bor", "Bahan stainless"],
                },
                write_deliverables=True,
            )
            self.assertFalse((root / "camp-b" / "_collaboration" / "collaboration-summary.json").exists())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "ORIGINAL_REF_DO_NOT_TOUCH")

            # Simulate broken JSON error in camp-b and ensure existing files stay preserved
            (root / "camp-b" / "campaign.json").write_text("{BROKEN_JSON", encoding="utf-8")
            with self.assertRaises(Exception):
                hce_bridge.run_collaboration_loop(self.runtime, root / "camp-b", None, write_deliverables=True)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "ORIGINAL_REF_DO_NOT_TOUCH")

    def test_existing_avd_commands_backward_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cdir = Path(tmp) / "legacy-avd-campaign"
            for rel in (
                "01-product-review/references",
                "02-generated-assets/hero",
                "03-storyboard",
                "04-video",
                "05-publishing",
            ):
                (cdir / rel).mkdir(parents=True, exist_ok=True)

            (cdir / "01-product-review" / "references" / "ref.txt").write_text("Legacy ref", encoding="utf-8")
            (cdir / "01-product-review" / "product-brief.md").write_text("# Brief\n", encoding="utf-8")
            (cdir / "01-product-review" / "marketing-strategy.md").write_text("# Strategy\n", encoding="utf-8")
            (cdir / "01-product-review" / "image-prompts.md").write_text("# Prompts\n", encoding="utf-8")
            (cdir / "05-publishing" / "publishing-package.md").write_text(
                "# Publishing\nCek keranjang kuning kiri bawah.\n", encoding="utf-8"
            )

            (cdir / "03-storyboard" / "storyboard.md").write_text(
                "\n".join(
                    [
                        "# Storyboard — Legacy",
                        "",
                        "## Tabel Timing Dialog",
                        "",
                        "| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |",
                        "|---|---|---|---|---|---|---|",
                        '| 1 | 00:00–00:02.5 | 2.5 | "Masih repot masak bumbu harian?" | 11 | 2.20 | OK |',
                        '| 2 | 00:02.5–00:06.5 | 4.0 | "Tinggal tekan sekali, bumbu dapur langsung halus merata!" | 18 | 3.60 | OK |',
                        '| 3 | 00:06.5–00:09.5 | 3.0 | "Cek variannya di keranjang kuning ya!" | 12 | 2.40 | OK |',
                        "",
                        "## Prompt Gambar Storyboard",
                        "",
                        "```text",
                        "Clean 3-panel 9:16 storyboard.",
                        "```",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            (cdir / "04-video" / "video-01.md").write_text(
                "\n".join(
                    [
                        "# Video 01",
                        "Mencakup Adegan 1 dan Adegan 2.",
                        "",
                        "## Tabel Timing Dialog",
                        "",
                        "| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |",
                        "|---|---|---|---|---|---|---|",
                        '| 1 | 00:00–00:02.5 | 2.5 | "Masih repot masak bumbu harian?" | 11 | 2.20 | OK |',
                        '| 2 | 00:02.5–00:06.5 | 4.0 | "Tinggal tekan sekali, bumbu dapur langsung halus merata!" | 18 | 3.60 | OK |',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (cdir / "04-video" / "video-02.md").write_text(
                "\n".join(
                    [
                        "# Video 02",
                        "Mencakup Adegan 3.",
                        "",
                        "## Tabel Timing Dialog",
                        "",
                        "| Adegan | Timestamp | Durasi (dtk) | Dialog (VO) | Suku kata | Estimasi (dtk) | Status |",
                        "|---|---|---|---|---|---|---|",
                        '| 3 | 00:06.5–00:09.5 | 3.0 | "Cek variannya di keranjang kuning ya!" | 12 | 2.40 | OK |',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            legacy_cj = {
                "schema_version": "1.0",
                "slug": "legacy-avd-campaign",
                "product_name": "Produk Legacy",
                "stages": {
                    "review": {"status": "approved"},
                    "storyboard": {
                        "status": "approved",
                        "total_duration": 9.5,
                        "scenes": [
                            {"id": 1, "timestamp": "00:00–00:02.5", "duration": 2.5},
                            {"id": 2, "timestamp": "00:02.5–00:06.5", "duration": 4.0},
                            {"id": 3, "timestamp": "00:06.5–00:09.5", "duration": 3.0},
                        ],
                    },
                    "video": {
                        "status": "draft",
                        "max_clip_duration": 10.0,
                        "generations": [
                            {"id": "GEN-01", "file": "04-video/video-01.md", "scenes": [1, 2], "duration": 6.5},
                            {"id": "GEN-02", "file": "04-video/video-02.md", "scenes": [3], "duration": 3.0},
                        ],
                    },
                },
            }
            (cdir / "campaign.json").write_text(json.dumps(legacy_cj, indent=2), encoding="utf-8")

            errs = campaign_check.validate_campaign_timing(cdir)
            self.assertEqual(errs, [], f"Legacy campaign timing errors: {errs}")
            rc = campaign_check.check_stage(cdir, "video", validate_timing=True)
            self.assertEqual(rc, 0)
            sb_res = dialogue_timing.check_table(cdir / "03-storyboard" / "storyboard.md")
            self.assertTrue(sb_res["ok"])


if __name__ == "__main__":
    unittest.main()
