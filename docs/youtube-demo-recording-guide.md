# YouTube Demo Recording Guide

Target length: 4 to 5 minutes.

Video style: screen recording only. You do not need to show your face.

## Files To Use

- Slide deck: `docs/web3-signal-to-lead-youtube-demo.pptx`
- Demo report: `data/output/demo_report.html`
- Kaggle writeup draft: `docs/kaggle-writeup-draft.md`

## Do Not Show

- `.env`
- `.env.bak`
- `Database_Connection.csv`
- API keys, database hostnames, usernames, passwords, or private RSS data.

## Before Recording

From the `Web3-Leads` folder:

```powershell
.\.venv\Scripts\Activate.ps1
python src/cli.py build-static-demo
python -m unittest discover -s tests -p "test_*.py"
```

Open these before pressing record:

- `docs/web3-signal-to-lead-youtube-demo.pptx`
- `data/output/demo_report.html`
- A terminal in the `Web3-Leads` folder.

## Recording Flow

### 0:00-0:40 - Problem And Value

Show slide 1 and slide 2.

Suggested narration:

> This project is Web3 Signal-to-Lead Agent, built for the Agents for Business track. Web3 business teams monitor many RSS feeds, governance forums, protocol blogs, grant pages, and security updates. The problem is not that there is no data. The problem is finding actionable business opportunities inside noisy, duplicated, fast-moving feeds.

### 0:40-1:40 - Architecture

Show slide 3.

Suggested narration:

> The pipeline starts with feed collection, then cleans and enriches events. The gatekeeper filters noise and requires evidence of an external action path. The finder creates candidate leads, the critique and refine stages improve evidence and wording, and the dedupe stage consolidates repeated opportunities. The public capstone also includes a Google ADK root agent, a local MCP server, and a reusable Agent Skill for Web3 lead qualification.

### 1:40-2:50 - CLI Demo And Static Artifact

Show slide 5, then switch to terminal.

Run:

```powershell
python src/cli.py build-static-demo
```

Point out:

- `events_read: 103`
- `deduped_leads: 3`
- `demo_opportunities.csv`
- `demo_report.md`
- `demo_report.html`

Then open or switch to:

```text
data/output/demo_report.html
```

Suggested narration:

> This public demo is deterministic and requires no API key, no database, and no private feed data. It reads a sanitized real-data sample from the June 24 pipeline run, rejects noisy items, retains evidence-backed opportunities, and writes CSV, Markdown, and HTML artifacts. The HTML report is useful for judges because it can be opened directly in a browser.

### 2:50-3:40 - ADK And MCP

Show slide 6.

For ADK, show or mention:

```powershell
adk run web3_leads_agent
```

Example prompt:

```text
Run the public demo and summarize the top leads.
```

For MCP, show or mention:

```powershell
python src/mcp_server.py
```

MCP tools to mention:

- `list_sample_events`
- `run_lead_demo`
- `read_demo_report`

Suggested narration:

> The ADK root agent exposes project tools for running the demo, explaining architecture, checking submission readiness, and running the security check. The MCP server exposes local read-only/demo tools so an agent can list sample events, run the lead demo, and read the report.

### 3:40-4:25 - Security And Deployability

Show slide 7.

Run or show:

```powershell
python src/cli.py security-check
```

Important note:

If this local development folder contains `.env`, `.env.bak`, or `Database_Connection.csv`, the security check should return `safe_for_public_demo: false`. That is expected locally. In the clean public GitHub/Kaggle copy, remove those files and rerun the check until it returns `true`.

Suggested narration:

> The public demo is designed to be safe to publish. It uses sanitized sample data, ignores secret files, and includes an executable security check. My local development folder may correctly fail the security check because private files exist locally. For public release, those files are removed and the check should pass.

### 4:25-5:00 - Concepts And Close

Show slide 4 and slide 8.

Suggested narration:

> The project demonstrates the core course concepts: a multi-stage agent system wrapped with Google ADK, a local MCP server, security controls, an Agent Skill, and reproducible local deployment. The business value is straightforward: it turns unstructured Web3 market signals into actionable business development work.

## Optional Final Screen

End with the HTML report or slide 8.

Recommended closing sentence:

> Thank you for reviewing Web3 Signal-to-Lead Agent for the Kaggle AI Agents capstone.
