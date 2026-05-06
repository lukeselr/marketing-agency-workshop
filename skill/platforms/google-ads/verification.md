# Google Ads developer-token tiers

| Tier | Approval | Limits | When to request |
|---|---|---|---|
| Test | Immediate | Test accounts only — no real spend | Default starting point |
| Basic | Automatic (within 24h) | 15,000 ops/day across all real accounts | Phase 0 default for marketing-agency |
| Standard | Manual review (3–10 business days) | 1,000,000+ ops/day | Only if scaling past Basic |

## Basic-tier requirements

- Real Google Ads account exists + has billing.
- Use case clearly states real campaigns, not just experimentation.
- Privacy policy live at the URL submitted.

## Common rejections + fixes

| Rejection | Fix |
|---|---|
| "Use case too vague" | Reference specific products + intent: "Manage Search + PMax campaigns for AU service business; conversion-tracking + audience uploads + automated reporting." |
| "No active campaigns" | Create at least one PAUSED campaign first (Step 6 above). |
| "Privacy policy 404" | Ensure the URL loads in incognito + describes data collected via Google Ads. |
| "Account suspended" | Resolve the suspension first (billing, policy strikes). |

## After approval

- Token visible at `ads.google.com/aw/apicenter`.
- Save under `~/.marketing-agency/tokens/google-ads.json` field `developer_token`.
- Run `04-oauth-credentials.spec.ts` to capture client ID + secret.
- Run companion `scripts/exchange-google-code.sh` to capture refresh token.
