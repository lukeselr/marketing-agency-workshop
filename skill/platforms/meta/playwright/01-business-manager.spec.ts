/** Meta — Step 01: Business Manager creation. */
import { test, expect } from "@playwright/test";

test("01-business-manager", async ({ page }) => {
  await page.goto("https://business.facebook.com/overview");
  if (await page.getByRole("button", { name: /Create.*Business/i }).first().isVisible()) {
    await page.getByRole("button", { name: /Create.*Business/i }).first().click();
    await page.getByLabel(/Business.*name/i).fill(process.env.MA_BUSINESS_NAME || "");
    await page.getByLabel(/Your name/i).fill(process.env.MA_USER_NAME || "");
    await page.getByLabel(/Business email/i).fill(process.env.MA_USER_EMAIL || "");
    await page.getByRole("button", { name: /Submit|Create/i }).click();
  }
  await page.waitForURL(/business_id=\d+/, { timeout: 60_000 });
  const url = page.url();
  const businessId = url.match(/business_id=(\d+)/)?.[1] ?? "";
  expect(businessId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ business_id: businessId }) + "\n");
});
