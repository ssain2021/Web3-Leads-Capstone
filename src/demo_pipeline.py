"""Deterministic demo pipeline for public capstone judging.

The original pipeline uses multiple LLM calls over a large RSS corpus. This
module gives the Kaggle project a reproducible local path that needs no API
keys, no database, and no private data.
"""

from __future__ import annotations

import csv
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from settings import OUTPUT_DIR, SAMPLE_DATA_DIR, ensure_runtime_dirs


ACTION_PATTERNS = {
    "rfp_or_grant": re.compile(r"\b(rfp|proposal|proposals|grant|application|applications)\b", re.I),
    "partner_intake": re.compile(r"\b(partner|partnership|pilot|intake|request access|contact)\b", re.I),
    "vendor_search": re.compile(r"\b(vendor|provider|procurement|pricing|maintenance|migration)\b", re.I),
    "integration": re.compile(r"\b(integrat|api|sdk|docs|dashboard|wallet|payment rail)\b", re.I),
    "security": re.compile(r"\b(security|audit|threat|scam|protection|risk)\b", re.I),
}

NOISE_PATTERNS = re.compile(
    r"\b(price|rumor|contest|giveaway|airdrop|meme|speculation|fan|art contest)\b",
    re.I,
)


@dataclass
class DemoLead:
    opportunity_id: str
    title: str
    target_company: str
    summary: str
    evidence_type: str
    evidence_snippet: str
    suggested_outreach_angle: str
    confidence: float
    source_event_ids: str
    source_url: str
    status: str


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _event_text(event: dict[str, Any]) -> str:
    return " ".join(
        str(event.get(key) or "")
        for key in (
            "title",
            "opportunity_title",
            "summary_text",
            "summary",
            "body_text",
            "opportunity_details",
            "description",
            "source",
        )
    )


def _target_company(event: dict[str, Any]) -> str:
    explicit_target = str(event.get("target_company") or "").strip()
    if explicit_target:
        return explicit_target
    source = str(event.get("source") or "").strip()
    if source:
        return re.sub(r"\s+(blog|governance|forum|feed)$", "", source, flags=re.I).strip()
    title = str(event.get("title") or "").strip()
    return title.split(" ", 1)[0] if title else "Unknown"


def _best_evidence_type(text: str) -> tuple[str, int]:
    scores: dict[str, int] = {}
    for label, pattern in ACTION_PATTERNS.items():
        scores[label] = len(pattern.findall(text))
    best_label, best_score = max(scores.items(), key=lambda item: item[1])
    return best_label if best_score else "none", best_score


def _snippet(text: str, max_chars: int = 260) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:max_chars].rstrip()


def extract_demo_leads(events: Iterable[dict[str, Any]]) -> list[DemoLead]:
    leads: list[DemoLead] = []
    for event in events:
        text = _event_text(event)
        evidence_type, signal_score = _best_evidence_type(text)
        provided_evidence_type = str(event.get("evidence_type") or "").strip()
        if provided_evidence_type:
            evidence_type = provided_evidence_type
            signal_score = max(signal_score, 3)
        noise_penalty = 2 if NOISE_PATTERNS.search(text) else 0
        net_score = signal_score - noise_penalty
        if evidence_type == "none" or net_score <= 0:
            continue

        event_id = str(event.get("event_id") or f"event_{len(leads) + 1}")
        target = _target_company(event)
        provided_confidence = event.get("confidence")
        confidence = float(provided_confidence) if provided_confidence not in {None, ""} else min(
            0.95,
            max(0.55, 0.55 + (net_score * 0.1)),
        )
        title = str(event.get("opportunity_title") or event.get("title") or "Untitled Web3 opportunity").strip()
        source_url = str(event.get("url") or event.get("event_url") or event.get("link") or "").strip()
        action = {
            "rfp_or_grant": "Prepare a proposal and respond through the published application path.",
            "partner_intake": "Contact the ecosystem or partnerships team with a focused pilot proposal.",
            "vendor_search": "Send a concise vendor capability note with migration, pricing, and prior work.",
            "integration": "Review the integration docs and propose a technical evaluation call.",
            "security": "Offer a security, risk, or threat-intelligence integration discussion.",
        }.get(evidence_type, "Review the source and qualify the next outreach step.")
        action = str(event.get("suggested_outreach_angle") or action).strip()

        leads.append(
            DemoLead(
                opportunity_id=f"lead_{event_id}",
                title=title,
                target_company=target,
                summary=_snippet(text, 420),
                evidence_type=evidence_type,
                evidence_snippet=_snippet(text),
                suggested_outreach_angle=action,
                confidence=round(confidence, 2),
                source_event_ids=event_id,
                source_url=source_url,
                status="KEEP",
            )
        )

    leads.sort(key=lambda lead: (-lead.confidence, lead.target_company, lead.title))
    return leads


def dedupe_demo_leads(leads: Iterable[DemoLead]) -> list[DemoLead]:
    winners: dict[tuple[str, str], DemoLead] = {}
    for lead in leads:
        key = (lead.target_company.lower(), lead.evidence_type)
        current = winners.get(key)
        if current is None or lead.confidence > current.confidence:
            winners[key] = lead
    return sorted(winners.values(), key=lambda lead: (-lead.confidence, lead.target_company))


