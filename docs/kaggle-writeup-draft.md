# Web3 Signal-to-Lead Agent

## Track

Agents for Business

## Project Summary

Web3 business development teams need to monitor a large number of public sources: protocol blogs, RSS feeds, governance forums, ecosystem updates, grant posts, RFPs, security announcements, and developer release notes. The problem is not lack of data. The problem is finding actionable business signals inside noisy feed streams.

This project builds a multi-agent system that turns noisy Web3 events into qualified, evidence-backed business development leads. In my production workflow, the system monitors 1,576 enabled Web3 sources and collects about 1,600-1,700 weekly feed events. Only a small percentage become useful candidates, so the pipeline is designed to reject routine updates and keep only opportunities with a concrete action path such as an RFP, grant, partner ask, integration request, vendor search, or security collaboration opportunity.

For the public Kaggle demo, I provide a sanitized real-data sample and a deterministic local demo path. The demo does not require private credentials, database access, paid APIs, or private feed files.

## Problem

Useful Web3 business opportunities are scattered and time-sensitive. A DAO may publish an RFP, a protocol may request vendors, an ecosystem may invite partners to integrate, or a security team may ask for threat-intelligence providers. These posts are mixed with routine product updates, price commentary, governance chatter, duplicate announcements, and community content.

A keyword search is not enough because the system must decide whether the event contains a real business development action surface. It must also avoid invented claims, keep source evidence, and produce a practical outreach angle.

## Solution

The Web3 Signal-to-Lead Agent uses a multi-stage agentic pipeline:

1. Collect public Web3 feed events.
2. Preprocess and enrich the events.
3. Run a matcher model across multiple BD-week horizons.
4. Use multiple agent roles to qualify or reject events.
5. Merge candidates from different passes.
6. Deduplicate by source event set and target company/action.
7. Produce CSV, Markdown, and HTML demo artifacts.

The matcher is the core multi-agent step. It includes:

- Gatekeeper: rejects noise and requires a real action surface.
- Lead Finder: creates candidate leads with target, evidence, and confidence.
- Critic: checks weak evidence, invented claims, and low-action items.
- Refiner: improves the outreach angle and BD-ready wording.
- Recovery / Watchlist: rescues strong near-misses for later review.

Running the matcher across multiple BD-week horizons reduces variance. A single model pass may miss or vary on some opportunities, but the multi-pass workflow improves coverage. The final merge and dedupe stages restore precision.

## Course Concepts Demonstrated

### 1. ADK and Multi-Agent System

The project includes a Google ADK root agent in `src/agent.py` and an ADK import bridge in `web3_leads_agent/agent.py`. The ADK agent exposes tools to run the sanitized public demo, explain the architecture, check submission readiness, and run the security check.

The production design is also multi-agent: collector, preprocess, gatekeeper, finder, critic, refiner, recovery/watchlist, and dedupe. The public demo keeps the same qualification logic in a deterministic and reviewer-safe form.

### 2. MCP Server

The project includes a local MCP server in `src/mcp_server.py`. It exposes controlled demo tools:

- `list_sample_events`
- `run_lead_demo`
- `read_demo_report`

The MCP server is intentionally local and read-only/demo-oriented for the public submission. This keeps the integration bounded and safe while demonstrating tool interoperability.

### 3. Security Features

The public demo is designed to run without secrets. It does not need `.env`, database credentials, API keys, or private production files. The repo includes `.env.example` for configuration documentation and `.gitignore` rules to exclude credentials, runtime data, caches, logs, and local database files.

The project also includes an executable security check:

```powershell
python src/cli.py security-check
```

The check verifies required ignore rules, absence of sensitive files, no obvious inline secrets, public sample-data safety, and read-only MCP posture.

### 4. Agent Skill

The project includes an Agent Skill at `skills/web3-lead-qualification/SKILL.md`. It packages the procedural knowledge for Web3 lead qualification:

- qualifying action surfaces,
- rejection rules,
- required evidence,
- confidence calibration,
- target company interpretation,
- outreach wording.

This separates domain knowledge from code and demonstrates the course idea of using skills to provide reusable agent behavior.

### 5. Deployability

The project supports reproducible local deployment. Reviewers can install dependencies, run the CLI demo, run tests, and open the generated HTML report locally.

```powershell
python src/cli.py build-static-demo
python -m unittest discover -s tests -p "test_*.py"
```

The demo generates:

- `data/output/demo_opportunities.csv`
- `data/output/demo_report.md`
- `data/output/demo_report.html`

## Public Demo Data

The public demo uses `data/sample/sample_events.jsonl`, a sanitized sample prepared from a real run. It keeps short event summaries and real source URLs where appropriate, while excluding private credentials, database fields, scraped article bodies, and private contact details.

The demo currently reads 103 sample events and retains 3 qualified leads:

- Gnosis Pay
- Hyperlane
- Kusama

Each retained lead includes evidence, source URL, confidence, and a suggested outreach angle.

## Why This Is Useful

Business development teams do not need every event. They need a short list of opportunities that are timely, evidence-backed, and actionable. This project converts a noisy weekly Web3 feed stream into a practical lead shortlist that a BD team can inspect and act on.

The system is intentionally bounded. It does not send outreach automatically, make financial decisions, or claim that every lead is final. It assists humans by reducing discovery workload and preserving evidence for review.

## Limitations and Future Work

The public demo is deterministic and smaller than the production workflow. The full private pipeline can use live RSS collection, AI enrichment, database inserts, weekly email reporting, and dashboard publishing, but those private credentials and runtime files are intentionally excluded from the public repository.

Future improvements could include CI-based secret scanning, richer evaluation datasets, a hosted static demo page, and stronger production SQL hardening.

## Repository and Demo

GitHub repository: add final GitHub URL here.

YouTube demo: add final YouTube URL here.
