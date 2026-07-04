"""Security posture checks for the Web3 Leads capstone.

The checks are intentionally local and deterministic. They help demonstrate
that the public demo can run without secrets, private data, or write-enabled
external systems.
"""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from settings import PROJECT_ROOT, SAMPLE_DATA_DIR


REQUIRED_GITIGNORE_PATTERNS = {
    ".env",
    ".env.*",
    "!.env.example",
    "Database_Connection.csv",
    "data/raw/",
    "data/processed/",
    "data/output/",
    "*.log",
    "__pycache__/",
    "*.pyc",
}

SENSITIVE_FILENAMES = {
    ".env",
    "Database_Connection.csv",
    "credentials.json",
    "service_account.json",
    "secrets.json",
}
SENSITIVE_GLOBS = {
    ".env.*",
}
ALLOWED_SENSITIVE_FILENAMES = {
    ".env.example",
}

SECRET_NAME_RE = re.compile(
    r"\b(api[_-]?key|apikey|secret|password|token|access[_-]?token|bearer[_-]?token)\b",
    re.IGNORECASE,
)
SECRET_LITERAL_RE = re.compile(
    r"""(?ix)
    \b(api[_-]?key|apikey|secret|password|token|access[_-]?token|bearer[_-]?token)\b
    \s*[:=]\s*
    ['"]?([^'"\s,#]{8,})['"]?
    """
)
SECRET_VALUE_RE = re.compile(
    r"\b(sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9_]{12,}|Bearer\s+[A-Za-z0-9._-]{12,})\b"
)


@dataclass(frozen=True)
class SecurityCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class SecurityReport:
    safe_for_public_demo: bool
    checks: list[SecurityCheck]

    def to_dict(self) -> dict[str, object]:
        return {
            "safe_for_public_demo": self.safe_for_public_demo,
            "checks": [asdict(check) for check in self.checks],
        }