def write_leads_csv(leads: Iterable[DemoLead], path: Path) -> None:
    rows = [asdict(lead) for lead in leads]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(DemoLead.__dataclass_fields__.keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(leads: list[DemoLead], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Web3 Business Leads Demo Report",
        "",
        f"Total leads retained: {len(leads)}",
        "",
        "Note: This public demo uses a small sanitized real-data sample from the June 24 pipeline run. "
        "It includes selected qualified opportunities plus rejected feed events, while excluding full scraped article bodies, database fields, and private credentials.",
        "",
    ]
    for idx, lead in enumerate(leads, 1):
        lines.extend(
            [
                f"## {idx}. {lead.title}",
                "",
                f"- Target: {lead.target_company}",
                f"- Evidence type: {lead.evidence_type}",
                f"- Confidence: {lead.confidence}",
                f"- Outreach: {lead.suggested_outreach_angle}",
                f"- Source: {lead.source_url}",
                "",
                lead.evidence_snippet,
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_static_html_report(leads: list[DemoLead], path: Path) -> None:
    """Write a standalone HTML report for public demo/repo review."""

    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx, lead in enumerate(leads, 1):
        rows.append(
            f"""
            <article class="lead">
              <div class="rank">#{idx}</div>
              <div>
                <h2>{html.escape(lead.title)}</h2>
                <dl>
                  <div><dt>Target</dt><dd>{html.escape(lead.target_company)}</dd></div>
                  <div><dt>Evidence</dt><dd>{html.escape(lead.evidence_type)}</dd></div>
                  <div><dt>Confidence</dt><dd>{lead.confidence:.2f}</dd></div>
                  <div><dt>Source event</dt><dd>{html.escape(lead.source_event_ids)}</dd></div>
                </dl>
                <p class="outreach">{html.escape(lead.suggested_outreach_angle)}</p>
                <blockquote>{html.escape(lead.evidence_snippet)}</blockquote>
                <a href="{html.escape(lead.source_url)}">{html.escape(lead.source_url)}</a>
              </div>
            </article>
            """
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Web3 Signal-to-Lead Demo Report</title>
  <style>
    :root {{
      --ink: #17201d;
      --muted: #5f6f68;
      --paper: #f7f4ed;
      --line: #d8d0c2;
      --accent: #126b58;
      --accent-2: #b44d2a;
      --panel: #fffdf7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(120deg, rgba(18, 107, 88, 0.12), transparent 32%),
        linear-gradient(250deg, rgba(180, 77, 42, 0.10), transparent 36%),
        var(--paper);
      font-family: Georgia, "Times New Roman", serif;
    }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 48px 22px 64px; }}
    header {{ border-bottom: 2px solid var(--ink); padding-bottom: 22px; margin-bottom: 26px; }}
    h1 {{ font-size: 42px; margin: 0 0 10px; line-height: 1.05; }}
    .subtitle {{ color: var(--muted); font-size: 18px; max-width: 760px; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 24px 0;
    }}
    .metric {{
      border: 1px solid var(--line);
      background: rgba(255, 253, 247, 0.72);
      padding: 14px;
    }}
    .metric strong {{ display: block; font-size: 28px; }}
    .metric span {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; }}
    .lead {{
      display: grid;
      grid-template-columns: 58px 1fr;
      gap: 18px;
      margin-top: 16px;
      padding: 20px;
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: 0 10px 24px rgba(23, 32, 29, 0.06);
    }}
    .rank {{ color: var(--accent-2); font-size: 24px; font-weight: 700; }}
    h2 {{ margin: 0 0 12px; font-size: 22px; line-height: 1.2; }}
    dl {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin: 0 0 14px; }}
    dt {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    dd {{ margin: 3px 0 0; font-weight: 700; }}
    .outreach {{ border-left: 4px solid var(--accent); padding-left: 12px; }}
    blockquote {{ margin: 14px 0; color: var(--muted); }}
    a {{ color: var(--accent); overflow-wrap: anywhere; }}
    @media (max-width: 760px) {{
      h1 {{ font-size: 32px; }}
      .summary, dl {{ grid-template-columns: 1fr; }}
      .lead {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Web3 Signal-to-Lead Demo Report</h1>
      <p class="subtitle">A static, no-secret artifact generated from a sanitized real-data sample from the June 24 pipeline run. Full scraped bodies, database fields, and private credentials are excluded.</p>
    </header>
    <section class="summary">
      <div class="metric"><strong>{len(leads)}</strong><span>Retained leads</span></div>
      <div class="metric"><strong>{len({lead.target_company for lead in leads})}</strong><span>Targets</span></div>
      <div class="metric"><strong>0</strong><span>Secrets required</span></div>
    </section>
    {''.join(rows)}
  </main>
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")


def run_demo_pipeline(
    input_path: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Run a reproducible no-key demo pipeline and return artifact paths."""

    ensure_runtime_dirs()
    source = Path(input_path) if input_path else SAMPLE_DATA_DIR / "sample_events.jsonl"
    out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    events = read_jsonl(source)
    raw_leads = extract_demo_leads(events)
    leads = dedupe_demo_leads(raw_leads)

    csv_path = out_dir / "demo_opportunities.csv"
    report_path = out_dir / "demo_report.md"
    html_path = out_dir / "demo_report.html"
    write_leads_csv(leads, csv_path)
    write_report(leads, report_path)
    write_static_html_report(leads, html_path)

    return {
        "input_path": str(source),
        "events_read": len(events),
        "raw_leads": len(raw_leads),
        "deduped_leads": len(leads),
        "csv_path": str(csv_path),
        "report_path": str(report_path),
        "html_path": str(html_path),
        "top_leads": [asdict(lead) for lead in leads[:5]],
    }
