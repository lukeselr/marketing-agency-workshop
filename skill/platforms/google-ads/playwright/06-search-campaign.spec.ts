/** Google Ads — Step 06: Search campaign template (PAUSED). AI Max for Search 2025-aware. */
import { test, expect } from "@playwright/test";

test("06-search-campaign", async ({ page }) => {
  const customerId = process.env.MA_GADS_CUSTOMER_ID;
  await page.goto(`https://ads.google.com/aw/campaigns/new?ocid=${customerId}`);
  await page.getByText(/Sales|Leads/i).first().click();
  await page.getByText(/Search/i).first().click();
  await page.getByRole("button", { name: /Continue/i }).click();
  await page.getByLabel(/Campaign name/i).fill(process.env.MA_GADS_CAMPAIGN_NAME || "Brand + Search Test");
  await page.getByLabel(/Status/i).selectOption({ label: "Paused" });
  // Bid strategy: Manual CPC for first run (per master strategy — switch to Smart Bidding after 30+ conversions)
  await page.getByLabel(/Bid strategy/i).selectOption({ label: "Manual CPC" });
  await page.getByRole("button", { name: /Save|Create campaign/i }).click();
  await page.waitForURL(/campaign_id=(\d+)/, { timeout: 60_000 });
  const campaignId = page.url().match(/campaign_id=(\d+)/)?.[1] ?? "";
  expect(campaignId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ campaign_id: campaignId, status: "PAUSED" }) + "\n");
});
