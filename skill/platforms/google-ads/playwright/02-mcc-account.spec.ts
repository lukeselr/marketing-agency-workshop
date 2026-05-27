/** Google Ads — Step 02: MCC (Manager) account. Optional — skip if user has single ad account. */
import { test, expect } from "@playwright/test";

test("02-mcc-account", async ({ page }) => {
  await page.goto("https://ads.google.com/aw/manager/start");
  const businessName = process.env.MA_BUSINESS_NAME || "My Agency";
  await page.getByLabel(/Manager.*account.*name/i).fill(process.env.MA_MCC_NAME || `${businessName} MCC`);
  await page.getByRole("radio", { name: /Manage other people's accounts/i }).check();
  await page.getByLabel(/Country/i).selectOption({ label: process.env.MA_GADS_COUNTRY || "Australia" });
  await page.getByLabel(/Time zone/i).selectOption({ label: process.env.MA_TIMEZONE || "(GMT+10:00) Brisbane" });
  await page.getByLabel(/Currency/i).selectOption({ label: process.env.MA_CURRENCY || "Australian Dollar (AUD $)" });
  await page.getByRole("button", { name: /Submit|Continue/i }).click();
  await page.waitForURL(/customers\/(\d+)/, { timeout: 60_000 });
  const customerId = page.url().match(/customers\/(\d+)/)?.[1] ?? "";
  expect(customerId).toMatch(/\d{10}/);
  process.stdout.write(JSON.stringify({ manager_customer_id: customerId }) + "\n");
});
