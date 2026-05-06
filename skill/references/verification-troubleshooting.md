# Verification troubleshooting

| Platform | Issue | Fix |
|---|---|---|
| Meta | Business Verification rejected | See `platforms/meta/verification.md` |
| Meta | Account suspended | Open Business Help Center case immediately, attach ID + business docs |
| LinkedIn | Marketing Dev Platform rejected | See `platforms/linkedin/verification.md` |
| LinkedIn | OAuth state mismatch | Re-run `03-oauth-tokens.spec.ts` — generate new random state |
| Google Ads | Developer token stuck in Test | Apply for Basic via apicenter — auto-approved within 24h |
| Google Ads | "API access not approved" 403 | Customer ID being queried isn't linked to the developer token's MCC |
| Google Ads | Quota exceeded | Drop to lighter polling cadence in `kill-rule-monitor.py` |
| All | Selectors broken (UI drift) | Run `bash shared/selectors-version-check.sh`. If older than 30 days, refresh selectors.json + bump version. |
