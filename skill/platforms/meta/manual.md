# Meta — manual fallback walk-through

Use this when Playwright selectors break or 2FA blocks automation.

## Step 0 — Sign in / sign up

1. Go to **business.facebook.com**.
2. If you have a personal Facebook → click **Continue as <you>** → land on Business Suite.
3. If not → go to **facebook.com/r.php** → fill name, email, password, DOB, gender → confirm via email link.

## Step 1 — Create Business Manager

1. business.facebook.com/overview → **Create Business** (top right).
2. Fill: business name, your name, business email.
3. Click **Submit**. Save the URL — `business_id=<NUMBER>` in the address bar.

## Step 2 — Create Ad Account

1. Settings → **Accounts → Ad Accounts → Add → Create a new ad account**.
2. Name = your business + "Primary".
3. Time zone and currency = your business location (defaults to `Australia/Brisbane` + `AUD`; override via `MA_TIMEZONE` and `MA_CURRENCY` env vars).
4. Save. Save the URL — `act=<NUMBER>` in the address bar.

## Step 3 — Generate System User token

1. Settings → **Users → System Users → Add → Create system user**.
2. Role = **Admin**.
3. **Generate new token** → pick the Ad Account → grant scopes:
   - ads_management
   - ads_read
   - business_management
   - leads_retrieval
   - pages_read_engagement
4. Copy the token. **It is shown ONCE.** Paste into `~/.marketing-agency/tokens/meta.json` under `system_user_token`.

## Step 4 — Create Pixel

1. **Events Manager → Connect Data Sources → Web → Pixel → Get started**.
2. Name = "Primary Pixel". Save.
3. Copy the Pixel ID (visible in URL `pixel_id=<NUMBER>`).

## Step 5 — Conversions API

1. Pixel → Settings → **Conversions API → Set up manually → Generate access token**.
2. Copy the token. Save under `capi_access_token`.

## Step 6 — Lead Gen Form (status PAUSED)

1. business.facebook.com/leadgen_forms/?page_id=<your_page_id>
2. **Create form → More volume → Save draft**.
3. Copy `form_id=<NUMBER>`.

## Verification

Run from terminal:

```bash
curl -s "https://graph.facebook.com/v19.0/me/adaccounts?access_token=<TOKEN>" | jq '.data[].name'
```

Should list your Ad Account.
