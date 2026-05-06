---
name: marketing-agency-google-ads
description: Sub-skill — Google Ads onboarding. Drives Cloud project, MCC account, developer token request, OAuth credentials, conversion tracking, and Search campaign. Loaded on demand by parent marketing-agency skill.
---

# Google Ads sub-skill (`marketing-agency/platforms/google-ads`)

## Specs

1. `00-create-or-signin.spec.ts` — sign in / create Google account
2. `01-cloud-project.spec.ts` — Google Cloud project (required for OAuth credentials)
3. `02-mcc-account.spec.ts` — Manager (MCC) account (skip if user has existing single ad account)
4. `03-developer-token.spec.ts` — Apply for Google Ads API developer token (test → basic auto-approved → standard on request)
5. `04-oauth-credentials.spec.ts` — OAuth 2.0 client + refresh token
6. `05-conversion-tracking.spec.ts` — EC4W (Enhanced Conversions for Web) + EC4L (Enhanced Conversions for Leads), both mandatory
7. `06-search-campaign.spec.ts` — Search campaign template (status PAUSED, AI Max for Search 2025-aware)

## Output

`~/.marketing-agency/tokens/google-ads.json` (mode 600):

```json
{
  "version": 1,
  "platform": "google-ads",
  "tested_on": "YYYY-MM-DD",
  "developer_token": "...",
  "oauth_client_id": "....apps.googleusercontent.com",
  "oauth_client_secret": "...",
  "refresh_token": "1//...",
  "customer_id": "1234567890",
  "manager_customer_id": "9876543210",
  "conversion_action_id_purchase": "...",
  "conversion_action_id_lead": "..."
}
```

## Known blockers

- **Developer token tiers**: Test → Basic (auto-approved) → Standard (manual review). Skill starts in Basic; only escalates to Standard if scaling.
- **PMax negs**: 100 → 10k cap raised in 2025. Skip PMax entirely until 50+ conversions per month exist (per master strategy).
