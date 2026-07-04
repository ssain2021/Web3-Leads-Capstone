---
name: web3-lead-qualification
description: Qualify Web3 RSS/forum/blog/governance events into evidence-backed business development leads. Use when reviewing Web3 events, RSS feed items, DAO/forum posts, protocol announcements, grants/RFPs, security updates, integration posts, vendor/procurement signals, or generated opportunity rows for the Web3 Signal-to-Lead Agent capstone.
---

# Web3 Lead Qualification

## Goal

Turn noisy Web3 events into actionable business development leads without inventing facts. Retain only events with a concrete external action surface and source evidence.

## Workflow

1. Read the event title, summary/body text, source, URL, and event ID.
2. Decide whether the event has a qualifying action surface.
3. Reject noise before writing a lead.
4. If retained, produce the required lead fields with source-grounded evidence.
5. Use the weakest accurate wording when the opportunity is early or uncertain.

## Qualifying Action Surfaces

Retain an event only when it includes at least one:

- RFP, RFQ, grant, proposal, application, or program intake.
- Partner intake, pilot access, ecosystem onboarding, or integration request.
- Vendor, provider, procurement, maintenance, migration, or pricing request.
- API, SDK, docs, dashboard, wallet, payment rail, or technical integration surface.
- Security, audit, risk, threat-intelligence, scam-protection, or protection integration path.

## Rejection Rules

Reject events that are only:

- Price movement, token speculation, market commentary, or listing rumors.
- Community contests, giveaways, fan campaigns, or non-commercial announcements.
- Generic product launches with no partner, procurement, integration, or adoption path.
- Governance discussion with no vendor, provider, implementation, or buyer-side action.
- Items where the target company, action path, or evidence would need to be invented.

## Evidence Rules

- Include `source_event_ids` for every retained lead.
- Include `source_url` when available.
- Include an `evidence_snippet` copied or tightly paraphrased from the event text.
- Do not invent deadlines, contacts, budgets, official program names, or authority.
- If an item is only a signal, say so plainly.

## Required Output Fields

Use these fields for retained leads:

- `opportunity_id`
- `title`
- `target_company`
- `summary`
- `evidence_type`
- `evidence_snippet`
- `suggested_outreach_angle`
- `confidence`
- `source_event_ids`
- `source_url`
- `status`

## Evidence Type Choices

Prefer one of:

- `rfp_or_grant`
- `partner_intake`
- `vendor_search`
- `integration`
- `security`
- `none`

Use `none` only for rejected or non-actionable items.

## Confidence Calibration

- `0.90-0.95`: explicit action path, clear target, direct source evidence.
- `0.70-0.89`: action path is present but some details are incomplete.
- `0.55-0.69`: weak but plausible business signal.
- Below `0.55`: do not retain in the public demo.

## Outreach Wording

Write action-oriented but modest outreach:

- RFP/grant: prepare a proposal or application through the published path.
- Partner intake: contact partnerships/ecosystem team with a focused pilot proposal.
- Vendor search: send a concise vendor capability note with prior work and pricing/migration detail.
- Integration: review docs and propose a technical evaluation call.
- Security: offer a risk, audit, threat-intelligence, or protection integration discussion.

Avoid inflated phrases such as "guaranteed partnership" or "confirmed revenue opportunity" unless the source explicitly supports them.

## Quick Examples

Retain:

- "DAO opens RFP for risk dashboard provider" -> `rfp_or_grant`
- "Wallet teams invited to request pilot integration access" -> `partner_intake`
- "Protocol asks vendors for migration/pricing proposals" -> `vendor_search`
- "Security providers invited to discuss threat-intel integration" -> `security`

Reject:

- "Token price rises after listing rumor"
- "Community art contest announced"
- "Protocol launches product with no partner or integration path"
