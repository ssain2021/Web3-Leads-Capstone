from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = PROJECT_ROOT / "skills" / "web3-lead-qualification" / "SKILL.md"


class AgentSkillTest(unittest.TestCase):
    def test_web3_lead_qualification_skill_exists(self) -> None:
        self.assertTrue(SKILL_PATH.exists())

    def test_skill_frontmatter_and_core_sections(self) -> None:
        text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("name: web3-lead-qualification", text)
        self.assertIn("description: Qualify Web3 RSS/forum/blog/governance events", text)
        self.assertIn("## Qualifying Action Surfaces", text)
        self.assertIn("## Rejection Rules", text)
        self.assertIn("## Required Output Fields", text)
        self.assertIn("## Confidence Calibration", text)

    def test_skill_names_required_output_fields(self) -> None:
        text = SKILL_PATH.read_text(encoding="utf-8")

        for field in (
            "opportunity_id",
            "target_company",
            "evidence_type",
            "evidence_snippet",
            "suggested_outreach_angle",
            "source_event_ids",
            "source_url",
        ):
            self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
