"""Build a small public demo sample from a private weekly pipeline run.

The script keeps only short, public-facing fields:
- selected final qualified opportunities,
- rejected/non-qualified feed events,
- source URLs,
- short summaries.

It intentionally excludes full scraped page bodies, database fields, credentials,
and private configuration.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_QUALIFIED_FILE = "Unique_Opportunities_24June_Published.csv"
DEFAULT_EVENTS_FILE = "Final_events.jsonl"
QUALIFIED_LIMIT = 3
REJECTED_LIMIT = 100
REJECTED_SKIP_RE = re.compile(
    r"\b(hackerone|malicious|exploit|vulnerability|bug bounty|attack|proof-of-concept|poc)\b",
    re.I,
)


def repair_text(value: Any) -> str:
    text = str(value or "")
    if any(marker in text for marker in ("â", "Ã", "Â")):
        try:
            text = text.encode("cp1252").decode("utf-8")
        except UnicodeError:
            pass
    return text


def compact_text(value: Any, max_chars: int = 520) -> str:
    text = re.sub(r"\s+", " ", repair_text(value)).strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0].rstrip() + "..."


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def read_qualified_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="cp1252") as f:
        return list(csv.DictReader(f))


def classify_evidence_type(row: dict[str, str]) -> str:
    categories = (row.get("categories") or "").lower()
    reason = (row.get("reason") or "").lower()
    title = (row.get("title") or "").lower()
    combined = " ".join([categories, reason, title])
    if "grant" in combined or "rfp" in combined or "bounty" in combined:
        return "rfp_or_grant"
    if "vendor" in combined or "proc" in combined:
        return "vendor_search"
    if "security" in combined or "audit" in combined:
        return "security"
    if "integrat" in combined:
        return "integration"
    return "partner_intake"


def event_is_actionable(event: dict[str, Any]) -> bool:
    direct = event.get("bd_signal")
    nested = (event.get("ai_enrichment") or {}).get("bd_signal")
    for signal in (direct, nested):
        if isinstance(signal, dict) and signal.get("has_action_surface") is True:
            return True
    return False


def event_summary(event: dict[str, Any]) -> str:
    return compact_text(
        event.get("AI_summary_text")
        or event.get("rss_summary_text")
        or event.get("summary_text")
        or event.get("description_raw")
        or event.get("body_text")
        or event.get("body_text_raw")
        or "",
        max_chars=520,
    )


def make_positive_record(row: dict[str, str], event: dict[str, Any] | None) -> dict[str, Any]:
    event_id = row.get("event_ids") or (event or {}).get("event_id") or row.get("opportunity_id")
    event_url = row.get("event_url") or (event or {}).get("url") or (event or {}).get("link") or ""
    source = repair_text((event or {}).get("source") or (event or {}).get("source_name") or "")
    if not source:
        source = compact_text(row.get("sources"), 120)

    return {
        "event_id": event_id,
        "title": compact_text(row.get("event_titles") or row.get("title"), 180),
        "opportunity_title": compact_text(row.get("title"), 180),
        "summary_text": compact_text(row.get("summary"), 620),
        "opportunity_details": compact_text(row.get("opportunity_details"), 620),
        "source": source,
        "url": event_url,
        "published_at": (event or {}).get("published_at") or row.get("time_found") or "",
        "target_company": row.get("target_company") or "",
        "evidence_type": classify_evidence_type(row),
        "suggested_outreach_angle": compact_text(row.get("suggested_outreach_angle"), 260),
        "confidence": float(row.get("confidence") or 0.95),
        "sample_label": "qualified_published",
    }


def make_rejected_record(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event.get("event_id") or "",
        "title": compact_text(event.get("title") or event.get("title_text") or event.get("title_raw"), 180),
        "summary_text": event_summary(event),
        "source": repair_text(event.get("source") or event.get("source_name") or ""),
        "url": event.get("url") or event.get("link") or "",
        "published_at": event.get("published_at") or "",
        "evidence_type": "none",
        "sample_label": "rejected_feed_event",
    }


def rejected_event_is_safe_for_public_sample(record: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(record.get("title") or ""),
            str(record.get("summary_text") or ""),
            str(record.get("source") or ""),
            str(record.get("url") or ""),
        ]
    )
    return not REJECTED_SKIP_RE.search(text)


def build_sample(source_dir: Path, output_path: Path) -> dict[str, int]:
    qualified_rows = read_qualified_csv(source_dir / DEFAULT_QUALIFIED_FILE)
    events = read_jsonl(source_dir / DEFAULT_EVENTS_FILE)
    event_by_id = {str(event.get("event_id")): event for event in events}
    qualified_event_ids = {str(row.get("event_ids") or "") for row in qualified_rows}

    selected_qualified = qualified_rows[:QUALIFIED_LIMIT]
    records: list[dict[str, Any]] = [
        make_positive_record(row, event_by_id.get(str(row.get("event_ids") or "")))
        for row in selected_qualified
    ]

    rejected_count = 0
    for event in events:
        event_id = str(event.get("event_id") or "")
        if not event_id or event_id in qualified_event_ids or event_is_actionable(event):
            continue
        record = make_rejected_record(event)
        if not record["title"] or not record["url"]:
            continue
        if not rejected_event_is_safe_for_public_sample(record):
            continue
        records.append(record)
        rejected_count += 1
        if rejected_count >= REJECTED_LIMIT:
            break

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "qualified_records": len(selected_qualified),
        "rejected_records": rejected_count,
        "total_records": len(records),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build sanitized public sample events.")
    parser.add_argument("--source-dir", required=True, help="Private pipeline Data folder")
    parser.add_argument(
        "--output",
        default="data/sample/sample_events.jsonl",
        help="Public sample JSONL output path",
    )
    args = parser.parse_args()

    result = build_sample(Path(args.source_dir), Path(args.output))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
