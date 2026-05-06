/** Meta — Step 05: Conversions API dataset + access token. */
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

test("05-capi-dataset", async ({ page }) => {
  const pixelId = process.env.MA_PIXEL_ID;
  await page.goto(`https://business.facebook.com/events_manager2/list/dataset/${pixelId}/settings`);
  await page.getByRole("tab", { name: /Conversions API/i }).click();
  await page.getByRole("button", { name: /Set up.*manually|Generate.*access token/i }).click();
  // user names + scopes the token
  const token = await page.locator("[data-testid='capi-access-token']").innerText();
  expect(token).toMatch(/^EAA/);
  writeToken("meta", "capi_access_token", token);
  process.stdout.write(JSON.stringify({ ok: true, wrote: "meta.capi_access_token" }) + "\n");
});
