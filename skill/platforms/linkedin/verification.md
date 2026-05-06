# LinkedIn Marketing Developer Platform vetting

LinkedIn approval gates the most useful APIs (audience targeting, lead retrieval, conversions reporting). Approval takes 1–5 business days. Rejections are common but recoverable.

## What gets reviewed

- **Use case** — must describe a real, sustained marketing programme for your company.
- **Company page** — must exist, be managed by you, and have a recent post.
- **Privacy policy** — must be live + describe what data you collect via LinkedIn.
- **App branding** — name, logo, description must match your business.

## Common rejection reasons

| Reason | Fix |
|---|---|
| Use case too vague | Reference specific products: "Sponsored Content + Single Image Ads + Lead Gen Forms for our software product targeting CTOs in AU/UK." |
| Company page mismatch | App's company field must match a LinkedIn Page where you're an admin. |
| Logo missing or low-res | Upload 300×300 PNG, transparent background. |
| Privacy policy 404 | Verify the URL loads in incognito. Don't link to a member page. |
| App name = personal brand | Use the registered business name. |

## Re-submitting after rejection

1. Read the email from `developer-relations@linkedin.com`.
2. Fix the cited issue.
3. linkedin.com/developers/apps/<APP_ID>/products → **Request access** again with revised use case.
4. Allow 3–5 business days for re-review.

## Escalation

If 7 days pass with no response, email `developer-platform@linkedin.com` with:
- App ID
- Submission date
- Brief use case recap

## While you wait

- Run `templates/while-you-wait.md` engagement loop.
- Read-only LinkedIn API access (`r_liteprofile`, `r_emailaddress`) does NOT require Marketing API approval — Phase 5 ships those first so the user makes progress.
