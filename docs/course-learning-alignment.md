# Course Learning Alignment

Source documents reviewed from `Kaggle-Weekly_Docs`:

- `Day_1_Introduction_To_Agents_VibeCoding.pdf`
- `Day_2_Agent Tools & Interoperability.pdf`
- `Day_3_Agent Skills.pdf`
- `Day_4_Vibe Coding Agent Security and Evaluation.pdf`
- `Day_5_Spec_Driven_Production_Grade_Development.pdf`

## Day 1: Agents, Vibe Coding, and Agentic Engineering

Main ideas:

- Vibe coding shifts development from syntax-first work to intent-driven development.
- The stronger version is agentic engineering: treat prompts, tools, context, skills, sandboxes, orchestration, and guardrails as engineered system components.
- Context engineering is a core skill. Agents need the right static and dynamic context, not just large prompts.
- The SDLC changes across requirements, architecture, implementation, testing, code review, deployment, and maintenance.
- A good agent project should show harness engineering: instructions, tools, MCP/API connections, sandboxing, orchestration, and guardrails.

Application to this capstone:

- Present the Web3 lead pipeline as agentic engineering, not just a script.
- Show the harness: ADK root agent, MCP server, deterministic demo tool, config files, safe data mode, and legacy/full pipeline.
- Explain how context is constrained: sample events, evidence snippets, category masters, filter masters, and source URLs.

## Day 2: Agent Tools and Interoperability

Main ideas:

- MCP is taught as the discovery, configuration, and connection layer for tool interoperability.
- MCP helps avoid one-off integrations between every agent and every external system.
- A2A introduces agent-to-agent interoperability, agent cards, registries, and remote agent interaction.
- Agent systems should avoid unbounded control flow and unclear orchestration.
- Bounded domains are easier to make reliable, inspectable, and safe.

Application to this capstone:

- Keep our MCP server local and read-only for the public demo: list sample events, run demo, read report.
- Frame Web3 lead discovery as a bounded domain: input events -> evidence-backed leads.
- Keep orchestration explicit: collector, preprocess, gatekeeper, finder, critic, refiner, recovery, dedupe.
- Avoid claiming open-ended autonomy; the agent assists BD lead discovery with clear tool boundaries.

## Day 3: Agent Skills

Main ideas:

- Agent Skills package procedural knowledge for agents.
- Skills use progressive disclosure: metadata first, detailed instructions only when needed.
- Good skill descriptions act like routing logic.
- Skills differ from MCP: MCP exposes tools/resources; skills teach the agent how and when to use capabilities.
- Skill evaluation should check trigger quality, output quality, tool trajectory, and token budget impact.

Application to this capstone:

- `skills/web3-lead-qualification/SKILL.md` packages the qualification rules as an Agent Skill.
- The skill teaches action surfaces, evidence snippets, target company handling, outreach wording, confidence, and noise rejection.
- The deterministic demo and tests act as evaluation fixtures for the skill.

## Day 4: Agent Security and Evaluation

Main ideas:

- Secure agentic development needs sandboxing, supply-chain defense, egress governance, contextual authorization, identity controls, and observability.
- Watch for hallucinated packages, MCP spoofing, confused-deputy risks, overprivileged agents, prompt injection, invisible payloads, and repository poisoning.
- Use zero ambient authority and just-in-time privilege where possible.
- Evaluation should cover quality, safety, intent drift, trust decay, and traceability.
- Human-in-the-loop matters for high-risk actions.

Application to this capstone:

- Public demo mode uses no API keys, no database, no private feeds, and sanitized sample data.
- `.env.example` documents secrets; `.gitignore` excludes `.env`, runtime data, and database credential files.
- MCP server is read-only.
- Full pipeline should require explicit local configuration before API or database actions.
- Add evaluation fixtures: known noisy event should be rejected; known RFP/vendor/security events should be retained.

## Day 5: Spec-Driven Production-Grade Development

Main ideas:

- Spec-driven development turns vague intent into testable behavior.
- Good specs define behavior, constraints, inputs, outputs, and acceptance criteria.
- MCP can provide one integration surface across frameworks.
- Production-grade vibe coding needs code review, sustainability, guardrails, sandboxing, human-in-the-loop, generated test coverage, evaluation, policy servers, and context hygiene.
- Prompt sanitization and context hygiene are part of production readiness.

Application to this capstone:

- Add a project specification for lead qualification behavior.
- Add acceptance tests for the demo pipeline.
- Keep a clear separation between public demo mode and full credentialed pipeline mode.
- Document setup and expected outputs so judges can reproduce the result.
- Keep generated outputs inspectable: CSV plus Markdown report.

## Course Concepts We Should Explicitly Demonstrate

| Concept | Project Evidence |
| --- | --- |
| Agentic engineering | Multi-stage Web3 lead discovery harness with ADK, tools, configs, outputs, and docs |
| ADK | `src/agent.py` and `web3_leads_agent/agent.py` |
| MCP | `src/mcp_server.py`, verified local MCP server startup and read-only/demo tools |
| Agent Skills | `skills/web3-lead-qualification/SKILL.md` |
| Security | no-secret demo mode, `.env.example`, `.gitignore`, local read-only MCP, sanitized sample data, executable security report |
| Evaluation | sample events with expected retained/rejected behavior, future tests |
| Spec-driven development | this alignment doc plus future lead qualification spec |
| Deployability | CLI demo, generated CSV/Markdown/HTML artifacts, ADK entrypoint, reproducible sample data |

## Recommended Next Changes

1. Add `docs/lead-qualification-spec.md` with behavior-driven acceptance criteria.
2. Add `tests/test_demo_pipeline.py` for the sample events.
3. Update the Kaggle writeup to explicitly mention course vocabulary: harness engineering, bounded domain, MCP, progressive disclosure, zero-secret demo mode, evaluation fixture, Agent Skill, and spec-driven workflow.
