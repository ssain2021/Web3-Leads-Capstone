"""Command-line entrypoints for the capstone demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from demo_pipeline import run_demo_pipeline
from security import security_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Web3 business lead capstone CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Run the no-secret sample pipeline")
    demo.add_argument("--input", default="", help="Optional JSONL event input")
    demo.add_argument("--output-dir", default="", help="Optional output directory")

    static_demo = sub.add_parser("build-static-demo", help="Build the no-secret static demo artifacts")
    static_demo.add_argument("--input", default="", help="Optional JSONL event input")
    static_demo.add_argument("--output-dir", default="", help="Optional output directory")

    sub.add_parser("security-check", help="Run public-demo security posture checks")

    args = parser.parse_args()

    if args.command in {"demo", "build-static-demo"}:
        result = run_demo_pipeline(
            input_path=Path(args.input) if args.input else None,
            output_dir=Path(args.output_dir) if args.output_dir else None,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "security-check":
        result = security_summary()
        print(json.dumps(result, indent=2))
        return 0 if bool(result["safe_for_public_demo"]) else 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
