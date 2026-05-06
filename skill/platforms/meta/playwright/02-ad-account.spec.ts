/** Meta — Step 02: Ad Account creation, currency + timezone, billing. */
import { test, expect } from "@playwright/test";

test("02-ad-account", async ({ page }) => {
  const businessId = process.env.MA_BUSINESS_ID;
  await page.goto(`https://business.facebook.com/settings/ad-accounts?business_id=${businessId}`);
  await page.getByRole("button", { name: /Add|Create new ad account/i }).first().click();
  await page.getByLabel(/Ad account name/i).fill(process.env.MA_AD_ACCOUNT_NAME || "Primary Ad Account");
  await page.getByLabel(/Time zone/i).fill(process.env.MA_TIMEZONE || "Australia/Brisbane");
  await page.getByLabel(/Currency/i).fill(process.env.MA_CURRENCY || "AUD");
  await page.getByRole("button", { name: /Create|Next/i }).click();
  await page.waitForURL(/act=\d+/, { timeout: 60_000 });
  const adAccountId = page.url().match(/act=(\d+)/)?.[1] ?? "";
  expect(adAccountId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ ad_account_id: `act_${adAccountId}` }) + "\n");
});
