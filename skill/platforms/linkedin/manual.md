# LinkedIn — manual fallback walk-through

## Step 0 — Sign in / sign up

1. linkedin.com/login → sign in.
2. If no account → linkedin.com/signup → fill email + password + name + DOB.

## Step 1 — Developer App

1. linkedin.com/developers/apps/new
2. Fill: App name, Company (must be a LinkedIn Company Page you admin), Privacy policy URL.
3. Upload logo (300x300 png).
4. Tick "I have read and agree to the API Terms".
5. **Create app**.
6. Open the **Auth** tab → copy Client ID + Client Secret.

## Step 2 — Marketing Developer Platform request

1. Open your app → **Products** tab.
2. Find **Marketing Developer Platform** → click **Request access**.
3. Use case (suggested):
   > Run targeted Sponsored Content + Lead Gen Form campaigns for our company. Use audience matching, conversions reporting, and creative API to scale safely.
4. Submit. Status = **Pending review**. Approval: 1–5 business days.

## Step 3 — OAuth

After approval:

1. Build the auth URL:
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code
   &client_id=<CLIENT_ID>
   &redirect_uri=<URL_ENCODED_REDIRECT>
   &state=<RANDOM>
   &scope=r_liteprofile%20r_emailaddress%20w_member_social%20r_ads%20rw_ads%20r_ads_reporting%20r_organization_social%20rw_organization_admin%20r_basicprofile%20w_organization_social
   ```
2. Open in browser → Allow → captures `code=` in redirect URL.
3. Exchange code for token:
   ```
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d grant_type=authorization_code \
     -d code=<CODE> \
     -d client_id=<CLIENT_ID> \
     -d client_secret=<CLIENT_SECRET> \
     -d redirect_uri=<REDIRECT>
   ```
4. Save `access_token` + `refresh_token` to `~/.marketing-agency/tokens/linkedin.json`.

## Step 4 — Insight Tag

1. linkedin.com/campaignmanager/accounts/<AD_ACCOUNT_ID>/insight-tag
2. **Install tag** → copy snippet → grab `_linkedin_partner_id = '<NUMBER>'`.
3. Save partner ID to tokens file.

## Step 5 — Lead Gen Form (PAUSED)

1. linkedin.com/campaignmanager/accounts/<AD_ACCOUNT_ID>/lead-gen-forms
2. **Create form** → name, headline, privacy URL → **Save draft**.
3. Copy form ID from URL.
