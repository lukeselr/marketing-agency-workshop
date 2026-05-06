/** LinkedIn — Step 03: OAuth flow → access + refresh tokens. */
import { test, expect } from "@playwright/test";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

function writeToken(platform: string, key: string, value: string) {
  const dir = path.join(os.homedir(), ".marketing-agency", "tokens");
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  const file = path.join(dir, `${platform}.json`);
  let cur: Record<string, unknown> = {};
  try { cur = JSON.parse(fs.readFileSync(file, "utf8")); } catch { cur = {}; }
  cur[key] = value;
  cur["platform"] = platform;
  cur["version"] = 1;
  fs.writeFileSync(file, JSON.stringify(cur, null, 2), { mode: 0o600 });
  fs.chmodSync(file, 0o600);
}

test("03-oauth-tokens", async ({ page }) => {
  const clientId = process.env.MA_LI_CLIENT_ID!;
  const redirect = process.env.MA_LI_REDIRECT || "http://localhost:3000/oauth/linkedin";
  const scopes = "r_liteprofile r_emailaddress w_member_social r_ads rw_ads r_ads_reporting r_organization_social rw_organization_admin r_basicprofile w_organization_social";
  const state = Math.random().toString(36).slice(2);

  await page.goto(
    `https://www.linkedin.com/oauth/v2/authorization?response_type=code` +
    `&client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirect)}` +
    `&state=${state}` +
    `&scope=${encodeURIComponent(scopes)}`
  );

  await page.getByRole("button", { name: /Allow/i }).click();
  await page.waitForURL(new RegExp(`code=`), { timeout: 60_000 });
  const code = page.url().match(/code=([^&]+)/)?.[1] ?? "";
  expect(code.length).toBeGreaterThan(8);
  writeToken("linkedin", "oauth_code", code);
  writeToken("linkedin", "oauth_state", state);
  process.stdout.write(JSON.stringify({ ok: true, wrote: ["linkedin.oauth_code", "linkedin.oauth_state"] }) + "\n");
  // The companion script `scripts/exchange-linkedin-code.sh` swaps this code for tokens
  // and writes them to ~/.marketing-agency/tokens/linkedin.json (mode 600).
});
