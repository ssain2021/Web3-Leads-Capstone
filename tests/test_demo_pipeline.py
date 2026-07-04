from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from demo_pipeline import DemoLead, dedupe_demo_leads, extract_demo_leads, read_jsonl, run_demo_pipeline


class DemoPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_path = PROJECT_ROOT / "data" / "sample" / "sample_events.jsonl"
        self.events = read_jsonl(self.sample_path)

    def test_sample_event_contract(self) -> None:
        result = run_demo_pipeline(output_dir=Path(tempfile.mkdtemp()))

        self.assertEqual(result["events_read"], 103)
        self.assertEqual(result["raw_leads"], 3)
        self.assertEqual(result["deduped_leads"], 3)

        targets = {lead["target_company"] for lead in result["top_leads"]}
        self.assertEqual(targets, {"Gnosis Pay", "Hyperlane", "Kusama"})

    def test_rejects_noise_events(self) -> None:
        leads = extract_demo_leads(self.events)
        retained_ids = {lead.source_event_ids for lead in leads}
        rejected_ids = {
            str(event["event_id"])
            for event in self.events
            if event.get("sample_label") == "rejected_feed_event"
        }

        self.assertGreaterEqual(len(rejected_ids), 100)
        self.assertTrue(retained_ids.isdisjoint(rejected_ids))

    def test_evidence_types_for_known_positive_events(self) -> None:
        leads = {lead.source_event_ids: lead for lead in extract_demo_leads(self.events)}

        self.assertEqual(leads["82fbe323fd54ccecd679a20c"].evidence_type, "vendor_search")
        self.assertEqual(leads["1f27d1d09171b5525bf89b59"].evidence_type, "rfp_or_grant")
        self.assertEqual(leads["00f6c2c7700be1c2f1323a36"].evidence_type, "rfp_or_grant")

    def test_dedupe_keeps_highest_confidence_for_same_company_and_type(self) -> None:
        low = DemoLead(
            opportunity_id="lead_low",
            title="Lower confidence",
            target_company="Aave",
            summary="summary",
            evidence_type="rfp_or_grant",
            evidence_snippet="snippet",
            suggested_outreach_angle="outreach",
            confidence=0.65,
            source_event_ids="evt_low",
            source_url="https://example.com/low",
            status="KEEP",
        )
        high = DemoLead(
            opportunity_id="lead_high",
            title="Higher confidence",
            target_company="Aave",
            summary="summary",
            evidence_type="rfp_or_grant",
            evidence_snippet="snippet",
            suggested_outreach_angle="outreach",
            confidence=0.95,
            source_event_ids="evt_high",
            source_url="https://example.com/high",
            status="KEEP",
        )

        deduped = dedupe_demo_leads([low, high])

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].opportunity_id, "lead_high")

    def test_run_demo_writes_csv_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_demo_pipeline(output_dir=Path(tmp))

            csv_path = Path(result["csv_path"])
            report_path = Path(result["report_path"])
            html_path = Path(result["html_path"])
            self.assertTrue(csv_path.exists())
            self.assertTrue(report_path.exists())
            self.assertTrue(html_path.exists())
            report_text = report_path.read_text(encoding="utf-8")
            html_text = html_path.read_text(encoding="utf-8")
            self.assertIn("Gnosis Pay Celo Card Infrastructure", report_text)
            self.assertIn("sanitized real-data sample", report_text)
            self.assertIn("Web3 Signal-to-Lead Demo Report", html_text)
            self.assertIn("sanitized real-data sample", html_text)


if __name__ == "__main__":
    unittest.main()
