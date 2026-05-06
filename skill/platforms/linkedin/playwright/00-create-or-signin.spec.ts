/** LinkedIn — Step 00: Sign in or create LinkedIn account. */
import { test, expect } from "@playwright/test";

test("00-create-or-signin", async ({ page }) => {
  await page.goto("https://www.linkedin.com/login");
  if (await page.locator("input[name='session_key']").isVisible()) {
    await page.waitForURL(/feed|home/, { timeout: 5 * 60_000 });
  } else {
    await page.goto("https://www.linkedin.com/signup");
    await page.waitForURL(/feed|home|onboarding/, { timeout: 5 * 60_000 });
  }
  await expect(page).toHaveURL(/linkedin\.com/);
});
