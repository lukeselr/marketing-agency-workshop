/** LinkedIn — Step 04: Insight Tag (partner ID + install snippet). */
import { test, expect } from "@playwright/test";

test("04-insight-tag", async ({ page }) => {
  const adAccountId = process.env.MA_LI_AD_ACCOUNT_ID;
  await page.goto(`https://www.linkedin.com/campaignmanager/accounts/${adAccountId}/insight-tag`);
  await page.getByRole("button", { name: /Generate.*tag|Install.*tag/i }).click();
  // partner ID is in the snippet
  const snippet = await page.locator("[data-testid='insight-tag-snippet']").innerText();
  const partnerId = snippet.match(/_linkedin_partner_id\s*=\s*['"](\d+)['"]/)?.[1] ?? "";
  expect(partnerId).toMatch(/\d+/);
  process.stdout.write(JSON.stringify({ insight_tag_partner_id: partnerId }) + "\n");
});
