/** Google Ads — Step 04: OAuth 2.0 client + refresh token. */
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

test("04-oauth-credentials", async ({ page }) => {
  const projectId = process.env.MA_GCP_PROJECT_ID;
  await page.goto(`https://console.cloud.google.com/apis/credentials?project=${projectId}`);
  // Configure consent screen first if missing
  if (await page.getByRole("button", { name: /Configure consent screen/i }).isVisible()) {
    await page.getByRole("button", { name: /Configure consent screen/i }).click();
    await page.getByRole("radio", { name: /External/i }).check();
    await page.getByRole("button", { name: /Create/i }).click();
    const businessName = process.env.MA_BUSINESS_NAME || "My Business";
    await page.getByLabel(/App name/i).fill(process.env.MA_GADS_OAUTH_APP_NAME || `${businessName} Google Ads`);
    await page.getByLabel(/User support email/i).selectOption({ index: 0 });
    await page.getByRole("button", { name: /Save and continue/i }).click();
  }
  // Create OAuth client ID
  await page.goto(`https://console.cloud.google.com/apis/credentials?project=${projectId}`);
  await page.getByRole("button", { name: /Create credentials/i }).click();
  await page.getByText(/OAuth client ID/i).click();
  await page.getByLabel(/Application type/i).selectOption({ label: "Desktop app" });
  await page.getByLabel(/Name/i).fill("marketing-agency-google-ads");
  await page.getByRole("button", { name: /Create/i }).click();
  const clientId = await page.locator("[data-testid='oauth-client-id']").innerText();
  const clientSecret = await page.locator("[data-testid='oauth-client-secret']").innerText();
  expect(clientId).toContain(".apps.googleusercontent.com");
  writeToken("google-ads", "oauth_client_id", clientId);
  writeToken("google-ads", "oauth_client_secret", clientSecret);
  process.stdout.write(JSON.stringify({ ok: true, wrote: ["google-ads.oauth_client_id", "google-ads.oauth_client_secret"] }) + "\n");
  // Refresh token is captured by the companion exchange-google-code.sh which runs after this spec.
});
