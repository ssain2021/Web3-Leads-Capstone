"""Google ADK wrapper for the Web3 business lead capstone."""

from __future__ import annotations

from typing import Any

from google.adk.agents.llm_agent import Agent

from demo_pipeline import run_demo_pipeline
from security import security_summary


def run_public_demo() -> dict[str, Any]:
    """Run the no-secret demo pipeline over sample Web3 events."""

    return run_demo_pipeline()


def explain_architecture() -> dict[str, Any]:
    """Return the capstone architecture in judge-friendly terms."""

    return {
        "track": "Agents for Business",
        "problem": "Business teams miss actionable Web3 opportunities because signals are scattered across many RSS feeds, governance forums, blogs, and release notes.",
        "workflow": [
            "RSS collector gathers Web3 events from configured sources.",
            "Preprocess agent cleans events, extracts contact/action fields, and enriches summaries.",
            "Gatekeeper filters noise and requires evidence of a real action surface.",
            "Finder proposes candidate leads with source event IDs and confidence subscores.",
            "Critic and Refiner improve evidence quality and wording.",
            "Recovery and Watchlist agents rescue strong near misses.",
            "Dedupe consolidates repeated opportunities across time horizons.",
        ],
        "course_concepts": [
            "Google ADK root agent with custom tools",
            "Multi-agent lead qualification pipeline",
            "Public-safe security controls and no-secret demo mode",
            "MCP server for local event/opportunity lookup",
            "Deployable CLI and ADK web/CLI entrypoints",
        ],
    }


def submission_readiness(
    has_writeup: bool,
    has_video: bool,
    has_public_repo: bool,
    has_demo_artifacts: bool,
) -> dict[str, Any]:
    """Check whether the capstone submission package is complete."""

    missing: list[str] = []
    if not has_writeup:
        missing.append("Kaggle Writeup")
    if not has_video:
        missing.append("YouTube video demo")
    if not has_public_repo:
        missing.append("public project link or repository")
    if not has_demo_artifacts:
        missing.append("demo outputs and setup instructions")

    return {"ready": not missing, "missing": missing}


def run_security_check() -> dict[str, Any]:
    """Return the public-demo security posture report."""

    return security_summary()


root_agent = Agent(
    model="gemini-2.5-flash",
    name="web3_leads_agent",
    description="Turns noisy Web3 feed events into evidence-backed business development leads.",
    instruction=(
        "You are a Web3 business lead discovery agent. Help the user run the "
        "public demo, explain the architecture, and assess Kaggle capstone "
        "submission readiness. Be evidence-grounded and avoid inventing leads."
    ),
    tools=[run_public_demo, explain_architecture, submission_readiness, run_security_check],
)
