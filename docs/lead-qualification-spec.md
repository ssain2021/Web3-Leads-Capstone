# Lead Qualification Spec

## Purpose

Define what the Web3 Signal-to-Lead Agent should retain, reject, and report.

The system is intentionally bounded: it does not make open-ended business decisions. It reads Web3 events and identifies evidence-backed business development opportunities.

## Inputs

Each event should contain as many of these fields as available:

- `event_id`
- `title`
- `summary_text`
- `body_text`
- `published_at`
- `source`
- `url`

## Output Lead Fields

Each retained lead should include:

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

## Qualifying Action Surfaces

An event can be retained only if it exposes at least one concrete external action surface:

- RFP, RFQ, grant, proposal, or application path.
- Partner intake, pilot access, ecosystem onboarding, or integration request.
- Vendor, provider, procurement, maintenance, migration, or pricing request.
- API, SDK, documentation, dashboard, wallet, payment rail, or integration surface.
- Security, audit, risk, threat-intelligence, or protection integration path.

## Rejection Rules

Reject events when they are only:

- Price movement, token speculation, market commentary, or listing rumors.
- Community contests, giveaways, fan campaigns, or non-commercial announcements.
- Generic product launches with no integration, procurement, partner, or adoption path.
- Governance discussion with no vendor, provider, implementation, or buyer-side action.
- Events where the model would need to invent the target company, action path, or evidence.

## Confidence Rules

Confidence should reflect evidence strength, not excitement.

- `0.90-0.95`: explicit action path, clear target, direct source evidence.
- `0.70-0.89`: action path is present but details are incomplete.
- `0.55-0.69`: weak but still plausible business signal.
- Below `0.55`: should not be retained in the public demo.

## Evidence Rules

- Every lead must include a source event ID.
- Every lead must include a source URL when available.
- Every lead must include an evidence snippet derived from the input event.
- The system must not invent deadlines, contacts, budgets, or official program names.

## Behavior-Driven Acceptance Criteria

### Scenario: Explicit RFP is retained

Given an event says a DAO is seeking service providers through an RFP  
When the demo pipeline processes the event  
Then it should retain a lead with `evidence_type = rfp_or_grant`  
And the outreach angle should recommend preparing a proposal.

### Scenario: Vendor migration thread is retained

Given an event says a protocol is discussing replacing vendor tooling  
When the demo pipeline processes the event  
Then it should retain a lead with `evidence_type = vendor_search`  
And the target company should be derived from the source or event context.

### Scenario: Partner pilot is retained

Given an event invites wallet teams or app developers to request pilot access  
When the demo pipeline processes the event  
Then it should retain a lead with `evidence_type = partner_intake`  
And the outreach angle should recommend a focused pilot proposal.

### Scenario: Security integration path is retained

Given an event invites threat-intelligence or security providers to discuss integrations  
When the demo pipeline processes the event  
Then it should retain a lead with `evidence_type = security`  
And the outreach angle should mention security, risk, or threat-intelligence integration.

### Scenario: Price rumor is rejected

Given an event is only about token price movement or exchange listing speculation  
When the demo pipeline processes the event  
Then it should not create a retained lead.

### Scenario: Community contest is rejected

Given an event is only a community art contest or fan campaign  
When the demo pipeline processes the event  
Then it should not create a retained lead.

### Scenario: Duplicate company and evidence type is consolidated

Given two retained leads share the same target company and evidence type  
When dedupe runs  
Then only the higher-confidence lead should remain.

## Public Demo Contract

The bundled sample file `data/sample/sample_events.jsonl` should produce:

- `103` events read from a sanitized real-data sample.
- `3` raw leads.
- `3` deduped leads.
- Retained targets: `Gnosis Pay`, `Hyperlane`, `Kusama`.
- Rejected examples: routine feed items with no concrete business development action surface.

## Full Pipeline Contract

The full `src/core_pipeline` scripts should preserve the same lead-quality principles while using the larger RSS corpus, LLM enrichment, database mode, and post-run dedupe.
