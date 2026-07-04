"""Small MCP server exposing capstone demo resources.

This is intentionally local and read-only. It lets the project demonstrate MCP
without requiring credentials or a live production database.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from demo_pipeline import read_jsonl, run_demo_pipeline
from settings import OUTPUT_DIR, SAMPLE_DATA_DIR


mcp = FastMCP("web3-leads")


@mcp.tool()
def list_sample_events() -> list[dict[str, Any]]:
    """Return the bundled public sample events."""

    return read_jsonl(SAMPLE_DATA_DIR / "sample_events.jsonl")


@mcp.tool()
def run_lead_demo() -> dict[str, Any]:
    """Run the deterministic demo lead pipeline."""

    return run_demo_pipeline(output_dir=OUTPUT_DIR)


@mcp.tool()
def read_demo_report() -> str:
    """Read the latest generated demo report."""

    report_path = OUTPUT_DIR / "demo_report.md"
    if not report_path.exists():
        run_demo_pipeline(output_dir=OUTPUT_DIR)
    return Path(report_path).read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
