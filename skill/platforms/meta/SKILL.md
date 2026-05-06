---
name: marketing-agency-meta
description: Sub-skill — Meta (Facebook + Instagram) ad-account onboarding. Drives Business Manager creation, Ad Account, System User, Pixel, CAPI Dataset, and Lead Gen Form via Playwright MCP. Loaded on demand by the parent marketing-agency skill.
---

# Meta sub-skill (`marketing-agency/platforms/meta`)

Loaded by Phase 3 of the parent skill when the user picks Meta as a target.

## What it does

Drives the Meta Business Suite + Developer Portal end-to-end via Playwright MCP, in a strict sequence:

1. `00-create-or-signin.spec.ts` — fresh user creates or signs into Facebook + Business Manager
2. `01-business-manager.spec.ts` — Business Manager profile created + verified
3. `02-ad-account.spec.ts` — Ad Account provisioned, currency + timezone set, billing attached
4. `03-system-user.spec.ts` — System User generated; long-lived token captured to `~/.marketing-agency/tokens/meta.json`
5. `04-pixel.spec.ts` — Meta Pixel created, ID captured, install snippet generated
6. `05-capi-dataset.spec.ts` — Conversions API dataset linked to Pixel; access token stored
7. `06-leadgen-form.spec.ts` — Lead Gen Form template created (campaign-ready, status PAUSED)

## Files in this directory

| File | Purpose |
|---|---|
| `playwright/00-create-or-signin.spec.ts` | Sign-in or new-account flow |
| `playwright/01-business-manager.spec.ts` | Business Manager creation |
| `playwright/02-ad-account.spec.ts` | Ad Account creation + billing |
| `playwright/03-system-user.spec.ts` | System User + long-lived token |
| `playwright/04-pixel.spec.ts` | Meta Pixel + install snippet |
| `playwright/05-capi-dataset.spec.ts` | CAPI dataset |
| `playwright/06-leadgen-form.spec.ts` | Lead Gen Form |
| `selectors.json` | Versioned DOM selectors (tested_on date stamped) |
| `verification.md` | Business Verification (DUNS, docs) walk-through for >$50/day spend |
| `manual.md` | Last-resort manual fallback with exact button labels |
| `setup.sh` | Orchestrates all 7 specs serially |

## How the parent skill invokes this

```bash
bash ~/.claude/skills/marketing-agency/platforms/meta/setup.sh
```

The parent skill (`SKILL.md`) handles state (`.state/meta-progress.json`) and resumes from the last-completed spec on re-run.

## Brand-protection guarantee

Every Meta launch (Phase 8) sets the campaign status to `PAUSED`. The user must explicitly approve activation via chat before the campaign goes live.

## Output

Token + IDs written to `~/.marketing-agency/tokens/meta.json` (mode 600):

```json
{
  "version": 1,
  "platform": "meta",
  "tested_on": "YYYY-MM-DD",
  "business_id": "...",
  "ad_account_id": "act_...",
  "system_user_token": "EAAB...",
  "pixel_id": "...",
  "capi_access_token": "...",
  "leadgen_form_id": "..."
}
```

This file is `.gitignore`'d — never committed.
