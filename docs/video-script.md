# Video Script

Target: 4 to 5 minutes.

## 0:00-0:30 Problem

Web3 business teams watch many sources, but the signal is scattered. A useful RFP, partner intake, vendor migration, security integration, or grants opportunity may appear in a forum thread or blog post and disappear into feed noise.

## 0:30-1:00 Solution

Introduce Web3 Signal-to-Lead Agent. It turns raw feed events into qualified business leads with evidence, confidence, and suggested outreach.

## 1:00-1:45 Architecture

Show the architecture diagram. Mention collector, preprocess, gatekeeper, finder, critic, refiner, recovery, dedupe, ADK root agent, and MCP server.

## 1:45-3:30 Demo

Run:

```powershell
python src/cli.py demo
```

Show:

- events read,
- leads retained,
- generated CSV,
- generated Markdown report,
- one rejected noisy example,
- one retained high-quality lead.

## 3:30-4:30 Course Concepts

Mention:

- ADK root agent,
- multi-agent workflow,
- MCP server,
- security/no-secret demo mode,
- deployable CLI.

## 4:30-5:00 Close

Summarize business value: the system reduces manual feed monitoring and turns unstructured Web3 market signals into actionable BD work.
