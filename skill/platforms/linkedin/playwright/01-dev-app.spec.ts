/** LinkedIn — Step 01: Developer App. */
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

test("01-dev-app", async ({ page }) => {
  await page.goto("https://www.linkedin.com/developers/apps/new");
  await page.getByLabel(/App name/i).fill(process.env.MA_LI_APP_NAME || "Selr AI Marketing");
  await page.getByLabel(/Company/i).fill(process.env.MA_LI_COMPANY_PAGE || "");
  await page.getByLabel(/Privacy policy URL/i).fill(process.env.MA_PRIVACY_URL || "https://example.com/privacy");
  // upload logo file path passed in env
  if (process.env.MA_LI_LOGO_PATH) {
    await page.locator("input[type='file']").setInputFiles(process.env.MA_LI_LOGO_PATH);
  }
  await page.getByLabel(/I have read and agree/i).check();
  await page.getByRole("button", { name: /Create app/i }).click();
  await page.waitForURL(/developers\/apps\/\d+/, { timeout: 60_000 });

  // capture client id + secret from Auth tab
  await page.getByRole("tab", { name: /Auth/i }).click();
  const clientId = await page.locator("[data-testid='client-id']").innerText();
  const clientSecret = await page.locator("[data-testid='client-secret']").innerText();
  expect(clientId.length).toBeGreaterThan(8);
  writeToken("linkedin", "client_id", clientId);
  writeToken("linkedin", "client_secret", clientSecret);
  process.stdout.write(JSON.stringify({ ok: true, wrote: ["linkedin.client_id", "linkedin.client_secret"] }) + "\n");
});
