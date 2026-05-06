# Meta Business Verification (DUNS / docs)

Triggered automatically when ad spend exceeds **$50/day** OR when running Lead Ads at scale OR when accessing certain APIs (advanced standard access).

## What you need

1. **Legal business name** — must match Australian company register (ASIC) or local equivalent.
2. **DUNS number** OR **business registration document** (ABN extract, certificate of incorporation, business licence, articles of association).
3. **Tax ID** — ABN for AU.
4. **Phone number** Meta can call.
5. **Website** — domain must match business name; Pixel + Privacy Policy + Terms must be live.
6. **Business email** — non-personal address (e.g. `info@yourbusiness.com.au`, not `@gmail.com`).

## Process

1. business.facebook.com → **Settings → Business Info → Verify Business**.
2. Search for your business by name + country. If found, select. If not, **Add manually**.
3. Upload docs. Most common accepted document: ABN extract from `abr.business.gov.au`.
4. Submit. Meta reviews within 1–5 business days.

## If rejected

- Re-check that legal name + address EXACTLY matches the document.
- Ensure phone is reachable (international format, e.g. `+61 7 XXXX XXXX`).
- Resubmit with a clearer scan / different doc type.
- Last resort: open a Business Help Center case → category "Business Verification" → escalate.

## While you wait

Run Phase 1's `templates/while-you-wait.md` engagement loop:
- Draft 3 organic LinkedIn posts (`linkedin-automation` skill)
- Draft creative variants from your `voice-fingerprint.json` (`ad-creative` skill)
- Draft Lead Gen Form copy (`copywriting` skill)
- Install Pixel + CAPI (Phase 6 — works pre-verification)

## DUNS workaround (AU)

DUNS is preferred but not required. ABN extract works for >95% of AU SMBs.

If DUNS is required:
1. Go to `dnb.com.au` → Get Free DUNS.
2. Wait 2–8 weeks. (Yes, that long — start now if you'll need it.)
