---
name: delegate-sms-instant
description: Phase 10 instant-reply SMS + ManyChat IG/FB DM auto-reply. Sub-60-sec response time agency-grade.
---

## When to invoke
Phase 10 deploy or when owner says "build my instant lead response".

## Context
- Voice fingerprint
- Existing GHL phone number (from tokens) or trigger ManyChat for social DMs

## Delegation
1. `sms-blast` for SMS templates (3 variants for split-test)
2. `manychat` for IG/FB Messenger auto-replies
3. `content-engine` voice-grade
4. Deploy as DRAFT in GHL via `ghl-crm`

## Read back
`.state/lifecycle/instant-reply.json` with 3 SMS + 2 ManyChat flow drafts.
