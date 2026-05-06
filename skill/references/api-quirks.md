# API quirks / known platform behaviours

## Meta
- System User token is the long-lived one. User access tokens expire — never use them for production.
- CAPI deduplication requires `event_id` matching the Pixel-side `eventID`. The skill stamps both with the same UUID.
- Lead Gen Forms: pulling leads via API requires `leads_retrieval` scope on the System User. Forget this and you get a silent empty array.

## LinkedIn
- October 2025 hierarchy rename: campaigns/groups now use slightly different terminology. Check `selectors.json`.
- Manual CPC requires `campaignType=SPONSORED_CONTENT` AND `costType=CPC` AND `optimizationTargetType=NONE`.
- Audience expansion is enabled by default — turn OFF for B2B precision (Wilcox rule).

## Google Ads
- AI Max for Search 2025: enable only after baseline Manual CPC has 50+ conversions of data.
- PMax: skip until 50+ conversions per month (per master strategy). Feed it negs aggressively (cap raised 100 → 10k in 2025).
- EC4W requires the gtag to have a transaction ID + value. EC4L requires hashed user data on form submit.
