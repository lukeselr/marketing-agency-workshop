---
name: marketing-agency-linkedin
description: Sub-skill — LinkedIn Marketing Developer Platform onboarding. Drives Dev App creation, Marketing API access request, OAuth + access token, Insight Tag, Lead Gen Form. Loaded on demand by parent marketing-agency skill.
---

# LinkedIn sub-skill (`marketing-agency/platforms/linkedin`)

Loaded by Phase 3 of the parent skill when the user picks LinkedIn as a target.

## Specs

1. `00-create-or-signin.spec.ts` — sign in or create LinkedIn account
2. `01-dev-app.spec.ts` — Developer App created at `linkedin.com/developers/apps`
3. `02-marketing-api-request.spec.ts` — request Marketing Developer Platform access (1–5 days approval)
4. `03-oauth-tokens.spec.ts` — OAuth flow, access + refresh tokens captured
5. `04-insight-tag.spec.ts` — Insight Tag created, partner ID captured + install snippet generated
6. `05-leadgen-form.spec.ts` — Lead Gen Form template (status PAUSED)

## Output

`~/.marketing-agency/tokens/linkedin.json` (mode 600):

```json
{
  "version": 1,
  "platform": "linkedin",
  "tested_on": "YYYY-MM-DD",
  "client_id": "...",
  "client_secret": "...",
  "access_token": "...",
  "refresh_token": "...",
  "ad_account_urn": "urn:li:sponsoredAccount:...",
  "insight_tag_partner_id": "...",
  "leadgen_form_id": "..."
}
```

## Known blocker

Marketing Developer Platform vetting takes 1–5 business days. While you wait, run `templates/while-you-wait.md` for organic LinkedIn engagement (TLA precursor).
