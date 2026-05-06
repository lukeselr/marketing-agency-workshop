/** Google Ads — Step 05: Conversion tracking. EC4W + EC4L mandatory per master strategy. */
import { test, expect } from "@playwright/test";

test("05-conversion-tracking", async ({ page }) => {
  const customerId = process.env.MA_GADS_CUSTOMER_ID;
  // Create Purchase conversion (EC4W)
  await page.goto(`https://ads.google.com/aw/conversions/new/website?ocid=${customerId}`);
  await page.getByLabel(/Conversion name/i).fill("Purchase");
  await page.getByLabel(/Category/i).selectOption({ label: "Purchase" });
  await page.getByLabel(/Value/i).check();
  await page.getByLabel(/Enhanced conversions for web/i).check();
  await page.getByRole("button", { name: /Save and continue/i }).click();
  await page.waitForURL(/conversion_actions\/(\d+)/, { timeout: 60_000 });
  const purchaseId = page.url().match(/conversion_actions\/(\d+)/)?.[1] ?? "";

  // Create Lead conversion (EC4L)
  await page.goto(`https://ads.google.com/aw/conversions/new/website?ocid=${customerId}`);
  await page.getByLabel(/Conversion name/i).fill("Lead Form Submit");
  await page.getByLabel(/Category/i).selectOption({ label: "Submit lead form" });
  await page.getByLabel(/Enhanced conversions for leads/i).check();
  await page.getByRole("button", { name: /Save and continue/i }).click();
  await page.waitForURL(/conversion_actions\/(\d+)/, { timeout: 60_000 });
  const leadId = page.url().match(/conversion_actions\/(\d+)/)?.[1] ?? "";

  expect(purchaseId).toMatch(/\d+/);
  expect(leadId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({
    conversion_action_id_purchase: purchaseId,
    conversion_action_id_lead: leadId,
  }) + "\n");
});
