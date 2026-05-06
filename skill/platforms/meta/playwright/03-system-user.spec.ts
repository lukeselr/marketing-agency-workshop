/** Meta — Step 03: System User + long-lived access token. */
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

test("03-system-user", async ({ page }) => {
  const businessId = process.env.MA_BUSINESS_ID;
  await page.goto(`https://business.facebook.com/settings/system-users?business_id=${businessId}`);
  await page.getByRole("button", { name: /Add|Create system user/i }).first().click();
  await page.getByLabel(/Name/i).fill(process.env.MA_SYSTEM_USER_NAME || "marketing-agency-su");
  await page.getByLabel(/Role/i).selectOption({ label: "Admin" });
  await page.getByRole("button", { name: /Create/i }).click();
  await page.getByRole("button", { name: /Generate.*token/i }).click();
  // user picks scopes ads_management, ads_read, business_management, leads_retrieval, pages_read_engagement
  await page.getByRole("button", { name: /Generate token/i }).click();
  const token = await page.locator("[data-testid='access-token-display']").innerText();
  expect(token).toMatch(/^EAA/);
  writeToken("meta", "system_user_token", token);
  process.stdout.write(JSON.stringify({ ok: true, wrote: "meta.system_user_token" }) + "\n");
});