def _read_gitignore_patterns(project_root: Path) -> set[str]:
    gitignore = project_root / ".gitignore"
    if not gitignore.exists():
        return set()
    return {
        line.strip()
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def check_required_gitignore_patterns(project_root: Path = PROJECT_ROOT) -> SecurityCheck:
    patterns = _read_gitignore_patterns(project_root)
    missing = sorted(REQUIRED_GITIGNORE_PATTERNS - patterns)
    return SecurityCheck(
        name="required_gitignore_patterns",
        passed=not missing,
        detail="All required secret/runtime patterns are ignored." if not missing else f"Missing patterns: {missing}",
    )


def check_sensitive_files_absent(project_root: Path = PROJECT_ROOT) -> SecurityCheck:
    found_paths: set[Path] = set()
    for name in SENSITIVE_FILENAMES:
        found_paths.update(project_root.rglob(name))
    for pattern in SENSITIVE_GLOBS:
        found_paths.update(project_root.rglob(pattern))

    found = sorted(
        str(path.relative_to(project_root))
        for path in found_paths
        if "REFERENCE-Codes" not in path.parts and path.name not in ALLOWED_SENSITIVE_FILENAMES
    )
    return SecurityCheck(
        name="sensitive_files_absent",
        passed=not found,
        detail="No sensitive credential files found in active project tree." if not found else f"Found sensitive files: {found}",
    )


def _iter_scannable_files(project_root: Path) -> Iterable[Path]:
    allowed_suffixes = {".py", ".md", ".toml", ".txt", ".example", ".json", ".gitignore"}
    skip_parts = {
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "REFERENCE-Codes",
        "data",
        "tests",
    }
    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.name == ".env.example" or path.suffix.lower() in allowed_suffixes or path.name == ".gitignore":
            yield path


def check_no_obvious_inline_secrets(project_root: Path = PROJECT_ROOT) -> SecurityCheck:
    findings: list[str] = []
    for path in _iter_scannable_files(project_root):
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        if path.suffix.lower() == ".py":
            try:
                tree = ast.parse(text, filename=str(path))
            except SyntaxError:
                findings.append(f"{path.relative_to(project_root)}:syntax")
                continue
            for node in ast.walk(tree):
                targets: list[ast.expr] = []
                value: ast.expr | None = None
                if isinstance(node, ast.Assign):
                    targets = list(node.targets)
                    value = node.value
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                    value = node.value
                if value is None:
                    continue
                if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                    continue
                if len(value.value.strip()) < 8 and not SECRET_VALUE_RE.search(value.value):
                    continue
                for target in targets:
                    if isinstance(target, ast.Name) and SECRET_NAME_RE.search(target.id):
                        findings.append(f"{path.relative_to(project_root)}:{node.lineno}")
                    elif isinstance(target, ast.Attribute) and SECRET_NAME_RE.search(target.attr):
                        findings.append(f"{path.relative_to(project_root)}:{node.lineno}")
            continue

        for line_no, line in enumerate(text.splitlines(), 1):
            if path.name == ".env.example":
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            literal_match = SECRET_LITERAL_RE.search(stripped)
            value_match = SECRET_VALUE_RE.search(stripped)
            if literal_match:
                value = literal_match.group(2)
                if not value.startswith(("os.getenv", "os.environ", "getenv")):
                    findings.append(f"{path.relative_to(project_root)}:{line_no}")
            elif value_match and SECRET_NAME_RE.search(stripped):
                findings.append(f"{path.relative_to(project_root)}:{line_no}")
    return SecurityCheck(
        name="no_obvious_inline_secrets",
        passed=not findings,
        detail="No obvious inline secret assignments found." if not findings else f"Potential inline secrets: {findings[:10]}",
    )


def check_public_demo_uses_sample_data(project_root: Path = PROJECT_ROOT) -> SecurityCheck:
    sample_file = project_root / "data" / "sample" / "sample_events.jsonl"
    if not sample_file.exists():
        return SecurityCheck("public_demo_sample_data", False, f"Missing sample data: {sample_file}")
    text = sample_file.read_text(encoding="utf-8", errors="ignore")
    risky_markers = SECRET_VALUE_RE.findall(text)
    return SecurityCheck(
        name="public_demo_sample_data",
        passed=not risky_markers,
        detail="Sample data exists and contains no obvious secret markers."
        if not risky_markers
        else f"Sample data contains risky markers: {risky_markers}",
    )


def check_mcp_server_read_only(project_root: Path = PROJECT_ROOT) -> SecurityCheck:
    mcp_path = project_root / "src" / "mcp_server.py"
    if not mcp_path.exists():
        return SecurityCheck("mcp_server_read_only", False, "MCP server file is missing.")
    text = mcp_path.read_text(encoding="utf-8", errors="ignore")
    risky_calls = [
        token
        for token in ("requests.", "subprocess", "psycopg2", "OpenAI(", "os.remove", "unlink(", "rmdir(")
        if token in text
    ]
    return SecurityCheck(
        name="mcp_server_read_only",
        passed=not risky_calls,
        detail="MCP server exposes local read-only/demo tools only." if not risky_calls else f"Risky calls found: {risky_calls}",
    )


def build_security_report(project_root: Path = PROJECT_ROOT) -> SecurityReport:
    checks = [
        check_required_gitignore_patterns(project_root),
        check_sensitive_files_absent(project_root),
        check_no_obvious_inline_secrets(project_root),
        check_public_demo_uses_sample_data(project_root),
        check_mcp_server_read_only(project_root),
    ]
    return SecurityReport(
        safe_for_public_demo=all(check.passed for check in checks),
        checks=checks,
    )


def security_summary(project_root: Path = PROJECT_ROOT) -> dict[str, object]:
    """Return a JSON-serializable security report for ADK/CLI use."""

    return build_security_report(project_root).to_dict()
