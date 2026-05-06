---
name: delegate-lead-research
description: Outbound prospecting. Identify high-quality leads matching ICP, enrich with public signals, output to GHL.
---

## When to invoke
On owner request: "find me leads matching X" or as Phase 12 monthly extension.

## Context
- ICP from `.state/business-baseline.md`
- Industry + geo from baseline
- Existing customer list (consented) for lookalike pattern

## Delegation
1. `lead-research-assistant` — primary engine
2. `apify-market-research` — geo + sizing
3. Push to GHL via `ghl-crm` as new contacts with custom field "icp_match_score"

## Read back
`.state/leads-batch-YYYY-MM-DD.csv`
