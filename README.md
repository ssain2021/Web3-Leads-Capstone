# Web3 Signal-to-Lead Agent

Kaggle AI Agents Intensive Vibe Coding Capstone project.

Track: **Agents for Business**

## Problem

Web3 business development teams monitor governance forums, protocol blogs, release notes, grants, RFPs, security updates, and ecosystem feeds. The signal is valuable, but the stream is noisy. Actionable opportunities are buried among price commentary, community posts, announcements with no buyer path, and duplicate coverage.

This project turns Web3 feed events into qualified, evidence-backed business leads.

## Solution

The system uses a multi-stage agent pipeline:

- RSS collector gathers events from configured Web3 sources.
- Preprocess agent cleans event text, extracts entities, contact hints, and action-surface fields.
- Gatekeeper agent filters noise and requires evidence of a concrete external action path.
- Finder agent proposes lead candidates with confidence subscores and source event IDs.
- Critic and Refiner agents improve quality, evidence grounding, and wording.
- Recovery and Watchlist agents rescue strong near misses.
- Dedupe stage consolidates repeated opportunities across multiple time horizons.
- ADK root agent exposes the capstone-facing orchestration tools.
- MCP server exposes sample events, demo execution, and report lookup.

## Course Concepts Demonstrated

- **Agent / multi-agent system with ADK:** `src/agent.py` defines a Google ADK `root_agent` with project tools.
- **MCP Server:** `src/mcp_server.py` exposes local read-only tools for sample events and demo reports.
- **Security features:** `.env.example`, `.gitignore`, no committed credentials, no database needed for public demo, and sanitized sample data.
- **Deployability:** CLI demo, ADK-compatible agent module, reproducible sample inputs and outputs.
- **Agent Skill / tool use:** `skills/web3-lead-qualification/SKILL.md` packages the Web3 lead qualification rules, while the ADK agent calls deterministic tools that run the demo pipeline and explain architecture.

## Project Structure

```text
Web3-Leads/
|-- REFERENCE-Codes/              # original scripts, preserved unchanged
|-- config/                       # public config copied from reference inputs
|-- data/
|   |-- sample/sample_events.jsonl
|   `-- output/                   # generated demo artifacts
|-- docs/
|-- skills/
|   `-- web3-lead-qualification/  # Agent Skill package
|-- src/
|   |-- agent.py                  # Google ADK root agent
|   |-- cli.py                    # local CLI demo
|   |-- demo_pipeline.py          # no-key deterministic demo path
|   |-- mcp_server.py             # local MCP tools
|   |-- security.py               # public-demo safety checks
|   `-- core_pipeline/            # adapted working copies of original scripts
|-- web3_leads_agent/             # ADK import bridge
`-- README.md
```

## Quick Start

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

Run the public no-secret demo:

```powershell
python src/cli.py demo
```

Build the static public demo artifacts:

```powershell
python src/cli.py build-static-demo
```

Run the public-demo security posture check:

```powershell
python src/cli.py security-check
```

Generated artifacts:

- `data/output/demo_opportunities.csv`
- `data/output/demo_report.md`
- `data/output/demo_report.html`

Run the ADK agent after installing `google-adk`:

```powershell
adk run web3_leads_agent
```

Run the ADK web interface from the parent folder:

```powershell
adk web --port 8000
```

Run the local MCP server:

```powershell
python src/mcp_server.py
```

The MCP server exposes read-only/demo tools:

- `list_sample_events`
- `run_lead_demo`
- `read_demo_report`

## Optional Full Pipeline

The full pipeline can use OpenAI, GitHub, Firecrawl, and PostgreSQL, but those are optional for the public capstone demo. Configure credentials in `.env`; never commit `.env`, `.env.*` backup files, or `Database_Connection.csv`.

## Current Capstone Status

Ready:

- Working copy separated from reference code.
- Public-safe sample data.
- Deterministic demo pipeline.
- ADK wrapper.
- MCP server.
- MCP server import, tool calls, and startup verified.
- Executable security posture checks.
- Agent Skill for Web3 lead qualification.
- Reproducible local deployment with static HTML demo artifact.
- Config and output paths moved under `Web3-Leads`.
- Basic database identifier hardening in working copies.

Next:

- Add a small Streamlit or static demo page if we want a more visual project link.
- Record demo video using the CLI output, report, and architecture diagram.
- Write the final Kaggle Writeup under 2,500 words.
