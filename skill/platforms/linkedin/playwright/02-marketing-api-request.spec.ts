/** LinkedIn — Step 02: Request Marketing Developer Platform access. 1-5 day approval. */
import { test, expect } from "@playwright/test";

test("02-marketing-api-request", async ({ page }) => {
  const appId = process.env.MA_LI_APP_ID;
  await page.goto(`https://www.linkedin.com/developers/apps/${appId}/products`);
  await page.getByRole("button", { name: /Marketing Developer Platform.*Request access/i }).click();
  await page.getByLabel(/Use case/i).fill(process.env.MA_LI_USE_CASE ||
    "Run targeted Sponsored Content + Lead Gen Form campaigns for our company. Use audience matching, conversions reporting, and creative API to scale safely.");
  await page.getByLabel(/I agree/i).check();
  await page.getByRole("button", { name: /Submit/i }).click();
  await expect(page.getByText(/Request submitted|Pending review/i)).toBeVisible({ timeout: 30_000 });
  process.stdout.write(JSON.stringify({ marketing_api_status: "pending" }) + "\n");
});
