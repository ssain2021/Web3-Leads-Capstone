from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import mcp_server


class MCPServerTest(unittest.TestCase):
    def test_mcp_server_exposes_expected_tools(self) -> None:
        self.assertTrue(hasattr(mcp_server, "mcp"))
        self.assertTrue(callable(mcp_server.list_sample_events))
        self.assertTrue(callable(mcp_server.run_lead_demo))
        self.assertTrue(callable(mcp_server.read_demo_report))

    def test_list_sample_events_returns_bundled_events(self) -> None:
        events = mcp_server.list_sample_events()

        self.assertEqual(len(events), 103)
        self.assertEqual(events[0]["target_company"], "Gnosis Pay")

    def test_run_lead_demo_and_read_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            original_output_dir = mcp_server.OUTPUT_DIR
            try:
                mcp_server.OUTPUT_DIR = Path(tmp)
                result = mcp_server.run_lead_demo()
                report = mcp_server.read_demo_report()
            finally:
                mcp_server.OUTPUT_DIR = original_output_dir

        self.assertEqual(result["deduped_leads"], 3)
        self.assertIn("Web3 Business Leads Demo Report", report)


if __name__ == "__main__":
    unittest.main()
