# Google Ads — manual fallback walk-through

## Step 0 — Sign in

accounts.google.com/signin → use the email that owns (or will own) the ad account.

## Step 1 — Cloud Project

1. console.cloud.google.com/projectcreate
2. Project name: `marketing-agency`. Create. Save the project ID from the URL.

## Step 2 — MCC (Manager) Account (skip if existing single ad account is enough)

1. ads.google.com/aw/manager/start
2. Name: e.g. "Selr AI MCC". Pick **Manage other people's accounts**.
3. Country, time zone, and currency = your business location (defaults shown in the spec are AU/Brisbane/AUD; override via `MA_COUNTRY`, `MA_TIMEZONE`, `MA_CURRENCY` env vars).
4. **Submit**. Save the customer ID (10 digits).

## Step 3 — Developer Token

1. ads.google.com/aw/apicenter
2. **Apply for token**. Use case (suggested):
   > Manage Search + PMax campaigns for our company. Build conversion tracking, audience uploads, automated reporting.
3. Submit. Approval starts in **Test** tier (immediate), upgrades to **Basic** automatically (no human review). Standard is on request.
4. Copy the token.

## Step 4 — OAuth Credentials

1. console.cloud.google.com/apis/credentials → **Configure consent screen** if missing.
   - User type: **External**.
   - App name: e.g. "Selr AI Google Ads". Save.
2. Back at credentials → **Create credentials → OAuth client ID**.
   - Application type: **Desktop app**.
   - Name: `marketing-agency-google-ads`.
   - **Create**. Save Client ID + Client Secret.
3. Generate refresh token via the companion script (or by running an OAuth flow with the saved client ID).

## Step 5 — Conversion Tracking (mandatory)

For each conversion type:
1. ads.google.com/aw/conversions/new/website
2. **Purchase** conversion: name = "Purchase", category = Purchase, tick **Value** + **Enhanced conversions for web (EC4W)**. Save.
3. **Lead** conversion: name = "Lead Form Submit", category = "Submit lead form", tick **Enhanced conversions for leads (EC4L)**. Save.
4. Save both conversion action IDs.

## Step 6 — Search Campaign (PAUSED)

1. ads.google.com/aw/campaigns/new
2. Goal = **Sales** or **Leads**. Type = **Search**.
3. Status = **Paused** (mandatory).
4. Bid strategy = **Manual CPC** for first 30 conversions, then switch to **Maximize Conversions** or **Target CPA**.
5. Save campaign ID.

## Master strategy reminders

- Skip Performance Max until 50+ conversions per month (per `ads-strategy-google-2026-05.md`).
- AI Max for Search 2025: enable only after baseline Manual CPC data exists.
- EC4W + EC4L are mandatory for all clients.
