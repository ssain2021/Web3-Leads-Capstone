from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from security import (
    REQUIRED_GITIGNORE_PATTERNS,
    build_security_report,
    check_mcp_server_read_only,
    check_no_obvious_inline_secrets,
    check_required_gitignore_patterns,
    check_sensitive_files_absent,
)


class SecurityChecksTest(unittest.TestCase):
    def _write_safe_project_fixture(self, root: Path) -> None:
        (root / ".gitignore").write_text("\n".join(sorted(REQUIRED_GITIGNORE_PATTERNS)), encoding="utf-8")
        src = root / "src"
        src.mkdir()
        (src / "mcp_server.py").write_text("def list_sample_events():\n    return []\n", encoding="utf-8")
        sample = root / "data" / "sample"
        sample.mkdir(parents=True)
        (sample / "sample_events.jsonl").write_text('{"event_id":"evt_1","title":"Safe sample"}\n', encoding="utf-8")

    def test_clean_public_fixture_is_public_demo_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_safe_project_fixture(root)
            report = build_security_report(root)

            self.assertTrue(report.safe_for_public_demo, report.to_dict())
            self.assertTrue(all(check.passed for check in report.checks), report.to_dict())

    def test_active_project_detects_local_sensitive_files_when_present(self) -> None:
        report = build_security_report(PROJECT_ROOT)
        sensitive_check = next(check for check in report.checks if check.name == "sensitive_files_absent")

        if (
            (PROJECT_ROOT / ".env").exists()
            or (PROJECT_ROOT / ".env.bak").exists()
            or (PROJECT_ROOT / "Database_Connection.csv").exists()
        ):
            self.assertFalse(sensitive_check.passed)
        else:
            self.assertTrue(sensitive_check.passed)

    def test_gitignore_check_fails_when_required_patterns_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")

            check = check_required_gitignore_patterns(root)

            self.assertFalse(check.passed)
            self.assertIn("Database_Connection.csv", check.detail)

    def test_sensitive_file_check_flags_env_backups_but_allows_example(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env.example").write_text("GOOGLE_API_KEY=\n", encoding="utf-8")
            (root / ".env.bak").write_text("GOOGLE_API_KEY=secret\n", encoding="utf-8")

            check = check_sensitive_files_absent(root)

            self.assertFalse(check.passed)
            self.assertIn(".env.bak", check.detail)
            self.assertNotIn(".env.example", check.detail)

    def test_sensitive_file_check_flags_database_connection_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text("\n".join(sorted(REQUIRED_GITIGNORE_PATTERNS)), encoding="utf-8")
            (root / "Database_Connection.csv").write_text("DB_PASSWORD,secret\n", encoding="utf-8")

            check = check_sensitive_files_absent(root)

            self.assertFalse(check.passed)
            self.assertIn("Database_Connection.csv", check.detail)

    def test_inline_secret_check_flags_assignments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.py").write_text("API_KEY = 'sk-test-value'\n", encoding="utf-8")

            check = check_no_obvious_inline_secrets(root)

            self.assertFalse(check.passed)
            self.assertIn("bad.py:1", check.detail)

    def test_mcp_read_only_check_flags_risky_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mcp_dir = root / "src"
            mcp_dir.mkdir()
            (mcp_dir / "mcp_server.py").write_text("import subprocess\n", encoding="utf-8")

            check = check_mcp_server_read_only(root)

            self.assertFalse(check.passed)
            self.assertIn("subprocess", check.detail)


if __name__ == "__main__":
    unittest.main()
