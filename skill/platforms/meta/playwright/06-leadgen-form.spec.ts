/** Meta — Step 06: Lead Gen Form template (status PAUSED). */
import { test, expect } from "@playwright/test";

test("06-leadgen-form", async ({ page }) => {
  const pageId = process.env.MA_FB_PAGE_ID;
  await page.goto(`https://business.facebook.com/leadgen_forms/?page_id=${pageId}`);
  await page.getByRole("button", { name: /Create form/i }).click();
  const businessName = process.env.MA_BUSINESS_NAME || "My Business";
  await page.getByLabel(/Form name/i).fill(process.env.MA_LEADGEN_FORM_NAME || `${businessName} Lead Form`);
  await page.getByRole("button", { name: /More volume|Higher intent/i }).click();
  await page.getByLabel(/Greeting headline/i).fill(process.env.MA_LEADGEN_HEADLINE || "Talk to us");
  await page.getByRole("button", { name: /Save draft/i }).click();
  await page.waitForURL(/form_id=\d+/, { timeout: 60_000 });
  const formId = page.url().match(/form_id=(\d+)/)?.[1] ?? "";
  expect(formId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ leadgen_form_id: formId }) + "\n");
});
