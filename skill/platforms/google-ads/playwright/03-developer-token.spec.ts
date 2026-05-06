/** Google Ads — Step 03: Developer token (test → basic → standard). */
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

test("03-developer-token", async ({ page }) => {
  const customerId = process.env.MA_GADS_CUSTOMER_ID;
  await page.goto(`https://ads.google.com/aw/apicenter?ocid=${customerId}`);
  // Apply for token if absent
  if (await page.getByRole("button", { name: /Apply for token/i }).isVisible()) {
    await page.getByRole("button", { name: /Apply for token/i }).click();
    await page.getByLabel(/Use case/i).fill(process.env.MA_GADS_USE_CASE ||
      "Manage Search + PMax campaigns for our company. Build conversion tracking, audience uploads, automated reporting.");
    await page.getByLabel(/I agree/i).check();
    await page.getByRole("button", { name: /Submit/i }).click();
  }
  // Token displayed once approval reaches "Basic"
  const token = await page.locator("[data-testid='developer-token']").innerText().catch(() => "");
  if (token) {
    expect(token.length).toBeGreaterThan(10);
    writeToken("google-ads", "developer_token", token);
    process.stdout.write(JSON.stringify({ ok: true, wrote: "google-ads.developer_token" }) + "\n");
  } else {
    process.stdout.write(JSON.stringify({ developer_token_status: "pending" }) + "\n");
  }
});
