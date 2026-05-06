/** Meta — Step 04: Pixel creation + install snippet capture. */
import { test, expect } from "@playwright/test";

test("04-pixel", async ({ page }) => {
  const businessId = process.env.MA_BUSINESS_ID;
  await page.goto(`https://business.facebook.com/events_manager2/list/dataset?business_id=${businessId}`);
  await page.getByRole("button", { name: /Connect data source|Add data source/i }).click();
  await page.getByText(/Web|Pixel/i).click();
  await page.getByRole("button", { name: /Get started|Connect/i }).click();
  await page.getByLabel(/Name/i).fill(process.env.MA_PIXEL_NAME || "Primary Pixel");
  await page.getByRole("button", { name: /Create/i }).click();
  await page.waitForURL(/pixel_id=\d+|dataset_id=\d+/, { timeout: 60_000 });
  const pixelId = page.url().match(/(?:pixel_id|dataset_id)=(\d+)/)?.[1] ?? "";
  expect(pixelId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ pixel_id: pixelId }) + "\n");
});
