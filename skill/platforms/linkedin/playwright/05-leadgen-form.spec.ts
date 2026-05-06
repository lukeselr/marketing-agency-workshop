/** LinkedIn — Step 05: Lead Gen Form (status PAUSED). */
import { test, expect } from "@playwright/test";

test("05-leadgen-form", async ({ page }) => {
  const adAccountId = process.env.MA_LI_AD_ACCOUNT_ID;
  await page.goto(`https://www.linkedin.com/campaignmanager/accounts/${adAccountId}/lead-gen-forms`);
  await page.getByRole("button", { name: /Create form/i }).click();
  await page.getByLabel(/Form name/i).fill(process.env.MA_LI_LEADGEN_NAME || "Selr AI Lead Form");
  await page.getByLabel(/Headline/i).fill(process.env.MA_LI_LEADGEN_HEADLINE || "Talk to us");
  await page.getByLabel(/Privacy policy URL/i).fill(process.env.MA_PRIVACY_URL || "https://example.com/privacy");
  await page.getByRole("button", { name: /Save draft|Create/i }).click();
  await page.waitForURL(/leadgen.*forms\/(\d+)/, { timeout: 60_000 });
  const formId = page.url().match(/leadgen.*forms\/(\d+)/)?.[1] ?? "";
  expect(formId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ leadgen_form_id: formId }) + "\n");
});
